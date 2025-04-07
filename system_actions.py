import os
import subprocess
import platform
from datetime import datetime


class SystemActions:
    @staticmethod
    def shutdown(timeout: int = 0) -> bool:
        """Desliga o computador após o timeout especificado (em segundos)"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/s", "/t", str(timeout)], check=True)
            else:
                subprocess.run(["shutdown", "-h", str(timeout)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar shutdown: {e}")
            return False

    @staticmethod
    def restart(timeout: int = 0) -> bool:
        """Reinicia o computador após o timeout especificado (em segundos)"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/r", "/t", str(timeout)], check=True)
            else:
                subprocess.run(["shutdown", "-r", str(timeout)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar restart: {e}")
            return False

    @staticmethod
    def suspend(timeout: int = 0) -> bool:
        """Coloca o computador em modo de suspensão"""
        try:
            if platform.system() == "Windows":
                if timeout > 0:
                    # Cria um arquivo batch temporário para executar a suspensão
                    batch_path = os.path.join(os.environ['TEMP'], 'suspend_scheduler.bat')
                    with open(batch_path, 'w', encoding="utf-8") as f:
                        f.write('@echo off\n')
                        f.write('title suspend_scheduler\n')  # Adiciona um título para identificação
                        f.write(f'timeout /t {timeout} /nobreak\n')
                        f.write('rundll32.exe powrprof.dll,SetSuspendState 0,1,0\n')
                        f.write('del "%~f0"\n')  # Auto-deletar o arquivo

                    # Executa o arquivo batch em segundo plano com um processo separado
                    process = subprocess.Popen(
                        ['cmd', '/c', 'start', '/b', batch_path],
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )

                    # Salva o PID do processo para possível cancelamento
                    try:
                        with open(os.path.join(os.environ['TEMP'], 'suspend_pid.txt'), 'w', encoding="utf-8") as f:
                            f.write(str(process.pid))
                    except OSError as e:
                        print(f"Erro ao salvar PID: {e}")
                else:
                    # Executa diretamente para suspensão imediata
                    subprocess.run(
                        ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                        check=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
            else:
                if timeout > 0:
                    subprocess.Popen(
                        f'sleep {timeout} && systemctl suspend',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    subprocess.run(["systemctl", "suspend"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar suspend: {e}")
            return False
        except OSError as e:
            print(f"Erro ao executar suspend: {e}")
            return False

    @staticmethod
    def hibernate(timeout: int = 0) -> bool:
        """Coloca o computador em modo de hibernação"""
        try:
            if platform.system() == "Windows":
                if timeout > 0:
                    # Cria um arquivo batch temporário para executar a hibernação
                    batch_path = os.path.join(os.environ['TEMP'], 'hibernate_scheduler.bat')
                    with open(batch_path, 'w', encoding="utf-8") as f:
                        f.write('@echo off\n')
                        f.write('title hibernate_scheduler\n')  # Adiciona um título para identificação
                        f.write(f'timeout /t {timeout} /nobreak\n')
                        f.write('rundll32.exe powrprof.dll,SetSuspendState 1,1,0\n')
                        f.write('del "%~f0"\n')  # Auto-deletar o arquivo

                    # Executa o arquivo batch em segundo plano com um processo separado
                    process = subprocess.Popen(
                        ['cmd', '/c', 'start', '/b', batch_path],
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )

                    # Salva o PID do processo para possível cancelamento
                    try:
                        with open(os.path.join(os.environ['TEMP'], 'hibernate_pid.txt'), 'w', encoding="utf-8") as f:
                            f.write(str(process.pid))
                    except OSError as e:
                        print(f"Erro ao salvar PID: {e}")
                else:
                    # Executa diretamente para hibernação imediata
                    subprocess.run(
                        ["rundll32.exe", "powrprof.dll,SetSuspendState", "1,1,0"],
                        check=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
            else:
                if timeout > 0:
                    subprocess.Popen(
                        f'sleep {timeout} && systemctl hibernate',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    subprocess.run(["systemctl", "hibernate"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar hibernate: {e}")
            return False
        except OSError as e:
            print(f"Erro ao executar hibernate: {e}")
            return False

    @staticmethod
    def cancel_shutdown() -> bool:
        """Cancela um desligamento, reinicialização, suspensão ou hibernação agendada"""
        try:
            if platform.system() == "Windows":
                # Cancela shutdown/restart
                result = subprocess.run(
                    ["shutdown", "/a"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Verifica se o erro é 1116 (sistema não estava sendo desligado)
                if result.returncode == 1116:
                    print("Nenhum desligamento agendado para cancelar.")
                elif result.returncode != 0:
                    print(f"Erro ao cancelar desligamento: {result.stderr}")
                    return False

                # Tenta matar processos relacionados a suspensão e hibernação
                for title in ["suspend_scheduler", "hibernate_scheduler"]:
                    try:
                        subprocess.run(
                            ["taskkill", "/F", "/FI", f"WINDOWTITLE eq {title}"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        print(f"Processos com título {title} encerrados.")
                    except subprocess.CalledProcessError as e:
                        print(f"Erro ao tentar matar processos com título {title}: {e}")

                # Verifica se existem PIDs salvos e tenta matá-los
                pid_files = ['suspend_pid.txt', 'hibernate_pid.txt']
                for pid_file in pid_files:
                    try:
                        pid_path = os.path.join(os.environ['TEMP'], pid_file)
                        if os.path.exists(pid_path):
                            with open(pid_path, 'r', encoding="utf-8") as f:
                                pid = f.read().strip()
                                if pid:
                                    subprocess.run(
                                        ["taskkill", "/F", "/PID", pid],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL,
                                        creationflags=subprocess.CREATE_NO_WINDOW
                                    )
                                    print(f"Processo com PID {pid} encerrado.")
                    except OSError as e:
                        print(f"Erro ao tentar matar processo com PID salvo em {pid_file}: {e}")

                # Remove arquivos batch temporários se existirem
                temp_files = [
                    'suspend_scheduler.bat', 'hibernate_scheduler.bat',
                    'suspend_pid.txt', 'hibernate_pid.txt'
                ]
                for file in temp_files:
                    try:
                        file_path = os.path.join(os.environ['TEMP'], file)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"Arquivo temporário {file} removido.")
                    except OSError as e:
                        print(f"Erro ao remover arquivo temporário {file}: {e}")

            else:
                # Cancela ações em sistemas baseados em Unix
                subprocess.run(["shutdown", "-c"], check=True)
                subprocess.run(["pkill", "-f", "suspend"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                subprocess.run(["pkill", "-f", "hibernate"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return True
        except subprocess.CalledProcessError as e:
            # Ignora o erro 1116 (sistema não estava sendo desligado)
            if e.returncode == 1116:
                print("Nenhuma ação agendada para cancelar.")
                return True
            print(f"Erro ao cancelar ação: {e}")
            return False
        except OSError as e:
            print(f"Erro ao cancelar ação: {e}")
            return False

    @staticmethod
    def execute_action(action: str, timeout: int = 0) -> bool:
        """Executa uma ação do sistema com base no nome"""
        actions = {
            "Desligar": SystemActions.shutdown,
            "Reiniciar": SystemActions.restart,
            "Suspender": SystemActions.suspend,
            "Hibernar": SystemActions.hibernate
        }

        if action in actions:
            return actions[action](timeout)
        return False

    @staticmethod
    def format_time_remaining(execution_time: datetime) -> str:
        """Formata o tempo restante até a execução"""
        now = datetime.now()
        if execution_time <= now:
            return "00:00:00"

        diff = execution_time - now
        total_seconds = int(diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @staticmethod
    def schedule_action(action: str, seconds: int) -> bool:
        """Agenda uma ação do sistema para executar após o número especificado de segundos"""
        try:
            if action == "Desligar":
                return SystemActions.shutdown(seconds)
            elif action == "Reiniciar":
                return SystemActions.restart(seconds)
            elif action == "Suspender":
                return SystemActions.suspend(seconds)
            elif action == "Hibernar":
                return SystemActions.hibernate(seconds)
            return False
        except OSError as e:
            print(f"Erro ao agendar ação: {e}")
            return False

    @staticmethod
    def check_windows_scheduled_shutdown():
        """Verifica se existe uma ação de desligamento agendada pelo Windows"""
        try:
            if platform.system() == "Windows":
                # Executa o comando para verificar ações de desligamento pendentes
                result = subprocess.run(
                    ["shutdown", "/s", "/a"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                # Se o código de retorno NÃO for 1116 (nenhum desligamento agendado)
                # então existe uma ação em andamento
                return result.returncode != 1116
            return False
        except Exception as e:
            print(f"Erro ao verificar ações agendadas pelo Windows: {e}")
            return False