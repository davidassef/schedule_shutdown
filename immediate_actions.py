"""
Módulo para gerenciar ações imediatas/temporárias no Agendador de Desligamento.
Este módulo lida com ações que são executadas apenas uma vez e não persistem no banco de dados.
"""
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Callable

from PyQt6 import QtCore
from system_actions import SystemActions


class ImmediateAction:
    """Classe que representa uma ação imediata/temporária"""
    def __init__(self, action: str, execution_time: datetime, total_seconds: int):
        self.action = action
        self.execution_time = execution_time
        self.total_seconds = total_seconds
        self.canceled = False


class ImmediateActionsManager:
    """Gerenciador de ações imediatas que não são salvas no banco de dados"""
    def __init__(self):
        self.current_action: Optional[ImmediateAction] = None
        self.timer = QtCore.QTimer()
        self.update_callback = None

    def set_update_callback(self, callback: Callable):
        """Define uma função de callback para atualizar a interface"""
        self.update_callback = callback
        self.timer.timeout.connect(self._update_display)
        self.timer.start(1000)  # Atualiza a cada segundo

    def schedule_action(self, action: str, hours: int, minutes: int, seconds: int) -> bool:
        """Agenda uma ação imediata para execução"""
        # Verifica se já existe uma ação em andamento
        if self.current_action:
            return False

        # Calcula o tempo total em segundos
        total_seconds = hours * 3600 + minutes * 60 + seconds

        if total_seconds <= 0:
            return False

        # Calcula o horário de execução
        execution_time = datetime.now() + timedelta(seconds=total_seconds)

        # Cria e armazena a ação
        self.current_action = ImmediateAction(action, execution_time, total_seconds)

        # Agenda a ação no sistema operacional
        success = SystemActions.schedule_action(action, total_seconds)
        if not success:
            self.current_action = None
            return False

        # Inicia o timer para atualização da interface
        if not self.timer.isActive() and self.update_callback:
            self.timer.start(1000)

        return True

    def get_current_action(self) -> Optional[Dict]:
        """Retorna informações sobre a ação atual, se existir"""
        if not self.current_action:
            return None

        time_remaining = SystemActions.format_time_remaining(self.current_action.execution_time)

        return {
            "action": self.current_action.action,
            "execution_time": self.current_action.execution_time,
            "time_remaining": time_remaining,
            "total_seconds": self.current_action.total_seconds
        }

    def cancel_action(self) -> bool:
        """Cancela a ação atual em andamento, se existir"""
        if not self.current_action:
            # Tenta cancelar qualquer ação externa que possa existir
            return SystemActions.cancel_shutdown()

        self.current_action.canceled = True
        success = SystemActions.cancel_shutdown()
        self.current_action = None
        return success

    def _update_display(self):
        """Atualiza a exibição do tempo restante periodicamente"""
        if self.current_action and self.update_callback:
            # Se a ação foi concluída, limpa o estado
            if datetime.now() >= self.current_action.execution_time:
                self.current_action = None

            # Chama o callback para atualizar a interface
            self.update_callback()