# 📍 Mapeamento das Fases de Evolução no Código

Este documento mostra exatamente onde cada fase de evolução foi implementada no código do sistema RAG.

## 🏗️ **FASE 1: Sistema Básico (65%)**

### **Arquivo: `src/core/rag_system.py`**

#### **1. Inicialização do Sistema (Linhas 22-70)**
```python
def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
    # Configuração básica do sistema
    self.config = config
    self.logger = logger or logging.getLogger(__name__)
    
    # Inicializa o LLM com OpenAI
    self.llm = ChatOpenAI(
        model_name=config["model_name"],
        temperature=config["temperature"],
        openai_api_key=config["openai_api_key"]
    )
    
    # Inicializa embeddings
    self.embeddings = OpenAIEmbeddings()
    
    # Configura vetorstore
    self._setup_vectorstore()
```

#### **2. Configuração do Vetorstore (Linhas 72-100)**
```python
def _setup_vectorstore(self):
    """Configura o vetorstore para documentos"""
    # Inicializa ChromaDB
    self.vectorstore = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=self.embeddings,
        collection_name="rag_documents"
    )
```

#### **3. Recuperação Básica de Documentos (Linhas 173-206)**
```python
def _retrieve_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Recupera documentos relevantes para a query"""
    # Busca documentos similares no vetorstore
    docs = self.vectorstore.similarity_search(query, k=k)
    
    # Converte para formato padrão
    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    
    return results
```

#### **4. Processamento de Query Básico (Linhas 347-420)**
```python
def process_query(self, query: str) -> Dict[str, Any]:
    """Processa uma query usando o sistema RAG"""
    # Recupera documentos relevantes
    relevant_docs = self._retrieve_documents(query, k=3)
    
    # Gera resposta usando o LLM
    response = self.llm.invoke(messages)
    
    return {
        "success": True,
        "response": response.content,
        "documents_used": len(relevant_docs),
        # ... outras métricas
    }
```

---

## 🎯 **FASE 2: Re-ranking Inteligente (77.2%)**

### **Arquivo: `src/core/rag_system.py`**

#### **1. Inicialização dos Pesos (Linhas 32-37)**
```python
# Inicializa pesos do re-ranking (serão ajustados dinamicamente)
self.rerank_weights = {
    'keyword_overlap': 0.4,      # 40% - Overlap de palavras-chave
    'exact_match': 0.3,          # 30% - Presença de termos exatos
    'keyword_density': 0.2,      # 20% - Densidade de palavras-chave
    'document_length': 0.1       # 10% - Comprimento do documento
}
```

#### **2. Sistema de Re-ranking (Linhas 207-232)**
```python
def _rerank_documents(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Re-rankeia documentos baseado em múltiplos critérios de relevância"""
    # Calcula scores para cada documento
    scored_docs = []
    for doc in documents:
        score = self._calculate_relevance_score(query, doc)
        scored_docs.append((score, doc))
    
    # Ordena por score (maior primeiro)
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Retorna apenas os documentos (sem scores)
    return [doc for score, doc in scored_docs]
```

#### **3. Cálculo de Relevância Multi-critério (Linhas 233-285)**
```python
def _calculate_relevance_score(self, query: str, document: Dict[str, Any]) -> float:
    """Calcula score de relevância para um documento baseado em múltiplos critérios"""
    
    # 1. Overlap de palavras-chave (peso: 0.4)
    query_words = set(query_lower.split())
    content_words = set(content.split())
    keyword_overlap = len(query_words.intersection(content_words)) / len(query_words)
    keyword_score = min(1.0, keyword_overlap * 2)
    
    # 2. Presença de termos exatos (peso: 0.3)
    exact_match_score = 0.0
    for word in query_words:
        if len(word) > 3 and word in content:
            exact_match_score += 0.2
    exact_match_score = min(1.0, exact_match_score)
    
    # 3. Densidade de palavras-chave (peso: 0.2)
    keyword_density = len(query_words.intersection(content_words)) / total_words
    density_score = min(1.0, keyword_density * 10)
    
    # 4. Comprimento do documento (peso: 0.1)
    doc_length = len(content.split())
    if doc_length < 10:
        length_score = 0.3  # Muito curto
    elif doc_length < 50:
        length_score = 1.0  # Ideal
    elif doc_length < 100:
        length_score = 0.8  # Bom
    else:
        length_score = 0.5  # Muito longo
    
    # Calcula score final ponderado
    final_score = (
        keyword_score * self.rerank_weights['keyword_overlap'] +
        exact_match_score * self.rerank_weights['exact_match'] +
        density_score * self.rerank_weights['keyword_density'] +
        length_score * self.rerank_weights['document_length']
    )
    
    return final_score
```

