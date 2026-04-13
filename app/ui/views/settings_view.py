from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QCheckBox, QMessageBox, QFrame, QFormLayout,
    QComboBox, QScrollArea
)
from PySide6.QtCore import Qt

from app.models.schema import AppSettings
from app.core.updater import check_for_update, apply_update
from app.database.connection import get_data_dir
from app.themes.qss_manager import APP_VERSION


class SettingsView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.main_window = parent

        outer = QVBoxLayout(self)
        outer.setSpacing(0)

        title = QLabel("Configurações")
        title.setObjectName("PageTitle")
        outer.addWidget(title)
        sub = QLabel("Gerencie as preferências do aplicativo")
        sub.setObjectName("PageSubtitle")
        outer.addWidget(sub)
        outer.addSpacing(12)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 12, 0)

        # ═══════ GERAL ═══════
        layout.addWidget(self._section_header("🏢  Informações da Empresa"))

        general = QFrame()
        general.setObjectName("Card")
        gl = QVBoxLayout(general)
        gl.setContentsMargins(20, 16, 20, 16)
        gl.setSpacing(14)

        form1 = QFormLayout()
        form1.setSpacing(10)
        form1.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.inp_company = QLineEdit()
        self.inp_company.setPlaceholderText("Nome que aparece nas listas")
        form1.addRow("Nome da Empresa:", self.inp_company)

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["dark", "light"])
        form1.addRow("Tema da Interface:", self.combo_theme)

        gl.addLayout(form1)
        layout.addWidget(general)

        # ═══════ GITHUB ═══════
        layout.addWidget(self._section_header("🔄  Atualização Automática"))

        github = QFrame()
        github.setObjectName("Card")
        gh_layout = QVBoxLayout(github)
        gh_layout.setContentsMargins(20, 16, 20, 16)
        gh_layout.setSpacing(14)

        note = QLabel(
            f"O sistema busca automaticamente por atualizações disponibilizadas em:\n"
            f"https://github.com/emersonkenji/gerador-de-lista-de-produ-o"
        )
        note.setObjectName("PageSubtitle")
        note.setWordWrap(True)
        note.setStyleSheet("padding: 8px 12px; background: #1a1a2e; border-radius: 6px; font-size: 12px;")
        gh_layout.addWidget(note)

        form2 = QFormLayout()
        form2.setSpacing(10)
        form2.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # GitHub configuration uses a fixed repository

        # Token no longer needed since repo is public

        self.inp_version = QLineEdit()
        self.inp_version.setReadOnly(True)
        self.inp_version.setStyleSheet("background: #1a1a2e;")
        form2.addRow("Versão Atual:", self.inp_version)

        gh_layout.addLayout(form2)

        # Hidden token toggle since token input is removed

        # Update buttons
        update_row = QHBoxLayout()
        self.btn_check = QPushButton("🔍  Verificar Atualizações")
        self.btn_check.setObjectName("Secondary")
        self.btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check.clicked.connect(self._on_check_update)

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("PageSubtitle")

        update_row.addWidget(self.btn_check)
        update_row.addWidget(self.lbl_status, 1)
        gh_layout.addLayout(update_row)

        layout.addWidget(github)

        # ═══════ SUPABASE ═══════
        layout.addWidget(self._section_header("☁️  Sincronização Supabase (Opcional)"))

        supa = QFrame()
        supa.setObjectName("Card")
        sl = QVBoxLayout(supa)
        sl.setContentsMargins(20, 16, 20, 16)
        sl.setSpacing(14)

        form3 = QFormLayout()
        form3.setSpacing(10)
        form3.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.inp_supa_url = QLineEdit()
        self.inp_supa_url.setPlaceholderText("https://xyzcompany.supabase.co")
        form3.addRow("URL do Projeto:", self.inp_supa_url)

        self.inp_supa_key = QLineEdit()
        self.inp_supa_key.setPlaceholderText("eyJhbGciOi...")
        self.inp_supa_key.setEchoMode(QLineEdit.EchoMode.Password)
        form3.addRow("API Key:", self.inp_supa_key)

        self.chk_sync = QCheckBox("Habilitar sincronização automática")
        form3.addRow("", self.chk_sync)

        sl.addLayout(form3)
        layout.addWidget(supa)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        # ── Fixed save bar ──
        save_bar = QFrame()
        save_bar.setObjectName("Card")
        save_bar.setMinimumHeight(65)
        sbl = QHBoxLayout(save_bar)
        sbl.setContentsMargins(16, 12, 16, 12)

        self.lbl_saved = QLabel("")
        self.lbl_saved.setObjectName("PageSubtitle")
        sbl.addWidget(self.lbl_saved, 1)

        btn_save = QPushButton("💾  Salvar Configurações")
        btn_save.setObjectName("Primary")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self._on_save)
        sbl.addWidget(btn_save)

        outer.addWidget(save_bar)

    def _section_header(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 15px; font-weight: 700; padding: 4px 0;")
        return lbl

    # toggle visibility removed

    def refresh_data(self):
        s = self.db.query(AppSettings).first()
        if s:
            self.inp_company.setText(s.company_name or "")
            idx = self.combo_theme.findText(s.theme or "dark")
            if idx >= 0:
                self.combo_theme.setCurrentIndex(idx)
            self.inp_supa_url.setText(s.supabase_url or "")
            self.inp_supa_key.setText(s.supabase_key or "")
            self.chk_sync.setChecked(s.enable_sync or False)
        # self.inp_repo is no longer used, repo is fixed
        # token is no longer mapped
            self.inp_version.setText(s.current_version or APP_VERSION)

    def _on_save(self, *args):
        s = self.db.query(AppSettings).first()
        if not s:
            s = AppSettings()
            self.db.add(s)

        s.company_name = self.inp_company.text().strip()
        s.theme = self.combo_theme.currentText()
        s.supabase_url = self.inp_supa_url.text().strip()
        s.supabase_key = self.inp_supa_key.text().strip()
        s.enable_sync = self.chk_sync.isChecked()
        # Github repo is fixed, no need to save in DB if it won't be edited
        # token is no longer saved

        self.db.commit()
        self.lbl_saved.setText("✅  Configurações salvas!")

    def _on_check_update(self, *args):
        repo = "emersonkenji/gerador-de-lista-de-produ-o"
        token = ""
        version = self.inp_version.text().strip() or APP_VERSION

        self.lbl_status.setText("Verificando...")
        self.btn_check.setEnabled(False)

        try:
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()

            release = check_for_update(repo, version, token)
            if release:
                notes = release.get('body', '') or ''
                if len(notes) > 200:
                    notes = notes[:200] + "…"

                reply = QMessageBox.question(
                    self, "🎉 Atualização Disponível",
                    f"Nova versão: v{release['tag']}\n\n"
                    f"{release.get('name', '')}\n"
                    f"{notes}\n\n"
                    f"Deseja baixar e aplicar agora?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.lbl_status.setText("Baixando...")
                    QApplication.processEvents()

                    target = get_data_dir()
                    ok = apply_update(release, target, token)
                    if ok:
                        s = self.db.query(AppSettings).first()
                        if s:
                            s.current_version = release["tag"]
                            self.db.commit()
                            self.inp_version.setText(release["tag"])

                        QMessageBox.information(
                            self, "Atualizado",
                            f"v{release['tag']} aplicada!\nReinicie o app."
                        )
                        self.lbl_status.setText(f"✅ v{release['tag']} instalada")
                    else:
                        self.lbl_status.setText("❌ Falha")
                        QMessageBox.critical(self, "Erro", "Falha ao baixar a atualização.")
                else:
                    self.lbl_status.setText(f"v{release['tag']} disponível")
            else:
                self.lbl_status.setText("✅ Versão mais recente!")
        except Exception as e:
            self.lbl_status.setText(f"❌ {str(e)[:50]}")
        finally:
            self.btn_check.setEnabled(True)
