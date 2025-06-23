#!/usr/bin/env python3
"""
Configurações do laboratório
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
        "test_queries_file": "input/inputs.txt"
    }
    
    if not config["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    return config 