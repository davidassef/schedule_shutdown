from PyQt6.QtWidgets import QSystemTrayIcon, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from datetime import datetime
from typing import Optional

class NotificationManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.tray_icon = None
        self.setup_tray_icon()
    
    def setup_tray_icon(self):
        """Configura o ícone na bandeja do sistema"""
        if not self.tray_icon:
            self.tray_icon = QSystemTrayIcon(self.parent)
            # TODO: Adicionar ícone personalizado
            self.tray_icon.show()
    
    def show_notification(self, title: str, message: str, icon: Optional[QIcon] = None):
        """Exibe uma notificação na bandeja do sistema"""
        if self.tray_icon:
            self.tray_icon.showMessage(title, message, icon or QIcon(), 5000)
    
    def show_warning_dialog(self, action: str, execution_time: datetime) -> bool:
        """Exibe um diálogo de aviso antes da execução de uma ação"""
        if not self.parent:
            return False
        
        remaining_time = execution_time - datetime.now()
        minutes = remaining_time.seconds // 60
        seconds = remaining_time.seconds % 60
        
        message = (
            f"Uma ação de {action.lower()} está programada para ser executada em "
            f"{minutes} minutos e {seconds} segundos.\n\n"
            "Deseja cancelar esta ação?"
        )
        
        reply = QMessageBox.question(
            self.parent,
            "Aviso de Execução",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        return reply == QMessageBox.StandardButton.Yes
    
    def show_error_dialog(self, title: str, message: str):
        """Exibe um diálogo de erro"""
        if self.parent:
            QMessageBox.critical(self.parent, title, message)
    
    def show_success_dialog(self, title: str, message: str):
        """Exibe um diálogo de sucesso"""
        if self.parent:
            QMessageBox.information(self.parent, title, message)
    
    def show_confirmation_dialog(self, title: str, message: str) -> bool:
        """Exibe um diálogo de confirmação"""
        if not self.parent:
            return False
        
        reply = QMessageBox.question(
            self.parent,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        return reply == QMessageBox.StandardButton.Yes 