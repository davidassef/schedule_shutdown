#!/usr/bin/env python
"""
Testes unitários para o módulo notifications do Agendador de Desligamento.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from PyQt6.QtWidgets import QSystemTrayIcon, QMessageBox
from PyQt6.QtGui import QIcon

from notifications import NotificationManager


class TestNotificationManager(unittest.TestCase):
    """Testes para a classe NotificationManager"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        # Criar mocks para os componentes Qt
        self.parent_mock = MagicMock()

        # Patches para classes Qt
        self.tray_icon_patch = patch('notifications.QSystemTrayIcon')
        self.message_box_patch = patch('notifications.QMessageBox')
        self.icon_patch = patch('notifications.QIcon')

        # Iniciar os patches
        self.mock_tray_icon_class = self.tray_icon_patch.start()
        self.mock_message_box = self.message_box_patch.start()
        self.mock_icon_class = self.icon_patch.start()

        # Configurar retornos dos mocks
        self.mock_tray_instance = MagicMock()
        self.mock_tray_icon_class.return_value = self.mock_tray_instance

        self.mock_icon_instance = MagicMock()
        self.mock_icon_class.return_value = self.mock_icon_instance

        # Configurar o valor padrão de StandardButton.Yes para os testes
        self.mock_message_box.StandardButton.Yes = QMessageBox.StandardButton.Yes
        self.mock_message_box.StandardButton.No = QMessageBox.StandardButton.No

    def tearDown(self):
        """Limpeza executada após cada teste"""
        # Parar todos os patches
        self.tray_icon_patch.stop()
        self.message_box_patch.stop()
        self.icon_patch.stop()

    def test_init_with_parent(self):
        """Testa a inicialização com um parent widget"""
        manager = NotificationManager(parent=self.parent_mock)

        # Verificar se o tray_icon foi criado e mostrado
        self.mock_tray_icon_class.assert_called_once_with(self.parent_mock)
        self.mock_tray_instance.show.assert_called_once()

    def test_init_without_parent(self):
        """Testa a inicialização sem parent widget"""
        manager = NotificationManager()

        # Verificar se o tray_icon foi criado e mostrado
        self.mock_tray_icon_class.assert_called_once_with(None)
        self.mock_tray_instance.show.assert_called_once()

    def test_show_notification(self):
        """Testa o método de exibir notificação"""
        manager = NotificationManager(parent=self.parent_mock)

        # Simular exibição de notificação
        manager.show_notification("Título", "Mensagem")

        # Verificar se o método showMessage foi chamado corretamente
        self.mock_tray_instance.showMessage.assert_called_once_with(
            "Título", "Mensagem", self.mock_icon_instance, 5000
        )

    def test_show_notification_with_icon(self):
        """Testa o método de exibir notificação com ícone personalizado"""
        manager = NotificationManager(parent=self.parent_mock)
        custom_icon = MagicMock(spec=QIcon)

        # Simular exibição de notificação com ícone personalizado
        manager.show_notification("Título", "Mensagem", custom_icon)

        # Verificar se o método showMessage foi chamado com o ícone personalizado
        self.mock_tray_instance.showMessage.assert_called_once_with(
            "Título", "Mensagem", custom_icon, 5000
        )

    def test_show_warning_dialog_yes(self):
        """Testa o diálogo de aviso quando o usuário seleciona Sim"""
        # Configurar o mock para simular que o usuário clicou em "Sim"
        self.mock_message_box.question.return_value = self.mock_message_box.StandardButton.Yes

        manager = NotificationManager(parent=self.parent_mock)
        execution_time = datetime.now() + timedelta(minutes=5, seconds=30)

        # Chamar o método
        result = manager.show_warning_dialog("Desligar", execution_time)

        # Verificar se o diálogo foi exibido corretamente
        self.mock_message_box.question.assert_called_once()
        self.assertTrue(result)  # Deve retornar True para "Sim"

    def test_show_warning_dialog_no(self):
        """Testa o diálogo de aviso quando o usuário seleciona Não"""
        # Configurar o mock para simular que o usuário clicou em "Não"
        self.mock_message_box.question.return_value = self.mock_message_box.StandardButton.No

        manager = NotificationManager(parent=self.parent_mock)
        execution_time = datetime.now() + timedelta(minutes=5, seconds=30)

        # Chamar o método
        result = manager.show_warning_dialog("Desligar", execution_time)

        # Verificar se o diálogo foi exibido corretamente
        self.mock_message_box.question.assert_called_once()
        self.assertFalse(result)  # Deve retornar False para "Não"

    def test_show_warning_dialog_without_parent(self):
        """Testa o diálogo de aviso quando não há parent widget"""
        manager = NotificationManager()  # Sem parent
        execution_time = datetime.now() + timedelta(minutes=5)

        # Chamar o método
        result = manager.show_warning_dialog("Desligar", execution_time)

        # Verificar que o diálogo não foi exibido e retornou False
        self.mock_message_box.question.assert_not_called()
        self.assertFalse(result)

    def test_show_error_dialog(self):
        """Testa o método de exibir diálogo de erro"""
        manager = NotificationManager(parent=self.parent_mock)

        # Simular exibição de erro
        manager.show_error_dialog("Erro", "Ocorreu um erro")

        # Verificar se o método critical foi chamado corretamente
        self.mock_message_box.critical.assert_called_once_with(
            self.parent_mock, "Erro", "Ocorreu um erro"
        )

    def test_show_error_dialog_without_parent(self):
        """Testa o método de exibir erro sem parent widget"""
        manager = NotificationManager()  # Sem parent

        # Simular exibição de erro
        manager.show_error_dialog("Erro", "Ocorreu um erro")

        # Verificar que o diálogo não foi exibido
        self.mock_message_box.critical.assert_not_called()

    def test_show_success_dialog(self):
        """Testa o método de exibir diálogo de sucesso"""
        manager = NotificationManager(parent=self.parent_mock)

        # Simular exibição de sucesso
        manager.show_success_dialog("Sucesso", "Operação bem-sucedida")

        # Verificar se o método information foi chamado corretamente
        self.mock_message_box.information.assert_called_once_with(
            self.parent_mock, "Sucesso", "Operação bem-sucedida"
        )

    def test_show_success_dialog_without_parent(self):
        """Testa o método de exibir sucesso sem parent widget"""
        manager = NotificationManager()  # Sem parent

        # Simular exibição de sucesso
        manager.show_success_dialog("Sucesso", "Operação bem-sucedida")

        # Verificar que o diálogo não foi exibido
        self.mock_message_box.information.assert_not_called()

    def test_show_confirmation_dialog_yes(self):
        """Testa o diálogo de confirmação quando o usuário seleciona Sim"""
        # Configurar o mock para simular que o usuário clicou em "Sim"
        self.mock_message_box.question.return_value = self.mock_message_box.StandardButton.Yes

        manager = NotificationManager(parent=self.parent_mock)

        # Chamar o método
        result = manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")

        # Verificar se o diálogo foi exibido corretamente
        self.mock_message_box.question.assert_called_once()
        self.assertTrue(result)  # Deve retornar True para "Sim"

    def test_show_confirmation_dialog_no(self):
        """Testa o diálogo de confirmação quando o usuário seleciona Não"""
        # Configurar o mock para simular que o usuário clicou em "Não"
        self.mock_message_box.question.return_value = self.mock_message_box.StandardButton.No

        manager = NotificationManager(parent=self.parent_mock)

        # Chamar o método
        result = manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")

        # Verificar se o diálogo foi exibido corretamente
        self.mock_message_box.question.assert_called_once()
        self.assertFalse(result)  # Deve retornar False para "Não"

    def test_show_confirmation_dialog_without_parent(self):
        """Testa o diálogo de confirmação quando não há parent widget"""
        manager = NotificationManager()  # Sem parent

        # Chamar o método
        result = manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")

        # Verificar que o diálogo não foi exibido e retornou False
        self.mock_message_box.question.assert_not_called()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()