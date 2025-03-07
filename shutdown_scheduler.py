import sys, os, json, locale, threading, time, requests, winreg
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtCore, QtGui

# ----------------- Configurações Globais -----------------
AGENDAMENTOS_FILE = "agendamentos.json"
APP_NAME = "ShutdownScheduler"
agendamentos = []
current_language = "en"  # Será atualizado conforme escolha do usuário

texts = {
    "pt": {
        "programar": "Programar Desligamento",
        "agendamentos": "Agendamentos",
        "opcoes": "Opções",
        "acao": "Ação:",
        "hora": "Hora:",
        "min": "Min:",
        "seg": "Seg:",
        "iniciar_windows": "Iniciar com o Windows",
        "iniciar": "Iniciar",
        "novo_agendamento": "Novo Agendamento",
        "editar": "Editar",
        "deletar": "Deletar",
        "repetir_tarefa": "Repetir tarefa:",
        "nenhum": "Nenhum",
        "todos_dias": "Todos os dias",
        "a_cada_7": "A cada 7 dias",
        "a_cada_15": "A cada 15 dias",
        "a_cada_30": "A cada 30 dias",
        "tema_interface": "Tema da Interface:",
        "aplicar_tema": "Aplicar Tema",
        "idioma": "Idioma:",
        "desenvolvimento": "Desenvolvido por: David Assef",
        "mensagem_doacao": "Este programa é 100% gratuito, considere apoiar o desenvolvedor.",
        "link_doacao": "http://link.mercadopago.com.br/davidassef",
        "erro": "Erro",
        "data_invalida": "Data/hora inválida ou já passada",
        "sucesso": "Sucesso",
        "confirmar": "Confirmar",
        "aviso": "Aviso",
        "dias": "dias",
        "agendamento_salvo": "Agendamento salvo com sucesso!",
        "selecione_agendamento": "Selecione um agendamento!",
        "confirmar_exclusao": "Deseja realmente excluir este agendamento?",
        "desligar": "Desligar",
        "reiniciar": "Reiniciar",
        "modo_timer": "Temporizador",
        "modo_hora": "Hora definida",
        "tipo_agendamento": "Tipo de Agendamento:",
        "selecione_idioma": "Selecione seu idioma",
        "minimizar_bandeja": "Iniciar minimizado"
    },
    "en": {
        "programar": "Schedule Shutdown",
        "agendamentos": "Schedules",
        "opcoes": "Options",
        "acao": "Action:",
        "hora": "Hour:",
        "min": "Min:",
        "seg": "Sec:",
        "iniciar_windows": "Start with Windows",
        "iniciar": "Start",
        "novo_agendamento": "New Schedule",
        "editar": "Edit",
        "deletar": "Delete",
        "repetir_tarefa": "Repeat task:",
        "nenhum": "None",
        "todos_dias": "Daily",
        "a_cada_7": "Every 7 days",
        "a_cada_15": "Every 15 days",
        "a_cada_30": "Every 30 days",
        "tema_interface": "Interface Theme:",
        "aplicar_tema": "Apply Theme",
        "idioma": "Language:",
        "desenvolvimento": "Developed by: David Assef",
        "mensagem_doacao": "This program is 100% free, please support the developer.",
        "link_doacao": "http://link.mercadopago.com.br/davidassef",
        "erro": "Error",
        "data_invalida": "Invalid or past date/time",
        "sucesso": "Success",
        "confirmar": "Confirm",
        "aviso": "Warning",
        "dias": "days",
        "agendamento_salvo": "Schedule saved successfully!",
        "selecione_agendamento": "Please select a schedule!",
        "confirmar_exclusao": "Are you sure you want to delete this schedule?",
        "desligar": "Shutdown",
        "reiniciar": "Restart",
        "modo_timer": "Timer",
        "modo_hora": "Scheduled Time",
        "tipo_agendamento": "Schedule Type:",
        "selecione_idioma": "Select your language",
        "minimizar_bandeja": "Start Minimized"
    },
    "es": {
        "programar": "Programar Apagado",
        "agendamentos": "Horarios",
        "opcoes": "Opciones",
        "acao": "Acción:",
        "hora": "Hora:",
        "min": "Min:",
        "seg": "Seg:",
        "iniciar_windows": "Iniciar con Windows",
        "iniciar": "Iniciar",
        "novo_agendamento": "Nuevo Horario",
        "editar": "Editar",
        "deletar": "Eliminar",
        "repetir_tarefa": "Repetir tarea:",
        "nenhum": "Ninguno",
        "todos_dias": "Diariamente",
        "a_cada_7": "Cada 7 días",
        "a_cada_15": "Cada 15 días",
        "a_cada_30": "Cada 30 días",
        "tema_interface": "Tema de Interfaz:",
        "aplicar_tema": "Aplicar Tema",
        "idioma": "Idioma:",
        "desenvolvimento": "Desarrollado por: David Assef",
        "mensagem_doacao": "Este programa es 100% gratis, por favor apoya al desarrollador.",
        "link_doacao": "http://link.mercadopago.com.br/davidassef",
        "erro": "Error",
        "data_invalida": "Fecha/hora inválida o pasada",
        "sucesso": "Éxito",
        "confirmar": "Confirmar",
        "aviso": "Advertencia",
        "dias": "días",
        "agendamento_salvo": "¡Horario guardado correctamente!",
        "selecione_agendamento": "¡Seleccione un horario!",
        "confirmar_exclusao": "¿Está seguro de que desea eliminar este horario?",
        "desligar": "Apagar",
        "reiniciar": "Reiniciar",
        "modo_timer": "Temporizador",
        "modo_hora": "Hora definida",
        "tipo_agendamento": "Tipo de Horario:",
        "selecione_idioma": "Seleccione su idioma",
        "minimizar_bandeja": "Iniciar minimizado"
    }
}

