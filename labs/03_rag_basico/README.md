# Lab 3: Sistema RAG Simplificado (Retrieval-Augmented Generation)

## 🎯 Propósito do Laboratório

**Implementar e validar um sistema RAG funcional com métricas reais e arquitetura simplificada.**

Este laboratório demonstra a implementação de um sistema RAG (Retrieval-Augmented Generation) com foco na funcionalidade essencial e métricas reais, utilizando LangChain e ChromaDB, com recursos como re-ranking semântico, query expansion, e sistema de métricas não mockado.

## 🚀 Recursos Implementados

### ✅ **1. Re-ranking Semântico**
- Cross-Encoder para re-ranking de documentos
- Melhoria na precisão da recuperação
- Scores reais de relevância

### ✅ **2. Query Expansion**
- Expansão automática de queries usando LLM
- Geração de variações semânticas (configurável)
- Melhoria no recall de documentos

### ✅ **3. Chunking Inteligente**
- Divisão de documentos com overlap otimizado
- Preservação de contexto entre chunks
- Metadados estruturados para cada chunk

### ✅ **4. Prompt Engineering Dinâmico**
- Análise de contexto da query
- Templates de prompt adaptativos
- Otimização por tipo de pergunta

### ✅ **5. Sistema de Métricas Reais**
- Context recall baseado em relevância real
- Precision calculada com scores de similaridade
- Scores de documentos usando Cross-Encoder
- Eliminação de mocks e simulações

## 🏆 Resultados Finais

### ✅ Status: SISTEMA RAG SIMPLIFICADO OPERACIONAL
- **Score Final**: 75.0% (métricas reais)
- **Taxa de Sucesso**: 100%
- **Recall de Contexto**: 58% (real, não mockado)
- **Precisão de Respostas**: 58% (real, não mockado)
- **Taxa de Uso de RAG**: 100%
- **Tempo de Resposta**: 5.99s

### 📊 Análise de Performance Real
- **Queries Técnicas**: Alta performance (recall/precision ~100%)
- **Queries Não-Técnicas**: Performance baixa (recall/precision ~0%)
- **Comportamento Esperado**: Sistema especializado em domínio técnico
- **Variação Real**: Métricas variam conforme relevância da query

## 📁 Estrutura do Projeto Simplificada

```
03_rag_basico/
├── 📂 src/                          # Código fonte principal
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   └── rag_system.py            # Sistema RAG simplificado
│   └── 📂 utils/
│       ├── __init__.py
│       ├── config.py                # Configurações do sistema
│       ├── logging_config.py        # Configuração de logs
│       └── metrics.py               # Métricas básicas reais
├── 📂 scripts/                      # Scripts essenciais
│   ├── 📂 core/                     # Execução principal e validação
│   │   ├── main.py                  # Script principal interativo
│   │   └── validate_lab.py          # Validação simplificada
│   ├── 📂 analysis/                 # Análise básica
│   │   ├── test_basic_metrics.py    # Teste de métricas reais
│   │   └── simple_query_test.py     # Teste simples de queries
│   └── 📂 optimization/             # Otimização básica
│       └── apply_optimizations.py   # Otimizações essenciais
├── 📂 docs/                         # Documentação mantida
│   └── 📂 posts/                    # Artigos sobre evolução
├── 📂 data/                         # Dados (limpos)
│   └── chroma_db/                   # Banco de dados vetorial
├── 📂 metrics/                      # Métricas simples
│   └── rag_metrics.json             # Arquivo de métricas limpo
├── 📂 reports/                      # Relatórios (limpos)
├── 📄 README.md                     # Este arquivo
├── 📄 requirements.txt              # Dependências essenciais
├── 📄 config.json                   # Configuração principal
├── 📄 .gitignore                    # Arquivo gitignore completo
└── 📂 venv/                         # Ambiente virtual Python
```

## 🚀 Como Usar

