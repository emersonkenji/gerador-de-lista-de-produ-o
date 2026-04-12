import sys
import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from app.database.connection import SessionLocal
from app.database.init_db import init_db
from app.ui.main_window import MainWindow
from app.themes.qss_manager import get_theme
from app.models.schema import AppSettings

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Iniciando Gerador de Lista de Produção...")

    # Initialize DB
    init_db()

    # Start session
    db_session = SessionLocal()

    # Read theme preference
    settings = db_session.query(AppSettings).first()
    theme_mode = settings.theme if settings and settings.theme else "dark"

    app = QApplication(sys.argv)

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Apply theme
    app.setStyleSheet(get_theme(theme_mode))

    # Create and show main window
    window = MainWindow(db_session)
    window.show()

    logger.info("Aplicativo pronto.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
