# flake8: noqa: E501
import os
import sys
from datetime import datetime

# Fix PyQt6 imports to help Pylint find the modules
from PyQt6 import QtCore, QtGui, QtWidgets

# Importa os novos módulos
from immediate_actions import ImmediateActionsManager
from scheduled_actions import ScheduledActionsManager
from notifications import NotificationManager
from schedule_dialog import ScheduleDialog
from settings import Settings
from system_actions import SystemActions

# pylint: disable=c-extension-no-member
class ShutdownScheduler(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agendador de Desligamento")
        # Tamanho mínimo calculado para acomodar todos os elementos sem scrollbar
        self.setMinimumSize(550, 450)
        self.setMaximumSize(800, 650)

        # Flag para controlar o fechamento do aplicativo
        self.is_quitting = False

        # Inicializa gerenciadores
        self.settings = Settings()
        self.notifications = NotificationManager(self)

        # Novos gerenciadores separados para ações imediatas e agendadas
        self.immediate_actions = ImmediateActionsManager()
        self.scheduled_actions = ScheduledActionsManager()

        # Configuração do tema
        self.is_dark_theme = self.settings.get("dark_theme", False)

        # Inicializar estilos
        self.init_styles()

        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setSpacing(15)  # Aumenta o espaçamento entre os elementos
        layout.setContentsMargins(20, 20, 20, 20)  # Adiciona margens

        # Timer no topo
        self.timer_label = QtWidgets.QLabel("Próxima ação: --:--:--")
        self.timer_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        # Tabs
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)

        # Criar as abas
        self.home_tab = QtWidgets.QWidget()
        self.schedule_tab = QtWidgets.QWidget()
        self.settings_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.home_tab, "Início")
        self.tab_widget.addTab(self.schedule_tab, "Agendamentos")
        self.tab_widget.addTab(self.settings_tab, "Configurações")

        # Configurar as abas
        self.setup_home_tab()
        self.setup_schedule_tab()
        self.setup_settings_tab()

        # Timer para atualização dos agendamentos
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_schedules_display)
        self.update_timer.start(3000)  # Atualiza a cada 3 segundos

        # Configura o callback para atualizar o timer de ações imediatas
        self.immediate_actions.set_update_callback(self.update_timer_display)

        # Timer para limpeza periódica
        self.cleanup_timer = QtCore.QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_old_notification_settings)
        self.cleanup_timer.start(60000)  # Executa a cada minuto

        # Tray icon
        self.setup_tray()

        # Conectar sinais
        self.confirm_button.clicked.connect(self.execute_immediate_action)
        self.cancel_button.clicked.connect(self.cancel_current_action)

        # Aplicar tema após criar todos os componentes
        self.setup_theme()

        # Limpa as configurações de notificação antigas
        self.cleanup_old_notification_settings()

    def init_styles(self):
        """Inicializa os estilos base que serão usados em toda a aplicação"""
        # Estilo dos botões principais - SIMPLIFICADO
        self.main_button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        # Estilo do ComboBox - SIMPLIFICADO
        self.combo_style = """
            QComboBox {
                border: 1px solid %s;
                padding: 4px;
            }
        """

        # Estilo dos botões da tabela - SIMPLIFICADO
        self.table_button_style = """
            QPushButton {
                background-color: %s;
                color: %s;
                padding: 4px;
                font-size: 11px;
            }
        """

        # Aplicar estilos base de acordo com o tema
        if self.is_dark_theme:
            self.combo_style = self.combo_style % ("#3d3d3d")
            self.table_button_style = self.table_button_style % ("#3b3b3b", "#ffffff")
        else:
            self.combo_style = self.combo_style % ("#e0e0e0")
            self.table_button_style = self.table_button_style % ("#ffffff", "#000000")

    def setup_theme(self):
        # Estilo base simplificado
        base_style = """
            QMainWindow, QWidget {
                background-color: %s;
                color: %s;
            }
            QTabWidget::pane {
                border: none;
                top: -1px; /* move o painel para cima para conectá-lo às abas */
                background: %s;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: %s;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: %s;
                font-weight: normal;
                min-width: 80px;
                transition: all 0.3s;
            }
            QTabBar::tab:selected {
                background-color: %s;
                font-weight: bold;
                border-bottom: 3px solid #4CAF50;
            }
            QTabBar::tab:hover:!selected {
                background-color: %s;
            }
            QLabel {
                color: %s;
            }
        """

        if self.is_dark_theme:
            self.setStyleSheet(
                base_style % (
                    "#222222",  # MainWindow, QWidget background - mais escuro
                    "#ffffff",  # MainWindow, QWidget text
                    "#2d2d2d",  # TabWidget pane
                    "#3d3d3d",  # TabBar::tab
                    "#cccccc",  # Tab text color
                    "#1e1e1e",  # TabBar::tab:selected - mais contrastante
                    "#444444",  # TabBar::tab:hover - destacado
                    "#ffffff",  # Label text
                )
            )
        else:
            self.setStyleSheet(
                base_style % (
                    "#f8f8f8",  # MainWindow, QWidget background - mais suave
                    "#333333",  # MainWindow, QWidget text - menos agressivo que preto puro
                    "#ffffff",  # TabWidget pane
                    "#e8e8e8",  # TabBar::tab - cinza claro
                    "#555555",  # Tab text color
                    "#ffffff",  # TabBar::tab:selected
                    "#f0f0f0",  # TabBar::tab:hover
                    "#333333",  # Label text
                )
            )

        # Atualiza os estilos específicos dos grupos
        self.update_group_styles()

        # Atualiza a tabela
        self.update_table_style()

        # Atualiza os botões
        self.update_buttons_style()  # Novo método para estilizar botões

        # Atualiza o estilo do timer_label ao mudar o tema
        self.timer_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: %s;
            background-color: %s;
        """ % (
            "#4CAF50" if self.is_dark_theme else "#388E3C",  # Cor do texto
            "#2d2d2d" if self.is_dark_theme else "#f0f0f0"  # Cor de fundo
        ))

        # Atualiza o estilo do timer_container ao mudar o tema
        self.timer_container.setStyleSheet("""
            QWidget {
                background-color: %s;
                border-radius: 6px;
                border: 1px solid %s;
            }
        """ % (
            "#2d2d2d" if self.is_dark_theme else "#f0f0f0",  # Cor de fundo
            "#444444" if self.is_dark_theme else "#dddddd"  # Cor da borda
        ))

        # Garante que o ícone da bandeja seja completamente removido antes de recriar
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
            self.tray_icon = None

    def setup_home_tab(self):
        layout = QtWidgets.QVBoxLayout(self.home_tab)
        # Reduzindo espaçamento para economizar espaço vertical
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # Timer no topo com estilo aprimorado
        # Define timer_container como um atributo da classe para acesso global
        self.timer_container = QtWidgets.QWidget()
        self.timer_container.setStyleSheet("""
            QWidget {
                background-color: %s;
                border-radius: 6px;
                border: 1px solid %s;
            }
        """ % (
            "#2d2d2d" if self.is_dark_theme else "#f0f0f0",
            "#444444" if self.is_dark_theme else "#dddddd"
        ))
        timer_layout = QtWidgets.QVBoxLayout(self.timer_container)
        timer_layout.setContentsMargins(12, 12, 12, 12)

        self.timer_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: %s;
        """ % ("#4CAF50" if self.is_dark_theme else "#388E3C"))

        # Adiciona efeito de sombra ao texto
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.timer_label)
        shadow.setBlurRadius(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 50))
        shadow.setOffset(1, 1)
        self.timer_label.setGraphicsEffect(shadow)

        timer_layout.addWidget(self.timer_label)
        layout.addWidget(self.timer_container)

        # Área de ações - diretamente no layout principal
        instruction_label = QtWidgets.QLabel("Selecione uma ação e defina o tempo:")
        instruction_label.setStyleSheet("font-size: 14px; margin-top: 8px;")
        layout.addWidget(instruction_label)

        # Layout para ação e tempo
        action_time_layout = QtWidgets.QHBoxLayout()

        # Dropdown de ação
        self.action_combo = QtWidgets.QComboBox()
        self.action_combo.addItems(["Desligar", "Reiniciar", "Hibernar", "Suspender"])
        self.action_combo.setStyleSheet(self.combo_style)
        action_time_layout.addWidget(self.action_combo)

        # Dropdowns para tempo (horas, minutos, segundos)
        self.hours_combo = QtWidgets.QComboBox()
        self.hours_combo.addItems([f"{i}h" for i in range(24)])
        self.hours_combo.setStyleSheet(self.combo_style)
        action_time_layout.addWidget(self.hours_combo)

        self.minutes_combo = QtWidgets.QComboBox()
        self.minutes_combo.addItems([f"{i}min" for i in range(60)])
        self.minutes_combo.setStyleSheet(self.combo_style)
        action_time_layout.addWidget(self.minutes_combo)

        self.seconds_combo = QtWidgets.QComboBox()
        self.seconds_combo.addItems([f"{i}s" for i in range(60)])
        self.seconds_combo.setStyleSheet(self.combo_style)
        action_time_layout.addWidget(self.seconds_combo)

        layout.addLayout(action_time_layout)

        # Botão de confirmar
        self.confirm_button = QtWidgets.QPushButton("Agendar Ação")
        self.confirm_button.setStyleSheet(self.main_button_style)
        layout.addWidget(self.confirm_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Botão de cancelar
        self.cancel_button = QtWidgets.QPushButton("Cancelar Ação em Andamento")
        self.cancel_button.setStyleSheet("background-color: #f44336; color: white;")
        self.cancel_button.setEnabled(False)
        layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Adiciona um espaço para os créditos na parte inferior da interface
        credits_label = QtWidgets.QLabel("Créditos: Desenvolvido por David Assef")
        credits_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        credits_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(credits_label, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

    def setup_schedule_tab(self):
        layout = QtWidgets.QVBoxLayout(self.schedule_tab)
        # Reduzindo espaçamento para economizar espaço vertical
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tabela de agendamentos
        self.schedule_table = QtWidgets.QTableWidget()
        self.schedule_table.setColumnCount(4)  # Reduzido para 4 colunas (sem ID)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Ação", "Data/Hora", "Status", "Ações"]  # Removido o cabeçalho "ID"
        )
        # Definimos uma altura fixa para a tabela para garantir que ela não use espaço demais
        self.schedule_table.setFixedHeight(250)  # Aumentado para 250px

        # Ajusta o estilo da tabela
        table_style = """
            QTableWidget {
                background-color: %s;
                color: %s;
                border: 1px solid %s;
                border-radius: 4px;
                gridline-color: %s;
            }
            QHeaderView::section {
                background-color: %s;
                color: %s;
                padding: 6px;
                border: none;
                border-right: 1px solid %s;
                border-bottom: 1px solid %s;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid %s;
            }
            QTableWidget::item:selected {
                background-color: %s;
                color: %s;
            }
        """
        if self.is_dark_theme:
            self.schedule_table.setStyleSheet(
                table_style % (
                    "#2d2d2d",  # background
                    "#ffffff",  # text color
                    "#3d3d3d",  # border
                    "#3d3d3d",  # gridline
                    "#1e1e1e",  # header background
                    "#ffffff",  # header text
                    "#3d3d3d",  # header border right
                    "#3d3d3d",  # header border bottom
                    "#3d3d3d",  # item border
                    "#3d3d3d",  # selection background
                    "#ffffff",  # selection text
                )
            )
        else:
            self.schedule_table.setStyleSheet(
                table_style % (
                    "#ffffff",  # background
                    "#000000",  # text color
                    "#e0e0e0",  # border
                    "#e0e0e0",  # gridline
                    "#f5f5f5",  # header background
                    "#000000",  # header text
                    "#e0e0e0",  # header border right
                    "#e0e0e0",  # header border bottom
                    "#e0e0e0",  # item border
                    "#f0f0f0",  # selection background
                    "#000000",  # selection text
                )
            )

        self.schedule_table.verticalHeader().setVisible(False)

        # Ajusta as dimensões
        self.schedule_table.setColumnWidth(0, 120)  # Ação (aumentado)
        self.schedule_table.setColumnWidth(1, 170)  # Data/Hora (aumentado)
        self.schedule_table.setColumnWidth(2, 80)   # Status
        self.schedule_table.setColumnWidth(3, 180)  # Ações - largura mínima ajustada

        # Configura a coluna de Ações para se expandir/contrair com o redimensionamento da janela
        header = self.schedule_table.horizontalHeader()
        for i in range(3):  # Para as 3 primeiras colunas
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.schedule_table)

        # Botão para novo agendamento
        self.new_schedule_button = QtWidgets.QPushButton("Novo Agendamento")
        self.new_schedule_button.clicked.connect(self.show_new_schedule_dialog)
        layout.addWidget(self.new_schedule_button)

        # Atualizar tabela
        self.update_schedule_table()

    def setup_settings_tab(self):
        layout = QtWidgets.QVBoxLayout(self.settings_tab)
        # Reduzindo espaçamento para economizar espaço vertical
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Grupo de aparência
        appearance_group = QtWidgets.QGroupBox("Aparência")
        appearance_layout = QtWidgets.QFormLayout()
        appearance_layout.setSpacing(10)  # Espaçamento entre elementos
        appearance_layout.setContentsMargins(15, 15, 15, 15)  # Margens internas

        # Tema escuro
        dark_theme_checkbox = QtWidgets.QCheckBox("Tema Escuro")
        dark_theme_checkbox.setChecked(self.is_dark_theme)
        dark_theme_checkbox.stateChanged.connect(self.toggle_theme)
        appearance_layout.addRow("Tema:", dark_theme_checkbox)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # Grupo de notificações
        notifications_group = QtWidgets.QGroupBox("Notificações")
        notifications_layout = QtWidgets.QFormLayout()
        notifications_layout.setSpacing(10)
        notifications_layout.setContentsMargins(15, 15, 15, 15)

        # Ativar alertas
        enable_alerts = QtWidgets.QCheckBox("Ativar alertas de confirmação")
        enable_alerts.setChecked(self.settings.get("enable_alerts", True))
        enable_alerts.stateChanged.connect(
            lambda state: self.settings.set("enable_alerts", bool(state))
        )
        notifications_layout.addRow("Alertas:", enable_alerts)

        # Tempo de aviso
        warning_time = QtWidgets.QSpinBox()
        warning_time.setRange(60, 3600)
        warning_time.setValue(self.settings.get("warning_time", 300))
        warning_time.valueChanged.connect(
            lambda value: self.settings.set("warning_time", value)
        )
        warning_time.setSuffix(" segundos")
        warning_time.setMinimumWidth(120)
        notifications_layout.addRow("Tempo de aviso:", warning_time)

        notifications_group.setLayout(notifications_layout)
        layout.addWidget(notifications_group)

        # Grupo de comportamento
        behavior_group = QtWidgets.QGroupBox("Comportamento")
        behavior_layout = QtWidgets.QFormLayout()
        behavior_layout.setSpacing(10)  # Espaçamento entre elementos
        behavior_layout.setContentsMargins(15, 15, 15, 15)  # Margens internas

        # Iniciar com Windows
        start_with_windows = QtWidgets.QCheckBox("Iniciar com Windows")
        start_with_windows.setChecked(self.settings.get("start_with_windows", False))
        start_with_windows.stateChanged.connect(
            lambda state: self.settings.set("start_with_windows", bool(state))
        )
        behavior_layout.addRow("Inicialização:", start_with_windows)

        # Minimizar para bandeja
        minimize_to_tray = QtWidgets.QCheckBox("Minimizar para bandeja")
        minimize_to_tray.setChecked(self.settings.get("minimize_to_tray", True))
        minimize_to_tray.stateChanged.connect(
            lambda state: self.settings.set("minimize_to_tray", bool(state))
        )
        behavior_layout.addRow("Ao fechar:", minimize_to_tray)

        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)

        # Fazendo o layout ajustar os elementos para não precisar de scrollbar
        layout.addStretch(1)  # Adiciona um espaço flexível no final para empurrar os elementos para cima

    def setup_tray(self):
        """Configura o ícone da bandeja do sistema"""
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)

        # Carrega o ícone
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
        else:
            # Cria um ícone padrão se o arquivo não existir
            pixmap = QtGui.QPixmap(32, 32)
            pixmap.fill(QtGui.QColor("#4CAF50"))
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
            painter.drawEllipse(8, 8, 16, 16)
            painter.drawLine(16, 8, 16, 16)
            painter.drawLine(16, 16, 24, 16)
            painter.end()
            icon = QtGui.QIcon(pixmap)

        # Define o ícone antes de mostrar o menu
        self.tray_icon.setIcon(icon)
        self.setWindowIcon(icon)

        # Menu de contexto
        tray_menu = QtWidgets.QMenu()

        # Ação para mostrar/esconder
        toggle_action = QtGui.QAction("Mostrar/Esconder", self)
        toggle_action.triggered.connect(self.toggle_window)
        tray_menu.addAction(toggle_action)

        # Separador
        tray_menu.addSeparator()

        # Ação para sair
        quit_action = QtGui.QAction("Sair", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        # Define o menu e mostra o ícone
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def update_timer_display(self):
        """Atualiza a exibição do timer para ações imediatas"""
        # Verifica ações imediatas
        action = self.immediate_actions.get_current_action()
        if action:
            self.timer_label.setText(f"Próxima ação ({action['action']}): {action['time_remaining']}")
            self.cancel_button.setEnabled(True)
            return

        # Se não há ações imediatas, verifica agendamentos regulares
        schedule = self.scheduled_actions.get_next_schedule()
        if schedule:
            time_remaining = SystemActions.format_time_remaining(schedule['execution_time'])
            self.timer_label.setText(f"Próxima ação ({schedule['action']}): {time_remaining}")
            self.cancel_button.setEnabled(True)

            # Verificar se os alertas estão habilitados e se é hora de mostrar o aviso
            if self.settings.get("enable_alerts", True):
                warning_time = self.settings.get("warning_time", 300)
                if (schedule['execution_time'] - datetime.now()).total_seconds() <= warning_time:
                    if self.notifications.show_warning_dialog(schedule["action"], schedule["execution_time"]):
                        self.scheduled_actions.cancel_schedule(schedule["id"])
                        self.notifications.show_notification(
                            "Ação Cancelada",
                            f"A ação de {schedule['action'].lower()} foi cancelada.",
                        )
                        self.cancel_button.setEnabled(False)
        else:
            self.timer_label.setText("Próxima ação: --:--:--")
            self.cancel_button.setEnabled(False)

    def update_schedules_display(self):
        """Atualiza as informações de agendamentos regulares"""
        # Atualiza a tabela de agendamentos
        self.update_schedule_table()

        # Verifica agendamentos próximos para notificações
        self.check_upcoming_scheduled_actions()

    def execute_immediate_action(self):
        """Executa uma ação imediata baseada nas seleções da interface"""
        # Lê os valores da interface
        action = self.action_combo.currentText()
        hours = int(self.hours_combo.currentText().split("h")[0])
        minutes = int(self.minutes_combo.currentText().split("min")[0])
        seconds = int(self.seconds_combo.currentText().split("s")[0])

        # Verifica se o tempo é válido
        if hours == 0 and minutes == 0 and seconds == 0:
            self.notifications.show_error_dialog(
                "Erro", "Por favor, defina um tempo maior que zero."
            )
            return

        # Verifica se os alertas estão habilitados
        if not self.settings.get("enable_alerts", True) or self.notifications.show_confirmation_dialog(
            "Confirmar Ação",
            f"Tem certeza que deseja {action.lower()} o computador em {hours}h, {minutes}min e {seconds}s?",
        ):
            try:
                # Agenda a ação usando o gerenciador de ações imediatas
                if self.immediate_actions.schedule_action(action, hours, minutes, seconds):
                    # Limpa os campos
                    self.hours_combo.setCurrentIndex(0)
                    self.minutes_combo.setCurrentIndex(0)
                    self.seconds_combo.setCurrentIndex(0)

                    # Envia uma notificação
                    self.notifications.show_notification(
                        "Ação Temporária Agendada",
                        f"A ação de {action.lower()} foi agendada com sucesso."
                    )
                else:
                    self.notifications.show_error_dialog(
                        "Erro",
                        "Não foi possível agendar a ação. Verifique se não há outra ação em andamento."
                    )
            except Exception as e:
                self.notifications.show_error_dialog(
                    "Erro", f"Ocorreu um erro ao agendar a ação: {str(e)}"
                )

    def cancel_current_action(self):
        """Cancela a ação atual em andamento"""
        # Primeiro tenta cancelar ações imediatas
        if self.immediate_actions.cancel_action():
            self.notifications.show_notification(
                "Ação Cancelada",
                "A ação temporária foi cancelada com sucesso."
            )
            self.update_timer_display()
            return

        # Se não havia ação imediata, verifica agendamentos regulares
        schedule = self.scheduled_actions.get_next_schedule()
        if schedule:
            if self.scheduled_actions.cancel_schedule(schedule['id']):
                self.notifications.show_notification(
                    "Agendamento Cancelado",
                    f"O agendamento de {schedule['action'].lower()} foi cancelado com sucesso."
                )
                self.update_schedule_table()
                self.update_timer_display()
                return

        # Se nenhum dos dois funcionou, tenta cancelar qualquer ação externa
        if SystemActions.cancel_shutdown():
            self.notifications.show_notification(
                "Ação Externa Cancelada",
                "Uma ação de desligamento agendada externamente foi cancelada com sucesso."
            )
        else:
            self.notifications.show_error_dialog(
                "Nenhuma Ação",
                "Não foi encontrada nenhuma ação para cancelar."
            )

    def show_new_schedule_dialog(self):
        """Mostra o diálogo para criar um novo agendamento persistente"""
        dialog = ScheduleDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            schedule_data = dialog.get_schedule_data()

            # Adiciona o agendamento usando o gerenciador de agendamentos
            if self.scheduled_actions.add_schedule(schedule_data["action"], schedule_data["execution_time"]):
                self.update_schedule_table()
                self.notifications.show_notification(
                    "Agendamento Criado",
                    f"Um novo agendamento de {schedule_data['action'].lower()} foi criado para {schedule_data['execution_time'].strftime('%d/%m/%Y %H:%M')}."
                )
            else:
                self.notifications.show_error_dialog(
                    "Erro", "Não foi possível criar o agendamento."
                )

    def update_schedule_table(self):
        """Atualiza a tabela de agendamentos"""
        self.schedule_table.setRowCount(0)  # Limpa a tabela
        schedules = self.scheduled_actions.get_active_schedules()

        for schedule in schedules:
            row = self.schedule_table.rowCount()
            self.schedule_table.insertRow(row)

            # Ajusta a altura da linha
            self.schedule_table.setRowHeight(row, 75)

            # Ação
            action_item = QtWidgets.QTableWidgetItem(schedule["action"])
            action_item.setFlags(action_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            action_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.schedule_table.setItem(row, 0, action_item)

            # Data/Hora
            execution_time = schedule["execution_time"]
            if isinstance(execution_time, str):
                execution_time = datetime.fromisoformat(execution_time)
            time_item = QtWidgets.QTableWidgetItem(execution_time.strftime("%d/%m/%Y %H:%M"))
            time_item.setFlags(time_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            time_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.schedule_table.setItem(row, 1, time_item)

            # Status
            status_item = QtWidgets.QTableWidgetItem("Ativo")
            status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            status_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.schedule_table.setItem(row, 2, status_item)

            # Botões de ação
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 5, 0, 5)
            action_layout.setSpacing(10)
            action_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Botão Editar
            edit_button = QtWidgets.QPushButton("Editar")
            edit_button.setFixedSize(75, 28)
            edit_button.setStyleSheet("""
                background-color: #2196F3;
                color: white;
                text-align: center;
                font-weight: bold;
                padding: 2px;
                border-radius: 3px;
            """)
            edit_button.clicked.connect(
                lambda checked, s=schedule: self.edit_schedule(s)
            )
            action_layout.addWidget(edit_button)

            # Botão Excluir
            delete_button = QtWidgets.QPushButton("Excluir")
            delete_button.setFixedSize(75, 28)
            delete_button.setStyleSheet("""
                background-color: #f44336;
                color: white;
                text-align: center;
                font-weight: bold;
                padding: 2px;
                border-radius: 3px;
            """)
            delete_button.clicked.connect(
                lambda checked, s=schedule: self.delete_schedule(s)
            )
            action_layout.addWidget(delete_button)

            self.schedule_table.setCellWidget(row, 3, action_widget)

        # Atualiza a tabela
        self.schedule_table.viewport().update()

    def edit_schedule(self, schedule):
        """Edita um agendamento existente"""
        dialog = ScheduleDialog(self, schedule)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            schedule_data = dialog.get_schedule_data()
            if self.scheduled_actions.update_schedule(
                schedule["id"],
                schedule_data["action"],
                schedule_data["execution_time"]
            ):
                self.update_schedule_table()
                self.notifications.show_notification(
                    "Agendamento Atualizado",
                    f"O agendamento de {schedule_data['action'].lower()} foi atualizado."
                )
            else:
                self.notifications.show_error_dialog(
                    "Erro", "Não foi possível atualizar o agendamento."
                )

    def delete_schedule(self, schedule):
        """Exclui um agendamento"""
        if self.notifications.show_confirmation_dialog(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o agendamento de {schedule['action'].lower()}?"
        ):
            # Cancela no sistema operacional e depois exclui do banco
            self.scheduled_actions.cancel_schedule(schedule['id'])
            if self.scheduled_actions.delete_schedule(schedule['id']):
                self.update_schedule_table()
                self.notifications.show_notification(
                    "Agendamento Excluído",
                    f"O agendamento de {schedule['action'].lower()} foi excluído."
                )
            else:
                self.notifications.show_error_dialog(
                    "Erro", "Não foi possível excluir o agendamento."
                )

    def check_upcoming_scheduled_actions(self):
        """Verifica os agendamentos que estão próximos e envia notificações"""
        if not self.settings.get("enable_alerts", True):
            return

        # Intervalos de notificação (em minutos)
        notification_intervals = [15, 10, 5]

        for interval in notification_intervals:
            upcoming = self.scheduled_actions.get_upcoming_schedules(interval)
            for schedule in upcoming:
                execution_time = schedule["execution_time"]
                # Calcula a diferença em minutos
                time_diff = (execution_time - datetime.now()).total_seconds() / 60

                # Se estiver dentro do intervalo (com margem de 1 minuto)
                for notify_at in notification_intervals:
                    if notify_at - 1 <= time_diff <= notify_at:
                        # Chave única para evitar notificações duplicadas
                        notification_key = f"{schedule['id']}_{notify_at}"

                        if not self.settings.get(notification_key, False):
                            # Envia notificação
                            self.notifications.show_notification(
                                "Agendamento Próximo",
                                f"O agendamento de {schedule['action'].lower()} acontecerá em aproximadamente {int(time_diff)} minutos."
                            )
                            self.settings.set(notification_key, True)

                            # Para notificação de 5 minutos, perguntar se deseja cancelar
                            if notify_at == 5:
                                if self.notifications.show_confirmation_dialog(
                                    "Confirmação de Agendamento",
                                    f"O agendamento de {schedule['action'].lower()} acontecerá em aproximadamente 5 minutos.\n\nDeseja cancelar este agendamento?"
                                ):
                                    self.scheduled_actions.cancel_schedule(schedule['id'])
                                    self.notifications.show_notification(
                                        "Agendamento Cancelado",
                                        f"O agendamento de {schedule['action'].lower()} foi cancelado."
                                    )
                                    self.update_schedule_table()

    def toggle_theme(self, state: int) -> None:
        """Altera o tema da aplicação e atualiza todos os componentes"""
        self.is_dark_theme = bool(state)
        self.settings.set("dark_theme", self.is_dark_theme)

        # Reinicializa os estilos base
        self.init_styles()

        # Aplica o tema geral
        self.setup_theme()

        # Atualiza a tabela de agendamentos
        self.update_table_style()

        # Atualiza o ícone do tray
        self.setup_tray()

    def update_group_styles(self) -> None:
        """Atualiza os estilos dos grupos de configuração"""
        group_style = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid %s;
                border-radius: 6px;
                margin-top: 12px;
                background-color: %s;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: %s;
                background-color: %s;
            }
            QCheckBox {
                color: %s;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid %s;
                border-radius: 3px;
                background-color: %s;
            }
            QCheckBox::indicator:checked {
                background-color: %s;
                border-color: %s;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid %s;
                border-radius: 4px;
                background-color: %s;
                color: %s;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: %s;
            }
        """

        if self.is_dark_theme:
            style = group_style % (
                "#3d3d3d",  # GroupBox border
                "#2d2d2d",  # GroupBox background
                "#ffffff",  # GroupBox text
                "#2d2d2d",  # GroupBox title background
                "#ffffff",  # GroupBox title text
                "#3d3d3d",  # CheckBox indicator border
                "#2d2d2d",  # CheckBox indicator background
                "#4CAF50",  # CheckBox indicator checked background
                "#4CAF50",  # CheckBox indicator checked border
                "#3d3d3d",  # SpinBox border
                "#2d2d2d",  # SpinBox background
                "#ffffff",  # SpinBox text
                "#3d3d3d",  # SpinBox buttons
            )
        else:
            style = group_style % (
                "#e0e0e0",  # GroupBox border
                "#ffffff",  # GroupBox background
                "#000000",  # GroupBox text
                "#ffffff",  # GroupBox title background
                "#000000",  # GroupBox title text
                "#e0e0e0",  # CheckBox indicator border
                "#ffffff",  # CheckBox indicator background
                "#4CAF50",  # CheckBox indicator checked background
                "#4CAF50",  # CheckBox indicator checked border
                "#e0e0e0",  # SpinBox border
                "#ffffff",  # SpinBox background
                "#000000",  # SpinBox text
                "#f5f5f5",  # SpinBox buttons
            )

        # Aplica o estilo aos grupos
        for group in self.settings_tab.findChildren(QtWidgets.QGroupBox):
            group.setStyleSheet(style)

    def update_table_style(self) -> None:
        """Atualiza o estilo da tabela de agendamentos"""
        table_style = """
            QTableWidget {
                background-color: %s;
                color: %s;
                border: 1px solid %s;
                border-radius: 4px;
                gridline-color: %s;
            }
            QHeaderView::section {
                background-color: %s;
                color: %s;
                padding: 6px;
                border: none;
                border-right: 1px solid %s;
                border-bottom: 1px solid %s;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid %s;
            }
            QTableWidget::item:selected {
                background-color: %s;
                color: %s;
            }
        """
        if self.is_dark_theme:
            self.schedule_table.setStyleSheet(
                table_style % (
                    "#2d2d2d",  # background
                    "#ffffff",  # text color
                    "#3d3d3d",  # border
                    "#3d3d3d",  # gridline
                    "#1e1e1e",  # header background
                    "#ffffff",  # header text
                    "#3d3d3d",  # header border right
                    "#3d3d3d",  # header border bottom
                    "#3d3d3d",  # item border
                    "#3d3d3d",  # selection background
                    "#ffffff",  # selection text
                )
            )
        else:
            self.schedule_table.setStyleSheet(
                table_style % (
                    "#ffffff",  # background
                    "#000000",  # text color
                    "#e0e0e0",  # border
                    "#e0e0e0",  # gridline
                    "#f5f5f5",  # header background
                    "#000000",  # header text
                    "#e0e0e0",  # header border right
                    "#e0e0e0",  # header border bottom
                    "#e0e0e0",  # item border
                    "#f0f0f0",  # selection background
                    "#000000",  # selection text
                )
            )

        # Define uma altura para as linhas da tabela
        self.schedule_table.verticalHeader().setDefaultSectionSize(75)  # Altura de 75px

        # Garante que as configurações das colunas sejam mantidas
        self.schedule_table.setColumnWidth(0, 120)  # Ação (aumentado)
        self.schedule_table.setColumnWidth(1, 170)  # Data/Hora (aumentado)
        self.schedule_table.setColumnWidth(2, 80)   # Status
        self.schedule_table.setColumnWidth(3, 180)  # Ações - largura fixa

        # Configuração das colunas fixas
        header = self.schedule_table.horizontalHeader()
        for i in range(4):  # TODAS as colunas com tamanho fixo, incluindo a coluna de Ações
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Fixed)

        # Garante que a tabela inteira se adapte ao conteúdo
        self.schedule_table.horizontalHeader().setStretchLastSection(True)

        # Atualiza a tabela para aplicar as mudanças
        self.schedule_table.viewport().update()

    def update_buttons_style(self):
        """Atualiza os estilos dos botões para uma aparência mais moderna"""
        # Botões principais com gradiente, sombra e transição
        main_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
                padding-top: 9px;
                padding-bottom: 7px;
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #999999;
            }
        """

        # Estilos para os botões de cancelamento/exclusão
        cancel_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 %s, stop:1 %s);
                padding-top: 9px;
                padding-bottom: 7px;
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #999999;
            }
        """

        # Estilos para ComboBoxes com design aprimorado
        combo_style = """
            QComboBox {
                border: 1px solid %s;
                border-radius: 4px;
                padding: 6px;
                min-width: 6em;
                background-color: %s;
                color: %s;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid %s;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.svg);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: %s;
                border: 1px solid %s;
                selection-background-color: %s;
                selection-color: white;
                border-radius: 0px;
            }
        """

        if self.is_dark_theme:
            # Estilos para tema escuro
            self.confirm_button.setStyleSheet(main_button_style % (
                "#4CAF50", "#3d8b40",  # Normal
                "#5cb860", "#4a9d4a",  # Hover
                "#3d8b40", "#367d36"  # Pressed
            ))
            self.cancel_button.setStyleSheet(cancel_button_style % (
                "#f44336", "#d32f2f",  # Normal
                "#ef5350", "#e53935",  # Hover
                "#d32f2f", "#c62828"  # Pressed
            ))
            self.new_schedule_button.setStyleSheet(main_button_style % (
                "#4CAF50", "#3d8b40",  # Normal
                "#5cb860", "#4a9d4a",  # Hover
                "#3d8b40", "#367d36"  # Pressed
            ))
            combo_colors = (
                "#3d3d3d",  # Border
                "#2d2d2d",  # Background
                "#ffffff",  # Text
                "#444444",  # Border dropdown
                "#2d2d2d",  # Dropdown background
                "#3d3d3d",  # Dropdown border
                "#4CAF50",  # Selection background
            )
        else:
            # Estilos para tema claro
            self.confirm_button.setStyleSheet(main_button_style % (
                "#4CAF50", "#3d8b40",  # Normal
                "#5cb860", "#4a9d4a",  # Hover
                "#3d8b40", "#367d36"  # Pressed
            ))
            self.cancel_button.setStyleSheet(cancel_button_style % (
                "#f44336", "#d32f2f",  # Normal
                "#ef5350", "#e53935",  # Hover
                "#d32f2f", "#c62828"  # Pressed
            ))
            self.new_schedule_button.setStyleSheet(main_button_style % (
                "#4CAF50", "#3d8b40",  # Normal
                "#5cb860", "#4a9d4a",  # Hover
                "#3d8b40", "#367d36"  # Pressed
            ))
            combo_colors = (
                "#d0d0d0",  # Border
                "#ffffff",  # Background
                "#333333",  # Text
                "#e0e0e0",  # Border dropdown
                "#ffffff",  # Dropdown background
                "#d0d0d0",  # Dropdown border
                "#4CAF50",  # Selection background
            )

        # Aplica os estilos aos ComboBoxes
        for combo in [self.action_combo, self.hours_combo, self.minutes_combo, self.seconds_combo]:
            combo.setStyleSheet(combo_style % combo_colors)

        # Também atualizamos os botões na tabela de agendamentos, caso existam
        self.update_table_buttons_style()

    def update_table_buttons_style(self):
        """Atualiza o estilo dos botões na tabela de agendamentos"""
        # Estilos para os botões de Editar e Excluir na tabela
        edit_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                font-weight: bold;
                padding: 4px;
                border: none;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #42A5F5, stop:1 #2196F3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #1976D2, stop:1 #1565C0);
                padding-top: 5px;
                padding-bottom: 3px;
            }
        """

        delete_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                font-weight: bold;
                padding: 4px;
                border: none;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #ef5350, stop:1 #e53935);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #d32f2f, stop:1 #c62828);
                padding-top: 5px;
                padding-bottom: 3px;
            }
        """

        # Percorre todas as linhas da tabela para aplicar o estilo aos botões
        for row in range(self.schedule_table.rowCount()):
            action_widget = self.schedule_table.cellWidget(row, 3)
            if action_widget:
                # Encontra os botões no layout do widget
                buttons = action_widget.findChildren(QtWidgets.QPushButton)
                if len(buttons) >= 2:
                    # Primeiro botão é o Editar
                    buttons[0].setStyleSheet(edit_button_style)
                    # Segundo botão é o Excluir
                    buttons[1].setStyleSheet(delete_button_style)

                    # Adiciona efeito de sombra aos botões
                    for button in buttons:
                        shadow = QtWidgets.QGraphicsDropShadowEffect(button)
                        shadow.setBlurRadius(10)
                        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
                        shadow.setOffset(0, 2)
                        button.setGraphicsEffect(shadow)

    def quit_application(self) -> None:
        """Fecha o aplicativo completamente"""
        self.tray_icon.hide()  # Esconde o ícone da bandeja antes de fechar
        QtWidgets.QApplication.quit()  # Fecha o aplicativo

    def closeEvent(self, event) -> None:
        """Evento chamado quando a janela é fechada"""
        if self.settings.get("minimize_to_tray", True) and not self.is_quitting:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Agendador de Desligamento",
                "O aplicativo foi minimizado para a bandeja do sistema.",
                QtGui.QIcon(),
                2000,
            )
        else:
            self.tray_icon.hide()  # Esconde o ícone da bandeja antes de fechar
            event.accept()

    def toggle_window(self) -> None:
        """Alterna a visibilidade da janela principal"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()  # Traz a janela para frente

    def clear_notification_settings(self, schedule_id: int) -> None:
        """Limpa as configurações de notificação quando um agendamento é cancelado ou excluído"""
        # Intervalos de notificação (em minutos)
        notification_intervals = [15, 10, 5]

        # Remove todas as marcações de notificação para este agendamento
        for interval in notification_intervals:
            notification_key = f"{schedule_id}_{interval}"
            self.settings.remove(notification_key)

    def cleanup_old_notification_settings(self) -> None:
        """Limpa configurações de notificação de agendamentos antigos ou inativos"""
        try:
            # Obtém todos os agendamentos ativos
            active_schedules = self.scheduled_actions.get_active_schedules()
            active_ids = [schedule["id"] for schedule in active_schedules]
            all_keys = list(self.settings.settings.keys())

            # Filtra as chaves relacionadas a notificações
            notification_keys = [
                key for key in all_keys if "_" in key and key.split("_")[0].isdigit()
            ]

            # Remove notificações de agendamentos que não estão mais ativos
            for key in notification_keys:
                schedule_id = int(key.split("_")[0])
                if schedule_id not in active_ids:
                    self.settings.remove(key)
        except (ValueError, TypeError, OSError) as e:
            print(f"Erro ao limpar configurações antigas: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ShutdownScheduler()
    window.show()
    sys.exit(app.exec())
