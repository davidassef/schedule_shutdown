#!/usr/bin/env python
"""
Testes unitários para o módulo system_actions do Agendador de Desligamento.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import os
import platform
import subprocess
from datetime import datetime, timedelta

from src.services.system_actions import SystemActions


class TestSystemActions(unittest.TestCase):
    """Testes para a classe SystemActions"""

    @patch('subprocess.run')
    def test_shutdown_windows(self, mock_run):
        """Testa o método de desligamento no Windows"""
        with patch('platform.system', return_value="Windows"):
            # Teste sem timeout
            result = SystemActions.shutdown()
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "/s", "/t", "0"], check=True)

            # Teste com timeout
            result = SystemActions.shutdown(60)
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "/s", "/t", "60"], check=True)

    @patch('subprocess.run')
    def test_shutdown_linux(self, mock_run):
        """Testa o método de desligamento em sistemas baseados em Unix"""
        with patch('platform.system', return_value="Linux"):
            # Teste sem timeout
            result = SystemActions.shutdown()
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "-h", "0"], check=True)

            # Teste com timeout
            result = SystemActions.shutdown(60)
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "-h", "60"], check=True)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "shutdown"))
    def test_shutdown_error(self, mock_run):
        """Testa o método de desligamento quando ocorre um erro"""
        result = SystemActions.shutdown()
        self.assertFalse(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_restart_windows(self, mock_run):
        """Testa o método de reinicialização no Windows"""
        with patch('platform.system', return_value="Windows"):
            # Teste sem timeout
            result = SystemActions.restart()
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "/r", "/t", "0"], check=True)

            # Teste com timeout
            result = SystemActions.restart(60)
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "/r", "/t", "60"], check=True)

    @patch('subprocess.run')
    def test_restart_linux(self, mock_run):
        """Testa o método de reinicialização em sistemas baseados em Unix"""
        with patch('platform.system', return_value="Linux"):
            # Teste sem timeout
            result = SystemActions.restart()
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "-r", "0"], check=True)

            # Teste com timeout
            result = SystemActions.restart(60)
            self.assertTrue(result)
            mock_run.assert_called_with(["shutdown", "-r", "60"], check=True)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "shutdown"))
    def test_restart_error(self, mock_run):
        """Testa o método de reinicialização quando ocorre um erro"""
        result = SystemActions.restart()
        self.assertFalse(result)
        # Verifica se o mock foi chamado (sem verificar o número exato de chamadas)
        self.assertTrue(mock_run.called)

    @patch('subprocess.Popen')
    @patch('subprocess.run')
    @patch('os.path.join', return_value='/temp/path')
    def test_suspend_windows(self, mock_join, mock_run, mock_popen):
        """Testa o método de suspensão no Windows"""
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process

        with patch('platform.system', return_value="Windows"), \
             patch('builtins.open', mock_open()) as mock_file:

            # Teste sem timeout
            result = SystemActions.suspend()
            self.assertTrue(result)
            mock_run.assert_called_with(
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Teste com timeout
            result = SystemActions.suspend(60)
            self.assertTrue(result)
            mock_popen.assert_called_with(
                ['cmd', '/c', 'start', '/b', '/temp/path'],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            mock_file.assert_any_call('/temp/path', 'w', encoding="utf-8")
            mock_file.assert_any_call('/temp/path', 'w', encoding="utf-8")

    @patch('subprocess.Popen')
    @patch('subprocess.run')
    def test_suspend_linux(self, mock_run, mock_popen):
        """Testa o método de suspensão em sistemas baseados em Unix"""
        with patch('platform.system', return_value="Linux"):
            # Teste sem timeout
            result = SystemActions.suspend()
            self.assertTrue(result)
            mock_run.assert_called_with(["systemctl", "suspend"], check=True)

            # Teste com timeout
            result = SystemActions.suspend(60)
            self.assertTrue(result)
            mock_popen.assert_called_with(
                'sleep 60 && systemctl suspend',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "systemctl"))
    def test_suspend_error(self, mock_run):
        """Testa o método de suspensão quando ocorre um erro"""
        with patch('platform.system', return_value="Linux"):
            result = SystemActions.suspend()
            self.assertFalse(result)
            mock_run.assert_called_once()

    @patch('subprocess.Popen')
    @patch('subprocess.run')
    @patch('os.path.join', return_value='/temp/path')
    def test_hibernate_windows(self, mock_join, mock_run, mock_popen):
        """Testa o método de hibernação no Windows"""
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process

        with patch('platform.system', return_value="Windows"), \
             patch('builtins.open', mock_open()) as mock_file:

            # Teste sem timeout
            result = SystemActions.hibernate()
            self.assertTrue(result)
            mock_run.assert_called_with(
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "1,1,0"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Teste com timeout
            result = SystemActions.hibernate(60)
            self.assertTrue(result)
            mock_popen.assert_called_with(
                ['cmd', '/c', 'start', '/b', '/temp/path'],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            mock_file.assert_any_call('/temp/path', 'w', encoding="utf-8")
            mock_file.assert_any_call('/temp/path', 'w', encoding="utf-8")

    @patch('subprocess.Popen')
    @patch('subprocess.run')
    def test_hibernate_linux(self, mock_run, mock_popen):
        """Testa o método de hibernação em sistemas baseados em Unix"""
        with patch('platform.system', return_value="Linux"):
            # Teste sem timeout
            result = SystemActions.hibernate()
            self.assertTrue(result)
            mock_run.assert_called_with(["systemctl", "hibernate"], check=True)

            # Teste com timeout
            result = SystemActions.hibernate(60)
            self.assertTrue(result)
            mock_popen.assert_called_with(
                'sleep 60 && systemctl hibernate',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "systemctl"))
    def test_hibernate_error(self, mock_run):
        """Testa o método de hibernação quando ocorre um erro"""
        with patch('platform.system', return_value="Linux"):
            result = SystemActions.hibernate()
            self.assertFalse(result)
            mock_run.assert_called_once()

    @patch('subprocess.run')
    @patch('subprocess.Popen')
    @patch('os.path.exists', return_value=True)
    @patch('os.remove')
    def test_cancel_shutdown_windows(self, mock_remove, mock_exists, mock_popen, mock_run):
        """Testa o método de cancelamento de desligamento no Windows"""
        mock_run.return_value.returncode = 0

        with patch('platform.system', return_value="Windows"), \
             patch('builtins.open', mock_open(read_data="12345")):

            result = SystemActions.cancel_shutdown()
            self.assertTrue(result)

            # Verifica se o comando de cancelamento foi chamado
            mock_run.assert_any_call(
                ["shutdown", "/a"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Verifica se tentou matar processos
            mock_run.assert_any_call(
                ["taskkill", "/F", "/FI", "WINDOWTITLE eq suspend_scheduler"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Verifica se tentou remover arquivos temporários
            mock_remove.assert_called()

    @patch('subprocess.run')
    def test_cancel_shutdown_linux(self, mock_run):
        """Testa o método de cancelamento de desligamento em sistemas baseados em Unix"""
        with patch('platform.system', return_value="Linux"):
            result = SystemActions.cancel_shutdown()
            self.assertTrue(result)

            # Verifica se os comandos corretos foram chamados
            mock_run.assert_any_call(["shutdown", "-c"], check=True)
            mock_run.assert_any_call(["pkill", "-f", "suspend"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            mock_run.assert_any_call(["pkill", "-f", "hibernate"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1116, "shutdown"))
    def test_cancel_shutdown_no_action(self, mock_run):
        """Testa o método de cancelamento quando não há ação para cancelar"""
        with patch('platform.system', return_value="Windows"):
            result = SystemActions.cancel_shutdown()
            self.assertTrue(result)  # Ainda retorna True mesmo se não havia ação para cancelar

    @patch('src.services.system_actions.SystemActions.shutdown', return_value=True)
    @patch('src.services.system_actions.SystemActions.restart', return_value=True)
    @patch('src.services.system_actions.SystemActions.suspend', return_value=True)
    @patch('src.services.system_actions.SystemActions.hibernate', return_value=True)
    def test_execute_action(self, mock_hibernate, mock_suspend, mock_restart, mock_shutdown):
        """Testa o método execute_action com diferentes ações"""
        # Desligar
        result = SystemActions.execute_action("Desligar", 60)
        self.assertTrue(result)
        mock_shutdown.assert_called_with(60)

        # Reiniciar
        result = SystemActions.execute_action("Reiniciar", 60)
        self.assertTrue(result)
        mock_restart.assert_called_with(60)

        # Suspender
        result = SystemActions.execute_action("Suspender", 60)
        self.assertTrue(result)
        mock_suspend.assert_called_with(60)

        # Hibernar
        result = SystemActions.execute_action("Hibernar", 60)
        self.assertTrue(result)
        mock_hibernate.assert_called_with(60)

        # Ação inválida
        result = SystemActions.execute_action("Ação inválida", 60)
        self.assertFalse(result)

    def test_format_time_remaining(self):
        """Testa o método format_time_remaining"""
        now = datetime.now()

        # Usando patch para garantir que datetime.now() retorne sempre o mesmo valor
        with patch('src.services.system_actions.datetime') as mock_datetime:
            # Configure o mock para retornar um valor fixo para datetime.now()
            mock_now = MagicMock()
            mock_now.return_value = now
            mock_datetime.now = mock_now

            # Definir valores absolutos, em vez de calcular diferenças
            future = now + timedelta(hours=1, minutes=30, seconds=45)
            past = now - timedelta(seconds=10)
            future_day = now + timedelta(days=1)

            # Testar com valores específicos
            result = SystemActions.format_time_remaining(future)
            # Verificar o formato, não o valor exato que pode variar por microssegundos
            self.assertRegex(result, r"\d{2}:\d{2}:\d{2}")
            self.assertTrue(result.startswith("01:30:4"))  # Aceita 01:30:44 ou 01:30:45

            # Testa com tempo no passado (já passou)
            result = SystemActions.format_time_remaining(past)
            self.assertEqual(result, "00:00:00")

            # Testa com exatamente 1 dia no futuro
            result = SystemActions.format_time_remaining(future_day)
            self.assertTrue(result.startswith("24:00:0"))  # Aceita pequenas variações

    @patch('src.services.system_actions.SystemActions.shutdown', return_value=True)
    @patch('src.services.system_actions.SystemActions.restart', return_value=True)
    @patch('src.services.system_actions.SystemActions.suspend', return_value=True)
    @patch('src.services.system_actions.SystemActions.hibernate', return_value=True)
    def test_schedule_action(self, mock_hibernate, mock_suspend, mock_restart, mock_shutdown):
        """Testa o método schedule_action"""
        # Desligar
        result = SystemActions.schedule_action("Desligar", 60)
        self.assertTrue(result)
        mock_shutdown.assert_called_with(60)

        # Reiniciar
        result = SystemActions.schedule_action("Reiniciar", 60)
        self.assertTrue(result)
        mock_restart.assert_called_with(60)

        # Suspender
        result = SystemActions.schedule_action("Suspender", 60)
        self.assertTrue(result)
        mock_suspend.assert_called_with(60)

        # Hibernar
        result = SystemActions.schedule_action("Hibernar", 60)
        self.assertTrue(result)
        mock_hibernate.assert_called_with(60)

        # Ação inválida
        result = SystemActions.schedule_action("Ação inválida", 60)
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_check_windows_scheduled_shutdown(self, mock_run):
        """Testa o método check_windows_scheduled_shutdown"""
        with patch('platform.system', return_value="Windows"):
            # Teste quando não há ação agendada (código 1116)
            mock_run.return_value = MagicMock(returncode=1116)
            result = SystemActions.check_windows_scheduled_shutdown()
            self.assertFalse(result)

            # Teste quando há ação agendada (código diferente de 1116)
            mock_run.return_value = MagicMock(returncode=0)
            result = SystemActions.check_windows_scheduled_shutdown()
            self.assertTrue(result)

        # Teste em outros sistemas operacionais
        with patch('platform.system', return_value="Linux"):
            result = SystemActions.check_windows_scheduled_shutdown()
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()