#!/usr/bin/env python3
"""
Geração de relatórios para o laboratório
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

def generate_report(results: Dict[str, Any], report_file: str, metrics_file: str):
    """
    Gera relatórios de resultados
    
    Args:
        results: Resultados dos testes
        report_file: Arquivo para salvar relatório completo
        metrics_file: Arquivo para salvar métricas
    """
    # Cria diretórios se não existirem
    Path(report_file).parent.mkdir(parents=True, exist_ok=True)
    Path(metrics_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Salva relatório completo
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Salva métricas separadamente
    metrics_data = {
        "summary": results["summary"],
        "timestamp": results["timestamp"]
    }
    
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=2, ensure_ascii=False) 