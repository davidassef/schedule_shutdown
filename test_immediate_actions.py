#!/usr/bin/env python
"""
Testes unitários para o módulo de ações imediatas do Agendador de Desligamento.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from immediate_actions import ImmediateAction, ImmediateActionsManager


class TestImmediateActionsManager(unittest.TestCase):
    """Testes para a classe ImmediateActionsManager"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.manager = ImmediateActionsManager()

    @patch('immediate_actions.SystemActions')
    def test_schedule_action(self, mock_system_actions):
        """Testa o agendamento de uma ação imediata"""
        # Configurar o mock para retornar True ao agendar ação
        mock_system_actions.schedule_action.return_value = True

        # Agendar uma ação
        result = self.manager.schedule_action("Desligar", 1, 30, 0)

        # Verificar resultado
        self.assertTrue(result)
        self.assertIsNotNone(self.manager.current_action)
        self.assertEqual(self.manager.current_action.action, "Desligar")
        self.assertEqual(self.manager.current_action.total_seconds, 5400)  # 1h30min = 5400s

        # Verificar se o método do SystemActions foi chamado
        mock_system_actions.schedule_action.assert_called_once()

    def test_get_current_action_none(self):
        """Testa obtenção de ação atual quando não há nenhuma"""
        result = self.manager.get_current_action()
        self.assertIsNone(result)

    @patch('immediate_actions.SystemActions.schedule_action', return_value=True)
    def test_get_current_action_with_action(self, mock_schedule):
        """Testa obtenção de ação atual quando existe uma agendada"""
        # Agendar uma ação primeiro
        self.manager.schedule_action("Desligar", 1, 0, 0)

        # Obter a ação atual
        result = self.manager.get_current_action()

        # Verificar resultado
        self.assertIsNotNone(result)
        self.assertEqual(result["action"], "Desligar")
        self.assertIn("time_remaining", result)

    @patch('immediate_actions.SystemActions.cancel_shutdown', return_value=True)
    def test_cancel_action(self, mock_cancel):
        """Testa o cancelamento de uma ação imediata"""
        # Definir uma ação atual
        self.manager.current_action = ImmediateAction(
            "Desligar",
            datetime.now() + timedelta(hours=1),
            3600
        )

        # Cancelar a ação
        result = self.manager.cancel_action()

        # Verificar resultado
        self.assertTrue(result)
        self.assertIsNone(self.manager.current_action)
        mock_cancel.assert_called_once()

    @patch('immediate_actions.SystemActions.cancel_shutdown', return_value=True)
    def test_cancel_action_without_current_action(self, mock_cancel):
        """Testa o cancelamento quando não há ação atual"""
        # Garantir que não há ação atual
        self.manager.current_action = None

        # Cancelar (deve chamar o método do SystemActions mesmo assim)
        result = self.manager.cancel_action()

        # Verificar resultado
        self.assertTrue(result)
        mock_cancel.assert_called_once()

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