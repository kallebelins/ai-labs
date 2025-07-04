#!/usr/bin/env python3
"""
Sistema RAG Simplificado.

Este módulo implementa um sistema RAG funcional com recursos essenciais:
- Re-ranking semântico com Cross-Encoder
- Query expansion usando LLM
- Busca vetorial com ChromaDB
- Chunking inteligente

Author: AI Labs
Version: 3.0.0 (Simplificado)
"""

import time
import logging
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder

@dataclass
class QueryContext:
    """Contexto da query para prompt engineering dinâmico."""
    query_type: str
    complexity: str
    domain: str
    user_intent: str

class RAGSystem:
    """Sistema RAG simplificado com recursos essenciais."""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """
        Inicializa o sistema RAG simplificado.
        
        Args:
            config: Configurações do sistema
            logger: Logger opcional
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        
        # Inicializa componentes essenciais
        self._setup_components()
        
        # Histórico simples para feedback
        self.feedback_history = []
        self.query_patterns = defaultdict(int)
        self.successful_queries = []
        
        self.logger.info("Sistema RAG Simplificado inicializado")
    
    def _setup_components(self):
        """Configura componentes essenciais do sistema"""
        
        # 1. Re-ranking semântico com Cross-Encoder
        try:
            self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            self.logger.info("Cross-Encoder carregado para re-ranking semântico")
        except Exception as e:
            self.logger.warning(f"Cross-Encoder não disponível: {e}")
            self.cross_encoder = None
        
        # 2. LLM para query expansion
        self.llm = ChatOpenAI(
            model=self.config["model_name"],
            temperature=self.config.get("temperature", 0.3),
            api_key=self.config["openai_api_key"]
        )
        
        # 3. Embeddings para busca vetorial
        self.embeddings = OpenAIEmbeddings()
        
        # 4. Text splitter otimizado
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.get("chunk_size", 300),
            chunk_overlap=self.config.get("chunk_overlap", 100),
            separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
        )
        
        # 5. Configura vetorstore
        self._setup_vectorstore()
        
        # 6. Prompt templates
        self._setup_prompt_templates()
    
    def _setup_vectorstore(self):
        """Configura vetorstore simples"""
        try:
            if self.config.get("test_mode", False):
                self.logger.info("Modo de teste - usando documentos simulados")
                self.vectorstore = None
                self._test_documents = self._load_test_documents()
                return
            
            persist_directory = Path("data/chroma_db")
            persist_directory.mkdir(parents=True, exist_ok=True)
            
            self.vectorstore = Chroma(
                persist_directory=str(persist_directory),
                embedding_function=self.embeddings,
                collection_name="rag_documents"
            )
            
            self.logger.info("Vetorstore configurado")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar vetorstore: {e}")
            self.vectorstore = None
            self._test_documents = self._load_test_documents()
    
    def _setup_prompt_templates(self):
        """Configura templates de prompt dinâmicos"""
        self.prompt_templates = {
            "definition": ChatPromptTemplate.from_template(
                "Baseado no contexto a seguir, forneça uma definição clara e precisa:\n\n"
                "Contexto: {context}\n\n"
                "Pergunta: {question}\n\n"
                "Definição:"
            ),
            "explanation": ChatPromptTemplate.from_template(
                "Usando o contexto fornecido, explique de forma didática e detalhada:\n\n"
                "Contexto: {context}\n\n"
                "Pergunta: {question}\n\n"
                "Explicação:"
            ),
            "general": ChatPromptTemplate.from_template(
                "Com base no contexto a seguir, responda à pergunta de forma completa e precisa:\n\n"
                "Contexto: {context}\n\n"
                "Pergunta: {question}\n\n"
                "Resposta:"
            )
        }
    
    def _load_test_documents(self) -> List[Document]:
        """Carrega documentos de teste simplificados"""
        test_docs = [
            "Inteligência Artificial (IA) é uma área da ciência da computação que se concentra na criação de sistemas capazes de realizar tarefas que normalmente requerem inteligência humana.",
            "Machine Learning é um subcampo da IA que permite que computadores aprendam e melhorem automaticamente através da experiência sem serem explicitamente programados.",
            "Deep Learning é uma técnica de machine learning baseada em redes neurais artificiais com múltiplas camadas.",
            "RAG (Retrieval-Augmented Generation) é uma técnica que combina recuperação de informações com geração de texto usando modelos de linguagem.",
            "LangChain é um framework para desenvolvimento de aplicações com modelos de linguagem que facilita a criação de sistemas RAG.",
            "ChromaDB é um banco de dados vetorial open-source projetado para aplicações de IA que trabalha com embeddings.",
            "Embeddings são representações vetoriais de texto que capturam significado semântico em um espaço multidimensional.",
            "OpenAI é uma empresa de pesquisa em IA que desenvolveu modelos como GPT-3, GPT-4 e DALL-E."
        ]
        
        documents = []
        for i, content in enumerate(test_docs):
            doc = Document(
                page_content=content,
                metadata={"source": f"test_doc_{i}", "type": "definition"}
            )
            documents.append(doc)
        
        return documents
    
    def _analyze_query_context(self, query: str) -> QueryContext:
        """Analisa contexto da query para prompt dinâmico"""
        query_lower = query.lower()
        
        # Determina tipo da query
        if any(word in query_lower for word in ["o que é", "defin", "signific"]):
            query_type = "definition"
        elif any(word in query_lower for word in ["explique", "como funciona"]):
            query_type = "explanation"
        else:
            query_type = "general"
        
        # Determina complexidade
        word_count = len(query.split())
        if word_count <= 4:
            complexity = "simple"
        elif word_count <= 8:
            complexity = "medium"
        else:
            complexity = "complex"
        
        # Determina domínio
        tech_terms = ["ia", "ai", "machine learning", "deep learning", "rag", "llm"]
        if any(term in query_lower for term in tech_terms):
            domain = "technical"
        else:
            domain = "general"
        
        return QueryContext(
            query_type=query_type,
            complexity=complexity,
            domain=domain,
            user_intent="learn"
        )
    
    def _expand_query(self, query: str) -> List[str]:
        """Expansão simples de query"""
        if not self.config.get("use_query_expansion", True):
            return [query]
        
        try:
            expansion_prompt = f"""
            Gere {self.config.get('expansion_count', 3)} variações da seguinte pergunta, mantendo o mesmo significado:

            Pergunta original: {query}

            Variações:
            """
            
            response = self.llm.invoke(expansion_prompt)
            expanded_queries = [query]  # Inclui query original
            
            # Extrai variações da resposta
            content = response.content
            if isinstance(content, list):
                content = ' '.join(str(item) for item in content)
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Pergunta') and not line.startswith('Variações'):
                    # Remove numeração se houver
                    cleaned_line = re.sub(r'^\d+[.)]\s*', '', line)
                    if cleaned_line and cleaned_line != query:
                        expanded_queries.append(cleaned_line)
            
            self.logger.info(f"Query expandida de '{query}' para {len(expanded_queries)} variações")
            return expanded_queries[:self.config.get('expansion_count', 3) + 1]
            
        except Exception as e:
            self.logger.error(f"Erro na expansão de query: {e}")
            return [query]
    
    def _calculate_similarity_scores(self, query: str, documents: List[Document]) -> List[float]:
        """Calcula scores de similaridade reais para os documentos"""
        if not documents:
            return []
        
        try:
            # Usa cross-encoder se disponível (mais preciso)
            if self.cross_encoder:
                pairs = [(query, doc.page_content) for doc in documents]
                scores = self.cross_encoder.predict(pairs)
                # Normaliza scores para 0-1 e converte para float Python
                scores = [float((score + 1) / 2) for score in scores]  # Cross-encoder retorna -1 a 1
                return scores
            
            # Fallback: similaridade baseada em sobreposição de palavras
            query_words = set(query.lower().split())
            scores = []
            
            for doc in documents:
                doc_words = set(doc.page_content.lower().split())
                if not query_words or not doc_words:
                    scores.append(0.0)
                    continue
                
                # Jaccard similarity
                intersection = len(query_words.intersection(doc_words))
                union = len(query_words.union(doc_words))
                similarity = intersection / union if union > 0 else 0.0
                scores.append(similarity)
            
            return scores
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular similaridade: {e}")
            return [0.5] * len(documents)  # Fallback conservador
    
    def _calculate_context_recall(self, query: str, documents: List[Document], scores: List[float]) -> float:
        """Calcula context recall real baseado na relevância dos documentos"""
        if not documents or not scores:
            return 0.0
        
        # Context recall = proporção de documentos relevantes encontrados
        relevance_threshold = self.config.get("similarity_threshold", 0.15)
        relevant_docs = sum(1 for score in scores if score >= relevance_threshold)
        
        # Assumindo que o sistema deveria encontrar pelo menos 1 documento relevante
        # para queries técnicas e pelo menos 1 para queries gerais
        expected_relevant = 1
        
        # Para queries técnicas, esperamos mais documentos relevantes
        query_lower = query.lower()
        tech_terms = ["ia", "ai", "machine learning", "deep learning", "rag", "llm", "embedding"]
        if any(term in query_lower for term in tech_terms):
            expected_relevant = min(2, len(documents))
        
        return min(relevant_docs / expected_relevant, 1.0)
    
    def _calculate_precision(self, query: str, documents: List[Document], scores: List[float]) -> float:
        """Calcula precision real baseada na qualidade dos documentos retornados"""
        if not documents or not scores:
            return 0.0
        
        # Precision = proporção de documentos retornados que são relevantes
        relevance_threshold = self.config.get("similarity_threshold", 0.15)
        relevant_docs = sum(1 for score in scores if score >= relevance_threshold)
        
        return relevant_docs / len(documents)
    
    def _retrieve_documents_with_similarity(self, queries: List[str]) -> Tuple[List[Document], List[float]]:
        """Busca documentos com scores de similaridade reais"""
        all_docs = []
        all_scores = []
        
        if self.vectorstore:
            # Busca real no vectorstore
            for query in queries:
                docs = self.vectorstore.similarity_search(
                    query, 
                    k=self.config.get("vectorstore_search_k", 5)
                )
                all_docs.extend(docs)
            
            # Remove duplicatas
            unique_docs = []
            seen_content = set()
            for doc in all_docs:
                if doc.page_content not in seen_content:
                    unique_docs.append(doc)
                    seen_content.add(doc.page_content)
            
            # Calcula scores reais para documentos únicos
            primary_query = queries[0]  # Usa query principal para scoring
            final_docs = unique_docs[:self.config.get("vectorstore_search_k", 5)]
            final_scores = self._calculate_similarity_scores(primary_query, final_docs)
            
            return final_docs, final_scores
        
        else:
            # Modo de teste: busca por similaridade real nos documentos de teste
            primary_query = queries[0]
            test_docs = self._test_documents
            
            # Calcula similaridade para todos os documentos de teste
            all_scores = self._calculate_similarity_scores(primary_query, test_docs)
            
            # Filtra documentos com similaridade acima do threshold
            threshold = self.config.get("similarity_threshold", 0.15)
            relevant_docs = []
            relevant_scores = []
            
            for doc, score in zip(test_docs, all_scores):
                if score >= threshold:
                    relevant_docs.append(doc)
                    relevant_scores.append(score)
            
            # Ordena por score e pega os top K
            if relevant_docs:
                doc_score_pairs = list(zip(relevant_docs, relevant_scores))
                doc_score_pairs.sort(key=lambda x: x[1], reverse=True)
                
                k = self.config.get("vectorstore_search_k", 5)
                final_docs = [doc for doc, score in doc_score_pairs[:k]]
                final_scores = [score for doc, score in doc_score_pairs[:k]]
            else:
                # Se nenhum documento relevante, retorna o mais similar
                if all_scores:
                    best_idx = max(range(len(all_scores)), key=lambda i: all_scores[i])
                    final_docs = [test_docs[best_idx]]
                    final_scores = [all_scores[best_idx]]
                else:
                    final_docs = []
                    final_scores = []
            
            return final_docs, final_scores

    def _retrieve_documents(self, queries: List[str]) -> List[Document]:
        """Busca documentos usando queries expandidas"""
        documents, _ = self._retrieve_documents_with_similarity(queries)
        return documents
    
    def _rerank_documents(self, query: str, documents: List[Document]) -> Tuple[List[Document], List[float]]:
        """Re-ranking semântico dos documentos com scores reais"""
        if not documents:
            return documents, []
        
        if not self.cross_encoder:
            # Sem cross-encoder, usa scores de similaridade básicos
            scores = self._calculate_similarity_scores(query, documents)
            doc_scores = list(zip(documents, scores))
            doc_scores.sort(key=lambda x: x[1], reverse=True)
            return [doc for doc, score in doc_scores], [score for doc, score in doc_scores]
        
        try:
            # Prepara pares query-documento
            pairs = [(query, doc.page_content) for doc in documents]
            
            # Calcula scores de re-ranking
            raw_scores = self.cross_encoder.predict(pairs)
            # Normaliza scores para 0-1 e converte para float Python
            scores = [float((score + 1) / 2) for score in raw_scores]
            
            # Ordena documentos por score
            doc_scores = list(zip(documents, scores))
            doc_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [doc for doc, score in doc_scores], [score for doc, score in doc_scores]
        
        except Exception as e:
            self.logger.error(f"Erro no re-ranking: {e}")
            scores = self._calculate_similarity_scores(query, documents)
            return documents, scores

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processa uma query usando o sistema RAG simplificado.
        
        Args:
            query: Query do usuário
            
        Returns:
            Dict com resultado do processamento
        """
        start_time = time.time()
        
        try:
            # Analisa contexto da query
            query_context = self._analyze_query_context(query)
            
            # Expande query
            expanded_queries = self._expand_query(query)
            
            # Busca documentos com scores reais
            documents, similarity_scores = self._retrieve_documents_with_similarity(expanded_queries)
            
            # Re-ranking semântico com scores reais
            if self.config.get("use_semantic_reranking", True) and documents:
                documents, final_scores = self._rerank_documents(query, documents)
            else:
                final_scores = similarity_scores
            
            # Calcula métricas REAIS
            context_recall = self._calculate_context_recall(query, documents, final_scores)
            precision = self._calculate_precision(query, documents, final_scores)
            
            if documents:
                # Combina contexto dos documentos
                context = "\n\n".join([doc.page_content for doc in documents])
                
                # Seleciona template de prompt
                template_type = query_context.query_type
                if template_type not in self.prompt_templates:
                    template_type = "general"
                
                prompt = self.prompt_templates[template_type]
                
                # Gera resposta
                response = self.llm.invoke(
                    prompt.format(context=context, question=query)
                )
                
                answer = response.content
                documents_used = len(documents)
            else:
                # Resposta sem contexto
                answer = f"Não encontrei informações relevantes sobre '{query}' na base de conhecimento."
                context = ""
                documents_used = 0
            
            response_time = time.time() - start_time
            
            # Registra padrão da query
            self.query_patterns[query_context.query_type] += 1
            
            result = {
                "success": True,
                "query": query,
                "answer": answer,
                "context": context,
                "response_time": response_time,
                "documents_used": documents_used,
                "context_recall": context_recall,
                "precision": precision,
                "expanded_queries": expanded_queries,
                "query_context": query_context.__dict__,
                "documents": [{"content": doc.page_content, "metadata": doc.metadata} for doc in documents],
                "document_scores": final_scores[:len(documents)]  # Scores REAIS
            }
            
            self.successful_queries.append(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao processar query: {e}")
            return {
                "success": False,
                "query": query,
                "error_message": str(e),
                "response_time": time.time() - start_time,
                "context_recall": 0.0,
                "precision": 0.0,
                "documents_used": 0
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações do sistema"""
        return {
            "model_name": self.config["model_name"],
            "temperature": self.config.get("temperature", 0.3),
            "test_mode": self.config.get("test_mode", False),
            "vectorstore_available": self.vectorstore is not None,
            "cross_encoder_available": self.cross_encoder is not None,
            "documents_count": len(self._test_documents) if hasattr(self, '_test_documents') else 0,
            "feedback_history_size": len(self.feedback_history),
            "advanced_features": {
                "query_expansion": self.config.get("use_query_expansion", True),
                "semantic_reranking": self.config.get("use_semantic_reranking", True),
                "dynamic_prompts": True,
                "embedding_cache": self.config.get("embedding_cache_enabled", True)
            }
        } 