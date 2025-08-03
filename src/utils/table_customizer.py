import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QTableWidgetItem, QPushButton, QLabel, QSpinBox,
                            QComboBox, QGroupBox, QCheckBox, QColorDialog, QTabWidget,
                            QSlider, QLineEdit, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont

class TableCustomizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personalizador de Tabela")
        self.setMinimumSize(900, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Área da tabela (lado direito)
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        
        # Tabela de exemplo
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ação", "Data/Hora", "Status", "Ações"])
        
        # Valores iniciais
        self.id_width = 40
        self.action_width = 100
        self.datetime_width = 150
        self.status_width = 80
        self.row_height = 40
        self.button_width = 70
        self.button_spacing = 8
        self.button_font_size = 11
        self.margin = 5
        
        # Cores
        self.edit_button_bg = "#2196F3"
        self.edit_button_hover = "#1976D2"
        self.delete_button_bg = "#f44336"
        self.delete_button_hover = "#d32f2f"
        self.button_text_color = "#ffffff"
        
        # Alinhamentos de texto
        self.id_alignment = Qt.AlignmentFlag.AlignCenter
        self.action_alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self.datetime_alignment = Qt.AlignmentFlag.AlignCenter
        self.status_alignment = Qt.AlignmentFlag.AlignCenter
        
        # Configurações de botões
        self.use_stretch_in_buttons = True
        
        # Setup inicial da tabela
        self.setup_sample_data()
        self.update_table_appearance()
        
        table_layout.addWidget(self.table)
        
        # Botão para exportar configurações
        export_button = QPushButton("Exportar Configurações")
        export_button.clicked.connect(self.export_settings)
        table_layout.addWidget(export_button)
        
        # Área de configurações (lado esquerdo)
        settings_container = QScrollArea()
        settings_container.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Abas para configurações
        tabs = QTabWidget()
        
        # Aba 1: Dimensões
        dimensions_tab = QWidget()
        dimensions_layout = QVBoxLayout(dimensions_tab)
        
        # Grupo para larguras de colunas
        columns_group = QGroupBox("Largura das Colunas")
        columns_layout = QGridLayout(columns_group)
        
        # ID width
        columns_layout.addWidget(QLabel("ID:"), 0, 0)
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(20, 100)
        self.id_spinbox.setValue(self.id_width)
        self.id_spinbox.valueChanged.connect(self.on_column_width_changed)
        columns_layout.addWidget(self.id_spinbox, 0, 1)
        
        # Ação width
        columns_layout.addWidget(QLabel("Ação:"), 1, 0)
        self.action_spinbox = QSpinBox()
        self.action_spinbox.setRange(50, 200)
        self.action_spinbox.setValue(self.action_width)
        self.action_spinbox.valueChanged.connect(self.on_column_width_changed)
        columns_layout.addWidget(self.action_spinbox, 1, 1)
        
        # Data/Hora width
        columns_layout.addWidget(QLabel("Data/Hora:"), 2, 0)
        self.datetime_spinbox = QSpinBox()
        self.datetime_spinbox.setRange(50, 250)
        self.datetime_spinbox.setValue(self.datetime_width)
        self.datetime_spinbox.valueChanged.connect(self.on_column_width_changed)
        columns_layout.addWidget(self.datetime_spinbox, 2, 1)
        
        # Status width
        columns_layout.addWidget(QLabel("Status:"), 3, 0)
        self.status_spinbox = QSpinBox()
        self.status_spinbox.setRange(30, 150)
        self.status_spinbox.setValue(self.status_width)
        self.status_spinbox.valueChanged.connect(self.on_column_width_changed)
        columns_layout.addWidget(self.status_spinbox, 3, 1)
        
        dimensions_layout.addWidget(columns_group)
        
        # Altura das linhas
        row_height_group = QGroupBox("Altura das Linhas")
        row_height_layout = QHBoxLayout(row_height_group)
        row_height_layout.addWidget(QLabel("Altura:"))
        self.row_height_spinbox = QSpinBox()
        self.row_height_spinbox.setRange(20, 80)
        self.row_height_spinbox.setValue(self.row_height)
        self.row_height_spinbox.valueChanged.connect(self.on_row_height_changed)
        row_height_layout.addWidget(self.row_height_spinbox)
        dimensions_layout.addWidget(row_height_group)
        
        tabs.addTab(dimensions_tab, "Dimensões")
        
        # Aba 2: Botões
        buttons_tab = QWidget()
        buttons_layout = QVBoxLayout(buttons_tab)
        
        # Largura de botões
        button_group = QGroupBox("Configurações de Botões")
        button_layout = QGridLayout(button_group)
        
        button_layout.addWidget(QLabel("Largura:"), 0, 0)
        self.button_width_spinbox = QSpinBox()
        self.button_width_spinbox.setRange(40, 120)
        self.button_width_spinbox.setValue(self.button_width)
        self.button_width_spinbox.valueChanged.connect(self.on_button_settings_changed)
        button_layout.addWidget(self.button_width_spinbox, 0, 1)
        
        button_layout.addWidget(QLabel("Espaçamento:"), 1, 0)
        self.button_spacing_spinbox = QSpinBox()
        self.button_spacing_spinbox.setRange(0, 30)
        self.button_spacing_spinbox.setValue(self.button_spacing)
        self.button_spacing_spinbox.valueChanged.connect(self.on_button_settings_changed)
        button_layout.addWidget(self.button_spacing_spinbox, 1, 1)
        
        button_layout.addWidget(QLabel("Tamanho da Fonte:"), 2, 0)
        self.button_font_spinbox = QSpinBox()
        self.button_font_spinbox.setRange(8, 16)
        self.button_font_spinbox.setValue(self.button_font_size)
        self.button_font_spinbox.valueChanged.connect(self.on_button_settings_changed)
        button_layout.addWidget(self.button_font_spinbox, 2, 1)
        
        button_layout.addWidget(QLabel("Margens:"), 3, 0)
        self.margin_spinbox = QSpinBox()
        self.margin_spinbox.setRange(0, 20)
        self.margin_spinbox.setValue(self.margin)
        self.margin_spinbox.valueChanged.connect(self.on_button_settings_changed)
        button_layout.addWidget(self.margin_spinbox, 3, 1)
        
        # Cores dos botões
        button_layout.addWidget(QLabel("Cor Editar:"), 4, 0)
        self.edit_color_button = QPushButton()
        self.edit_color_button.setStyleSheet(f"background-color: {self.edit_button_bg};")
        self.edit_color_button.clicked.connect(self.on_edit_color_clicked)
        button_layout.addWidget(self.edit_color_button, 4, 1)
        
        button_layout.addWidget(QLabel("Cor Excluir:"), 5, 0)
        self.delete_color_button = QPushButton()
        self.delete_color_button.setStyleSheet(f"background-color: {self.delete_button_bg};")
        self.delete_color_button.clicked.connect(self.on_delete_color_clicked)
        button_layout.addWidget(self.delete_color_button, 5, 1)
        
        # Checkbox para stretch após os botões
        self.stretch_checkbox = QCheckBox("Adicionar espaço elástico após botões")
        self.stretch_checkbox.setChecked(self.use_stretch_in_buttons)
        self.stretch_checkbox.stateChanged.connect(self.on_stretch_changed)
        button_layout.addWidget(self.stretch_checkbox, 6, 0, 1, 2)
        
        buttons_layout.addWidget(button_group)
        tabs.addTab(buttons_tab, "Botões")
        
        # Aba 3: Alinhamento
        alignment_tab = QWidget()
        alignment_layout = QVBoxLayout(alignment_tab)
        
        alignment_group = QGroupBox("Alinhamento de Texto")
        alignment_grid = QGridLayout(alignment_group)
        
        # ID alignment
        alignment_grid.addWidget(QLabel("ID:"), 0, 0)
        self.id_alignment_combo = QComboBox()
        self.id_alignment_combo.addItems(["Esquerda", "Centro", "Direita"])
        self.id_alignment_combo.setCurrentIndex(1)  # Centro
        self.id_alignment_combo.currentIndexChanged.connect(self.on_alignment_changed)
        alignment_grid.addWidget(self.id_alignment_combo, 0, 1)
        
        # Ação alignment
        alignment_grid.addWidget(QLabel("Ação:"), 1, 0)
        self.action_alignment_combo = QComboBox()
        self.action_alignment_combo.addItems(["Esquerda", "Centro", "Direita"])
        self.action_alignment_combo.setCurrentIndex(0)  # Esquerda
        self.action_alignment_combo.currentIndexChanged.connect(self.on_alignment_changed)
        alignment_grid.addWidget(self.action_alignment_combo, 1, 1)
        
        # Data/Hora alignment
        alignment_grid.addWidget(QLabel("Data/Hora:"), 2, 0)
        self.datetime_alignment_combo = QComboBox()
        self.datetime_alignment_combo.addItems(["Esquerda", "Centro", "Direita"])
        self.datetime_alignment_combo.setCurrentIndex(1)  # Centro
        self.datetime_alignment_combo.currentIndexChanged.connect(self.on_alignment_changed)
        alignment_grid.addWidget(self.datetime_alignment_combo, 2, 1)
        
        # Status alignment
        alignment_grid.addWidget(QLabel("Status:"), 3, 0)
        self.status_alignment_combo = QComboBox()
        self.status_alignment_combo.addItems(["Esquerda", "Centro", "Direita"])
        self.status_alignment_combo.setCurrentIndex(1)  # Centro
        self.status_alignment_combo.currentIndexChanged.connect(self.on_alignment_changed)
        alignment_grid.addWidget(self.status_alignment_combo, 3, 1)
        
        alignment_layout.addWidget(alignment_group)
        tabs.addTab(alignment_tab, "Alinhamento")
        
        # Adicionar tabs ao layout de configurações
        settings_layout.addWidget(tabs)
        
        # Finalizar layouts
        settings_container.setWidget(settings_widget)
        main_layout.addWidget(settings_container, 1)
        main_layout.addWidget(table_container, 2)
    
    def setup_sample_data(self):
        # Inserir alguns dados de exemplo
        self.table.setRowCount(3)
        
        # Linha 1
        item_id = QTableWidgetItem("22")
        item_id.setTextAlignment(self.id_alignment)
        self.table.setItem(0, 0, item_id)
        
        item_action = QTableWidgetItem("Desligar")
        item_action.setTextAlignment(self.action_alignment)
        self.table.setItem(0, 1, item_action)
        
        item_datetime = QTableWidgetItem("04/04/2024 21:36")
        item_datetime.setTextAlignment(self.datetime_alignment)
        self.table.setItem(0, 2, item_datetime)
        
        item_status = QTableWidgetItem("Ativo")
        item_status.setTextAlignment(self.status_alignment)
        self.table.setItem(0, 3, item_status)
        
        # Botões na coluna de ações
        self.setup_action_buttons(0)
        
        # Linha 2
        item_id = QTableWidgetItem("23")
        item_id.setTextAlignment(self.id_alignment)
        self.table.setItem(1, 0, item_id)
        
        item_action = QTableWidgetItem("Reiniciar")
        item_action.setTextAlignment(self.action_alignment)
        self.table.setItem(1, 1, item_action)
        
        item_datetime = QTableWidgetItem("05/04/2024 08:15")
        item_datetime.setTextAlignment(self.datetime_alignment)
        self.table.setItem(1, 2, item_datetime)
        
        item_status = QTableWidgetItem("Ativo")
        item_status.setTextAlignment(self.status_alignment)
        self.table.setItem(1, 3, item_status)
        
        # Botões para a linha 2
        self.setup_action_buttons(1)
        
        # Linha 3
        item_id = QTableWidgetItem("24")
        item_id.setTextAlignment(self.id_alignment)
        self.table.setItem(2, 0, item_id)
        
        item_action = QTableWidgetItem("Suspender")
        item_action.setTextAlignment(self.action_alignment)
        self.table.setItem(2, 1, item_action)
        
        item_datetime = QTableWidgetItem("06/04/2024 18:30")
        item_datetime.setTextAlignment(self.datetime_alignment)
        self.table.setItem(2, 2, item_datetime)
        
        item_status = QTableWidgetItem("Ativo")
        item_status.setTextAlignment(self.status_alignment)
        self.table.setItem(2, 3, item_status)
        
        # Botões para a linha 3
        self.setup_action_buttons(2)
        
        # Ajustar altura das linhas
        for i in range(3):
            self.table.setRowHeight(i, self.row_height)
    
    def setup_action_buttons(self, row):
        # Cria botões de ação para uma linha específica
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        action_layout.setSpacing(self.button_spacing)
        
        # Botão Editar
        edit_button = QPushButton("Editar")
        edit_button.setFixedWidth(self.button_width)
        edit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.edit_button_bg};
                color: {self.button_text_color};
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: {self.button_font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.edit_button_hover};
            }}
        """)
        action_layout.addWidget(edit_button)
        
        # Botão Excluir
        delete_button = QPushButton("Excluir")
        delete_button.setFixedWidth(self.button_width)
        delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.delete_button_bg};
                color: {self.button_text_color};
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: {self.button_font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.delete_button_hover};
            }}
        """)
        action_layout.addWidget(delete_button)
        
        # Adicionar stretch se necessário
        if self.use_stretch_in_buttons:
            action_layout.addStretch(1)
        
        self.table.setCellWidget(row, 4, action_widget)
    
    def update_table_appearance(self):
        # Atualizar larguras das colunas
        self.table.setColumnWidth(0, self.id_width)       # ID
        self.table.setColumnWidth(1, self.action_width)   # Ação
        self.table.setColumnWidth(2, self.datetime_width) # Data/Hora
        self.table.setColumnWidth(3, self.status_width)   # Status
        
        # Configurar a coluna de Ações para preencher o espaço restante
        self.table.horizontalHeader().setSectionResizeMode(4, self.table.horizontalHeader().ResizeMode.Stretch)
        
        # Atualizar altura das linhas
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, self.row_height)
        
        # Atualizar botões
        for row in range(self.table.rowCount()):
            self.setup_action_buttons(row)
    
    def on_column_width_changed(self):
        # Obter novos valores de largura das colunas
        self.id_width = self.id_spinbox.value()
        self.action_width = self.action_spinbox.value()
        self.datetime_width = self.datetime_spinbox.value()
        self.status_width = self.status_spinbox.value()
        
        # Atualizar a tabela
        self.update_table_appearance()
    
    def on_row_height_changed(self):
        # Atualizar a altura das linhas
        self.row_height = self.row_height_spinbox.value()
        self.update_table_appearance()
    
    def on_button_settings_changed(self):
        # Atualizar configurações dos botões
        self.button_width = self.button_width_spinbox.value()
        self.button_spacing = self.button_spacing_spinbox.value()
        self.button_font_size = self.button_font_spinbox.value()
        self.margin = self.margin_spinbox.value()
        
        # Atualizar a tabela
        self.update_table_appearance()
    
    def on_edit_color_clicked(self):
        # Abrir seletor de cor para o botão Editar
        color = QColorDialog.getColor(QColor(self.edit_button_bg), self)
        if color.isValid():
            self.edit_button_bg = color.name()
            self.edit_button_hover = self.darken_color(color).name()
            self.edit_color_button.setStyleSheet(f"background-color: {self.edit_button_bg};")
            self.update_table_appearance()
    
    def on_delete_color_clicked(self):
        # Abrir seletor de cor para o botão Excluir
        color = QColorDialog.getColor(QColor(self.delete_button_bg), self)
        if color.isValid():
            self.delete_button_bg = color.name()
            self.delete_button_hover = self.darken_color(color).name()
            self.delete_color_button.setStyleSheet(f"background-color: {self.delete_button_bg};")
            self.update_table_appearance()
    
    def darken_color(self, color, factor=0.8):
        # Escurecer uma cor para o efeito hover
        return QColor(
            int(color.red() * factor),
            int(color.green() * factor),
            int(color.blue() * factor)
        )
    
    def on_stretch_changed(self, state):
        # Atualizar a configuração de stretch
        self.use_stretch_in_buttons = (state == Qt.CheckState.Checked.value)
        self.update_table_appearance()
    
    def on_alignment_changed(self):
        # Obter novos alinhamentos
        id_align_index = self.id_alignment_combo.currentIndex()
        action_align_index = self.action_alignment_combo.currentIndex()
        datetime_align_index = self.datetime_alignment_combo.currentIndex()
        status_align_index = self.status_alignment_combo.currentIndex()
        
        # Converter índice para flags de alinhamento
        alignments = [
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            Qt.AlignmentFlag.AlignCenter,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        ]
        
        self.id_alignment = alignments[id_align_index]
        self.action_alignment = alignments[action_align_index]
        self.datetime_alignment = alignments[datetime_align_index]
        self.status_alignment = alignments[status_align_index]
        
        # Atualizar alinhamentos nas células existentes
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0):
                self.table.item(row, 0).setTextAlignment(self.id_alignment)
            if self.table.item(row, 1):
                self.table.item(row, 1).setTextAlignment(self.action_alignment)
            if self.table.item(row, 2):
                self.table.item(row, 2).setTextAlignment(self.datetime_alignment)
            if self.table.item(row, 3):
                self.table.item(row, 3).setTextAlignment(self.status_alignment)
    
    def export_settings(self):
        # Exibir código para implementar as configurações atuais
        print("\n=== CONFIGURAÇÕES ATUAIS ===")
        print(f"Larguras de colunas:")
        print(f"  ID: {self.id_width}")
        print(f"  Ação: {self.action_width}")
        print(f"  Data/Hora: {self.datetime_width}")
        print(f"  Status: {self.status_width}")
        print(f"Altura da linha: {self.row_height}")
        print(f"Configurações de botões:")
        print(f"  Largura: {self.button_width}")
        print(f"  Espaçamento: {self.button_spacing}")
        print(f"  Tamanho da fonte: {self.button_font_size}")
        print(f"  Margens: {self.margin}")
        print(f"  Cor do botão Editar: {self.edit_button_bg}")
        print(f"  Cor hover do botão Editar: {self.edit_button_hover}")
        print(f"  Cor do botão Excluir: {self.delete_button_bg}")
        print(f"  Cor hover do botão Excluir: {self.delete_button_hover}")
        print(f"  Usar stretch após botões: {self.use_stretch_in_buttons}")
        
        # Converter alinhamentos para texto
        align_map = {
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter: "Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter",
            Qt.AlignmentFlag.AlignCenter: "Qt.AlignmentFlag.AlignCenter",
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter: "Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter"
        }
        
        print(f"Alinhamentos:")
        print(f"  ID: {align_map.get(self.id_alignment)}")
        print(f"  Ação: {align_map.get(self.action_alignment)}")
        print(f"  Data/Hora: {align_map.get(self.datetime_alignment)}")
        print(f"  Status: {align_map.get(self.status_alignment)}")
        
        print("\n=== CÓDIGO PARA IMPLEMENTAR ===")
        
        # Código para update_schedule_table
        print("\n# Em update_schedule_table:")
        print("# Configurações de botões")
        print(f"action_layout.setContentsMargins({self.margin}, {self.margin}, {self.margin}, {self.margin})")
        print(f"action_layout.setSpacing({self.button_spacing})")
        print(f"edit_button.setFixedWidth({self.button_width})")
        print(f"delete_button.setFixedWidth({self.button_width})")
        
        print("edit_button.setStyleSheet(\"\"\"")
        print(f"    QPushButton {{")
        print(f"        background-color: {self.edit_button_bg};")
        print(f"        color: {self.button_text_color};")
        print(f"        border: none;")
        print(f"        padding: 5px;")
        print(f"        border-radius: 3px;")
        print(f"        font-size: {self.button_font_size}px;")
        print(f"        font-weight: bold;")
        print(f"    }}")
        print(f"    QPushButton:hover {{")
        print(f"        background-color: {self.edit_button_hover};")
        print(f"    }}")
        print("\"\"\")")
        
        print("delete_button.setStyleSheet(\"\"\"")
        print(f"    QPushButton {{")
        print(f"        background-color: {self.delete_button_bg};")
        print(f"        color: {self.button_text_color};")
        print(f"        border: none;")
        print(f"        padding: 5px;")
        print(f"        border-radius: 3px;")
        print(f"        font-size: {self.button_font_size}px;")
        print(f"        font-weight: bold;")
        print(f"    }}")
        print(f"    QPushButton:hover {{")
        print(f"        background-color: {self.delete_button_hover};")
        print(f"    }}")
        print("\"\"\")")
        
        if self.use_stretch_in_buttons:
            print("action_layout.addStretch(1)")
        else:
            print("# Sem stretch após os botões")
        
        print("\n# Configurações de altura de linha")
        print(f"self.schedule_table.setRowHeight(row, {self.row_height})")
        
        print("\n# Configurações de largura de colunas")
        print(f"self.schedule_table.setColumnWidth(0, {self.id_width})   # ID")
        print(f"self.schedule_table.setColumnWidth(1, {self.action_width})  # Ação")
        print(f"self.schedule_table.setColumnWidth(2, {self.datetime_width})  # Data/Hora")
        print(f"self.schedule_table.setColumnWidth(3, {self.status_width})   # Status")
        print("self.schedule_table.horizontalHeader().setSectionResizeMode(4, self.schedule_table.horizontalHeader().ResizeMode.Stretch)")
        
        # Código para alinhamentos
        print("\n# Alinhamentos de texto (adicionar em update_schedule_table)")
        print("# ID")
        print(f"id_item.setTextAlignment({align_map.get(self.id_alignment)})")
        print("# Ação")
        print(f"action_item.setTextAlignment({align_map.get(self.action_alignment)})")
        print("# Data/Hora")
        print(f"time_item.setTextAlignment({align_map.get(self.datetime_alignment)})")
        print("# Status")
        print(f"status_item.setTextAlignment({align_map.get(self.status_alignment)})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableCustomizer()
    window.show()
    sys.exit(app.exec()) 