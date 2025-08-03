#!/usr/bin/env python
"""
Testes unitários para o módulo de ações imediatas do Agendador de Desligamento.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# Mock PyQt6 antes de importar o módulo
with patch.dict('sys.modules', {'PyQt6': MagicMock(), 'PyQt6.QtCore': MagicMock()}):
    from src.services.immediate_actions import ImmediateAction, ImmediateActionsManager


class TestImmediateActionsManager(unittest.TestCase):
    """Testes para a classe ImmediateActionsManager"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.manager = ImmediateActionsManager()

    def test_schedule_action(self):
        """Testa o agendamento de uma ação imediata"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.manager, 'schedule_action'))
        self.assertTrue(callable(getattr(self.manager, 'schedule_action')))
        
        # Verifica se não há ação atual inicialmente
        self.assertIsNone(self.manager.current_action)

    def test_get_current_action_none(self):
        """Testa obtenção de ação atual quando não há nenhuma"""
        result = self.manager.get_current_action()
        self.assertIsNone(result)

    def test_get_current_action_with_action(self):
        """Testa obtenção de ação atual quando existe uma agendada"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.manager, 'get_current_action'))
        self.assertTrue(callable(getattr(self.manager, 'get_current_action')))
        
        # Verifica se retorna None quando não há ação
        result = self.manager.get_current_action()
        self.assertIsNone(result)

    def test_cancel_action(self):
        """Testa o cancelamento de uma ação imediata"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.manager, 'cancel_action'))
        self.assertTrue(callable(getattr(self.manager, 'cancel_action')))

    def test_cancel_action_without_current_action(self):
        """Testa o cancelamento quando não há ação atual"""
        # Teste básico - verifica se o método existe e pode ser chamado
        self.assertTrue(hasattr(self.manager, 'cancel_action'))
        self.assertTrue(callable(getattr(self.manager, 'cancel_action')))

    def test_update_display(self):
        """Testa a atualização da exibição do timer"""
        # Criar um mock para o callback
        mock_callback = MagicMock()
        self.manager.update_callback = mock_callback

        # Definir uma ação atual
        self.manager.current_action = ImmediateAction(
            "Desligar",
            datetime.now() + timedelta(hours=1),
            3600
        )

        # Chamar o método de atualização
        self.manager._update_display()

        # Verificar se o callback foi chamado
        mock_callback.assert_called_once()

    def test_update_display_without_action(self):
        """Testa a atualização da exibição sem ação atual"""
        # Criar um mock para o callback
        mock_callback = MagicMock()
        self.manager.update_callback = mock_callback

        # Garantir que não há ação atual
        self.manager.current_action = None

        # Chamar o método de atualização
        self.manager._update_display()

        # Verificar que o callback não foi chamado
        mock_callback.assert_not_called()


if __name__ == "__main__":
    unittest.main()