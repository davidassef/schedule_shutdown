import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTableWidget, QTableWidgetItem, QPushButton, QLabel, QSpinBox)
from PyQt6.QtCore import Qt

class ColumnAdjuster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajustador de Colunas")
        self.setMinimumSize(600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Criar tabela de exemplo
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ação", "Data/Hora", "Status", "Ações"])
        self.setup_sample_data()
        
        # Valores iniciais
        self.id_width = 35
        self.action_width = 100
        self.datetime_width = 150
        self.status_width = 80
        
        # Aplicar valores iniciais
        self.update_column_widths()
        
        main_layout.addWidget(self.table)
        
        # Controles para ajustar as larguras
        controls_layout = QHBoxLayout()
        
        # ID width
        id_layout = QVBoxLayout()
        id_label = QLabel("Largura ID:")
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(20, 100)
        self.id_spinbox.setValue(self.id_width)
        self.id_spinbox.valueChanged.connect(self.on_width_changed)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_spinbox)
        controls_layout.addLayout(id_layout)
        
        # Ação width
        action_layout = QVBoxLayout()
        action_label = QLabel("Largura Ação:")
        self.action_spinbox = QSpinBox()
        self.action_spinbox.setRange(50, 200)
        self.action_spinbox.setValue(self.action_width)
        self.action_spinbox.valueChanged.connect(self.on_width_changed)
        action_layout.addWidget(action_label)
        action_layout.addWidget(self.action_spinbox)
        controls_layout.addLayout(action_layout)
        
        # Data/Hora width
        datetime_layout = QVBoxLayout()
        datetime_label = QLabel("Largura Data/Hora:")
        self.datetime_spinbox = QSpinBox()
        self.datetime_spinbox.setRange(50, 250)
        self.datetime_spinbox.setValue(self.datetime_width)
        self.datetime_spinbox.valueChanged.connect(self.on_width_changed)
        datetime_layout.addWidget(datetime_label)
        datetime_layout.addWidget(self.datetime_spinbox)
        controls_layout.addLayout(datetime_layout)
        
        # Status width
        status_layout = QVBoxLayout()
        status_label = QLabel("Largura Status:")
        self.status_spinbox = QSpinBox()
        self.status_spinbox.setRange(30, 150)
        self.status_spinbox.setValue(self.status_width)
        self.status_spinbox.valueChanged.connect(self.on_width_changed)
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_spinbox)
        controls_layout.addLayout(status_layout)
        
        main_layout.addLayout(controls_layout)
        
        # Botão para mostrar os valores
        show_values_button = QPushButton("Mostrar Valores")
        show_values_button.clicked.connect(self.show_values)
        main_layout.addWidget(show_values_button)
    
    def setup_sample_data(self):
        # Inserir alguns dados de exemplo
        self.table.setRowCount(3)
        
        # Linha 1
        self.table.setItem(0, 0, QTableWidgetItem("22"))
        self.table.setItem(0, 1, QTableWidgetItem("Desligar"))
        self.table.setItem(0, 2, QTableWidgetItem("04/04/2024 21:36"))
        self.table.setItem(0, 3, QTableWidgetItem("Ativo"))
        
        # Botões na coluna de ações
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 5, 5, 5)
        action_layout.setSpacing(8)
        
        edit_button = QPushButton("Editar")
        edit_button.setFixedWidth(70)
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout.addWidget(edit_button)
        
        delete_button = QPushButton("Excluir")
        delete_button.setFixedWidth(70)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout.addWidget(delete_button)
        action_layout.addStretch(1)
        
        self.table.setCellWidget(0, 4, action_widget)
        
        # Linha 2
        self.table.setItem(1, 0, QTableWidgetItem("23"))
        self.table.setItem(1, 1, QTableWidgetItem("Reiniciar"))
        self.table.setItem(1, 2, QTableWidgetItem("05/04/2024 08:15"))
        self.table.setItem(1, 3, QTableWidgetItem("Ativo"))
        
        # Mesmo setup de botões
        action_widget2 = QWidget()
        action_layout2 = QHBoxLayout(action_widget2)
        action_layout2.setContentsMargins(5, 5, 5, 5)
        action_layout2.setSpacing(8)
        
        edit_button2 = QPushButton("Editar")
        edit_button2.setFixedWidth(70)
        edit_button2.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout2.addWidget(edit_button2)
        
        delete_button2 = QPushButton("Excluir")
        delete_button2.setFixedWidth(70)
        delete_button2.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout2.addWidget(delete_button2)
        action_layout2.addStretch(1)
        
        self.table.setCellWidget(1, 4, action_widget2)
        
        # Linha 3
        self.table.setItem(2, 0, QTableWidgetItem("24"))
        self.table.setItem(2, 1, QTableWidgetItem("Suspender"))
        self.table.setItem(2, 2, QTableWidgetItem("06/04/2024 18:30"))
        self.table.setItem(2, 3, QTableWidgetItem("Ativo"))
        
        # Mesmo setup de botões
        action_widget3 = QWidget()
        action_layout3 = QHBoxLayout(action_widget3)
        action_layout3.setContentsMargins(5, 5, 5, 5)
        action_layout3.setSpacing(8)
        
        edit_button3 = QPushButton("Editar")
        edit_button3.setFixedWidth(70)
        edit_button3.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout3.addWidget(edit_button3)
        
        delete_button3 = QPushButton("Excluir")
        delete_button3.setFixedWidth(70)
        delete_button3.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        action_layout3.addWidget(delete_button3)
        action_layout3.addStretch(1)
        
        self.table.setCellWidget(2, 4, action_widget3)
        
        # Ajustar altura das linhas
        for i in range(3):
            self.table.setRowHeight(i, 40)
    
    def update_column_widths(self):
        # Atualizar as larguras das colunas
        self.table.setColumnWidth(0, self.id_width)       # ID
        self.table.setColumnWidth(1, self.action_width)   # Ação
        self.table.setColumnWidth(2, self.datetime_width) # Data/Hora
        self.table.setColumnWidth(3, self.status_width)   # Status
        
        # A coluna de Ações deve preencher o espaço restante
        self.table.horizontalHeader().setSectionResizeMode(4, self.table.horizontalHeader().ResizeMode.Stretch)
    
    def on_width_changed(self):
        # Obter os novos valores
        self.id_width = self.id_spinbox.value()
        self.action_width = self.action_spinbox.value()
        self.datetime_width = self.datetime_spinbox.value()
        self.status_width = self.status_spinbox.value()
        
        # Atualizar as larguras
        self.update_column_widths()
    
    def show_values(self):
        print("\nValores atuais das colunas:")
        print(f"ID: {self.id_width}")
        print(f"Ação: {self.action_width}")
        print(f"Data/Hora: {self.datetime_width}")
        print(f"Status: {self.status_width}")
        print("\nCódigo para atualizar no main.py:")
        print(f"self.schedule_table.setColumnWidth(0, {self.id_width})   # ID")
        print(f"self.schedule_table.setColumnWidth(1, {self.action_width})  # Ação")
        print(f"self.schedule_table.setColumnWidth(2, {self.datetime_width})  # Data/Hora")
        print(f"self.schedule_table.setColumnWidth(3, {self.status_width})   # Status")
        print("self.schedule_table.horizontalHeader().setSectionResizeMode(4, self.schedule_table.horizontalHeader().ResizeMode.Stretch)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColumnAdjuster()
    window.show()
    sys.exit(app.exec()) 