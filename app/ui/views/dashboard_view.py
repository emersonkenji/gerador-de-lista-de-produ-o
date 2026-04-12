from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from app.models.schema import ProductionList, ProductMapping, Store


class DashboardView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Header
        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        sub = QLabel("Visão geral da sua operação de produção")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)

        layout.addSpacing(8)

        # Metric cards
        grid = QGridLayout()
        grid.setSpacing(14)

        self.card_lists = self._make_card("📋", "Listas Geradas", "0")
        self.card_products = self._make_card("📦", "Produtos Mapeados", "0")
        self.card_buckets = self._make_card("🪣", "Baldes (Total)", "0")
        self.card_stores = self._make_card("🏪", "Lojas Cadastradas", "0")

        grid.addWidget(self.card_lists["frame"], 0, 0)
        grid.addWidget(self.card_products["frame"], 0, 1)
        grid.addWidget(self.card_buckets["frame"], 0, 2)
        grid.addWidget(self.card_stores["frame"], 0, 3)

        layout.addLayout(grid)

        # Recent activity
        layout.addSpacing(12)
        recent_title = QLabel("Atividade Recente")
        recent_title.setObjectName("PageTitle")
        recent_title.setStyleSheet("font-size: 16px;")
        layout.addWidget(recent_title)

        self.recent_frame = QFrame()
        self.recent_frame.setObjectName("Card")
        self.recent_layout = QVBoxLayout(self.recent_frame)
        self.recent_layout.setContentsMargins(16, 12, 16, 12)
        self.lbl_recent = QLabel("Nenhuma lista importada ainda.")
        self.lbl_recent.setObjectName("PageSubtitle")
        self.lbl_recent.setWordWrap(True)
        self.recent_layout.addWidget(self.lbl_recent)
        layout.addWidget(self.recent_frame)

        # Stores section
        layout.addSpacing(8)
        stores_title = QLabel("🏪  Empresas / Lojas Cadastradas")
        stores_title.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(stores_title)

        self.stores_frame = QFrame()
        self.stores_frame.setObjectName("Card")
        self.stores_layout = QVBoxLayout(self.stores_frame)
        self.stores_layout.setContentsMargins(16, 12, 16, 12)
        self.lbl_stores_list = QLabel("Nenhuma empresa cadastrada.")
        self.lbl_stores_list.setObjectName("PageSubtitle")
        self.lbl_stores_list.setWordWrap(True)
        self.stores_layout.addWidget(self.lbl_stores_list)
        layout.addWidget(self.stores_frame)

        layout.addStretch()

    def _make_card(self, icon: str, title_text: str, value_text: str) -> dict:
        frame = QFrame()
        frame.setObjectName("Card")
        frame.setMinimumHeight(110)
        l = QVBoxLayout(frame)
        l.setContentsMargins(18, 16, 18, 16)
        l.setSpacing(6)

        row = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 22px;")
        t = QLabel(title_text)
        t.setObjectName("CardTitle")
        row.addWidget(icon_lbl)
        row.addWidget(t)
        row.addStretch()
        l.addLayout(row)

        v = QLabel(value_text)
        v.setObjectName("CardValue")
        l.addWidget(v)
        l.addStretch()

        return {"frame": frame, "value_label": v}

    def refresh_data(self):
        try:
            total_lists = self.db.query(ProductionList).count()
            self.card_lists["value_label"].setText(str(total_lists))

            total_products = self.db.query(ProductMapping).count()
            self.card_products["value_label"].setText(str(total_products))

            total_stores = self.db.query(Store).count()
            self.card_stores["value_label"].setText(str(total_stores))

            all_lists = self.db.query(ProductionList).all()
            total_buckets = sum(l.total_buckets or 0 for l in all_lists)
            self.card_buckets["value_label"].setText(str(total_buckets))

            # Recent list
            last = self.db.query(ProductionList).order_by(ProductionList.id.desc()).first()
            if last:
                self.lbl_recent.setText(
                    f"Última lista: {last.list_date} — {last.source_file_name} "
                    f"({last.total_buckets} baldes)"
                )
            else:
                self.lbl_recent.setText("Nenhuma lista importada ainda.")

            # Store names
            stores = self.db.query(Store).all()
            if stores:
                names = [f"•  {s.name}" for s in stores]
                self.lbl_stores_list.setText("\n".join(names))
            else:
                self.lbl_stores_list.setText("Nenhuma empresa cadastrada ainda. Importe um XLSX.")
        except Exception:
            pass
