#!/usr/bin/env python3
"""
Teste de métricas básicas do sistema RAG simplificado.

Este script testa as métricas básicas do sistema RAG:
- Taxa de sucesso
- Tempo de resposta
- Recall e precisão básicos
"""

import os
import sys
import json
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.rag_system import RAGSystem
from src.utils.config import load_config
from src.utils.metrics import SimpleMetrics

def test_basic_metrics():
    """Testa métricas básicas do sistema RAG"""
    
    print("🧪 TESTE DE MÉTRICAS BÁSICAS")
    print("=" * 50)
    
    # Carrega configuração
    config = load_config()
    config["test_mode"] = True
    
    # Inicializa sistema RAG
    rag_system = RAGSystem(config)
    
    # Inicializa coletor de métricas
    metrics = SimpleMetrics()
    metrics.reset_metrics()
    
    # Queries de teste
    test_queries = [
        "O que é inteligência artificial?",
        "Explique machine learning",
        "Como funciona deep learning?",
        "O que é RAG?",
        "Defina embeddings"
    ]
    
    print(f"📊 Executando {len(test_queries)} queries de teste...")
    
    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Processando: '{query}'")
        
        start_time = time.time()
        result = rag_system.process_query(query)
        result["response_time"] = time.time() - start_time
        
        # Registra métricas
        metrics.record_query_result(result)
        results.append(result)
        
        # Mostra resultado
        if result["success"]:
            print(f"   ✅ Sucesso - {result['response_time']:.2f}s")
            print(f"   📄 Documentos: {result['documents_used']}")
            print(f"   📋 Recall: {result['context_recall']:.2f}")
            print(f"   🎯 Precisão: {result['precision']:.2f}")
        else:
            print(f"   ❌ Falha: {result.get('error_message', 'Erro desconhecido')}")
    
    # Mostra resumo das métricas
    print("\n" + "=" * 50)
    print("📊 RESUMO DAS MÉTRICAS")
    print("=" * 50)
    
    summary = metrics.get_summary()
    final_score = metrics.calculate_final_score()
    
    print(f"Total de queries: {summary['total_queries']}")
    print(f"Taxa de sucesso: {summary['success_rate']:.1f}%")
    print(f"Tempo médio: {summary['avg_response_time']:.2f}s")
    print(f"Recall médio: {summary['avg_context_recall']:.2f}")
    print(f"Precisão média: {summary['avg_precision']:.2f}")
    print(f"Taxa de uso RAG: {summary['rag_usage_rate']:.1f}%")
    print(f"\n🎯 SCORE FINAL: {final_score:.1f}%")
    
    # Salva relatório
    report = {
        "test_type": "basic_metrics",
        "timestamp": time.time(),
        "config": config,
        "results": results,
        "summary": summary,
        "final_score": final_score
    }
    
    report_file = Path("reports") / f"basic_metrics_test_{int(time.time())}.json"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Relatório salvo: {report_file}")
    
    return final_score >= 70.0

if __name__ == "__main__":
    success = test_basic_metrics()
    sys.exit(0 if success else 1) 