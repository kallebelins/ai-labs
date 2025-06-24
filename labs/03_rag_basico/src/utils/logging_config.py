#!/usr/bin/env python3
"""
Configuração de logging para o sistema RAG básico
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(
    log_file: str = "logs/rag_system.log",
    log_level: str = "INFO",
    logger_name: Optional[str] = None
) -> logging.Logger:
    """
    Configura o sistema de logging
    
    Args:
        log_file: Caminho do arquivo de log
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        logger_name: Nome do logger (opcional)
    
    Returns:
        Logger configurado
    """
    # Cria diretório de logs se não existir
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configura o logger
    logger = logging.getLogger(logger_name or __name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Formato do log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adiciona handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retorna um logger configurado
    
    Args:
        name: Nome do logger
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name or __name__) 