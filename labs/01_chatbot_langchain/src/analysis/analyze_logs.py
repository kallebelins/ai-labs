#!/usr/bin/env python3
"""
Script para analisar logs JSON e calcular métricas
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import statistics

def load_json_logs(log_file: str) -> List[Dict[str, Any]]:
    """
    Carrega logs em formato JSON (uma linha por entrada)
    
    Args:
        log_file: Caminho para o arquivo de log
        
    Returns:
        Lista de entradas de log como dicionários
    """
    logs = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    log_entry = json.loads(line)
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    print(f"Erro ao decodificar linha: {line[:100]}...")
                    continue
    return logs

def extract_metrics_from_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extrai métricas dos logs
    
    Args:
        logs: Lista de entradas de log
        
    Returns:
        Dicionário com métricas calculadas
    """
    # Filtra logs relacionados a métricas
    metric_logs = []
    for log in logs:
        if "Métricas:" in log.get("message", ""):
            metric_logs.append(log)
    
    if not metric_logs:
        return {
            "error": "Nenhum log de métricas encontrado",
            "total_logs": len(logs),
            "metric_logs": 0
        }
    
    # Extrai métricas dos logs
    response_times = []
    tokens_used = []
    confidences = []
    
    for log in metric_logs:
        message = log.get("message", "")
        if "Métricas:" in message:
            # Parse da mensagem de métricas
            # Exemplo: "Métricas: tempo=1.234s, tokens=150, confiança=0.85"
            try:
                parts = message.split("Métricas:")[1].strip().split(", ")
                for part in parts:
                    if "tempo=" in part:
                        time_str = part.split("=")[1].replace("s", "")
                        response_times.append(float(time_str))
                    elif "tokens=" in part:
                        tokens_str = part.split("=")[1]
                        tokens_used.append(int(tokens_str))
                    elif "confiança=" in part:
                        conf_str = part.split("=")[1]
                        confidences.append(float(conf_str))
            except (IndexError, ValueError) as e:
                print(f"Erro ao parsear métricas: {message}")
                continue
    
    # Calcula estatísticas
    metrics = {
        "total_logs": len(logs),
        "metric_logs": len(metric_logs),
        "total_queries": len(response_times),
        "response_time": {
            "count": len(response_times),
            "mean": statistics.mean(response_times) if response_times else 0,
            "median": statistics.median(response_times) if response_times else 0,
            "min": min(response_times) if response_times else 0,
            "max": max(response_times) if response_times else 0,
            "std": statistics.stdev(response_times) if len(response_times) > 1 else 0
        },
        "tokens": {
            "count": len(tokens_used),
            "mean": statistics.mean(tokens_used) if tokens_used else 0,
            "median": statistics.median(tokens_used) if tokens_used else 0,
            "min": min(tokens_used) if tokens_used else 0,
            "max": max(tokens_used) if tokens_used else 0,
            "total": sum(tokens_used) if tokens_used else 0
        },
        "confidence": {
            "count": len(confidences),
            "mean": statistics.mean(confidences) if confidences else 0,
            "median": statistics.median(confidences) if confidences else 0,
            "min": min(confidences) if confidences else 0,
            "max": max(confidences) if confidences else 0
        }
    }
    
    return metrics

def print_metrics(metrics: Dict[str, Any]):
    """
    Exibe métricas formatadas
    
    Args:
        metrics: Dicionário com métricas
    """
    if "error" in metrics:
        print(f"❌ {metrics['error']}")
        return
    
    print("📊 MÉTRICAS CALCULADAS DOS LOGS")
    print("=" * 50)
    print(f"📝 Total de logs: {metrics['total_logs']}")
    print(f"🔍 Logs com métricas: {metrics['metric_logs']}")
    print(f"💬 Total de queries: {metrics['total_queries']}")
    print()
    
    print("⏱️  TEMPO DE RESPOSTA")
    print("-" * 30)
    rt = metrics['response_time']
    print(f"  Média: {rt['mean']:.3f}s")
    print(f"  Mediana: {rt['median']:.3f}s")
    print(f"  Mínimo: {rt['min']:.3f}s")
    print(f"  Máximo: {rt['max']:.3f}s")
    print(f"  Desvio padrão: {rt['std']:.3f}s")
    print()
    
    print("🔤 TOKENS UTILIZADOS")
    print("-" * 30)
    tk = metrics['tokens']
    print(f"  Média: {tk['mean']:.1f}")
    print(f"  Mediana: {tk['median']:.1f}")
    print(f"  Mínimo: {tk['min']}")
    print(f"  Máximo: {tk['max']}")
    print(f"  Total: {tk['total']}")
    print()
    
    print("🎯 CONFIANÇA")
    print("-" * 30)
    cf = metrics['confidence']
    print(f"  Média: {cf['mean']:.3f}")
    print(f"  Mediana: {cf['median']:.3f}")
    print(f"  Mínimo: {cf['min']:.3f}")
    print(f"  Máximo: {cf['max']:.3f}")

def save_metrics_report(metrics: Dict[str, Any], output_file: str):
    """
    Salva relatório de métricas em arquivo JSON
    
    Args:
        metrics: Dicionário com métricas
        output_file: Arquivo de saída
    """
    # Adiciona timestamp
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics
    }
    
    # Cria diretório se não existir
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Relatório salvo em: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Analisa logs JSON e calcula métricas")
    parser.add_argument("log_file", help="Arquivo de log para analisar")
    parser.add_argument("--output", "-o", help="Arquivo de saída para o relatório")
    
    args = parser.parse_args()
    
    # Verifica se arquivo existe
    if not Path(args.log_file).exists():
        print(f"❌ Arquivo não encontrado: {args.log_file}")
        return
    
    print(f"📖 Analisando logs: {args.log_file}")
    
    # Carrega logs
    logs = load_json_logs(args.log_file)
    print(f"📊 Carregados {len(logs)} logs")
    
    # Calcula métricas
    metrics = extract_metrics_from_logs(logs)
    
    # Exibe métricas
    print_metrics(metrics)
    
    # Salva relatório se especificado
    if args.output:
        save_metrics_report(metrics, args.output)

if __name__ == "__main__":
    main() 