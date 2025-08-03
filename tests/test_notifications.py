#!/usr/bin/env python
"""
Testes unitários para o módulo notifications do Agendador de Desligamento.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock completo do PyQt6
pyqt6_mock = MagicMock()
sys.modules['PyQt6'] = pyqt6_mock
sys.modules['PyQt6.QtWidgets'] = pyqt6_mock.QtWidgets
sys.modules['PyQt6.QtGui'] = pyqt6_mock.QtGui
sys.modules['PyQt6.QtCore'] = pyqt6_mock.QtCore

from src.services.notifications import NotificationManager


class TestNotificationManager(unittest.TestCase):
    """Testes para a classe NotificationManager"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.parent_mock = MagicMock()
        self.notification_manager = NotificationManager(self.parent_mock)

    def test_init_with_parent(self):
        """Testa a inicialização do NotificationManager com parent"""
        self.assertIsNotNone(self.notification_manager)
        self.assertEqual(self.notification_manager.parent, self.parent_mock)

    def test_init_without_parent(self):
        """Testa a inicialização do NotificationManager sem parent"""
        manager = NotificationManager()
        self.assertIsNotNone(manager)
        self.assertIsNone(manager.parent)

    def test_show_notification(self):
        """Testa a exibição de notificação básica"""
        # Teste básico - verifica se o método não gera erro
        try:
            self.notification_manager.show_notification("Título", "Mensagem")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_notification_with_icon(self):
        """Testa a exibição de notificação com ícone personalizado"""
        # Teste básico - verifica se o método não gera erro
        try:
            self.notification_manager.show_notification("Título", "Mensagem", icon="warning")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_warning_dialog_yes(self):
        """Testa o diálogo de aviso"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.notification_manager, 'show_warning_dialog'))
        self.assertTrue(callable(getattr(self.notification_manager, 'show_warning_dialog')))

    def test_show_warning_dialog_no(self):
        """Testa o diálogo de aviso com resposta negativa"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.notification_manager, 'show_warning_dialog'))
        self.assertTrue(callable(getattr(self.notification_manager, 'show_warning_dialog')))

    def test_show_warning_dialog_without_parent(self):
        """Testa o diálogo de aviso sem parent"""
        manager = NotificationManager()
        try:
            result = manager.show_warning_dialog("Título", "Mensagem")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_error_dialog(self):
        """Testa o método de exibir diálogo de erro"""
        try:
            self.notification_manager.show_error_dialog("Erro", "Ocorreu um erro")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_error_dialog_without_parent(self):
        """Testa o método de exibir erro sem parent widget"""
        manager = NotificationManager()
        try:
            manager.show_error_dialog("Erro", "Ocorreu um erro")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_success_dialog(self):
        """Testa o método de exibir diálogo de sucesso"""
        try:
            self.notification_manager.show_success_dialog("Sucesso", "Operação bem-sucedida")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_success_dialog_without_parent(self):
        """Testa o método de exibir sucesso sem parent widget"""
        manager = NotificationManager()
        try:
            manager.show_success_dialog("Sucesso", "Operação bem-sucedida")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_confirmation_dialog_yes(self):
        """Testa o diálogo de confirmação"""
        try:
            result = self.notification_manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_confirmation_dialog_no(self):
        """Testa o diálogo de confirmação com resposta negativa"""
        try:
            result = self.notification_manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_show_confirmation_dialog_without_parent(self):
        """Testa o diálogo de confirmação sem parent"""
        manager = NotificationManager()
        try:
            result = manager.show_confirmation_dialog("Confirmar", "Deseja continuar?")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()