from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QComboBox,
                           QDateTimeEdit, QPushButton, QLabel, QFormLayout)
from PyQt6.QtCore import Qt, QDateTime
from datetime import datetime, timedelta

class ScheduleDialog(QDialog):
    def __init__(self, parent=None, schedule=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Agendamento" if schedule is None else "Editar Agendamento")
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        
        # Verifica se é modo de edição
        self.is_editing = schedule is not None
        self.schedule = schedule
        
        # Herda o tema do pai
        if hasattr(parent, "is_dark_theme"):
            self.is_dark_theme = parent.is_dark_theme
        else:
            self.is_dark_theme = False
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Form layout para os campos
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        
        # Dropdown de ação
        self.action_combo = QComboBox()
        self.action_combo.addItems(["Desligar", "Reiniciar", "Suspender", "Hibernar"])
        if self.is_editing:
            index = self.action_combo.findText(schedule["action"])
            if index >= 0:
                self.action_combo.setCurrentIndex(index)
        form_layout.addRow("Ação:", self.action_combo)
        
        # Campo de data/hora
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setCalendarPopup(True)
        if self.is_editing:
            self.datetime_edit.setDateTime(datetime.fromisoformat(schedule["execution_time"]))
        else:
            # Define para uma hora a partir de agora por padrão
            self.datetime_edit.setDateTime(datetime.now() + timedelta(hours=1))
        form_layout.addRow("Data/Hora:", self.datetime_edit)
        
        layout.addLayout(form_layout)
        
        # Botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        ok_button = QPushButton("OK")
        ok_button.setMinimumWidth(80)
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setMinimumWidth(80)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Aplica o tema
        self.setup_theme()
    
    def setup_theme(self):
        base_style = """
            QDialog {
                background-color: %s;
                color: %s;
            }
            QLabel {
                color: %s;
            }
            QComboBox {
                padding: 6px 12px;
                border: 1px solid %s;
                border-radius: 4px;
                background: %s;
                color: %s;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QDateTimeEdit {
                padding: 6px 12px;
                border: 1px solid %s;
                border-radius: 4px;
                background: %s;
                color: %s;
                min-width: 200px;
            }
            QPushButton {
                background-color: %s;
                color: %s;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        
        if self.is_dark_theme:
            self.setStyleSheet(base_style % (
                "#1e1e1e",  # Dialog background
                "#ffffff",  # Dialog text
                "#ffffff",  # Label text
                "#3d3d3d",  # ComboBox border
                "#2d2d2d",  # ComboBox background
                "#ffffff",  # ComboBox text
                "#3d3d3d",  # DateTimeEdit border
                "#2d2d2d",  # DateTimeEdit background
                "#ffffff",  # DateTimeEdit text
                "#4CAF50",  # Button background
                "#ffffff",  # Button text
                "#45a049"   # Button hover
            ))
        else:
            self.setStyleSheet(base_style % (
                "#ffffff",  # Dialog background
                "#000000",  # Dialog text
                "#000000",  # Label text
                "#e0e0e0",  # ComboBox border
                "#ffffff",  # ComboBox background
                "#000000",  # ComboBox text
                "#e0e0e0",  # DateTimeEdit border
                "#ffffff",  # DateTimeEdit background
                "#000000",  # DateTimeEdit text
                "#4CAF50",  # Button background
                "#ffffff",  # Button text
                "#45a049"   # Button hover
            ))
    
    def get_schedule_data(self):
        return {
            "action": self.action_combo.currentText(),
            "execution_time": self.datetime_edit.dateTime().toPyDateTime()
        } 