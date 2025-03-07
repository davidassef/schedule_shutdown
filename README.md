# Shutdown Scheduler

**Desenvolvido por:** David Assef

## Descrição

O Shutdown Scheduler é um aplicativo desenvolvido em Python que permite agendar o desligamento ou reinicialização do sistema através de uma interface gráfica construída com PyQt5.  
Com ele, você pode escolher entre agendar a ação por meio de um temporizador ou definir um horário específico usando um calendário e um QDateTimeEdit. Além disso, o aplicativo oferece a opção de iniciar com o Windows.

## Funcionalidades

- **Agendamento de desligamento ou reinicialização:**  
  Permite programar o desligamento ou reinicialização do computador.

- **Modos de agendamento:**  
  - **Temporizador:** Selecione horas, minutos e segundos para contar o tempo até a ação.  
  - **Hora definida:** Utilize um calendário e um QDateTimeEdit para definir a data e a hora exatas.

- **Opção de Startup:**  
  Configure o aplicativo para iniciar automaticamente com o Windows.

- **Suporte a múltiplos idiomas:**  
  Disponível em Português, English e Español.

- **Temas personalizáveis:**  
  Escolha entre tema Automático, Clara ou Escura para adaptar a interface.

## Requisitos

- Python 3.x  
- PyQt5  
- requests  

## Instalação e Execução

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/shutdown-scheduler.git
   cd shutdown-scheduler

2. **Instale as dependências:**

   ```bash
   pip install pyqt5 requests

3. **Execute o aplicativo:**

   ```bash
   python shutdown_scheduler.py

## Empacotando o Aplicativo

Para gerar um executável (por exemplo, para Windows) utilize o PyInstaller. Recomenda-se usar as opções --windowed (para não abrir o console) e --uac-admin (para solicitar privilégios de administrador):

```bash
pyinstaller --onefile --windowed --uac-admin --icon=icon.ico shutdown_scheduler.py
```

Após a execução, o executável será gerado na pasta dist.

## Licença
Este projeto é licenciado sob a MIT License.

## Contato
Para sugestões, dúvidas ou contribuições, sinta-se à vontade para entrar em contato.

[Visite meu GitHub](https://github.com/davidassef)