def get_text(key):
    return texts.get(current_language, texts["en"]).get(key, key)

# ----------------- Funções Auxiliares -----------------
def carregar_agendamentos():
    global agendamentos
    try:
        with open(AGENDAMENTOS_FILE, 'r') as f:
            agendamentos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        agendamentos = []

def salvar_agendamentos():
    with open(AGENDAMENTOS_FILE, 'w') as f:
        json.dump(agendamentos, f)

def obter_data_hora_atual():
    try:
        response = requests.get("http://worldtimeapi.org/api/ip", timeout=5)
        if response.status_code == 200:
            return datetime.fromisoformat(response.json()["datetime"][:-6])
    except Exception:
        pass
    return datetime.now()

def validar_data_hora(data_str, hora_str):
    try:
        ag_dt = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, None
    return (ag_dt > obter_data_hora_atual()), ag_dt

def agendar_tarefa(acao, data, hora, repeat_interval=None):
    valido, ag_dt = validar_data_hora(data, hora)
    if not valido:
        QtWidgets.QMessageBox.warning(None, get_text("erro"), get_text("data_invalida"))
        return False
    comando = "shutdown /s /f /t 0" if acao == get_text("desligar") else "shutdown /r /f /t 0"
    agendamentos.append({
        "acao": acao,
        "data": data,
        "hora": hora,
        "comando": comando,
        "repeat": repeat_interval
    })
    salvar_agendamentos()
    return True

def agendar_tarefa_timer(acao, total_seconds):
    ag_dt = obter_data_hora_atual() + timedelta(seconds=total_seconds)
    comando = "shutdown /s /f /t 0" if acao == get_text("desligar") else "shutdown /r /f /t 0"
    agendamentos.append({
        "acao": acao,
        "data": ag_dt.strftime("%Y-%m-%d"),
        "hora": ag_dt.strftime("%H:%M:%S"),
        "comando": comando,
        "repeat": None
    })
    salvar_agendamentos()
    return True

