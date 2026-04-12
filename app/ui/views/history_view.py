from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QTextEdit, QMessageBox, QFileDialog, QApplication, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument, QFont

from app.models.schema import ProductionList


class HistoryView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header area
        header_container = QWidget()
        hl = QVBoxLayout(header_container)
        hl.setSpacing(4)
        
        title = QLabel("Histórico de Listas")
        title.setObjectName("PageTitle")
        hl.addWidget(title)
        
        sub = QLabel("Selecione uma lista salva para visualizar, imprimir ou exportar.")
        sub.setObjectName("PageSubtitle")
        hl.addWidget(sub)
        
        layout.addWidget(header_container)

        # Main Card
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 16, 20, 16)
        cl.setSpacing(14)

        # Top row: Select and Actions
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self.combo_lists = QComboBox()
        self.combo_lists.setStyleSheet("font-size: 14px; padding: 6px;")
        self.combo_lists.currentIndexChanged.connect(self._on_list_selected)
        top_row.addWidget(QLabel("📂 Lista: "))
        top_row.addWidget(self.combo_lists, 1)

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

        self.btn_del = QPushButton("🗑️  Excluir")
        self.btn_del.setObjectName("Destructive")
        self.btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_del.clicked.connect(self._on_delete)

        top_row.addWidget(self.btn_copy)
        top_row.addWidget(self.btn_export)
        top_row.addWidget(self.btn_print)
        top_row.addWidget(self.btn_del)
        
        cl.addLayout(top_row)

        # Text area
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        # Using larger font for preview readability
        font = QFont("Consolas", 11)
        self.txt_output.setFont(font)
        cl.addWidget(self.txt_output)

        layout.addWidget(card, 1)
        
        # Internal state
        self._current_lists = []

    def refresh_data(self):
        # Prevent triggering selection event while rebuilding
        self.combo_lists.blockSignals(True)
        self.combo_lists.clear()
        self.txt_output.clear()

        self._current_lists = self.db.query(ProductionList).order_by(ProductionList.id.desc()).all()
        
        if not self._current_lists:
            self.combo_lists.addItem("Nenhuma lista cadastrada")
            self.combo_lists.setEnabled(False)
            self._set_buttons_enabled(False)
        else:
            self.combo_lists.setEnabled(True)
            self._set_buttons_enabled(True)
            for pl in self._current_lists:
                date_str = pl.list_date or "Data desconhecida"
                file_str = pl.source_file_name or "Arquivo desconhecido"
                buckets = pl.total_buckets or 0
                label = f"{date_str} — {file_str} ({buckets} baldes) [ID: {pl.id}]"
                self.combo_lists.addItem(label, pl.id)
                
            # Simulate selection of first item
            self._load_list_content(0)
            
        self.combo_lists.blockSignals(False)

    def _set_buttons_enabled(self, enabled: bool):
        self.btn_copy.setEnabled(enabled)
        self.btn_export.setEnabled(enabled)
        self.btn_print.setEnabled(enabled)
        self.btn_del.setEnabled(enabled)

    def _on_list_selected(self, index: int):
        self._load_list_content(index)

    def _load_list_content(self, index: int):
        if index < 0 or index >= len(self._current_lists):
            self.txt_output.clear()
            return
        pl = self._current_lists[index]
        self.txt_output.setText(pl.raw_text_output or "")

    def _on_delete(self, *args):
        idx = self.combo_lists.currentIndex()
        if idx < 0 or idx >= len(self._current_lists):
            return
            
        pl = self._current_lists[idx]
        
        reply = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja excluir a lista do dia {pl.list_date} permanentemente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            db_item = self.db.query(ProductionList).filter(ProductionList.id == pl.id).first()
            if db_item:
                self.db.delete(db_item)
                self.db.commit()
                self.refresh_data()

    def _on_copy(self, *args):
        text = self.txt_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Copiado", "Texto copiado para a área de transferência!")

    def _on_export(self, *args):
        text = self.txt_output.toPlainText()
        if not text:
            return
            
        pl = self._current_lists[self.combo_lists.currentIndex()]
        default_name = f"lista_producao_{pl.list_date.replace('/', '-')}.txt" if pl.list_date else "lista_producao.txt"
        
        path, _ = QFileDialog.getSaveFileName(self, "Salvar como .txt", default_name, "Text (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            QMessageBox.information(self, "Exportado", f"Arquivo salvo com sucesso em:\n{path}")

    def _on_print(self, *args):
        text = self.txt_output.toPlainText()
        if not text:
            return
            
        try:
            from PySide6.QtPrintSupport import QPrinter, QPrintDialog
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Imprimir Lista de Produção")
            
            if dialog.exec() == QPrintDialog.Accepted:
                doc = QTextDocument()
                doc.setPlainText(text)
                doc.setDefaultFont(QFont("Consolas", 11))
                doc.print_(printer)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao acessar impressora:\n{str(e)}")
