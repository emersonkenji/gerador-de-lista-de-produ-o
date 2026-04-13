"""QSS Theme Manager — Estilo profissional inspirado em Shadcn/UI."""
from app.version import VERSION

# Versão atual do app (usada na sidebar e updater)
APP_VERSION = VERSION


def get_theme(mode: str = "dark") -> str:
    if mode == "dark":
        bg = "#0a0a0b"
        bg_elevated = "#111113"
        card_bg = "#18181b"
        text = "#fafafa"
        text_secondary = "#a1a1aa"
        border = "#27272a"
        hover = "#27272a"
        accent = "#6366f1"       # Indigo
        accent_hover = "#818cf8"
        primary_btn_bg = "#6366f1"
        primary_btn_text = "#ffffff"
        destructive = "#ef4444"
        success = "#22c55e"
        warning = "#eab308"
        input_bg = "#09090b"
        sidebar_bg = "#111113"
        badge_bg = "#27272a"
    else:
        bg = "#fafafa"
        bg_elevated = "#ffffff"
        card_bg = "#ffffff"
        text = "#09090b"
        text_secondary = "#71717a"
        border = "#e4e4e7"
        hover = "#f4f4f5"
        accent = "#6366f1"
        accent_hover = "#4f46e5"
        primary_btn_bg = "#6366f1"
        primary_btn_text = "#ffffff"
        destructive = "#dc2626"
        success = "#16a34a"
        warning = "#ca8a04"
        input_bg = "#ffffff"
        sidebar_bg = "#f4f4f5"
        badge_bg = "#e4e4e7"

    return f"""
    /* ===== GLOBAL ===== */
    * {{
        font-family: "Segoe UI", "Inter", system-ui, sans-serif;
        font-size: 13px;
    }}
    QWidget {{
        background-color: {bg};
        color: {text};
    }}

    /* ===== SIDEBAR ===== */
    QFrame#Sidebar {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}

    QLabel#AppTitle {{
        font-size: 18px;
        font-weight: 700;
        color: {accent};
        padding: 4px 0px;
    }}
    QLabel#AppVersion {{
        font-size: 11px;
        color: {text_secondary};
        padding: 0px;
    }}

    /* Sidebar nav buttons */
    QPushButton#NavBtn {{
        background-color: transparent;
        color: {text_secondary};
        text-align: left;
        padding: 10px 14px;
        border-radius: 8px;
        border: none;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#NavBtn:hover {{
        background-color: {hover};
        color: {text};
    }}
    QPushButton#NavBtn:checked {{
        background-color: {accent};
        color: {primary_btn_text};
        font-weight: 600;
    }}

    /* ===== CARDS ===== */
    QFrame#Card {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 16px;
    }}

    /* ===== LABELS ===== */
    QLabel#PageTitle {{
        font-size: 22px;
        font-weight: 700;
        color: {text};
        padding-bottom: 4px;
    }}
    QLabel#PageSubtitle {{
        font-size: 13px;
        color: {text_secondary};
    }}
    QLabel#CardTitle {{
        font-size: 12px;
        font-weight: 600;
        color: {text_secondary};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    QLabel#CardValue {{
        font-size: 28px;
        font-weight: 700;
        color: {text};
    }}
    QLabel#Badge {{
        background-color: {badge_bg};
        color: {text_secondary};
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
    }}
    QLabel#BadgeSuccess {{
        background-color: {success};
        color: #ffffff;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
    }}
    QLabel#BadgePending {{
        background-color: {warning};
        color: #000000;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
    }}

    /* ===== BUTTONS ===== */
    QPushButton {{
        background-color: {primary_btn_bg};
        color: {primary_btn_text};
        border: none;
        border-radius: 8px;
        padding: 9px 18px;
        font-weight: 600;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background-color: {accent_hover};
    }}
    QPushButton:disabled {{
        background-color: {border};
        color: {text_secondary};
    }}
    QPushButton#Secondary {{
        background-color: transparent;
        color: {text};
        border: 1px solid {border};
    }}
    QPushButton#Secondary:hover {{
        background-color: {hover};
    }}
    QPushButton#Destructive {{
        background-color: {destructive};
        color: #ffffff;
    }}
    QPushButton#Destructive:hover {{
        background-color: #b91c1c;
    }}
    QPushButton#DestructiveTable {{
        background-color: {destructive};
        color: #ffffff;
        padding: 5px 10px;
        font-size: 11px;
    }}
    QPushButton#DestructiveTable:hover {{
        background-color: #b91c1c;
    }}
    QPushButton#Ghost {{
        background-color: transparent;
        color: {accent};
        border: none;
        padding: 6px 10px;
    }}
    QPushButton#Ghost:hover {{
        background-color: {hover};
    }}

    /* ===== INPUTS ===== */
    QLineEdit, QComboBox {{
        background-color: {input_bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QComboBox:focus {{
        border: 2px solid {accent};
    }}
    QLineEdit::placeholder {{
        color: {text_secondary};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {card_bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 6px;
        selection-background-color: {accent};
        selection-color: {primary_btn_text};
    }}

    /* ===== TEXTEDIT ===== */
    QTextEdit, QPlainTextEdit {{
        background-color: {input_bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 10px;
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 13px;
    }}

    /* ===== TABLE ===== */
    QTableWidget, QTableView {{
        background-color: {card_bg};
        alternate-background-color: {bg_elevated};
        color: {text};
        gridline-color: {border};
        border: 1px solid {border};
        border-radius: 8px;
        outline: none;
    }}
    QTableWidget::item {{
        padding: 6px 8px;
        border-bottom: 1px solid {border};
        color: {text};
        background-color: {card_bg};
    }}
    QTableWidget::item:alternate {{
        background-color: {bg_elevated};
        color: {text};
    }}
    QTableWidget::item:selected {{
        background-color: {accent};
        color: {primary_btn_text};
    }}
    QHeaderView::section {{
        background-color: {bg_elevated};
        color: {text_secondary};
        padding: 8px;
        border: none;
        border-bottom: 2px solid {border};
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
    }}

    /* ===== SCROLLBAR ===== */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {border};
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {text_secondary};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {border};
        border-radius: 4px;
        min-width: 30px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    /* ===== CHECKBOX ===== */
    QCheckBox {{
        spacing: 8px;
        color: {text};
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid {border};
        background-color: {input_bg};
    }}
    QCheckBox::indicator:checked {{
        background-color: {accent};
        border-color: {accent};
    }}

    /* ===== PROGRESS BAR ===== */
    QProgressBar {{
        background-color: {border};
        border-radius: 4px;
        height: 6px;
        text-align: center;
        font-size: 0px;
    }}
    QProgressBar::chunk {{
        background-color: {accent};
        border-radius: 4px;
    }}

    /* ===== SEPARATOR ===== */
    QFrame#Separator {{
        background-color: {border};
        max-height: 1px;
    }}
    """
