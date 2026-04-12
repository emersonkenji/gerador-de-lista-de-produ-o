from functools import partial

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QMessageBox, QComboBox, QFrame, QTabWidget, QGridLayout
)
from PySide6.QtCore import Qt

from app.models.schema import ProductMapping, TypeVariation, VolumeVariation


class ProductsView(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self._all_mappings = []

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Produtos e Variações")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        sub = QLabel("Gerencie mapeamentos de produtos, tipos de tinta e litragens")
        sub.setObjectName("PageSubtitle")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #27272a; border-radius: 8px; padding: 8px; }
            QTabBar::tab { padding: 8px 20px; font-weight: 600; border-radius: 6px 6px 0 0; }
            QTabBar::tab:selected { background: #6366f1; color: #fff; }
            QTabBar::tab:!selected { background: #18181b; color: #a1a1aa; }
        """)

        # Tab 1: Mapeamentos de Produto
        self.tabs.addTab(self._build_mappings_tab(), "📦  Mapeamentos")
        # Tab 2: Tipos de Tinta
        self.tabs.addTab(self._build_types_tab(), "🎨  Tipos de Tinta")
        # Tab 3: Litragens
        self.tabs.addTab(self._build_volumes_tab(), "📏  Litragens")

        layout.addWidget(self.tabs, 1)

    # ═══════════════════ TAB 1: MAPEAMENTOS ═══════════════════

    def _build_mappings_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)

        # Add form
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        fl = QVBoxLayout(form_frame)
        fl.setContentsMargins(14, 12, 14, 12)
        fl.setSpacing(8)

        fl.addWidget(QLabel("Adicionar Novo Mapeamento"))

        row1 = QHBoxLayout()
        self.input_pattern = QLineEdit()
        self.input_pattern.setPlaceholderText("Título ou padrão do produto")
        self.input_keywords = QLineEdit()
        self.input_keywords.setPlaceholderText("Palavras-chave (vírgula)")
        row1.addWidget(self.input_pattern, 2)
        row1.addWidget(self.input_keywords, 1)
        fl.addLayout(row1)

        row2 = QHBoxLayout()
        self.combo_type = QComboBox()
        self.combo_vol = QComboBox()
        self.combo_vol.addItem("Automático")

        self.btn_add = QPushButton("➕  Adicionar")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.clicked.connect(self._on_add)

        row2.addWidget(QLabel("Tipo:"))
        row2.addWidget(self.combo_type)
        row2.addWidget(QLabel("Litragem:"))
        row2.addWidget(self.combo_vol)
        row2.addStretch()
        row2.addWidget(self.btn_add)
        fl.addLayout(row2)

        layout.addWidget(form_frame)

        # Filter bar
        filter_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Buscar por título ou keyword...")
        self.search_input.textChanged.connect(self._on_filter_changed)

        self.filter_type = QComboBox()
        self.filter_type.currentTextChanged.connect(self._on_filter_changed)

        self.filter_source = QComboBox()
        self.filter_source.addItems(["Todos", "Manual", "Automático"])
        self.filter_source.currentTextChanged.connect(self._on_filter_changed)

        filter_bar.addWidget(self.search_input, 2)
        filter_bar.addWidget(self.filter_type)
        filter_bar.addWidget(self.filter_source)
        layout.addLayout(filter_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título / Padrão", "Keywords", "Tipo", "Litragem", "Var.", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

        self.lbl_count = QLabel("")
        self.lbl_count.setObjectName("PageSubtitle")
        layout.addWidget(self.lbl_count)

        return w

    # ═══════════════════ TAB 2: TIPOS ═══════════════════

    def _build_types_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)

        desc = QLabel(
            "Cadastre tipos de tinta personalizados. Eles aparecem nos dropdowns de classificação."
        )
        desc.setObjectName("PageSubtitle")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        add_row = QHBoxLayout()
        self.inp_new_type = QLineEdit()
        self.inp_new_type.setPlaceholderText("Nome do novo tipo (ex: Texturizada)")
        btn_add_type = QPushButton("➕  Adicionar Tipo")
        btn_add_type.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_type.clicked.connect(self._on_add_type)
        add_row.addWidget(self.inp_new_type, 1)
        add_row.addWidget(btn_add_type)
        layout.addLayout(add_row)

        self.types_table = QTableWidget()
        self.types_table.setColumnCount(3)
        self.types_table.setHorizontalHeaderLabels(["ID", "Nome do Tipo", "Ações"])
        self.types_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.types_table.setAlternatingRowColors(True)
        layout.addWidget(self.types_table, 1)

        return w

    # ═══════════════════ TAB 3: VOLUMES ═══════════════════

    def _build_volumes_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)

        desc = QLabel(
            "Cadastre litragens personalizadas. Elas aparecem nos dropdowns de classificação."
        )
        desc.setObjectName("PageSubtitle")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        add_row = QHBoxLayout()
        self.inp_new_vol = QLineEdit()
        self.inp_new_vol.setPlaceholderText("Nova litragem (ex: 20L)")
        btn_add_vol = QPushButton("➕  Adicionar Litragem")
        btn_add_vol.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_vol.clicked.connect(self._on_add_volume)
        add_row.addWidget(self.inp_new_vol, 1)
        add_row.addWidget(btn_add_vol)
        layout.addLayout(add_row)

        self.vols_table = QTableWidget()
        self.vols_table.setColumnCount(3)
        self.vols_table.setHorizontalHeaderLabels(["ID", "Litragem", "Ações"])
        self.vols_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.vols_table.setAlternatingRowColors(True)
        layout.addWidget(self.vols_table, 1)

        return w

    # ═══════════════════ ACTIONS ═══════════════════

    def _on_add(self, *args):
        pattern = self.input_pattern.text().strip()
        if not pattern:
            QMessageBox.warning(self, "Aviso", "Informe o padrão/título do produto.")
            return
        vol = self.combo_vol.currentText()
        if vol == "Automático":
            vol = None
        new_map = ProductMapping(
            title_pattern=pattern,
            keywords=self.input_keywords.text().strip(),
            product_type=self.combo_type.currentText(),
            default_volume=vol,
            auto_registered=False
        )
        self.db.add(new_map)
        self.db.commit()
        self.input_pattern.clear()
        self.input_keywords.clear()
        self.refresh_data()

    def _on_add_type(self, *args):
        name = self.inp_new_type.text().strip()
        if not name:
            return
        exists = self.db.query(TypeVariation).filter(TypeVariation.name == name).first()
        if exists:
            QMessageBox.warning(self, "Aviso", f"O tipo '{name}' já existe.")
            return
        self.db.add(TypeVariation(name=name))
        self.db.commit()
        self.inp_new_type.clear()
        self.refresh_data()

    def _on_add_volume(self, *args):
        name = self.inp_new_vol.text().strip()
        if not name:
            return
        exists = self.db.query(VolumeVariation).filter(VolumeVariation.name == name).first()
        if exists:
            QMessageBox.warning(self, "Aviso", f"A litragem '{name}' já existe.")
            return
        self.db.add(VolumeVariation(name=name))
        self.db.commit()
        self.inp_new_vol.clear()
        self.refresh_data()

    def _on_delete_mapping(self, mid, *args):
        reply = QMessageBox.question(
            self, "Confirmar Exclusão", "Excluir este mapeamento?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            m = self.db.query(ProductMapping).filter(ProductMapping.id == mid).first()
            if m:
                self.db.delete(m)
                self.db.commit()
                self.refresh_data()

    def _on_delete_type(self, tid, *args):
        reply = QMessageBox.question(
            self, "Confirmar", "Excluir este tipo de tinta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            t = self.db.query(TypeVariation).filter(TypeVariation.id == tid).first()
            if t:
                self.db.delete(t)
                self.db.commit()
                self.refresh_data()

    def _on_delete_volume(self, vid, *args):
        reply = QMessageBox.question(
            self, "Confirmar", "Excluir esta litragem?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            v = self.db.query(VolumeVariation).filter(VolumeVariation.id == vid).first()
            if v:
                self.db.delete(v)
                self.db.commit()
                self.refresh_data()

    # ═══════════════════ REFRESH ═══════════════════

    def refresh_data(self):
        # Reload types from DB
        types = self.db.query(TypeVariation).filter(TypeVariation.is_active == True).all()
        type_names = [t.name for t in types]

        # Update combo_type (mapping form)
        current = self.combo_type.currentText()
        self.combo_type.clear()
        self.combo_type.addItems(type_names)
        if current in type_names:
            self.combo_type.setCurrentText(current)

        # Update filter
        current_filter = self.filter_type.currentText()
        self.filter_type.clear()
        self.filter_type.addItems(["Todos"] + type_names + ["Outros"])
        if current_filter in (["Todos"] + type_names + ["Outros"]):
            self.filter_type.setCurrentText(current_filter)

        # Update combo_vol (mapping form)
        vols = self.db.query(VolumeVariation).filter(VolumeVariation.is_active == True).all()
        vol_names = [v.name for v in vols]
        current_vol = self.combo_vol.currentText()
        self.combo_vol.clear()
        self.combo_vol.addItems(["Automático"] + vol_names)
        if current_vol in (["Automático"] + vol_names):
            self.combo_vol.setCurrentText(current_vol)

        # Refresh mappings table
        self._all_mappings = self.db.query(ProductMapping).order_by(ProductMapping.id.desc()).all()
        self._apply_filter()

        # Refresh types table
        self._refresh_types_table(types)

        # Refresh volumes table
        self._refresh_vols_table(vols)

    def _refresh_types_table(self, types):
        self.types_table.setRowCount(0)
        for t in types:
            idx = self.types_table.rowCount()
            self.types_table.insertRow(idx)
            self.types_table.setItem(idx, 0, QTableWidgetItem(str(t.id)))
            self.types_table.setItem(idx, 1, QTableWidgetItem(t.name))

            btn = QPushButton("🗑️  Excluir")
            btn.setObjectName("Destructive")
            btn.setFixedWidth(90)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(partial(self._on_delete_type, t.id))
            self.types_table.setCellWidget(idx, 2, btn)

    def _refresh_vols_table(self, vols):
        self.vols_table.setRowCount(0)
        for v in vols:
            idx = self.vols_table.rowCount()
            self.vols_table.insertRow(idx)
            self.vols_table.setItem(idx, 0, QTableWidgetItem(str(v.id)))
            self.vols_table.setItem(idx, 1, QTableWidgetItem(v.name))

            btn = QPushButton("🗑️  Excluir")
            btn.setObjectName("Destructive")
            btn.setFixedWidth(90)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(partial(self._on_delete_volume, v.id))
            self.vols_table.setCellWidget(idx, 2, btn)

    def _on_filter_changed(self, *args):
        self._apply_filter()

    def _apply_filter(self):
        search = self.search_input.text().lower().strip()
        type_filter = self.filter_type.currentText()
        source_filter = self.filter_source.currentText()

        filtered = []
        for m in self._all_mappings:
            if type_filter != "Todos" and m.product_type != type_filter:
                continue
            if source_filter == "Manual" and m.auto_registered:
                continue
            if source_filter == "Automático" and not m.auto_registered:
                continue
            if search:
                haystack = f"{m.title_pattern} {m.keywords or ''}".lower()
                if search not in haystack:
                    continue
            filtered.append(m)

        self.table.setRowCount(0)
        for m in filtered:
            idx = self.table.rowCount()
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(str(m.id)))

            title_text = m.title_pattern
            if len(title_text) > 65:
                title_text = title_text[:65] + "…"
            ti = QTableWidgetItem(title_text)
            if m.auto_registered:
                ti.setToolTip("Auto-cadastrado via XLSX")
            self.table.setItem(idx, 1, ti)

            self.table.setItem(idx, 2, QTableWidgetItem(m.keywords or "—"))
            self.table.setItem(idx, 3, QTableWidgetItem(m.product_type))
            self.table.setItem(idx, 4, QTableWidgetItem(m.default_volume or "Auto"))
            self.table.setItem(idx, 5, QTableWidgetItem(str(m.variation_count or 0)))

            btn = QPushButton("🗑️  Excluir")
            btn.setObjectName("Destructive")
            btn.setFixedWidth(90)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(partial(self._on_delete_mapping, m.id))
            self.table.setCellWidget(idx, 6, btn)

        self.lbl_count.setText(f"{len(filtered)} de {len(self._all_mappings)} mapeamento(s)")
