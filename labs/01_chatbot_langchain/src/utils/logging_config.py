#!/usr/bin/env python3
"""
Configuração de logging para o laboratório
"""

import json
import logging
from datetime import datetime
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """Formatter para logs em formato JSON"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging(log_file: str) -> logging.Logger:
    """
    Configura o sistema de logging com formato JSON
    
    Args:
        log_file: Caminho para o arquivo de log
        
    Returns:
        Logger configurado
    """
    # Cria diretório de logs se não existir
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configura logging com formato JSON
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para arquivo (JSON)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    # Handler para console (formato legível)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger 