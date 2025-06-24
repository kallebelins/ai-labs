#!/usr/bin/env python3
"""
Configurações do laboratório de chatbot com memória de longo prazo
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def load_config() -> Dict[str, Any]:
    """
    Carrega configurações do laboratório
    
    Returns:
        Dicionário com configurações
    """
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "model_name": os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        "max_tokens": int(os.getenv("MAX_TOKENS", "500")),
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "max_response_time": float(os.getenv("MAX_RESPONSE_TIME", "3.0")),
        "min_success_rate": float(os.getenv("MIN_SUCCESS_RATE", "95.0")),
        
        # Configurações específicas de memória
        "memory_window": int(os.getenv("MEMORY_WINDOW", "10")),
        "max_summary_tokens": int(os.getenv("MAX_SUMMARY_TOKENS", "2000")),
        "memory_persistence_path": os.getenv("MEMORY_PERSISTENCE_PATH", "data/chroma_db"),
        "memory_search_k": int(os.getenv("MEMORY_SEARCH_K", "3")),
        "memory_chunk_size": int(os.getenv("MEMORY_CHUNK_SIZE", "1000")),
        "memory_chunk_overlap": int(os.getenv("MEMORY_CHUNK_OVERLAP", "200")),
        
        # Configurações de teste
        "test_queries_file": "input/inputs.txt",
        "test_sessions": ["session_1", "session_2", "session_3"],
        
        # Configurações de métricas de memória
        "memory_retention_threshold": float(os.getenv("MEMORY_RETENTION_THRESHOLD", "0.8")),
        "context_coherence_threshold": float(os.getenv("CONTEXT_COHERENCE_THRESHOLD", "0.7")),
        
        # Modo de teste
        "test_mode": os.getenv("TEST_MODE", "false").lower() == "true"
    }
    
    # Se estiver em modo de teste, não requer API key
    if not config["test_mode"] and not config["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    return config 