### 1. **Configuração Inicial**
```bash
# Clonar o repositório
git clone <repository-url>
cd 03_rag_basico

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 2. **Configuração do Ambiente**
```bash
# Configurar .env com suas credenciais
# OPENAI_API_KEY=sua_chave_aqui
```

### 3. **Execução do Sistema**
```bash
# Executar sistema principal (interativo)
python scripts/core/main.py

# Validar laboratório com métricas reais
python scripts/core/validate_lab.py

# Testar métricas básicas
python scripts/analysis/test_basic_metrics.py

# Teste simples de queries
python scripts/analysis/simple_query_test.py

# Aplicar otimizações básicas
python scripts/optimization/apply_optimizations.py
```

## 📈 Evolução do Projeto

### **Fase 1: Sistema Básico → Avançado**
- ✅ Implementação de recursos modernos
- ✅ Sistema complexo com múltiplas funcionalidades
- ✅ Métricas granulares complexas (posteriormente simplificadas)

### **Fase 2: Complexidade Excessiva**
- ❌ Projeto tornou-se muito complexo
- ❌ Muitos arquivos desnecessários (363 arquivos de cache)
- ❌ Configurações duplicadas
- ❌ Métricas mockadas/simuladas

### **Fase 3: Simplificação e Métricas Reais**
- ✅ Remoção de 70% da complexidade desnecessária
- ✅ Implementação de métricas reais
- ✅ Estrutura limpa e maintível
- ✅ Foco na funcionalidade essencial

## 🛠️ Arquitetura Simplificada

### **Sistema RAG Principal** (`src/core/rag_system.py`)
- Sistema unificado com recursos essenciais
- Re-ranking semântico com Cross-Encoder
- Query expansion configurável
- Busca vetorial com ChromaDB
- Chunking inteligente
- Prompt engineering dinâmico
- Métricas reais de performance

### **Utilitários** (`src/utils/`)
- **config.py**: Configurações centralizadas
- **metrics.py**: Métricas básicas reais (simplificado de 519 para 134 linhas)
- **logging_config.py**: Configuração de logs

## 🚧 Desafios Enfrentados e Soluções Implementadas

### 🔍 **Desafio 1: Complexidade Excessiva do Projeto**

**Problema**: 
- Projeto havia se tornado extremamente complexo com muitos arquivos desnecessários
- 4 configurações duplicadas
- 6 scripts de otimização complexos (totalizing 62KB)
- Arquivo de métricas com 20.191 linhas
- 363 arquivos de cache PKL acumulados
- Documentação redundante e confusa

**Solução Implementada**:
Realizada uma simplificação radical do projeto, removendo toda a complexidade desnecessária e mantendo apenas o essencial. A estrutura foi reorganizada para ser mais limpa e maintível, com foco na funcionalidade core do sistema RAG.

**Resultado**: Redução de 70% no código complexo, estrutura clara e fácil manutenção

### 🔍 **Desafio 2: Métricas Mockadas e Irreais**

**Problema**: 
- Context recall sempre retornava 1.0 se havia documentos
- Precision sempre retornava 1.0 se havia documentos  
- Document scores eram valores fixos simulados [0.8, 0.7, 0.6, 0.5, 0.4]
- Sistema sempre retornava todos os documentos de teste
- Métricas não refletiam performance real do sistema

**Solução Implementada**:
Implementação completa de métricas reais baseadas em cálculos de similaridade e relevância. O sistema agora calcula context recall baseado na proporção de documentos relevantes encontrados, precision baseada na qualidade dos documentos retornados, e utiliza scores reais do Cross-Encoder em vez de valores simulados.

**Resultado**: Métricas reais que variam conforme a performance (recall médio: 58%, precision média: 58%)

### 🔍 **Desafio 3: Sistema de Busca Irreal**

**Problema**: 
- Modo de teste sempre retornava todos os 8 documentos
- Não havia filtragem por similaridade real
- Busca não considerava relevância da query
- Comportamento idêntico para todas as queries

**Solução Implementada**:
Implementação de busca por similaridade real mesmo no modo de teste. O sistema agora calcula scores de similaridade para todos os documentos, filtra por threshold de relevância, ordena por score e retorna apenas os documentos mais relevantes. Queries técnicas encontram documentos relevantes, queries não-técnicas retornam poucos ou nenhum documento.

**Resultado**: Comportamento realista com variação de documentos (1-2 docs técnicos vs 0 docs não-técnicos)

### 🔍 **Desafio 4: Query Expansion Desnecessária**

**Problema**: 
- Query expansion estava habilitada por padrão
- Causava lentidão no sistema (6+ queries por busca)
- Nem sempre melhorava os resultados
- Complexidade adicional desnecessária

**Solução Implementada**:
Query expansion foi desabilitada por padrão e tornada configurável. O sistema agora foca na qualidade da busca principal em vez de múltiplas variações, resultando em respostas mais rápidas e ainda mantendo boa qualidade.

**Resultado**: Tempo de resposta melhorado e sistema mais direto

### 🔍 **Desafio 5: Organização de Arquivos e Gitignore**

**Problema**: 
- Falta de .gitignore adequado
- Arquivos sensíveis e cache sendo versionados
- Estrutura desorganizada
- Dificuldade para manter o repositório

**Solução Implementada**:
Criação de .gitignore completo e abrangente, incluindo arquivos Python padrão, dados sensíveis, cache, logs, relatórios temporários, e arquivos específicos do projeto RAG. Organização da estrutura de arquivos com foco na simplicidade.

**Resultado**: Repositório limpo e organizado, com controle adequado de versionamento

## 📊 Configuração e Personalização

### **Configuração Principal** (`config.json`)
```json
{
  "model_name": "gpt-4o-mini-2024-07-18",
  "temperature": 0.2,
  "chunk_size": 250,
  "chunk_overlap": 150,
  "vectorstore_search_k": 8,
  "similarity_threshold": 0.1,
  "use_query_expansion": false,
  "use_semantic_reranking": true,
  "embedding_cache_enabled": true
}
```

### **Critérios de Avaliação**
- Taxa de sucesso ≥ 90%: ✅ (100.0%)
- Tempo médio ≤ 5s: ❌ (5.99s)
- Recall médio ≥ 70%: ❌ (58%)
- Precisão média ≥ 70%: ❌ (58%)
- Taxa uso RAG ≥ 70%: ✅ (100.0%)
- Score final ≥ 70%: ✅ (75.0%)

## 📊 Métricas Reais vs Mockadas

| Métrica | **Antes (Mock)** | **Depois (Real)** |
|---------|------------------|-------------------|
| Recall médio | 100% (sempre) | 58% (variável) |
| Precisão média | 100% (sempre) | 58% (variável) |
| Score final | 100% (sempre) | 75% (real) |
| Documentos | 8 (sempre) | 1-2 (variável) |
| Comportamento | Idêntico | Varia por query |

## 📚 Scripts Principais

- **`scripts/core/main.py`**: Sistema interativo principal
- **`scripts/core/validate_lab.py`**: Validação com métricas reais
- **`scripts/analysis/test_basic_metrics.py`**: Teste de métricas básicas
- **`scripts/analysis/simple_query_test.py`**: Teste simples de queries
- **`scripts/optimization/apply_optimizations.py`**: Otimizações básicas

## 🎯 Status Atual

### ✅ **Conquistas**
- Sistema RAG funcional e simplificado
- Métricas 100% reais (não mockadas)
- Estrutura limpa e maintível
- Performance realista para domínio técnico
- Repositório organizado com .gitignore

### 🔄 **Próximas Melhorias Possíveis**
- Expandir base de documentos para melhorar recall
- Otimizar tempo de resposta (atual: 5.99s)
- Melhorar performance para queries não-técnicas
- Implementar cache mais eficiente

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Execute os testes: `python scripts/core/validate_lab.py`
5. Submeta um Pull Request

---

**Desenvolvido como parte do Laboratório 3: Sistema RAG Simplificado com Métricas Reais**
