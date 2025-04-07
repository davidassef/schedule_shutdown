# Agendador de Desligamento v2.0

Um aplicativo desktop em Python que permite agendar operações do sistema como desligar, reiniciar, suspender e hibernar o computador.

![Agendador de Desligamento](icon.svg)

## Funcionalidades

- Agendar ações do sistema para horários específicos
- Programar ações imediatas com contagem regressiva
- Interface gráfica moderna e intuitiva
- Suporte para temas claro e escuro
- Notificações e alertas do sistema
- Personalização de configurações
- Histórico de ações realizadas

## Requisitos do Sistema

- Sistema operacional: Windows (10/11)
- Não requer instalação: basta executar o arquivo .exe

## Uso

1. **Ações imediatas**: Selecione uma ação (Desligar, Reiniciar, etc.) e defina um tempo para a contagem regressiva
2. **Ações agendadas**: Programe ações para horários específicos através do diálogo de agendamento
3. **Configurações**: Personalize o funcionamento do aplicativo através do menu de configurações

## Instruções para Desenvolvimento

### Dependências

Para desenvolver ou modificar o código-fonte, você precisará:

```bash
# Instale as dependências usando pip
pip install -r requirements.txt
```

### Estrutura do Projeto

O projeto está organizado nos seguintes módulos:

- `main.py` - Ponto de entrada do aplicativo e interface principal
- `system_actions.py` - Gerencia as ações do sistema (desligar, reiniciar, etc.)
- `scheduled_actions.py` - Gerencia as ações agendadas
- `immediate_actions.py` - Gerencia as ações imediatas
- `database.py` - Gerencia a persistência de dados em SQLite
- `settings.py` - Gerencia as configurações do aplicativo
- `notifications.py` - Gerencia as notificações e alertas
- `schedule_dialog.py` - Diálogo para agendamento de ações

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

## Histórico de Versões

### v2.0 (Abril/2025)
- Refatoração completa do código
- Adicionada interface aprimorada
- Suporte completo a temas
- Melhor gerenciamento de agendamentos
- Cobertura de testes expandida
- Notificações aprimoradas

### v1.0 (Lançamento inicial)
- Funcionalidades básicas de agendamento
- Suporte para ações do sistema
- Interface gráfica simples

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um pull request.