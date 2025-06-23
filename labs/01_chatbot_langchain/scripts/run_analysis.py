#!/usr/bin/env python3
"""
Script para executar análise de logs
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para que os imports funcionem
sys.path.append(str(Path(__file__).parent.parent))

from src.analysis.analyze_logs import load_json_logs, extract_metrics_from_logs, print_metrics, save_metrics_report

def main():
    # Se não foram passados argumentos, usa o log padrão
    if len(sys.argv) == 1:
        log_file = "logs/app.log"
    else:
        log_file = sys.argv[1]
    
    # Verifica se arquivo existe
    if not Path(log_file).exists():
        print(f"❌ Arquivo não encontrado: {log_file}")
        return
    
    print(f"📖 Analisando logs: {log_file}")
    
    # Carrega logs
    logs = load_json_logs(log_file)
    print(f"📊 Carregados {len(logs)} logs")
    
    # Calcula métricas
    metrics = extract_metrics_from_logs(logs)
    
    # Exibe métricas
    print_metrics(metrics)
    
    # Salva relatório se especificado
    if len(sys.argv) > 2 and sys.argv[2] == "-o" and len(sys.argv) > 3:
        output_file = sys.argv[3]
        save_metrics_report(metrics, output_file)

if __name__ == "__main__":
    main() 