def verificar_agendamentos():
    global agendamentos
    while True:
        agora = obter_data_hora_atual()
        novos_agendamentos = []
        for ag in agendamentos:
            try:
                ag_dt = datetime.strptime(f"{ag['data']} {ag['hora']}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if agora >= ag_dt:
                os.system(ag['comando'])
                if ag['repeat']:
                    while agora >= ag_dt:
                        ag_dt += timedelta(days=ag['repeat'])
                    ag['data'] = ag_dt.strftime("%Y-%m-%d")
                    ag['hora'] = ag_dt.strftime("%H:%M:%S")
                    novos_agendamentos.append(ag)
            else:
                novos_agendamentos.append(ag)
        agendamentos = novos_agendamentos
        salvar_agendamentos()
        time.sleep(5)

# ----------------- Função de Startup do Windows -----------------
def configurar_inicio_windows(ativar):
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    app_path = os.path.abspath(sys.argv[0])
    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            if ativar:
                winreg.SetValueEx(reg_key, APP_NAME, 0, winreg.REG_SZ, app_path)
            else:
                try:
                    winreg.DeleteValue(reg_key, APP_NAME)
                except FileNotFoundError:
                    pass
    except Exception as e:
        QtWidgets.QMessageBox.warning(None, get_text("erro"), str(e))

def verificar_inicio_windows():
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ) as reg_key:
            winreg.QueryValueEx(reg_key, APP_NAME)
            return True
    except FileNotFoundError:
        return False

