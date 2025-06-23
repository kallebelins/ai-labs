# Lab01: Chatbot LangChain

## Estrutura do Projeto

```
01_chatbot_langchain/
│
├── scripts/
│   ├── main.py                # Interface interativa do chatbot
│   ├── test_chatbot.py         # Script de teste com perguntas predefinidas
│   ├── run_analysis.py         # Script de análise de logs
│   └── setup_env.py            # Script de configuração automática
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── chatbot.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── metrics.py
│   │   ├── testing.py
│   │   └── reporting.py
│   │
│   └── analysis/
│       ├── __init__.py
│       └── analyze_logs.py
│
├── input/
│   └── inputs.txt
│
├── logs/
│   └── (arquivos de logs gerados nas execuções)
│
├── metrics/
│   └── (relatórios de métricas)
│
├── requirements.txt
└── README.md
```

### Descrição dos Arquivos

#### **Scripts Principais (`scripts/`):**
- **main.py**: Interface interativa do chatbot. Permite conversar com o chatbot em tempo real.
- **test_chatbot.py**: Script de teste com perguntas predefinidas. Útil para testes automatizados e demonstração.
- **run_analysis.py**: Script para executar análise de logs e calcular métricas.
- **setup_env.py**: Script para configurar automaticamente o ambiente virtual e dependências.

#### **Módulo Core (`src/core/`):**
- **chatbot.py**: Motor do chatbot usando LangChain. Contém a classe ChatbotEngine.

#### **Módulo Utils (`src/utils/`):**
- **config.py**: Carregamento e gerenciamento de configurações do laboratório.
- **logging_config.py**: Configuração de logging estruturado em JSON.
- **metrics.py**: Coleta e análise de métricas. Contém MetricsCollector e classes de dados.
- **testing.py**: Execução de testes automatizados. Contém TestRunner.
- **reporting.py**: Geração de relatórios e exportação de resultados.

#### **Módulo Analysis (`src/analysis/`):**
- **analyze_logs.py**: Script para analisar logs JSON e calcular métricas de performance.

### Pastas

