#!/usr/bin/env python
"""
Testes unitários para o módulo de ações agendadas do Agendador de Desligamento.
"""

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import sqlite3
from scheduled_actions import ScheduledActionsManager


class TestScheduledActionsManager(unittest.TestCase):
    """Testes para a classe ScheduledActionsManager"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        # Usar banco de dados em memória para testes
        self.manager = ScheduledActionsManager(":memory:")
        self.manager.database.create_tables()

    def test_add_schedule(self):
        """Testa a adição de um novo agendamento"""
        # Data futura para o agendamento
        future = datetime.now() + timedelta(days=1)

        # Adicionar um agendamento
        result = self.manager.add_schedule("Desligar", future)

        # Verificar resultado
        self.assertTrue(result)

        # Verificar se o agendamento foi adicionado
        schedules = self.manager.get_active_schedules()
        self.assertEqual(len(schedules), 1)
        self.assertEqual(schedules[0]["action"], "Desligar")

    def test_get_active_schedules(self):
        """Testa a obtenção de agendamentos ativos"""
        # Adicionar dois agendamentos para datas futuras
        future1 = datetime.now() + timedelta(hours=1)
        future2 = datetime.now() + timedelta(hours=2)

        self.manager.add_schedule("Desligar", future1)
        self.manager.add_schedule("Reiniciar", future2)

        # Obter agendamentos ativos
        schedules = self.manager.get_active_schedules()

        # Verificar resultado
        self.assertEqual(len(schedules), 2)
        self.assertEqual(schedules[0]["action"], "Desligar")  # Primeiro agendamento
        self.assertEqual(schedules[1]["action"], "Reiniciar")  # Segundo agendamento

    def test_get_next_schedule(self):
        """Testa a obtenção do próximo agendamento"""
        # Adicionar dois agendamentos com datas diferentes
        future1 = datetime.now() + timedelta(hours=2)  # Mais tarde
        future2 = datetime.now() + timedelta(hours=1)  # Mais cedo

        self.manager.add_schedule("Desligar", future1)
        self.manager.add_schedule("Reiniciar", future2)

        # Obter o próximo agendamento
        next_schedule = self.manager.get_next_schedule()

        # Verificar que retornou o mais próximo (Reiniciar)
        self.assertIsNotNone(next_schedule)
        self.assertEqual(next_schedule["action"], "Reiniciar")

    def test_get_upcoming_schedules(self):
        """Testa a obtenção de agendamentos próximos"""
        # Adicionar agendamentos com diferentes tempos
        now = datetime.now()

        # Dentro de 10 minutos
        self.manager.add_schedule("Reiniciar", now + timedelta(minutes=10))

        # Dentro de 20 minutos
        self.manager.add_schedule("Desligar", now + timedelta(minutes=20))

        # Depois de 30 minutos (fora do intervalo de 15 minutos)
        self.manager.add_schedule("Suspender", now + timedelta(minutes=30))

        # Obter agendamentos nos próximos 15 minutos
        upcoming = self.manager.get_upcoming_schedules(minutes_ahead=15)

        # Verificar resultado
        self.assertEqual(len(upcoming), 1)  # Apenas o primeiro está no intervalo
        self.assertEqual(upcoming[0]["action"], "Reiniciar")

    def test_update_schedule(self):
        """Testa a atualização de um agendamento"""
        # Adicionar um agendamento
        future = datetime.now() + timedelta(hours=1)
        self.manager.add_schedule("Desligar", future)

        # Obter o ID do agendamento
        schedule = self.manager.get_active_schedules()[0]
        schedule_id = schedule["id"]

        # Nova data e ação
        new_future = datetime.now() + timedelta(hours=2)

        # Atualizar o agendamento
        result = self.manager.update_schedule(schedule_id, "Reiniciar", new_future)

        # Verificar resultado
        self.assertTrue(result)

        # Verificar se o agendamento foi atualizado
        updated_schedule = self.manager.get_active_schedules()[0]
        self.assertEqual(updated_schedule["action"], "Reiniciar")

    def test_update_schedule_status(self):
        """Testa a atualização do status de um agendamento"""
        # Adicionar um agendamento
        future = datetime.now() + timedelta(hours=1)
        self.manager.add_schedule("Desligar", future)

        # Obter o ID do agendamento
        schedule = self.manager.get_active_schedules()[0]
        schedule_id = schedule["id"]

        # Desativar o agendamento
        result = self.manager.update_schedule_status(schedule_id, False)

        # Verificar resultado
        self.assertTrue(result)

        # Verificar se o agendamento foi desativado
        active_schedules = self.manager.get_active_schedules()
        self.assertEqual(len(active_schedules), 0)

    def test_delete_schedule(self):
        """Testa a exclusão de um agendamento"""
        # Adicionar um agendamento
        future = datetime.now() + timedelta(hours=1)
        self.manager.add_schedule("Desligar", future)

        # Obter o ID do agendamento
        schedule = self.manager.get_active_schedules()[0]
        schedule_id = schedule["id"]

        # Excluir o agendamento
        result = self.manager.delete_schedule(schedule_id)

        # Verificar resultado
        self.assertTrue(result)

        # Verificar se o agendamento foi excluído
        active_schedules = self.manager.get_active_schedules()
        self.assertEqual(len(active_schedules), 0)

    @patch('scheduled_actions.SystemActions.cancel_shutdown', return_value=True)
    def test_cancel_schedule(self, mock_cancel):
        """Testa o cancelamento de um agendamento"""
        # Adicionar um agendamento
        future = datetime.now() + timedelta(hours=1)
        self.manager.add_schedule("Desligar", future)

        # Obter o ID do agendamento
        schedule = self.manager.get_active_schedules()[0]
        schedule_id = schedule["id"]

        # Cancelar o agendamento
        result = self.manager.cancel_schedule(schedule_id)

        # Verificar resultado
        self.assertTrue(result)

        # Verificar se o método do SystemActions foi chamado
        mock_cancel.assert_called_once()

        # Verificar se o agendamento foi desativado
        active_schedules = self.manager.get_active_schedules()
        self.assertEqual(len(active_schedules), 0)


if __name__ == "__main__":
    unittest.main()