# ----------------- Janela de Edição/Criação de Agendamento -----------------
class EditorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, index=None):
        super().__init__(parent)
        self.index = index
        self.setWindowTitle(get_text("novo_agendamento"))
        self.setFixedSize(450, 550)
        self.init_ui()
        if index is not None:
            self.load_data()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Tipo de Agendamento
        tipo_label = QtWidgets.QLabel(get_text("tipo_agendamento"))
        tipo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(tipo_label)
        self.tipo_group = QtWidgets.QButtonGroup(self)
        tipo_layout = QtWidgets.QHBoxLayout()
        self.radio_horario = QtWidgets.QRadioButton(get_text("modo_hora"))
        self.radio_timer = QtWidgets.QRadioButton(get_text("modo_timer"))
        self.radio_horario.setChecked(True)
        self.tipo_group.addButton(self.radio_horario)
        self.tipo_group.addButton(self.radio_timer)
        tipo_layout.addWidget(self.radio_horario)
        tipo_layout.addWidget(self.radio_timer)
        layout.addLayout(tipo_layout)
        self.tipo_group.buttonClicked.connect(self.toggle_tipo)

        # Área para agendamento por horário (com QDateTimeEdit e calendário)
        self.frame_horario = QtWidgets.QWidget()
        fh_layout = QtWidgets.QVBoxLayout(self.frame_horario)
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar.setMinimumDate(QtCore.QDate.currentDate())
        fh_layout.addWidget(self.calendar)
        self.date_time_edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_time_edit.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        fh_layout.addWidget(self.date_time_edit)
        layout.addWidget(self.frame_horario)

        # Área para agendamento por temporizador (dropdowns)
        self.frame_timer = QtWidgets.QWidget()
        ft_layout = QtWidgets.QVBoxLayout(self.frame_timer)
        ft_layout.setAlignment(QtCore.Qt.AlignCenter)
        ft_layout.addWidget(QtWidgets.QLabel(get_text("modo_timer")))
        timer_layout = QtWidgets.QHBoxLayout()
        self.cb_horas = QtWidgets.QComboBox()
        self.cb_horas.setFixedWidth(60)
        self.cb_horas.addItems([f"{i:02d}" for i in range(24)])
        self.cb_minutos = QtWidgets.QComboBox()
        self.cb_minutos.setFixedWidth(60)
        self.cb_minutos.addItems([f"{i:02d}" for i in range(60)])
        self.cb_segundos = QtWidgets.QComboBox()
        self.cb_segundos.setFixedWidth(60)
        self.cb_segundos.addItems([f"{i:02d}" for i in range(60)])
        timer_layout.addWidget(QtWidgets.QLabel("HH"))
        timer_layout.addWidget(self.cb_horas)
        timer_layout.addWidget(QtWidgets.QLabel("MM"))
        timer_layout.addWidget(self.cb_minutos)
        timer_layout.addWidget(QtWidgets.QLabel("SS"))
        timer_layout.addWidget(self.cb_segundos)
        ft_layout.addLayout(timer_layout)
        layout.addWidget(self.frame_timer)
        self.frame_timer.hide()

        # Repetir tarefa (apenas para agendamento por horário)
        rep_layout = QtWidgets.QHBoxLayout()
        rep_layout.setAlignment(QtCore.Qt.AlignCenter)
        rep_layout.addWidget(QtWidgets.QLabel(get_text("repetir_tarefa")))
        self.repeat_combo = QtWidgets.QComboBox()
        self.repeat_combo.addItems([get_text("nenhum"), get_text("todos_dias"),
                                     get_text("a_cada_7"), get_text("a_cada_15"), get_text("a_cada_30")])
        rep_layout.addWidget(self.repeat_combo)
        layout.addLayout(rep_layout)

        # Botão Salvar
        self.save_btn = QtWidgets.QPushButton(get_text("iniciar"))
        self.save_btn.setFixedWidth(120)
        self.save_btn.clicked.connect(self.salvar)
        layout.addWidget(self.save_btn, alignment=QtCore.Qt.AlignCenter)

    def toggle_tipo(self):
        if self.radio_horario.isChecked():
            self.frame_timer.hide()
            self.frame_horario.show()
        else:
            self.frame_horario.hide()
            self.frame_timer.show()

    def load_data(self):
        ag = agendamentos[self.index]
        self.radio_horario.setChecked(True)
        dt = QtCore.QDateTime.fromString(ag["data"] + " " + ag["hora"], "yyyy-MM-dd HH:mm:ss")
        self.calendar.setSelectedDate(QtCore.QDate.fromString(ag["data"], "yyyy-MM-dd"))
        self.date_time_edit.setDateTime(dt)
        self.repeat_combo.setCurrentText(str(ag["repeat"]) if ag["repeat"] else get_text("nenhum"))

    def salvar(self):
        if self.radio_horario.isChecked():
            dt = self.date_time_edit.dateTime()
            data = dt.toString("yyyy-MM-dd")
            hora = dt.toString("HH:mm:ss")
            interval_map = {
                get_text("nenhum"): None,
                get_text("todos_dias"): 1,
                get_text("a_cada_7"): 7,
                get_text("a_cada_15"): 15,
                get_text("a_cada_30"): 30
            }
            repeat = interval_map.get(self.repeat_combo.currentText())
            if agendar_tarefa(self.parent().acao_combo.currentText(), data, hora, repeat):
                QtWidgets.QMessageBox.information(self, get_text("sucesso"), get_text("agendamento_salvo"))
                self.parent().atualizar_lista()
                self.accept()
        else:
            horas = int(self.cb_horas.currentText())
            minutos = int(self.cb_minutos.currentText())
            segundos = int(self.cb_segundos.currentText())
            total_segundos = horas * 3600 + minutos * 60 + segundos
            if agendar_tarefa_timer(self.parent().acao_combo.currentText(), total_segundos):
                QtWidgets.QMessageBox.information(self, get_text("sucesso"), get_text("agendamento_salvo"))
                self.parent().atualizar_lista()
                self.accept()