- **input/**: Contém os arquivos de entrada usados para testar ou simular o lab (`inputs.txt`).
- **logs/**: Guarda os logs gerados durante as execuções do lab (formato JSON estruturado).
- **metrics/**: Contém arquivos com métricas extraídas de cada execução.

## Como Executar

### Pré-requisitos
- Python 3.11 (recomendado para compatibilidade)
- Chave da API OpenAI configurada no arquivo `.env`

### 🚀 Configuração Rápida (Recomendado)

Execute o script de configuração automática:

```bash
# Windows
python scripts/setup_env.py

# Linux/macOS
python3 scripts/setup_env.py
```

O script irá:
- ✅ Verificar a versão do Python
- ✅ Criar ambiente virtual (.venv)
- ✅ Instalar todas as dependências
- ✅ Criar arquivo .env de exemplo
- ✅ Criar diretórios necessários
- ✅ Mostrar próximos passos

**Depois do script, apenas:**
1. Editar o arquivo `.env` e adicionar sua chave da API OpenAI
2. Ativar o ambiente virtual: `.venv\Scripts\activate` (Windows) ou `source .venv/bin/activate` (Linux/macOS)
3. Executar: `python scripts/main.py`

### Configuração Manual

#### **1. Configuração do Ambiente Virtual**

#### **Windows (PowerShell/CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate
where python
```

#### **Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
which python
```

#### **Usando Python 3.11 especificamente (Windows):**
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
python --version
```

#### **2. Instalação das Dependências**

```bash
pip install -r requirements.txt
pip list
```

#### **3. Configuração da API OpenAI**

Crie um arquivo `.env` na raiz do projeto:

```bash
echo OPENAI_API_KEY=sua_chave_api_aqui > .env
echo MODEL_NAME=gpt-3.5-turbo >> .env
echo TEMPERATURE=0.7 >> .env
echo MAX_RESPONSE_TIME=3.0 >> .env
echo MIN_SUCCESS_RATE=95.0 >> .env
```

**⚠️ Importante:** Substitua `sua_chave_api_aqui` pela sua chave real da API OpenAI.

#### **4. Executar o Projeto**

##### **Opção A: Interface Interativa (Recomendado para uso real)**
```bash
python scripts/main.py
```

##### **Opção B: Teste com Perguntas Predefinidas**
```bash
python scripts/test_chatbot.py
```

##### **Opção C: Analisar logs e calcular métricas**
```bash
python scripts/run_analysis.py logs/app.log
# Ou para salvar relatório:
python scripts/run_analysis.py logs/app.log -o metrics/metrics_report.json
```

#### **5. Desativar Ambiente Virtual**

```bash
deactivate
```

## Logs Estruturados

O laboratório usa logs em formato JSON para facilitar a análise posterior:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "level": "INFO",
  "logger": "src.utils.logging_config",
  "message": "Métricas: tempo=1.234s, tokens=150, confiança=0.85",
  "module": "main",
  "function": "main",
  "line": 27
}
```

## Métricas Coletadas

O script `run_analysis.py` calcula as seguintes métricas:

- **Tempo de resposta**: média, mediana, mínimo, máximo, desvio padrão
- **Tokens utilizados**: média, mediana, total, estatísticas
- **Confiança**: média, mediana, range de valores
- **Estatísticas gerais**: total de logs, queries processadas

## Exemplo de Uso Completo

```bash
# 1. Executar script de configuração
python scripts/setup_env.py

# 2. Editar .env com sua chave da API
# 3. Ativar ambiente virtual
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# 4. Executar projeto (escolha uma opção):
# Opção A: Interface interativa
python scripts/main.py

# Opção B: Teste com perguntas predefinidas
python scripts/test_chatbot.py

# 5. Analisar logs
python scripts/run_analysis.py logs/app.log

# 6. Desativar ambiente
 deactivate
```

## Solução de Problemas

### **Erro de módulo não encontrado:**
Certifique-se de rodar os scripts sempre pelo diretório raiz do projeto e usando o caminho `python scripts/nome_do_script.py`. Os scripts já ajustam o `sys.path` automaticamente para encontrar os módulos internos.

### **Erro de versão do Python:**
```bash
python --version
# Se não for 3.11, use especificamente:
py -3.11 scripts/main.py
```

### **Erro de dependências:**
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### **Erro de API OpenAI:**
```bash
cat .env
# Verifique se a chave é válida
```

## Arquitetura Modular Organizada

O projeto segue uma arquitetura modular organizada em pastas com separação clara de responsabilidades:

```
src/
├── core/           # Funcionalidades principais
│   └── chatbot.py  # Motor do chatbot
├── utils/          # Funções auxiliares
│   ├── config.py           # Configurações
│   ├── logging_config.py   # Logging
│   ├── metrics.py          # Métricas
│   ├── testing.py          # Testes
│   └── reporting.py        # Relatórios
└── analysis/       # Análise de dados
    └── analyze_logs.py     # Análise de logs
```

### **Benefícios da Organização:**
- ✅ **Separação por responsabilidade**: Cada pasta tem uma função específica
- ✅ **Manutenibilidade**: Fácil localizar e modificar funcionalidades
- ✅ **Reutilização**: Módulos podem ser importados independentemente
- ✅ **Testabilidade**: Cada módulo pode ser testado isoladamente
- ✅ **Escalabilidade**: Fácil adicionar novas funcionalidades
- ✅ **Organização profissional**: Estrutura padrão da indústria

### **Imports Organizados:**
```python
# Core functionality
from src.core.chatbot import ChatbotEngine

# Utilities
from src.utils.config import load_config
from src.utils.logging_config import setup_logging
from src.utils.metrics import MetricsCollector

# Analysis
from src.analysis.analyze_logs import load_json_logs
```

## Objetivo

Implementar e avaliar um chatbot modular usando LangChain e OpenAI, com foco em:
- Interface interativa para uso real
- Script de teste com perguntas predefinidas
- Logging estruturado para análise posterior
- Cálculo de métricas a partir dos logs
- Separação clara entre código de aplicação e análise
- Arquitetura modular com responsabilidades bem definidas
- Manutenibilidade e escalabilidade do código
- Organização profissional em pastas
- Configuração adequada de ambiente virtual
- Script de configuração automática para facilitar o setup
