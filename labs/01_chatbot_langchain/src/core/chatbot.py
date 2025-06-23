#!/usr/bin/env python3
"""
Chatbot Engine usando LangChain
"""

import time
import logging
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class ChatbotEngine:
    """Motor do chatbot usando LangChain"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o chatbot
        
        Args:
            config: Configurações do chatbot
        """
        self.config = config
        self.llm = ChatOpenAI(
            model=config["model_name"],
            temperature=config["temperature"]
        )
        
        # Template do prompt
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente útil e amigável. Responda de forma clara e concisa."),
            ("human", "{input}")
        ])
        
        # Chain do LangChain
        self.chain = self.prompt_template | self.llm
        
        self.logger = logging.getLogger(__name__)
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processa uma query e retorna a resposta com métricas
        
        Args:
            query: Query do usuário
            
        Returns:
            Dicionário com resposta e métricas
        """
        start_time = time.time()
        
        try:
            # Processa a query
            response = self.chain.invoke({"input": query})
            
            # Calcula métricas
            response_time = time.time() - start_time
            
            # Simula contagem de tokens (em produção, usar tiktoken)
            response_text = str(response)
            tokens_used = len(query.split()) + len(response_text.split())
            
            # Simula score de confiança (em produção, usar modelo de confiança)
            confidence = min(1.0, max(0.0, 1.0 - (response_time / self.config["max_response_time"])))
            
            return {
                "success": True,
                "response": response_text,
                "response_time": response_time,
                "tokens_used": tokens_used,
                "confidence": confidence,
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
                "error_message": str(e)
            } 