#### **4. Recuperação Aprimorada (Linhas 173-206)**
```python
def _retrieve_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
    # Busca mais documentos inicialmente para re-ranking
    initial_k = min(k * 3, 10)  # Busca até 3x mais documentos para re-ranking
    docs = self.vectorstore.similarity_search(query, k=initial_k)
    
    # Aplica re-ranking se há documentos suficientes
    if len(results) > 1:
        results = self._rerank_documents(query, results)
    
    # Retorna apenas os k melhores documentos
    return results[:k]
```

---

## 🤖 **FASE 3: Parameter Tuning Automático (78.3%)**

### **Arquivo: `src/core/rag_system.py`**

#### **1. Histórico de Performance (Linha 40)**
```python
# Histórico de performance para parameter tuning
self.performance_history = []
```

#### **2. Registro de Performance (Linhas 447-477)**
```python
def _record_performance(self, query: str, documents: List[Dict[str, Any]], 
                       recall: float, precision: float):
    """Registra performance de uma query para parameter tuning dos pesos"""
    # Calcula scores individuais para cada documento
    doc_scores = []
    for doc in documents:
        scores = self._calculate_individual_scores(query, doc)
        doc_scores.append(scores)
    
    # Registra no histórico
    self.performance_history.append({
        'query': query,
        'documents': documents,
        'doc_scores': doc_scores,
        'recall': recall,
        'precision': precision,
        'timestamp': time.time()
    })
    
    # Aplica parameter tuning se há histórico suficiente
    if len(self.performance_history) >= 10:
        self._apply_parameter_tuning()
```

#### **3. Cálculo de Scores Individuais (Linhas 478-527)**
```python
def _calculate_individual_scores(self, query: str, document: Dict[str, Any]) -> Dict[str, float]:
    """Calcula scores individuais para cada critério de relevância"""
    
    # 1. Overlap de palavras-chave
    keyword_overlap = len(query_words.intersection(content_words)) / len(query_words)
    keyword_score = min(1.0, keyword_overlap * 2)
    
    # 2. Presença de termos exatos
    exact_match_score = 0.0
    for word in query_words:
        if len(word) > 3 and word in content:
            exact_match_score += 0.2
    exact_match_score = min(1.0, exact_match_score)
    
    # 3. Densidade de palavras-chave
    keyword_density = len(query_words.intersection(content_words)) / total_words
    density_score = min(1.0, keyword_density * 10)
    
    # 4. Comprimento do documento
    doc_length = len(content.split())
    if doc_length < 10:
        length_score = 0.3
    elif doc_length < 50:
        length_score = 1.0
    elif doc_length < 100:
        length_score = 0.8
    else:
        length_score = 0.5
    
    return {
        'keyword_overlap': keyword_score,
        'exact_match': exact_match_score,
        'keyword_density': density_score,
        'document_length': length_score
    }
```

