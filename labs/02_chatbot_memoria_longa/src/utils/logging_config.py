#!/usr/bin/env python3
"""
Configuração de logging estruturado para o laboratório
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """Formatter para logs em formato JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formata o log record como JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Adiciona campos extras se existirem
        if hasattr(record, 'memory_metrics'):
            log_entry['memory_metrics'] = getattr(record, 'memory_metrics')
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = getattr(record, 'session_id')
        if hasattr(record, 'response_time'):
            log_entry['response_time'] = getattr(record, 'response_time')
        if hasattr(record, 'tokens_used'):
            log_entry['tokens_used'] = getattr(record, 'tokens_used')
        if hasattr(record, 'confidence'):
            log_entry['confidence'] = getattr(record, 'confidence')
        
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging(log_file: str = "logs/app.log") -> logging.Logger:
    """
    Configura o sistema de logging
    
    Args:
        log_file: Caminho para o arquivo de log
        
    Returns:
        Logger configurado
    """
    # Cria diretório de logs se não existir
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configura o logger
    logger = logging.getLogger("chatbot_memory")
    logger.setLevel(logging.INFO)
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para arquivo (JSON)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    
    # Handler para console (formato legível)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Adiciona handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_memory_metrics(logger: logging.Logger, metrics: Dict[str, Any], session_id: str):
    """
    Loga métricas específicas de memória
    
    Args:
        logger: Logger configurado
        metrics: Dicionário com métricas
        session_id: ID da sessão
    """
    logger.info(
        f"Métricas de memória para sessão {session_id}",
        extra={
            'memory_metrics': metrics,
            'session_id': session_id
        }
    ) 