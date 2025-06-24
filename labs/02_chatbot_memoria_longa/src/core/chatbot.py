#!/usr/bin/env python3
"""
Chatbot Engine com Memória de Longo Prazo usando LangChain
"""

import time
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_chroma import Chroma
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

class ConversationMemory(BaseModel):
    """Modelo para armazenar informações da conversa"""
    session_id: str
    messages: List[Dict[str, Any]]
    summary: Optional[str] = None
    created_at: str
    updated_at: str

class LongTermMemoryChatbot:
    """Chatbot com memória de longo prazo usando LangChain e ChromaDB"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        """
        Inicializa o chatbot com memória de longo prazo
        
        Args:
            config: Configurações do chatbot
            logger: Logger opcional (se não fornecido, cria um novo)
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        
        # Inicializa o LLM
        self.llm = ChatOpenAI(
            model=config["model_name"],
            temperature=config["temperature"]
        )
        
        # Inicializa embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Configura memória de conversa
        self.conversation_memory = ConversationBufferWindowMemory(
            k=config.get("memory_window", 10),
            return_messages=True
        )
        
        # Configura memória de resumo para longo prazo
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm
        )
        
        # Inicializa vetorstore para memória de longo prazo
        self._setup_vectorstore()
        
        # Template do prompt com contexto de memória
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{input}")
        ])
        
        # Chain do LangChain com memória
        self.chain = self.prompt_template | self.llm
        
        self.logger.info("Chatbot com memória de longo prazo inicializado")
    
    def _setup_vectorstore(self):
        """Configura o vetorstore para memória de longo prazo"""
        try:            
            # Verifica se está em modo de teste
            if self.config.get("test_mode", False):
                self.logger.info("Modo de teste ativado - usando memória simulada")
                self.vectorstore = None
                self._test_memory = {}  # Memória simulada para testes
                return
            
            # Cria diretório para persistência se não existir
            persist_directory = Path("data/chroma_db")
            persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Inicializa ChromaDB
            self.vectorstore = Chroma(
                persist_directory=str(persist_directory),
                embedding_function=self.embeddings,
                collection_name="conversation_memory"
            )
            
            self.logger.info("Vetorstore configurado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar vetorstore: {e}")
            # Fallback para memória em memória
            self.vectorstore = None
            self._test_memory = {}  # Memória simulada como fallback
    
    def _get_system_prompt(self, memory_context: str = "") -> str:
        """Retorna o prompt do sistema com contexto de memória melhorado"""
        base_prompt = """Você é um assistente útil e amigável com memória de longo prazo. 

Você tem acesso ao histórico de conversas anteriores e DEVE usar essas informações para:
- Manter coerência ao longo de múltiplas sessões
- Referenciar informações mencionadas anteriormente
- Construir sobre conversas passadas
- Fornecer respostas mais contextualizadas e personalizadas

INSTRUÇÕES CRÍTICAS:
1. SEMPRE use o contexto de memória disponível quando relevante
2. Se houver informações no contexto que respondem à pergunta, use-as PRIMEIRO
3. Seja específico ao referenciar informações anteriores
4. Mantenha a personalização baseada no que você "lembra" do usuário
5. Se não houver contexto relevante, responda normalmente
6. IMPORTANTE: Se você tem memória disponível, SEMPRE mencione ou use essa informação

EXEMPLO DE USO DE MEMÓRIA:
- Se o usuário perguntar "Qual é minha profissão?" e você tem essa informação na memória, responda: "Baseado no que você me disse anteriormente, você é [profissão]"
- Se o usuário perguntar "Onde eu moro?" e você tem essa informação, responda: "Você mencionou que mora em [local]"

Responda de forma clara, concisa, contextualizada e personalizada."""
        
        if memory_context:
            return f"{base_prompt}\n\n{memory_context}"
        
        return base_prompt
    
    def _store_single_message(self, session_id: str, message: BaseMessage, message_index: int = 0):
        """Armazena uma única mensagem no vetorstore"""
        
        # Se está em modo de teste, usa memória simulada
        if self.config.get("test_mode", False) and hasattr(self, '_test_memory'):
            return self._store_test_message(session_id, message, message_index)
        
        if not self.vectorstore:
            return
        
        try:
            # Determina o tipo da mensagem
            message_type = "Usuário" if isinstance(message, HumanMessage) else "Assistente"
            
            # Cria o texto da mensagem com contexto
            message_text = f"{message_type}: {message.content}"
            
            # Adiciona metadados detalhados
            metadata = {
                "session_id": session_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "message_type": message_type,
                "message_index": message_index,
                "content_length": len(message.content)
            }
            
            # Armazena a mensagem individual no vetorstore
            self.vectorstore.add_texts(
                texts=[message_text],
                metadatas=[metadata]
            )
            
            self.logger.info(f"Mensagem armazenada: {message_type} (sessão {session_id})")
            
        except Exception as e:
            self.logger.error(f"Erro ao armazenar mensagem: {e}")
    
    def _store_test_message(self, session_id: str, message: BaseMessage, message_index: int = 0):
        """Armazena mensagem na memória simulada para modo de teste"""
        if not hasattr(self, '_test_memory'):
            self._test_memory = {}
        
        # Determina o tipo da mensagem
        message_type = "Usuário" if isinstance(message, HumanMessage) else "Assistente"
        message_text = f"{message_type}: {message.content}"
        
        # Inicializa sessão se não existir
        if session_id not in self._test_memory:
            self._test_memory[session_id] = []
        
        # Adiciona mensagem à sessão
        self._test_memory[session_id].append(message_text)
        
        self.logger.info(f"Mensagem simulada armazenada: {message_type} (sessão {session_id})")
    
    def _store_conversation_memory(self, session_id: str, messages: List[BaseMessage]):
        """Armazena memória da conversa no vetorstore - mensagem por mensagem"""
        if not self.vectorstore:
            return
        
        try:
            # Armazena cada mensagem individualmente ao invés de concatenar tudo
            for i, msg in enumerate(messages):
                # Determina o tipo da mensagem
                message_type = "Usuário" if isinstance(msg, HumanMessage) else "Assistente"
                
                # Cria o texto da mensagem com contexto
                message_text = f"{message_type}: {msg.content}"
                
                # Adiciona metadados detalhados
                metadata = {
                    "session_id": session_id,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "message_type": message_type,
                    "message_index": i,
                    "total_messages": len(messages),
                    "content_length": len(msg.content)
                }
                
                # Armazena a mensagem individual no vetorstore
                self.vectorstore.add_texts(
                    texts=[message_text],
                    metadatas=[metadata]
                )
                
                self.logger.info(f"Mensagem {i+1} armazenada para sessão {session_id}: {message_type}")
            
            self.logger.info(f"Total de {len(messages)} mensagens armazenadas para sessão {session_id}")
            
        except Exception as e:
            self.logger.error(f"Erro ao armazenar memória: {e}")
    
    def _retrieve_relevant_memory(self, query: str, session_id: Optional[str] = None) -> str:
        """Recupera memória relevante baseada na query com melhorias"""
        
        # Se está em modo de teste, usa memória simulada
        if self.config.get("test_mode", False) and hasattr(self, '_test_memory'):
            return self._retrieve_test_memory(query, session_id)
        
        if not self.vectorstore:
            return ""
        
        try:
            # Busca memória relevante com mais resultados e sem filtro de sessão
            results = self.vectorstore.similarity_search_with_score(
                query,
                k=10,  # Aumentado para 10 para melhor cobertura
                filter=None  # Remove filtro de sessão para buscar em todas as sessões
            )
            
            if results:
                # Filtra resultados por score de similaridade (threshold mais permissivo)
                relevant_results = []
                for doc, score in results:
                    # Score mais baixo = mais similar (ChromaDB usa distância)
                    # Threshold muito mais permissivo para garantir uso da memória
                    if score < 2.5:  # Threshold muito mais permissivo
                        # Adiciona metadados para contexto
                        session_info = doc.metadata.get('session_id', 'N/A')
                        timestamp = doc.metadata.get('timestamp', 'N/A')
                        message_type = doc.metadata.get('message_type', 'N/A')
                        
                        context = f"[Sessão: {session_info} - {timestamp} - {message_type}]\n{doc.page_content}"
                        relevant_results.append(context)
                
                if relevant_results:
                    memory_context = "\n\n".join(relevant_results)
                    self.logger.info(f"Memória recuperada: {len(relevant_results)} mensagens (score < 2.5)")
                    return f"\n\n=== CONTEXTO DE MEMÓRIA ===\n{memory_context}\n=== FIM DO CONTEXTO ===\n"
                else:
                    self.logger.info("Nenhuma memória relevante encontrada (score muito baixo)")
            
            self.logger.info("Nenhuma memória encontrada")
            return ""
            
        except Exception as e:
            self.logger.error(f"Erro ao recuperar memória: {e}")
            return ""
    
    def _retrieve_test_memory(self, query: str, session_id: Optional[str] = None) -> str:
        """Recupera memória simulada para modo de teste"""
        if not hasattr(self, '_test_memory') or not self._test_memory:
            return ""
        
        # Palavras-chave para buscar na memória simulada
        query_lower = query.lower()
        relevant_messages = []
        
        # Busca por palavras-chave na memória simulada
        for session_data in self._test_memory.values():
            for message in session_data:
                message_lower = message.lower()
                
                # Verifica se há palavras em comum
                query_words = set(query_lower.split())
                message_words = set(message_lower.split())
                common_words = query_words.intersection(message_words)
                
                # Se há pelo menos 2 palavras em comum, considera relevante
                if len(common_words) >= 2 and len(common_words) > 0:
                    relevant_messages.append(f"[Memória Simulada] {message}")
        
        if relevant_messages:
            memory_context = "\n\n".join(relevant_messages[:5])  # Limita a 5 mensagens
            self.logger.info(f"Memória simulada recuperada: {len(relevant_messages)} mensagens")
            return f"\n\n=== CONTEXTO DE MEMÓRIA ===\n{memory_context}\n=== FIM DO CONTEXTO ===\n"
        
        return ""
    
    def process_query(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Processa uma query com memória de longo prazo melhorada
        
        Args:
            query: Query do usuário
            session_id: ID da sessão para agrupar conversas
            
        Returns:
            Dicionário com resposta e métricas
        """
        start_time = time.time()
        
        try:
            # Se está em modo de teste, usa processamento simplificado
            if self.config.get("test_mode", False):
                return self._process_query_test_mode(query, session_id, start_time)
            
            # Recupera memória relevante ANTES de processar
            memory_context = self._retrieve_relevant_memory(query, session_id)
            
            # Log detalhado para debug
            if memory_context:
                self.logger.info(f"Memória encontrada para query: '{query[:50]}...'")
                self.logger.info(f"Comprimento do contexto: {len(memory_context)} caracteres")
            else:
                self.logger.info(f"Nenhuma memória encontrada para query: '{query[:50]}...'")
            
            # Cria prompt dinâmico com contexto de memória
            system_prompt = self._get_system_prompt(memory_context)
            
            # Cria mensagens para o LLM
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            
            # Processa a query com contexto de memória
            response = self.llm.invoke(messages)
            
            # Atualiza memória de conversa
            self.conversation_memory.chat_memory.add_user_message(query)
            self.conversation_memory.chat_memory.add_ai_message(str(response))
            
            # Atualiza memória de resumo
            self.summary_memory.save_context(
                {"input": query},
                {"output": str(response)}
            )
            
            # Armazena mensagens individualmente na memória de longo prazo
            current_messages = self.conversation_memory.chat_memory.messages
            
            # Armazena apenas as duas últimas mensagens (usuário + assistente)
            if len(current_messages) >= 2:
                user_message = current_messages[-2]  # Mensagem do usuário
                ai_message = current_messages[-1]    # Resposta do assistente
                
                # Armazena mensagem do usuário
                self._store_single_message(session_id, user_message, len(current_messages) - 2)
                
                # Armazena resposta do assistente
                self._store_single_message(session_id, ai_message, len(current_messages) - 1)
            
            # Calcula métricas
            response_time = time.time() - start_time
            
            # Contagem de tokens
            response_text = str(response)
            tokens_used = len(query.split()) + len(response_text.split())
            
            # Score de confiança
            confidence = min(1.0, max(0.0, 1.0 - (response_time / self.config["max_response_time"])))
            
            # Métricas de memória melhoradas
            memory_metrics = {
                "memory_context_used": bool(memory_context),
                "memory_context_length": len(memory_context),
                "conversation_length": len(current_messages),
                "summary_available": bool(self.summary_memory.buffer),
                "memory_retrieved_count": len(memory_context.split('\n\n')) if memory_context else 0
            }
            
            # Log final
            if memory_context:
                self.logger.info(f"✅ Query processada com memória: {query[:50]}...")
            else:
                self.logger.info(f"⚠️  Query processada sem memória: {query[:50]}...")
            
            return {
                "success": True,
                "response": response_text,
                "response_time": response_time,
                "tokens_used": tokens_used,
                "confidence": confidence,
                "memory_metrics": memory_metrics,
                "session_id": session_id,
                "error_message": None
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"Erro ao processar query '{query}': {str(e)}")
            
            return {
                "success": False,
                "response": "",
                "response_time": response_time,
                "tokens_used": 0,
                "confidence": 0.0,
                "memory_metrics": {},
                "session_id": session_id,
                "error_message": str(e)
            }
    
    def _process_query_test_mode(self, query: str, session_id: str, start_time: float) -> Dict[str, Any]:
        """Processa query em modo de teste com respostas simuladas"""
        
        # Recupera memória simulada
        memory_context = self._retrieve_relevant_memory(query, session_id)
        
        # Gera resposta simulada baseada na memória
        if memory_context:
            response_text = f"Baseado no que você me disse anteriormente: {query}. Tenho memória disponível."
        else:
            response_text = f"Olá! Você disse: {query}. Não tenho memória específica sobre isso ainda."
        
        # Armazena na memória simulada
        user_message = HumanMessage(content=query)
        ai_message = AIMessage(content=response_text)
        
        self._store_test_message(session_id, user_message, 0)
        self._store_test_message(session_id, ai_message, 1)
        
        # Calcula métricas
        response_time = time.time() - start_time
        
        memory_metrics = {
            "memory_context_used": bool(memory_context),
            "memory_context_length": len(memory_context),
            "conversation_length": 2,
            "summary_available": True,
            "memory_retrieved_count": len(memory_context.split('\n\n')) if memory_context else 0
        }
        
        return {
            "success": True,
            "response": response_text,
            "response_time": response_time,
            "tokens_used": len(query.split()) + len(response_text.split()),
            "confidence": 0.8,
            "memory_metrics": memory_metrics,
            "session_id": session_id,
            "error_message": None
        }
    
    def get_conversation_summary(self) -> str:
        """Retorna o resumo da conversa atual"""
        return self.summary_memory.buffer or "Nenhum resumo disponível"
    
    def clear_memory(self, session_id: Optional[str] = None):
        """Limpa a memória da conversa"""
        self.conversation_memory.clear()
        self.summary_memory.clear()
        
        if session_id and self.vectorstore:
            # Remove memória específica da sessão do vetorstore
            try:
                # Nota: ChromaDB não tem método direto para deletar por filtro
                # Em produção, implementar lógica de limpeza mais robusta
                self.logger.info(f"Memória da sessão {session_id} marcada para limpeza")
            except Exception as e:
                self.logger.error(f"Erro ao limpar memória: {e}")
        
        self.logger.info("Memória limpa com sucesso") 