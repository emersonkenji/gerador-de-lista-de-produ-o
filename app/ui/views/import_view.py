import os
import pandas as pd

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QMessageBox, QFrame, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument, QFont

from app.core.engine import process_dataframe, extract_date_from_filename, generate_text_output
from app.models.schema import ProductionList, ProductionListItem, AppSettings, ProductMapping
from app.ui.dialogs.classify_dialog import ClassifyDialog
from app.core.parser import normalize_text, extract_volume


class ImportView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.main_window = parent
        self.current_filepath = None
        self.parsed_records = []
        self.text_preview_output = ""
        self.list_date_str = ""
        self.source_datetime = None
        self.total_buckets_count = 0

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Importar Planilha XLSX")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        sub = QLabel("Selecione um arquivo exportado do UpSeller — a lista é salva automaticamente")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)

        layout.addSpacing(4)

        # File bar
        file_bar = QFrame()
        file_bar.setObjectName("Card")
        fb = QHBoxLayout(file_bar)
        fb.setContentsMargins(14, 10, 14, 10)

        self.btn_select = QPushButton("📂  Selecionar Arquivo")
        self.btn_select.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select.clicked.connect(self._on_select_file)

        self.lbl_file = QLabel("Nenhum arquivo selecionado")
        self.lbl_file.setObjectName("PageSubtitle")
        self.lbl_date = QLabel("")
        self.lbl_date.setObjectName("Badge")
        self.lbl_stores = QLabel("")
        self.lbl_stores.setObjectName("Badge")

        fb.addWidget(self.btn_select)
        fb.addWidget(self.lbl_file, 1)
        fb.addWidget(self.lbl_date)
        fb.addWidget(self.lbl_stores)
        layout.addWidget(file_bar)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Título Original", "Variação", "Status", "Tipo", "Volume", "Cor"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        splitter.addWidget(self.table)

        preview_container = QWidget()
        pc = QVBoxLayout(preview_container)
        pc.setContentsMargins(0, 8, 0, 0)
        lbl = QLabel("📝  Pré-visualização da Lista")
        lbl.setStyleSheet("font-weight: 600; font-size: 13px;")
        pc.addWidget(lbl)
        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(True)
        pc.addWidget(self.txt_preview)
        splitter.addWidget(preview_container)

        splitter.setSizes([300, 280])
        layout.addWidget(splitter, 1)

        # Bottom bar
        bottom = QHBoxLayout()
        self.lbl_summary = QLabel("")
        self.lbl_summary.setObjectName("PageSubtitle")

        self.btn_print = QPushButton("🖨️  Imprimir Lista")
        self.btn_print.setObjectName("Secondary")
        self.btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print.clicked.connect(self._on_print)
        self.btn_print.setVisible(False)

        bottom.addWidget(self.lbl_summary, 1)
        bottom.addWidget(self.btn_print)
        layout.addLayout(bottom)

    def _on_select_file(self, *args):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar XLSX", "", "Excel (*.xlsx)")
        if path:
            self.current_filepath = path
            self.lbl_file.setText(os.path.basename(path))
            self.process_file()

    def process_file(self):
        try:
            df = pd.read_excel(self.current_filepath)
            self.parsed_records = process_dataframe(df, self.db)

            filename = os.path.basename(self.current_filepath)
            self.list_date_str, self.source_datetime = extract_date_from_filename(filename)
            self.lbl_date.setText(f"📅 {self.list_date_str}")

            stores = set(r["store_name"] for r in self.parsed_records if r.get("store_name"))
            if stores:
                self.lbl_stores.setText(f"🏪 {len(stores)} loja(s)")

            # Classify pending
            pending = self._get_pending_items()
            if pending:
                self._show_classify_dialog(pending)

            self.update_table()
            self.generate_preview()
            self.auto_save()
            self.btn_print.setVisible(True)

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Erro", f"Falha ao processar:\n{str(e)}")

    def _get_pending_items(self):
        pending = []
        for i, r in enumerate(self.parsed_records):
            if r["product_type"] == "Outros" or r["classification_status"] == "pending" or not r["product_type"]:
                item = dict(r)
                item["_index"] = i
                pending.append(item)
        return pending

    def _show_classify_dialog(self, pending_items):
        dialog = ClassifyDialog(pending_items, self.db, parent=self)
        result = dialog.exec()

        if result == ClassifyDialog.Accepted:
            classifications = dialog.get_classifications()
            for idx, chosen in classifications.items():
                self.parsed_records[idx]["product_type"] = chosen["type"]
                self.parsed_records[idx]["volume"] = chosen["volume"]
                self.parsed_records[idx]["classification_status"] = "success"

            title_types = dialog.get_title_classifications()
            for title, chosen in title_types.items():
                self._save_mapping(title, chosen["type"], chosen["volume"])
        else:
            for item in pending_items:
                idx = item["_index"]
                self.parsed_records[idx]["product_type"] = "Econômica"
                if self.parsed_records[idx]["volume"] == "Indefinida":
                    self.parsed_records[idx]["volume"] = "18L"
                self.parsed_records[idx]["classification_status"] = "success"

    def _save_mapping(self, title, product_type, volume=None):
        norm = normalize_text(title)
        if volume == "Automático":
            volume = extract_volume(title)

        mappings = self.db.query(ProductMapping).filter(ProductMapping.is_active == True).all()
        for m in mappings:
            pat = normalize_text(m.title_pattern)
            if pat and (pat in norm or norm in pat):
                m.product_type = product_type
                if volume:
                    m.default_volume = volume
                self.db.commit()
                return
        new = ProductMapping(
            title_pattern=title,
            product_type=product_type,
            default_volume=volume,
            is_active=True,
            auto_registered=True
        )
        self.db.add(new)
        self.db.commit()

    def update_table(self):
        self.table.setRowCount(0)
        for r in self.parsed_records:
            idx = self.table.rowCount()
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(r["original_title"][:80]))
            self.table.setItem(idx, 1, QTableWidgetItem(r["original_variation"]))
            si = QTableWidgetItem("✅" if r["classification_status"] == "success" else "⚠️")
            si.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(idx, 2, si)
            self.table.setItem(idx, 3, QTableWidgetItem(r["product_type"]))
            self.table.setItem(idx, 4, QTableWidgetItem(r["volume"]))
            self.table.setItem(idx, 5, QTableWidgetItem(r["color"]))

    def generate_preview(self):
        grouped = {}
        for r in self.parsed_records:
            t, v, c, q = r["product_type"], r["volume"], r["color"], r["quantity"]
            grouped.setdefault(t, {}).setdefault(v, {})
            grouped[t][v][c] = grouped[t][v].get(c, 0) + q

        settings = self.db.query(AppSettings).first()
        company = settings.company_name if settings else "E.F.S.T COMERCIAL LTDA"
        self.text_preview_output, self.total_buckets_count = generate_text_output(
            grouped, company, self.list_date_str
        )
        self.txt_preview.setText(self.text_preview_output)

    def auto_save(self):
        if not self.parsed_records:
            return
        try:
            settings = self.db.query(AppSettings).first()
            company = settings.company_name if settings else "E.F.S.T COMERCIAL LTDA"
            new_list = ProductionList(
                company_name=company,
                list_date=self.list_date_str,
                source_file_name=os.path.basename(self.current_filepath),
                source_file_datetime=self.source_datetime,
                raw_text_output=self.text_preview_output,
                total_buckets=self.total_buckets_count
            )
            self.db.add(new_list)
            self.db.commit()
            for r in self.parsed_records:
                self.db.add(ProductionListItem(
                    production_list_id=new_list.id,
                    product_type=r["product_type"],
                    volume=r["volume"],
                    color=r["color"],
                    quantity=r["quantity"],
                    original_title=r["original_title"],
                    original_variation=r["original_variation"],
                    store_name=r.get("store_name", ""),
                    classification_status=r["classification_status"]
                ))
            self.db.commit()
            self.lbl_summary.setText(
                f"✅  Salvo!  •  {len(self.parsed_records)} itens  •  {self.total_buckets_count} baldes"
            )
        except Exception as e:
            self.db.rollback()
            self.lbl_summary.setText(f"❌  Erro: {str(e)[:60]}")

    def _on_print(self, *args):
        """Abre o diálogo de impressão do sistema."""
        text = self.txt_preview.toPlainText()
        if not text:
            QMessageBox.warning(self, "Aviso", "Nenhuma lista para imprimir.")
            return

        try:
            from PySide6.QtPrintSupport import QPrinter, QPrintDialog
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Imprimir Lista de Produção")

            if dialog.exec() == QPrintDialog.Accepted:
                doc = QTextDocument()
                doc.setPlainText(text)
                font = QFont("Consolas", 11)
                doc.setDefaultFont(font)
                doc.print_(printer)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao imprimir:\n{str(e)}")
