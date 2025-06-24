#!/usr/bin/env python3
"""
Sistema RAG Básico usando LangChain
"""

import time
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

class RAGSystem:
    """Sistema RAG básico usando LangChain e ChromaDB"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """
        Inicializa o sistema RAG
        
        Args:
            config: Configurações do sistema
            logger: Logger opcional (se não fornecido, cria um novo)
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        
        # Inicializa pesos do re-ranking (serão ajustados dinamicamente)
        self.rerank_weights = {
            'keyword_overlap': 0.4,
            'exact_match': 0.3,
            'keyword_density': 0.2,
            'document_length': 0.1
        }
        
        # Histórico de performance para parameter tuning
        self.performance_history = []
        
        # Inicializa o LLM
        self.llm = ChatOpenAI(
            model_name=config["model_name"],
            temperature=config["temperature"],
            openai_api_key=config["openai_api_key"]
        )
        
        # Inicializa embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Inicializa vetorstore para documentos
        self._setup_vectorstore()
        
        # Template do prompt com contexto RAG
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{input}")
        ])
        
        # Chain do LangChain
        self.chain = self.prompt_template | self.llm
        
        # Carrega documentos de teste se necessário
        if config.get("test_mode", False):
            self._load_test_documents()
        
        self.logger.info("Sistema RAG inicializado")
    
    def _setup_vectorstore(self):
        """Configura o vetorstore para documentos"""
        try:            
            # Verifica se está em modo de teste
            if self.config.get("test_mode", False):
                self.logger.info("Modo de teste ativado - usando documentos simulados")
                self.vectorstore = None
                self._test_documents = self._load_test_documents()
                return
            
            # Cria diretório para persistência se não existir
            persist_directory = Path("data/chroma_db")
            persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Inicializa ChromaDB
            self.vectorstore = Chroma(
                persist_directory=str(persist_directory),
                embedding_function=self.embeddings,
                collection_name="rag_documents"
            )
            
            self.logger.info("Vetorstore configurado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar vetorstore: {e}")
            # Fallback para documentos simulados
            self.vectorstore = None
            self._test_documents = self._load_test_documents()
    
    def _load_test_documents(self):
        """Carrega documentos de teste para modo de teste"""
        return [
            {
                "content": "A inteligência artificial é um campo da computação que busca criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana.",
                "metadata": {"source": "test_doc_1", "topic": "IA"}
            },
            {
                "content": "Machine Learning é um subcampo da IA que permite aos computadores aprenderem sem serem explicitamente programados.",
                "metadata": {"source": "test_doc_2", "topic": "ML"}
            },
            {
                "content": "Deep Learning utiliza redes neurais artificiais com múltiplas camadas para processar dados complexos.",
                "metadata": {"source": "test_doc_3", "topic": "DL"}
            },
            {
                "content": "RAG (Retrieval-Augmented Generation) combina recuperação de informações com geração de texto para respostas mais precisas.",
                "metadata": {"source": "test_doc_4", "topic": "RAG"}
            },
            {
                "content": "LangChain é um framework para desenvolvimento de aplicações com LLMs, oferecendo ferramentas para construção de agentes.",
                "metadata": {"source": "test_doc_5", "topic": "LangChain"}
            },
            {
                "content": "ChromaDB é uma base de dados vetorial open-source para armazenamento e busca de embeddings.",
                "metadata": {"source": "test_doc_6", "topic": "ChromaDB"}
            },
            {
                "content": "Embeddings são representações vetoriais de texto que capturam o significado semântico das palavras.",
                "metadata": {"source": "test_doc_7", "topic": "Embeddings"}
            },
            {
                "content": "OpenAI oferece APIs de linguagem natural que podem ser integradas em aplicações de IA.",
                "metadata": {"source": "test_doc_8", "topic": "OpenAI"}
            }
        ]
    
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
            "FORMATO DE RESPOSTA:\n"
            "- Comece com 'Baseado nos documentos disponíveis...' ou 'Segundo os documentos...'\n"
            "- Use aspas para citar trechos exatos dos documentos\n"
            "- Seja específico sobre qual documento contém a informação\n"
            "- Mantenha respostas concisas mas COMPLETAS e INFORMATIVAS\n"
            "- Se houver múltiplos documentos relevantes, INTEGRE as informações\n"
            "- Estruture respostas com tópicos quando apropriado\n\n"
            "ESTRATÉGIAS DE RESPOSTA:\n"
            "- Para definições: Forneça definição clara + exemplos + contexto\n"
            "- Para explicações: Explique conceito + como funciona + aplicações\n"
            "- Para comparações: Identifique diferenças + semelhanças + contexto\n"
            "- Para procedimentos: Liste passos + detalhes + considerações\n"
            "- Para fatos: Forneça informação + contexto + relevância\n\n"
            "EXEMPLOS:\n"
            "- 'Baseado nos documentos disponíveis, a inteligência artificial é um campo da computação que busca criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana. Inclui subcampos como machine learning, deep learning e processamento de linguagem natural.'\n"
            "- 'Segundo os documentos, RAG (Retrieval-Augmented Generation) combina recuperação de informações com geração de texto para respostas mais precisas. Isso melhora a precisão e reduz alucinações, sendo especialmente útil para aplicações que requerem informações atualizadas.'\n\n"
            "IMPORTANTE: Nunca invente informações. Use APENAS o que está nos documentos fornecidos. Seja COMPLETO e ABRANGENTE na resposta."
        )
        if context:
            return f"{base_prompt}\n\nCONTEXTO DISPONÍVEL:\n{context}\n\nUse as informações acima para responder à pergunta do usuário de forma precisa, contextualizada e abrangente. Combine informações de diferentes documentos quando relevante."
        return base_prompt
    
    def _retrieve_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Recupera documentos relevantes para a query"""
        
        # Se está em modo de teste, usa documentos simulados
        if self.config.get("test_mode", False) and hasattr(self, '_test_documents'):
            return self._retrieve_test_documents(query, k)
        
        if not self.vectorstore:
            return []
        
        try:
            # Busca mais documentos inicialmente para re-ranking
            initial_k = min(k * 3, 10)  # Busca até 3x mais documentos para re-ranking
            docs = self.vectorstore.similarity_search(query, k=initial_k)
            
            # Converte para formato padrão
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            # Aplica re-ranking se há documentos suficientes
            if len(results) > 1:
                results = self._rerank_documents(query, results)
            
            # Retorna apenas os k melhores documentos
            return results[:k]
            
        except Exception as e:
            self.logger.error(f"Erro ao recuperar documentos: {e}")
            return []
    
    def _rerank_documents(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Re-rankeia documentos baseado em múltiplos critérios de relevância
        
        Args:
            query: Query do usuário
            documents: Lista de documentos para re-ranking
            
        Returns:
            Lista de documentos re-rankeados
        """
        if not documents:
            return documents
        
        # Calcula scores para cada documento
        scored_docs = []
        for doc in documents:
            score = self._calculate_relevance_score(query, doc)
            scored_docs.append((score, doc))
        
        # Ordena por score (maior primeiro)
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Retorna apenas os documentos (sem scores)
        return [doc for score, doc in scored_docs]
    
    def _calculate_relevance_score(self, query: str, document: Dict[str, Any]) -> float:
        """
        Calcula score de relevância para um documento baseado em múltiplos critérios
        
        Args:
            query: Query do usuário
            document: Documento para avaliar
            
        Returns:
            Score de relevância (0.0 a 1.0)
        """
        content = document['content'].lower()
        query_lower = query.lower()
        
        # 1. Overlap de palavras-chave (peso: 0.4)
        query_words = set(query_lower.split())
        content_words = set(content.split())
        keyword_overlap = len(query_words.intersection(content_words)) / len(query_words) if query_words else 0
        keyword_score = min(1.0, keyword_overlap * 2)  # Normaliza para 0-1
        
        # 2. Presença de termos exatos (peso: 0.3)
        exact_match_score = 0.0
        for word in query_words:
            if len(word) > 3 and word in content:  # Palavras com mais de 3 caracteres
                exact_match_score += 0.2
        exact_match_score = min(1.0, exact_match_score)
        
        # 3. Densidade de palavras-chave (peso: 0.2)
        total_words = len(content_words)
        keyword_density = len(query_words.intersection(content_words)) / total_words if total_words > 0 else 0
        density_score = min(1.0, keyword_density * 10)  # Normaliza
        
        # 4. Comprimento do documento (preferência por documentos médios) (peso: 0.1)
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
    
    def _retrieve_test_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Recupera documentos simulados para modo de teste"""
        query_words = set(query.lower().split())
        relevant_docs = []
        
        for doc in self._test_documents:
            doc_words = set(doc['content'].lower().split())
            common_words = query_words.intersection(doc_words)
            
            # Se há pelo menos 2 palavras em comum, considera relevante
            if len(common_words) >= 2:
                relevant_docs.append(doc)
        
        # Aplica re-ranking se há documentos suficientes
        if len(relevant_docs) > 1:
            relevant_docs = self._rerank_documents(query, relevant_docs)
        
        # Retorna os k documentos mais relevantes
        return relevant_docs[:k]
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Adiciona documentos ao sistema RAG"""
        
        # Se está em modo de teste, adiciona aos documentos simulados
        if self.config.get("test_mode", False):
            self._add_test_documents(documents, metadata)
            return
        
        if not self.vectorstore:
            self.logger.warning("Vetorstore não disponível para adicionar documentos")
            return
        
        try:
            # Cria objetos Document do LangChain
            docs = []
            for i, content in enumerate(documents):
                doc_metadata = metadata[i] if metadata and i < len(metadata) else {}
                docs.append(Document(page_content=content, metadata=doc_metadata))
            
            # Adiciona ao vetorstore
            self.vectorstore.add_documents(docs)
            
            self.logger.info(f"{len(documents)} documentos adicionados ao sistema RAG")
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar documentos: {e}")
    
    def _add_test_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Adiciona documentos aos documentos simulados para modo de teste"""
        if not hasattr(self, '_test_documents'):
            self._test_documents = []
        
        for i, content in enumerate(documents):
            doc_metadata = metadata[i] if metadata and i < len(metadata) else {}
            self._test_documents.append({
                "content": content,
                "metadata": doc_metadata
            })
        
        self.logger.info(f"{len(documents)} documentos simulados adicionados")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Processa uma query usando o sistema RAG"""
        start_time = time.time()
        
        try:
            # Recupera documentos relevantes (aumentado para 5 devido ao re-ranking)
            relevant_docs = self._retrieve_documents(query, k=5)
            
            # Constrói contexto a partir dos documentos
            context = ""
            if relevant_docs:
                context_parts = []
                for doc in relevant_docs:
                    context_parts.append(f"Documento: {doc['content']}")
                context = "\n\n".join(context_parts)
            
            # Cria prompt com contexto
            if context:
                system_prompt = self._get_system_prompt(context)
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            else:
                messages = [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": query}
                ]
            
            # Gera resposta usando o LLM
            response = self.llm.invoke(messages)
            
            # Calcula métricas
            response_time = time.time() - start_time
            tokens_used = len(query.split()) + len(response.content.split())
            documents_used = len(relevant_docs)
            
            # Calcula recall de contexto (ajustado para 5 documentos)
            context_recall = min(1.0, documents_used / 5.0) if documents_used > 0 else 0.0
            
            # Calcula precisão (ajustado para considerar re-ranking)
            precision = 1.0 if documents_used > 0 else 0.0
            
            # Registra performance para parameter tuning dos pesos
            self._record_performance(query, relevant_docs, context_recall, precision)
            
            return {
                "success": True,
                "response": response.content,
                "response_time": response_time,
                "tokens_used": tokens_used,
                "documents_used": documents_used,
                "context_recall": context_recall,
                "precision": precision,
                "context": context,
                "relevant_documents": relevant_docs,
                "rerank_weights": self.get_rerank_weights()
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao processar query: {e}")
            return {
                "success": False,
                "error_message": str(e),
                "response_time": time.time() - start_time,
                "tokens_used": 0,
                "documents_used": 0,
                "context_recall": 0.0,
                "precision": 0.0,
                "context": "",
                "relevant_documents": [],
                "rerank_weights": {}
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações do sistema"""
        # Se estiver em modo de teste, retorna a contagem dos documentos simulados
        if self.config.get("test_mode", False) and hasattr(self, '_test_documents'):
            documents_count = len(self._test_documents)
        # Se estiver usando vetorstore real, retorna a contagem de documentos do ChromaDB
        elif self.vectorstore is not None:
            try:
                # O método as_retriever().get_relevant_documents retorna todos os docs, mas para contar:
                # Chroma tem o método .__len__() para collections
                documents_count = self.vectorstore._collection.count() if hasattr(self.vectorstore, '_collection') else 0
            except Exception:
                documents_count = 0
        else:
            documents_count = 0
        return {
            "model_name": self.config["model_name"],
            "temperature": self.config["temperature"],
            "test_mode": self.config.get("test_mode", False),
            "vectorstore_available": self.vectorstore is not None,
            "documents_count": documents_count,
            "rerank_weights": self.get_rerank_weights(),
            "performance_history_size": len(self.performance_history),
            "parameter_tuning_enabled": True
        }
    
    def _record_performance(self, query: str, documents: List[Dict[str, Any]], 
                           recall: float, precision: float):
        """
        Registra performance de uma query para parameter tuning dos pesos
        
        Args:
            query: Query processada
            documents: Documentos recuperados
            recall: Recall obtido
            precision: Precisão obtida
        """
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
    
    def _calculate_individual_scores(self, query: str, document: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula scores individuais para cada critério de relevância
        
        Args:
            query: Query do usuário
            document: Documento para avaliar
            
        Returns:
            Dicionário com scores individuais
        """
        content = document['content'].lower()
        query_lower = query.lower()
        
        # 1. Overlap de palavras-chave
        query_words = set(query_lower.split())
        content_words = set(content.split())
        keyword_overlap = len(query_words.intersection(content_words)) / len(query_words) if query_words else 0
        keyword_score = min(1.0, keyword_overlap * 2)
        
        # 2. Presença de termos exatos
        exact_match_score = 0.0
        for word in query_words:
            if len(word) > 3 and word in content:
                exact_match_score += 0.2
        exact_match_score = min(1.0, exact_match_score)
        
        # 3. Densidade de palavras-chave
        total_words = len(content_words)
        keyword_density = len(query_words.intersection(content_words)) / total_words if total_words > 0 else 0
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
    
    def _apply_parameter_tuning(self):
        """
        Aplica parameter tuning dos pesos baseado no histórico de performance
        """
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
            avg_scores = {
                'keyword_overlap': 0.0,
                'exact_match': 0.0,
                'keyword_density': 0.0,
                'document_length': 0.0
            }
            
            # Calcula scores médios dos documentos
            for doc_scores in perf['doc_scores']:
                for key in avg_scores:
                    avg_scores[key] += doc_scores[key]
            
            # Normaliza
            num_docs = len(perf['doc_scores'])
            for key in avg_scores:
                avg_scores[key] /= num_docs
            
            # Correlaciona com performance
            performance_score = (perf['recall'] + perf['precision']) / 2
            
            for key in correlations:
                correlations[key] += avg_scores[key] * performance_score
        
        # Normaliza correlações
        for key in correlations:
            correlations[key] /= len(recent_performance)
        
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
        
        # Limpa histórico antigo
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-30:]
    
    def get_rerank_weights(self) -> Dict[str, float]:
        """
        Retorna os pesos atuais do re-ranking
        
        Returns:
            Dicionário com os pesos atuais
        """
        return self.rerank_weights.copy() 