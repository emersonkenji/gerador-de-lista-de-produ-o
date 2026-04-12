"""Diálogo popup para classificar produtos não identificados.

- Agrupa títulos idênticos (aparece UMA vez)
- Puxa tipos  e litragens do banco de dados (dinâmico)
- Salva no banco para não perguntar de novo
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame, QScrollArea, QWidget
)
from PySide6.QtCore import Qt

from app.models.schema import TypeVariation, VolumeVariation


class ClassifyDialog(QDialog):
    def __init__(self, pending_items: list[dict], db_session, parent=None):
        super().__init__(parent)
        self.db = db_session
        self.setWindowTitle("Classificar Produtos Pendentes")
        self.setMinimumWidth(750)
        self.setMinimumHeight(400)
        self.setModal(True)

        # Puxar tipos do banco
        types = self.db.query(TypeVariation).filter(TypeVariation.is_active == True).all()
        self.type_names = [t.name for t in types] if types else ["Econômica", "Piso", "Externa", "Emborrachada", "Premium"]

        # Puxar litragens do banco
        vols = self.db.query(VolumeVariation).filter(VolumeVariation.is_active == True).all()
        self.vol_names = ["Automático"] + [v.name for v in vols] if vols else ["Automático", "3,6L", "10L", "18L", "500ml"]

        # Agrupa por título
        self.title_groups: dict[str, list[dict]] = {}
        for item in pending_items:
            title = item["original_title"]
            self.title_groups.setdefault(title, []).append(item)

        self.combos_type: dict[str, QComboBox] = {}
        self.combos_vol: dict[str, QComboBox] = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        unique_count = len(self.title_groups)
        total_count = len(pending_items)
        header = QLabel(
            f"⚠️  {unique_count} produto(s) precisam de revisão "
            f"({total_count} itens no arquivo).\n"
            "Escolha o Tipo de Tinta e a Litragem. Suas escolhas serão lembradas automaticamente."
        )
        header.setStyleSheet("font-size: 14px; font-weight: 600; padding: 8px 0;")
        header.setWordWrap(True)
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)

        for title, items in self.title_groups.items():
            card = QFrame()
            card.setObjectName("Card")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(14, 10, 14, 10)
            card_layout.setSpacing(12)

            display = title if len(title) <= 70 else title[:70] + "…"
            count = f"  ({len(items)}x)" if len(items) > 1 else ""
            lbl = QLabel(f"📦 {display}{count}")
            lbl.setStyleSheet("font-size: 13px;")
            lbl.setWordWrap(True)

            combo_t = QComboBox()
            combo_t.addItems(self.type_names)
            combo_t.setFixedWidth(130)
            
            # Pre-selecionar se já houver chute
            guess_t = items[0].get("product_type")
            if guess_t and guess_t in self.type_names:
                combo_t.setCurrentText(guess_t)

            combo_v = QComboBox()
            combo_v.addItems(self.vol_names)
            combo_v.setFixedWidth(110)
            
            # Pre-selecionar se já houver volume
            guess_v = items[0].get("volume")
            if guess_v and guess_v in self.vol_names:
                combo_v.setCurrentText(guess_v)
            else:
                combo_v.setCurrentText("Automático")

            card_layout.addWidget(lbl, 1)
            card_layout.addWidget(QLabel("Tipo:"))
            card_layout.addWidget(combo_t)
            card_layout.addWidget(QLabel("Vol:"))
            card_layout.addWidget(combo_v)

            scroll_layout.addWidget(card)
            self.combos_type[title] = combo_t
            self.combos_vol[title] = combo_v

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

    def get_classifications(self) -> dict[int, dict]:
        """Retorna {index: {'type': ..., 'volume': ...}}"""
        result = {}
        for title in self.title_groups.keys():
            chosen_type = self.combos_type[title].currentText()
            chosen_vol = self.combos_vol[title].currentText()
            for item in self.title_groups[title]:
                result[item["_index"]] = {
                    "type": chosen_type,
                    "volume": chosen_vol if chosen_vol != "Automático" else item.get("volume", "Indefinida")
                }
        return result

    def get_title_classifications(self) -> dict[str, dict]:
        """Retorna {titulo: {'type': ..., 'volume': ...}}"""
        return {
            title: {
                "type": self.combos_type[title].currentText(),
                "volume": self.combos_vol[title].currentText()
            }
            for title in self.title_groups.keys()
        }
