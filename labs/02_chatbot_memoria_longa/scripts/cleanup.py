#!/usr/bin/env python3
"""
Script de limpeza para o projeto chatbot com memória longa.
Remove logs antigos, métricas e relatórios desnecessários.
"""

import os
import glob
import json
from datetime import datetime
from pathlib import Path

def cleanup_logs():
    """Remove todos os arquivos de log."""
    log_files = glob.glob("logs/*.log")
    for log_file in log_files:
        try:
            os.remove(log_file)
            print(f"Removido: {log_file}")
        except Exception as e:
            print(f"Erro ao remover {log_file}: {e}")

def cleanup_metrics():
    """Remove métricas antigas, mantendo apenas a mais recente."""
    metric_files = glob.glob("metrics/*.json")
    if len(metric_files) > 1:
        # Ordenar por data de modificação
        metric_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        # Manter apenas o mais recente
        for metric_file in metric_files[1:]:
            try:
                os.remove(metric_file)
                print(f"Removido: {metric_file}")
            except Exception as e:
                print(f"Erro ao remover {metric_file}: {e}")

def cleanup_reports():
    """Remove relatórios antigos, mantendo apenas o mais recente."""
    report_files = glob.glob("reports/*.json")
    if len(report_files) > 1:
        # Ordenar por data de modificação
        report_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        # Manter apenas o mais recente
        for report_file in report_files[1:]:
            try:
                os.remove(report_file)
                print(f"Removido: {report_file}")
            except Exception as e:
                print(f"Erro ao remover {report_file}: {e}")

def cleanup_cache():
    """Remove arquivos de cache Python."""
    cache_dirs = ["__pycache__", ".pytest_cache"]
    for cache_dir in cache_dirs:
        for root, dirs, files in os.walk("."):
            if cache_dir in dirs:
                cache_path = os.path.join(root, cache_dir)
                try:
                    import shutil
                    shutil.rmtree(cache_path)
                    print(f"Removido: {cache_path}")
                except Exception as e:
                    print(f"Erro ao remover {cache_path}: {e}")

def main():
    """Executa a limpeza completa do projeto."""
    print("Iniciando limpeza do projeto...")
    print("=" * 50)
    
    cleanup_logs()
    cleanup_metrics()
    cleanup_reports()
    cleanup_cache()
    
    print("=" * 50)
    print("Limpeza concluída!")

if __name__ == "__main__":
    main() 