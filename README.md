# 🕐 Agendador de Desligamento v2

> **Um aplicativo desktop moderno e intuitivo para agendar ações do sistema**

Desenvolvido em Python com PyQt6, oferece uma interface elegante para agendar desligamento, reinicialização, suspensão e hibernação do seu computador.

## 📥 Download

### 🚀 Executável Pronto para Uso

**[⬇️ Baixar Agendador de Desligamento v2.exe](./dist/Agendador%20de%20Desligamento.exe)** *(35.2 MB)*

> ✅ **Não requer instalação** - Execute diretamente após o download  
> ✅ **Compatível com Windows** - Testado no Windows 10/11  
> ✅ **Executável único** - Todas as dependências incluídas  

### 💡 Como Usar o Executável
1. Faça o download do arquivo `.exe` acima
2. Execute o arquivo (pode aparecer um aviso do Windows Defender - clique em "Mais informações" → "Executar assim mesmo")
3. O aplicativo será iniciado e estará pronto para uso!

---

## 📁 Estrutura do Projeto

```
Agendador de Desligamento v2/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências do projeto
├── pytest.ini               # Configuração do pytest
├── build_app.py              # Script para build da aplicação
├── update_git.py             # Script para atualização do Git
│
├── src/                      # Código fonte principal
│   ├── __init__.py
│   ├── core/                 # Configurações e funcionalidades centrais
│   │   ├── __init__.py
│   │   └── settings.py       # Gerenciamento de configurações
│   ├── models/               # Modelos de dados
│   │   ├── __init__.py
│   │   └── database.py       # Gerenciamento do banco de dados SQLite
│   ├── services/             # Serviços e lógica de negócio
│   │   ├── __init__.py
│   │   ├── system_actions.py # Ações do sistema (desligar, reiniciar, etc.)
│   │   ├── notifications.py  # Sistema de notificações
│   │   ├── immediate_actions.py # Gerenciamento de ações imediatas
│   │   └── scheduled_actions.py # Gerenciamento de ações agendadas
│   ├── ui/                   # Interface do usuário
│   │   ├── __init__.py
│   │   ├── main.py           # Janela principal da aplicação
│   │   └── schedule_dialog.py # Diálogo de agendamento
│   └── utils/                # Utilitários e helpers
│       ├── __init__.py
│       ├── column_adjuster.py # Ajuste de colunas de tabela
│       └── table_customizer.py # Customização de tabelas
│
├── tests/                    # Testes unitários
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_system_actions.py
│   ├── test_notifications.py
│   ├── test_immediate_actions.py
│   ├── test_scheduled_actions.py
│   ├── test_settings.py
│   └── test_coverage.py
│
├── docs/                     # Documentação
│   ├── CHANGELOG.md
│   ├── LICENSE
│   └── regras.txt
│
└── assets/                   # Recursos visuais
    ├── icon.ico
    ├── icon.svg
    ├── check.svg
    ├── down_arrow.svg
    └── icon_*.png
```

## 📚 Documentação e Recursos

### 📖 Documentação Principal
- **[📋 Changelog](./CHANGELOG.md)** - Histórico de versões e mudanças
- **[📄 Licença](./docs/LICENSE)** - Termos de uso e licenciamento
- **[📋 Regras de Desenvolvimento](./docs/regras.txt)** - Diretrizes do projeto

### 🛠️ Para Desenvolvedores

#### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

#### Instalação para Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/davidassef/schedule_shutdown
cd "Agendador de Desligamento v2"
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python main.py
```

## 🧪 Executar Testes

Para executar todos os testes:
```bash
python -m pytest tests/ -v
```

Para executar testes específicos:
```bash
python -m pytest tests/test_database.py -v
```

Para executar testes com cobertura:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 📦 Build da Aplicação

Para gerar um executável:
```bash
python build_app.py
```

## 🏗️ Arquitetura

### Camadas da Aplicação

1. **UI Layer** (`src/ui/`): Interface gráfica usando PyQt6
2. **Services Layer** (`src/services/`): Lógica de negócio e serviços
3. **Models Layer** (`src/models/`): Modelos de dados e acesso ao banco
4. **Core Layer** (`src/core/`): Configurações e funcionalidades centrais
5. **Utils Layer** (`src/utils/`): Utilitários e helpers

### Principais Componentes

- **SystemActions**: Gerencia ações do sistema (desligar, reiniciar, suspender, hibernar)
- **Database**: Gerencia persistência de dados usando SQLite
- **NotificationManager**: Sistema de notificações do sistema
- **Settings**: Gerenciamento de configurações da aplicação
- **ScheduledActionsManager**: Gerencia ações agendadas
- **ImmediateActionsManager**: Gerencia ações imediatas

### Testes

O projeto inclui uma suíte completa de testes:

```bash
# Execute os testes unitários
python -m unittest discover

# Execute os testes de cobertura
python test_coverage.py
```

### Gerar Executável

Para criar um arquivo executável autônomo:

```bash
python build_app.py
```

O executável será gerado na pasta `dist/`.

## ✨ Recursos Principais

- ⏰ **Agendamento Flexível**: Configure horários específicos ou intervalos de tempo
- 🔄 **Múltiplas Ações**: Desligar, reiniciar, suspender ou hibernar
- 📊 **Histórico Completo**: Acompanhe todas as ações executadas
- 🎨 **Interface Moderna**: Design limpo e intuitivo com tema escuro/claro
- 🔔 **Notificações**: Alertas visuais e sonoros personalizáveis
- ⚙️ **Configurável**: Personalize comportamentos e aparência
- 🚀 **Executável Único**: Não requer instalação
- 🔧 **Minimização**: Execute na bandeja do sistema

## 📊 Status do Projeto

- ✅ **69 Testes Automatizados** - Cobertura de 40%
- ✅ **Documentação Completa** - Código bem documentado
- ✅ **Build Automatizado** - Executável gerado automaticamente
- ✅ **Arquitetura Modular** - Código organizado e manutenível

## 📝 Histórico e Mudanças

Para ver o histórico completo de versões e mudanças, consulte o **[📋 Changelog](./CHANGELOG.md)**.

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo **[📄 LICENSE](./docs/LICENSE)** para detalhes completos.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

<div align="center">

**Desenvolvido com ❤️ em Python + PyQt6**

[⬆️ Voltar ao topo](#-agendador-de-desligamento-v2)

</div>