#!/usr/bin/env python3
"""
Configurações do sistema RAG básico
"""

import os
import json
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def load_config() -> Dict[str, Any]:
    """
    Carrega configurações do sistema RAG
    
    Returns:
        Dict com as configurações
    """
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "model_name": os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        "max_tokens": int(os.getenv("MAX_TOKENS", "1000")),
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "max_response_time": float(os.getenv("MAX_RESPONSE_TIME", "5.0")),
        "min_success_rate": float(os.getenv("MIN_SUCCESS_RATE", "90.0")),
        
        # Configurações específicas de RAG
        "chunk_size": int(os.getenv("CHUNK_SIZE", "1000")),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "200")),
        "vectorstore_persistence_path": os.getenv("VECTORSTORE_PERSISTENCE_PATH", "data/chroma_db"),
        "vectorstore_search_k": int(os.getenv("VECTORSTORE_SEARCH_K", "3")),
        "collection_name": os.getenv("COLLECTION_NAME", "rag_documents"),
        
        # Configurações de teste
        "test_queries_file": "input/inputs.txt",
        
        # Configurações de métricas RAG
        "context_recall_threshold": float(os.getenv("CONTEXT_RECALL_THRESHOLD", "0.7")),
        "precision_threshold": float(os.getenv("PRECISION_THRESHOLD", "0.8")),
        
        # Modo de teste
        "test_mode": os.getenv("TEST_MODE", "false").lower() == "true",
        
        # Configurações de logging e relatórios
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_file": "logs/rag_system.log",
        "metrics_file": "metrics/rag_metrics.json",
        "reports_dir": "reports"
    }
    
    # Se estiver em modo de teste, não requer API key
    if not config["test_mode"] and not config["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    # Tenta carregar configuração personalizada
    config_file = Path("config.json")
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                custom_config = json.load(f)
                config.update(custom_config)
        except Exception as e:
            print(f"Erro ao carregar config.json: {e}")
    
    # Cria diretórios necessários
    Path("logs").mkdir(exist_ok=True)
    Path("metrics").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("input").mkdir(exist_ok=True)
    
    return config

def save_config(config: Dict[str, Any], filename: str = "config.json"):
    """
    Salva configurações em arquivo
    
    Args:
        config: Configurações para salvar
        filename: Nome do arquivo
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar configuração: {e}")

def get_test_config() -> Dict[str, Any]:
    """
    Retorna configuração para modo de teste
    
    Returns:
        Dict com configurações de teste
    """
    config = load_config()
    config["test_mode"] = True
    config["openai_api_key"] = "test_key"
    return config 