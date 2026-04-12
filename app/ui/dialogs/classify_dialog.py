"""Diálogo popup para classificar produtos não identificados.

- Agrupa títulos idênticos (aparece UMA vez)
- Puxa tipos do banco de dados (dinâmico)
- Salva no banco para não perguntar de novo
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame, QScrollArea, QWidget
)
from PySide6.QtCore import Qt

from app.models.schema import TypeVariation


class ClassifyDialog(QDialog):
    def __init__(self, pending_items: list[dict], db_session, parent=None):
        super().__init__(parent)
        self.db = db_session
        self.setWindowTitle("Classificar Produtos")
        self.setMinimumWidth(650)
        self.setMinimumHeight(350)
        self.setModal(True)

        # Puxar tipos do banco
        types = self.db.query(TypeVariation).filter(TypeVariation.is_active == True).all()
        self.type_names = [t.name for t in types] if types else ["Econômica", "Piso", "Externa", "Emborrachada", "Premium"]

        # Agrupa por título
        self.title_groups: dict[str, list[int]] = {}
        for item in pending_items:
            title = item["original_title"]
            self.title_groups.setdefault(title, []).append(item["_index"])

        self.combos: dict[str, QComboBox] = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        unique_count = len(self.title_groups)
        total_count = len(pending_items)
        header = QLabel(
            f"⚠️  {unique_count} produto(s) precisam de classificação "
            f"({total_count} itens).\n"
            "Escolha o tipo — será salvo para importações futuras."
        )
        header.setStyleSheet("font-size: 14px; font-weight: 600; padding: 8px 0;")
        header.setWordWrap(True)
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)

        for title, indices in self.title_groups.items():
            card = QFrame()
            card.setObjectName("Card")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(14, 10, 14, 10)
            card_layout.setSpacing(12)

            display = title if len(title) <= 75 else title[:75] + "…"
            count = f"  ({len(indices)}x)" if len(indices) > 1 else ""
            lbl = QLabel(f"📦 {display}{count}")
            lbl.setStyleSheet("font-size: 13px;")
            lbl.setWordWrap(True)

            combo = QComboBox()
            combo.addItems(self.type_names)
            combo.setFixedWidth(160)

            card_layout.addWidget(lbl, 1)
            card_layout.addWidget(combo)

            scroll_layout.addWidget(card)
            self.combos[title] = combo

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, 1)

        bottom = QHBoxLayout()
        bottom.addStretch()
        btn = QPushButton("✅  Confirmar e Salvar")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("padding: 10px 28px; font-size: 14px;")
        btn.clicked.connect(self._on_confirm)
        bottom.addWidget(btn)
        layout.addLayout(bottom)

    def _on_confirm(self, *args):
        self.accept()

    def get_classifications(self) -> dict[int, str]:
        result = {}
        for title, combo in self.combos.items():
            chosen = combo.currentText()
            for idx in self.title_groups[title]:
                result[idx] = chosen
        return result

    def get_title_classifications(self) -> dict[str, str]:
        return {title: combo.currentText() for title, combo in self.combos.items()}