# ----------------- Interface Principal -----------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        global current_language
        # Substituindo getdefaultlocale() por getlocale() para evitar DeprecationWarning
        lang_tuple = locale.getlocale()
        sys_lang = lang_tuple[0][:2] if lang_tuple[0] else "en"
        current_language = sys_lang if sys_lang in texts.keys() else "en"
        self.setWindowTitle("Shutdown Scheduler")
        self.setFixedSize(600, 500)
        self.init_ui()
        carregar_agendamentos()
        self.start_verificador()

    def init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { min-width: 100px; padding: 4px; }")
        main_layout.addWidget(self.tabs)

        # Aba Programar (com opção de Timer ou Hora definida)
        self.tab_programar = QtWidgets.QWidget()
        self.init_tab_programar()
        self.tabs.addTab(self.tab_programar, get_text("programar"))

        # Aba Agendamentos
        self.tab_agendamentos = QtWidgets.QWidget()
        self.init_tab_agendamentos()
        self.tabs.addTab(self.tab_agendamentos, get_text("agendamentos"))

        # Aba Opções (conteúdo centralizado)
        self.tab_opcoes = QtWidgets.QWidget()
        self.init_tab_opcoes()
        self.tabs.addTab(self.tab_opcoes, get_text("opcoes"))

        # Rodapé com créditos e link clicável para doação
        credits = QtWidgets.QLabel(get_text("desenvolvimento") + "\n" + get_text("mensagem_doacao"))
        credits.setAlignment(QtCore.Qt.AlignCenter)
        footer = QtWidgets.QLabel("<a href=\"" + get_text("link_doacao") + "\">" + get_text("link_doacao") + "</a>")
        footer.setOpenExternalLinks(True)
        footer.setAlignment(QtCore.Qt.AlignCenter)
        footer_layout = QtWidgets.QVBoxLayout()
        footer_layout.addWidget(credits)
        footer_layout.addWidget(footer)
        main_layout.addLayout(footer_layout)

    def init_tab_programar(self):
        layout = QtWidgets.QVBoxLayout(self.tab_programar)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Ação (Shutdown ou Restart)
        acao_layout = QtWidgets.QHBoxLayout()
        acao_label = QtWidgets.QLabel(get_text("acao"))
        self.acao_combo = QtWidgets.QComboBox()
        self.acao_combo.addItems([get_text("desligar"), get_text("reiniciar")])
        acao_layout.addWidget(acao_label)
        acao_layout.addWidget(self.acao_combo)
        acao_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(acao_layout)
        
        # Escolha do modo de agendamento: Timer ou Hora definida
        modo_layout = QtWidgets.QHBoxLayout()
        self.radio_timer_main = QtWidgets.QRadioButton(get_text("modo_timer"))
        self.radio_hora_main = QtWidgets.QRadioButton(get_text("modo_hora"))
        self.radio_timer_main.setChecked(True)
        self.modo_group = QtWidgets.QButtonGroup(self)
        self.modo_group.addButton(self.radio_timer_main)
        self.modo_group.addButton(self.radio_hora_main)
        modo_layout.addWidget(self.radio_timer_main)
        modo_layout.addWidget(self.radio_hora_main)
        modo_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(modo_layout)
        self.modo_group.buttonClicked.connect(self.toggle_programar)
        
        # Área para temporizador (dropdowns)
        self.area_timer = QtWidgets.QWidget()
        timer_layout = QtWidgets.QHBoxLayout(self.area_timer)
        self.cb_horas_main = QtWidgets.QComboBox()
        self.cb_horas_main.setFixedWidth(60)
        self.cb_horas_main.addItems([f"{i:02d}" for i in range(24)])
        self.cb_minutos_main = QtWidgets.QComboBox()
        self.cb_minutos_main.setFixedWidth(60)
        self.cb_minutos_main.addItems([f"{i:02d}" for i in range(60)])
        self.cb_segundos_main = QtWidgets.QComboBox()
        self.cb_segundos_main.setFixedWidth(60)
        self.cb_segundos_main.addItems([f"{i:02d}" for i in range(60)])
        timer_layout.addWidget(QtWidgets.QLabel("HH"))
        timer_layout.addWidget(self.cb_horas_main)
        timer_layout.addWidget(QtWidgets.QLabel("MM"))
        timer_layout.addWidget(self.cb_minutos_main)
        timer_layout.addWidget(QtWidgets.QLabel("SS"))
        timer_layout.addWidget(self.cb_segundos_main)
        layout.addWidget(self.area_timer)
        
        # Área para hora definida (QDateTimeEdit e calendário)
        self.area_hora = QtWidgets.QWidget()
        hora_layout = QtWidgets.QVBoxLayout(self.area_hora)
        self.calendar_prog = QtWidgets.QCalendarWidget()
        self.calendar_prog.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar_prog.setMinimumDate(QtCore.QDate.currentDate())
        hora_layout.addWidget(self.calendar_prog)
        self.date_time_edit_main = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_time_edit_main.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_time_edit_main.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        hora_layout.addWidget(self.date_time_edit_main)
        layout.addWidget(self.area_hora)
        self.area_hora.hide()

        # Botão Iniciar
        btn_iniciar = QtWidgets.QPushButton(get_text("iniciar"))
        btn_iniciar.setFixedWidth(120)
        btn_iniciar.clicked.connect(self.iniciar_agendamento)
        layout.addWidget(btn_iniciar, alignment=QtCore.Qt.AlignCenter)

    def toggle_programar(self):
        if self.radio_timer_main.isChecked():
            self.area_hora.hide()
            self.area_timer.show()
        else:
            self.area_timer.hide()
            self.area_hora.show()

    def iniciar_agendamento(self):
        if self.radio_timer_main.isChecked():
            horas = int(self.cb_horas_main.currentText())
            minutos = int(self.cb_minutos_main.currentText())
            segundos = int(self.cb_segundos_main.currentText())
            total_segundos = horas * 3600 + minutos * 60 + segundos
            if total_segundos == 0:
                QtWidgets.QMessageBox.warning(self, get_text("erro"), get_text("data_invalida"))
                return
            if agendar_tarefa_timer(self.acao_combo.currentText(), total_segundos):
                QtWidgets.QMessageBox.information(self, get_text("sucesso"), get_text("agendamento_salvo"))
                self.atualizar_lista()
        else:
            dt = self.date_time_edit_main.dateTime()
            data = dt.toString("yyyy-MM-dd")
            hora = dt.toString("HH:mm:ss")
            if agendar_tarefa(self.acao_combo.currentText(), data, hora):
                QtWidgets.QMessageBox.information(self, get_text("sucesso"), get_text("agendamento_salvo"))
                self.atualizar_lista()

    def init_tab_agendamentos(self):
        layout = QtWidgets.QVBoxLayout(self.tab_agendamentos)
        self.lista_ag = QtWidgets.QListWidget()
        layout.addWidget(self.lista_ag)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_novo = QtWidgets.QPushButton(get_text("novo_agendamento"))
        btn_novo.clicked.connect(self.abrir_editor)
        btn_editar = QtWidgets.QPushButton(get_text("editar"))
        btn_editar.clicked.connect(self.editar_agendamento)
        btn_deletar = QtWidgets.QPushButton(get_text("deletar"))
        btn_deletar.clicked.connect(self.deletar_agendamento)
        for btn in (btn_novo, btn_editar, btn_deletar):
            btn.setFixedWidth(120)
        btn_layout.addWidget(btn_novo)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_deletar)
        layout.addLayout(btn_layout)
        self.atualizar_lista()

    def init_tab_opcoes(self):
        layout = QtWidgets.QFormLayout(self.tab_opcoes)
        layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.tema_combo = QtWidgets.QComboBox()
        self.tema_combo.setFixedWidth(150)
        self.tema_combo.addItems(["Automático", "Clara", "Escura"])
        btn_aplicar = QtWidgets.QPushButton(get_text("aplicar_tema"))
        btn_aplicar.setFixedWidth(120)
        btn_aplicar.clicked.connect(self.aplicar_tema)
        layout.addRow(get_text("tema_interface"), self.tema_combo)
        layout.addRow("", btn_aplicar)
        
        self.idioma_combo = QtWidgets.QComboBox()
        self.idioma_combo.setFixedWidth(150)
        self.idioma_combo.addItem(get_text("selecione_idioma"))
        self.idioma_combo.addItems(["Português", "English", "Español"])
        self.idioma_combo.currentIndexChanged.connect(self.mudar_idioma)
        layout.addRow(get_text("idioma"), self.idioma_combo)
        
        self.check_inicio_windows = QtWidgets.QCheckBox(get_text("iniciar_windows"))
        layout.addRow(self.check_inicio_windows)

    def aplicar_tema(self):
        tema = self.tema_combo.currentText()
        if tema == "Escura":
            estilo = ("QWidget { background-color: #2d2d2d; color: white; }"
                      "QTabWidget::pane { border: none; }"
                      "QTabBar::tab { background: #3d3d3d; color: white; padding: 8px; }")
        elif tema == "Clara":
            estilo = ("QWidget { background-color: white; color: black; }"
                      "QTabWidget::pane { border: none; }"
                      "QTabBar::tab { background: #f0f0f0; color: black; padding: 8px; }")
        else:  # Automático
            palette = QtWidgets.QApplication.palette()
            color = palette.color(QtGui.QPalette.Window)
            brightness = (color.red()*299 + color.green()*587 + color.blue()*114) / 1000
            if brightness < 128:
                estilo = ("QWidget { background-color: #2d2d2d; color: white; }"
                          "QTabWidget::pane { border: none; }"
                          "QTabBar::tab { background: #3d3d3d; color: white; padding: 8px; }")
            else:
                estilo = ("QWidget { background-color: white; color: black; }"
                          "QTabWidget::pane { border: none; }"
                          "QTabBar::tab { background: #f0f0f0; color: black; padding: 8px; }")
        self.setStyleSheet(estilo)
        cal_style = ""
        if tema == "Escura" or (tema == "Automático" and brightness < 128):
            cal_style = "QCalendarWidget { background-color: #3d3d3d; color: white; }"
        elif tema == "Clara" or (tema == "Automático" and brightness >= 128):
            cal_style = "QCalendarWidget { background-color: white; color: black; }"
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, EditorDialog):
                widget.calendar.setStyleSheet(cal_style)

    def mudar_idioma(self):
        if self.idioma_combo.currentText() == get_text("selecione_idioma"):
            return
        lang_map = {"Português": "pt", "English": "en", "Español": "es"}
        global current_language
        current_language = lang_map[self.idioma_combo.currentText()]
        self.init_ui()

    def atualizar_lista(self):
        self.lista_ag.clear()
        for idx, ag in enumerate(agendamentos):
            rep_text = f" ({ag['repeat']} {get_text('dias')})" if ag['repeat'] else ""
            item = f"{idx+1}. {ag['acao']} - {ag['data']} {ag['hora']}{rep_text}"
            self.lista_ag.addItem(item)

    def abrir_editor(self):
        dlg = EditorDialog(self)
        dlg.exec_()

    def editar_agendamento(self):
        item = self.lista_ag.currentRow()
        if item < 0:
            QtWidgets.QMessageBox.warning(self, get_text("aviso"), get_text("selecione_agendamento"))
            return
        dlg = EditorDialog(self, index=item)
        dlg.exec_()

    def deletar_agendamento(self):
        item = self.lista_ag.currentRow()
        if item < 0:
            QtWidgets.QMessageBox.warning(self, get_text("aviso"), get_text("selecione_agendamento"))
            return
        reply = QtWidgets.QMessageBox.question(self, get_text("confirmar"), get_text("confirmar_exclusao"),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            del agendamentos[item]
            salvar_agendamentos()
            self.atualizar_lista()

    def start_verificador(self):
        thread = threading.Thread(target=verificar_agendamentos, daemon=True)
        thread.start()

    def alterar_inicio_windows(self, ativar):
        configurar_inicio_windows(ativar)

# ----------------- Execução -----------------
def main():
    carregar_agendamentos()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.check_inicio_windows.setChecked(verificar_inicio_windows())
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
