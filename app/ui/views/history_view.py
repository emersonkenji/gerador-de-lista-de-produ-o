from functools import partial

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
    QMessageBox, QFrame, QSplitter, QFileDialog, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument, QFont

from app.models.schema import ProductionList


class HistoryView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Histórico de Listas")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        sub = QLabel("Todas as listas de produção geradas — clique no 👁️ para visualizar")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)

        layout.addSpacing(4)

        splitter = QSplitter(Qt.Orientation.Vertical)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data", "Arquivo Origem", "Baldes", "Criada em", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        splitter.addWidget(self.table)

        # Detail area
        detail = QWidget()
        dl = QVBoxLayout(detail)
        dl.setContentsMargins(0, 8, 0, 0)

        header = QHBoxLayout()
        header.addWidget(QLabel("📝  Texto da Lista Selecionada"))

        self.btn_copy = QPushButton("📋  Copiar")
        self.btn_copy.setObjectName("Secondary")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.clicked.connect(self._on_copy)

        self.btn_export = QPushButton("💾  Exportar .txt")
        self.btn_export.setObjectName("Secondary")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.clicked.connect(self._on_export)

        self.btn_print = QPushButton("🖨️  Imprimir")
        self.btn_print.setObjectName("Secondary")
        self.btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_print.clicked.connect(self._on_print)

        header.addStretch()
        header.addWidget(self.btn_copy)
        header.addWidget(self.btn_export)
        header.addWidget(self.btn_print)
        dl.addLayout(header)

        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        dl.addWidget(self.txt_output)
        splitter.addWidget(detail)

        splitter.setSizes([280, 320])
        layout.addWidget(splitter, 1)

    def refresh_data(self):
        self.table.setRowCount(0)
        self.txt_output.clear()

        lists = self.db.query(ProductionList).order_by(ProductionList.id.desc()).all()
        for pl in lists:
            idx = self.table.rowCount()
            self.table.insertRow(idx)

            self.table.setItem(idx, 0, QTableWidgetItem(str(pl.id)))
            self.table.setItem(idx, 1, QTableWidgetItem(pl.list_date or "—"))
            self.table.setItem(idx, 2, QTableWidgetItem(pl.source_file_name or "—"))
            self.table.setItem(idx, 3, QTableWidgetItem(str(pl.total_buckets or 0)))

            created = ""
            if pl.created_at:
                created = pl.created_at.strftime("%d/%m/%Y %H:%M")
            self.table.setItem(idx, 4, QTableWidgetItem(created))

            # Action buttons with icons
            actions = QWidget()
            al = QHBoxLayout(actions)
            al.setContentsMargins(4, 2, 4, 2)
            al.setSpacing(4)

            btn_view = QPushButton("👁️ Ver")
            btn_view.setObjectName("Ghost")
            btn_view.setFixedWidth(60)
            btn_view.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_view.clicked.connect(partial(self._on_view, pl.raw_text_output))

            btn_del = QPushButton("🗑️ Excluir")
            btn_del.setObjectName("Destructive")
            btn_del.setFixedWidth(80)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(partial(self._on_delete, pl.id))

            al.addWidget(btn_view)
            al.addWidget(btn_del)
            self.table.setCellWidget(idx, 5, actions)

    def _on_view(self, text, *args):
        self.txt_output.setText(text or "")

    def _on_delete(self, list_id, *args):
        reply = QMessageBox.question(
            self, "Confirmar Exclusão",
            "Excluir esta lista e todos os seus itens?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            pl = self.db.query(ProductionList).filter(ProductionList.id == list_id).first()
            if pl:
                self.db.delete(pl)
                self.db.commit()
                self.refresh_data()

    def _on_copy(self, *args):
        text = self.txt_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Copiado", "Texto copiado!")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma lista primeiro (botão 👁️ Ver).")

    def _on_export(self, *args):
        text = self.txt_output.toPlainText()
        if not text:
            QMessageBox.warning(self, "Aviso", "Selecione uma lista primeiro (botão 👁️ Ver).")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Salvar como .txt", "lista_producao.txt", "Text (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            QMessageBox.information(self, "Exportado", f"Salvo em:\n{path}")

    def _on_print(self, *args):
        text = self.txt_output.toPlainText()
        if not text:
            QMessageBox.warning(self, "Aviso", "Selecione uma lista primeiro (botão 👁️ Ver).")
            return
        try:
            from PySide6.QtPrintSupport import QPrinter, QPrintDialog
            printer = QPrinter(QPrinter.Mode.HighResolution)
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Imprimir Lista")
            if dialog.exec() == QPrintDialog.Accepted:
                doc = QTextDocument()
                doc.setPlainText(text)
                doc.setDefaultFont(QFont("Consolas", 11))
                doc.print_(printer)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao imprimir:\n{str(e)}")
