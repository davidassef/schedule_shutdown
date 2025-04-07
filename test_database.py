#!/usr/bin/env python
"""
Testes unitários para o módulo de banco de dados do Agendador de Desligamento.
"""

import unittest
import os
from datetime import datetime, timedelta
from database import Database
import sqlite3


class TestDatabase(unittest.TestCase):
    """Testes para a classe Database"""

    def setUp(self):
        # Usar banco de dados em memória para testes
        self.db = Database(":memory:")
        with sqlite3.connect(self.db.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    execution_time DATETIME NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_immediate BOOLEAN DEFAULT 0
                )
            """)
            conn.commit()

    def test_add_schedule(self):
        """Testa a adição de agendamentos no banco de dados"""
        now = datetime.now()
        future_time = now + timedelta(hours=2)

        # Adicionar um agendamento
        result = self.db.add_schedule("Desligar", future_time)
        self.assertTrue(result)

        # Verificar se o agendamento foi adicionado
        schedules = self.db.get_schedules()
        self.assertEqual(len(schedules), 1)
        self.assertEqual(schedules[0]["action"], "Desligar")

    def test_get_active_schedules(self):
        """Testa a obtenção de agendamentos ativos"""
        now = datetime.now()
        future_time = now + timedelta(hours=2)

        # Adicionar um agendamento ativo
        self.db.add_schedule("Desligar", future_time)

        # Adicionar um agendamento no passado (inativo)
        past_time = now - timedelta(hours=2)
        self.db.add_schedule("Reiniciar", past_time)

        # Verificar agendamentos ativos
        active = self.db.get_active_schedules()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["action"], "Desligar")

    def test_update_schedule_status(self):
        """Testa a atualização do status de um agendamento"""
        now = datetime.now()
        future_time = now + timedelta(hours=2)

        # Adicionar um agendamento
        self.db.add_schedule("Desligar", future_time)
        schedules = self.db.get_schedules()
        schedule_id = schedules[0]["id"]

        # Desativar o agendamento
        result = self.db.update_schedule_status(schedule_id, False)
        self.assertTrue(result)

        # Verificar se foi desativado
        active = self.db.get_active_schedules()
        self.assertEqual(len(active), 0)

    def test_delete_schedule(self):
        """Testa a exclusão de um agendamento"""
        now = datetime.now()
        future_time = now + timedelta(hours=2)

        # Adicionar um agendamento
        self.db.add_schedule("Desligar", future_time)
        schedules = self.db.get_schedules()
        schedule_id = schedules[0]["id"]

        # Excluir o agendamento
        result = self.db.delete_schedule(schedule_id)
        self.assertTrue(result)

        # Verificar se foi excluído
        schedules = self.db.get_schedules()
        self.assertEqual(len(schedules), 0)

    def test_update_schedule(self):
        """Testa a atualização de um agendamento"""
        now = datetime.now()
        future_time = now + timedelta(hours=2)

        # Adicionar um agendamento
        self.db.add_schedule("Desligar", future_time)
        schedules = self.db.get_schedules()
        schedule_id = schedules[0]["id"]

        # Atualizar o agendamento
        new_time = now + timedelta(hours=3)
        result = self.db.update_schedule(schedule_id, "Reiniciar", new_time)
        self.assertTrue(result)

        # Verificar se foi atualizado
        schedules = self.db.get_schedules()
        self.assertEqual(schedules[0]["action"], "Reiniciar")


if __name__ == "__main__":
    unittest.main()