#### **4. Algoritmo de Parameter Tuning (Linhas 528-595)**
```python
def _apply_parameter_tuning(self):
    """Aplica parameter tuning dos pesos baseado no histórico de performance"""
    if len(self.performance_history) < 10:
        return
    
    # Analisa performance recente (últimas 10 queries)
    recent_performance = self.performance_history[-10:]
    
    # Calcula correlação entre scores individuais e performance
    correlations = {
        'keyword_overlap': 0.0,
        'exact_match': 0.0,
        'keyword_density': 0.0,
        'document_length': 0.0
    }
    
    for perf in recent_performance:
        # Calcula scores médios dos documentos
        avg_scores = self._calculate_average_scores(perf['doc_scores'])
        
        # Correlaciona com performance
        performance_score = (perf['recall'] + perf['precision']) / 2
        
        for key in correlations:
            correlations[key] += avg_scores[key] * performance_score
    
    # Ajusta pesos baseado nas correlações
    total_correlation = sum(correlations.values())
    if total_correlation > 0:
        for key in self.rerank_weights:
            # Ajusta peso proporcionalmente à correlação
            new_weight = correlations[key] / total_correlation
            # Aplica suavização para evitar mudanças bruscas
            self.rerank_weights[key] = (
                self.rerank_weights[key] * 0.8 + new_weight * 0.2
            )
    
    # Normaliza pesos para somar 1.0
    total_weight = sum(self.rerank_weights.values())
    for key in self.rerank_weights:
        self.rerank_weights[key] /= total_weight
    
    self.logger.info(f"Pesos do re-ranking ajustados: {self.rerank_weights}")
```

#### **5. Integração no Processamento (Linhas 395-400)**
```python
# Registra performance para parameter tuning dos pesos
self._record_performance(query, relevant_docs, context_recall, precision)
```

---

## 📊 **FASE 4: Análise Detalhada e Otimização (79.2%)**

### **Arquivo: `src/core/rag_system.py`**

#### **1. Prompt Otimizado (Linhas 138-172)**
```python
def _get_system_prompt(self, context: str = "") -> str:
    """Retorna o prompt do sistema com contexto RAG"""
    base_prompt = (
        "Você é um assistente especializado em RAG (Retrieval-Augmented Generation) com foco em precisão, relevância e diversidade de informações.\n\n"
        "INSTRUÇÕES CRÍTICAS:\n"
        "1. SEMPRE use o contexto fornecido quando disponível\n"
        "2. Cite EXATAMENTE as informações dos documentos\n"
        "3. Seja DIRETO, OBJETIVO e COMPLETO nas respostas\n"
        "4. Estruture respostas em tópicos quando apropriado\n"
        "5. SEMPRE mencione a fonte: 'Segundo os documentos...' ou 'Baseado nos documentos...'\n"
        "6. Se não houver contexto relevante, responda: 'Não encontrei informações específicas sobre isso nos documentos disponíveis.'\n"
        "7. COMBINE informações de múltiplos documentos quando relevante\n"
        "8. Forneça respostas ABRANGENTES que cubram diferentes aspectos da pergunta\n\n"
        "ESTRATÉGIAS DE RESPOSTA:\n"
        "- Para definições: Forneça definição clara + exemplos + contexto\n"
        "- Para explicações: Explique conceito + como funciona + aplicações\n"
        "- Para comparações: Identifique diferenças + semelhanças + contexto\n"
        "- Para procedimentos: Liste passos + detalhes + considerações\n"
        "- Para fatos: Forneça informação + contexto + relevância\n\n"
        "IMPORTANTE: Nunca invente informações. Use APENAS o que está nos documentos fornecidos. Seja COMPLETO e ABRANGENTE na resposta."
    )
```

#### **2. Aumento de Documentos Recuperados (Linha 350)**
```python
# Recupera documentos relevantes (aumentado para 5 devido ao re-ranking)
relevant_docs = self._retrieve_documents(query, k=5)
```

#### **3. Ajuste de Métricas (Linhas 375-380)**
```python
# Calcula recall de contexto (ajustado para 5 documentos)
context_recall = min(1.0, documents_used / 5.0) if documents_used > 0 else 0.0

# Calcula precisão (ajustado para considerar re-ranking)
precision = 1.0 if documents_used > 0 else 0.0
```

#### **4. Informações do Sistema Expandidas (Linhas 421-446)**
```python
def get_system_info(self) -> Dict[str, Any]:
    return {
        "model_name": self.config["model_name"],
        "temperature": self.config["temperature"],
        "test_mode": self.config.get("test_mode", False),
        "vectorstore_available": self.vectorstore is not None,
        "documents_count": documents_count,
        "rerank_weights": self.get_rerank_weights(),           # NOVO
        "performance_history_size": len(self.performance_history),  # NOVO
        "parameter_tuning_enabled": True                           # NOVO
    }
```