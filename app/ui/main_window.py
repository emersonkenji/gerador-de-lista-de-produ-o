from functools import partial

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PySide6.QtCore import Qt

from app.themes.qss_manager import APP_VERSION
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.import_view import ImportView
from app.ui.views.products_view import ProductsView
from app.ui.views.history_view import HistoryView
from app.ui.views.settings_view import SettingsView


class MainWindow(QMainWindow):
    def __init__(self, db_session):
        super().__init__()
        self.db = db_session
        self.setWindowTitle("Gerador de Lista de Produção")
        self.resize(1100, 750)
        self.setMinimumSize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── SIDEBAR ──
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 20, 12, 16)
        sb_layout.setSpacing(4)

        title = QLabel("⚡ Gerador")
        title.setObjectName("AppTitle")
        sb_layout.addWidget(title)

        ver = QLabel(f"v{APP_VERSION}")
        ver.setObjectName("AppVersion")
        sb_layout.addWidget(ver)

        sb_layout.addSpacing(24)

        sep = QFrame()
        sep.setObjectName("Separator")
        sep.setFixedHeight(1)
        sb_layout.addWidget(sep)
        sb_layout.addSpacing(12)

        # ── VIEWS ──
        self.stack = QStackedWidget()

        self.views = [
            ("📊  Dashboard", DashboardView(self.db, self)),
            ("📥  Importar XLSX", ImportView(self.db, self)),
            ("📦  Produtos", ProductsView(self.db, self)),
            ("📋  Histórico", HistoryView(self.db, self)),
            ("⚙️  Configurações", SettingsView(self.db, self)),
        ]

        self.nav_buttons: list[QPushButton] = []
        for i, (label, view) in enumerate(self.views):
            self.stack.addWidget(view)

            btn = QPushButton(label)
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            # Use functools.partial to avoid lambda closure issues
            btn.clicked.connect(partial(self._on_nav_clicked, i))
            sb_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sb_layout.addStretch()

        footer = QLabel("© 2026 ColorsPro")
        footer.setObjectName("AppVersion")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(footer)

        root.addWidget(sidebar)

        # ── CONTENT AREA ──
        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.addWidget(self.stack)
        root.addWidget(content_wrapper)

        # Initial view
        self.switch_to(0)

    def _on_nav_clicked(self, index, *args):
        """Slot for sidebar navigation buttons."""
        self.switch_to(index)

    def switch_to(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        current_view = self.stack.currentWidget()
        if hasattr(current_view, 'refresh_data'):
            current_view.refresh_data()
