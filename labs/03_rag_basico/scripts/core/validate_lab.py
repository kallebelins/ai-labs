#!/usr/bin/env python3
"""
Validação simplificada do sistema RAG.

Este script valida o sistema RAG usando métricas básicas:
- Taxa de sucesso
- Tempo de resposta
- Recall e precisão básicos
"""

import sys
import os
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.logging_config import setup_logging
from src.core.rag_system import RAGSystem
from src.utils.config import load_config
from src.utils.metrics import SimpleMetrics

# Configura logging
logger = setup_logging()

def validate_rag_system():
    """Valida o sistema RAG com métricas básicas"""
    
    print("🔍 LABORATÓRIO 3: VALIDAÇÃO DO SISTEMA RAG SIMPLIFICADO")
    print("=" * 60)
    
    # Carrega configuração
    config = load_config()
    config["test_mode"] = True
    
    # Inicializa sistema RAG
    print("🚀 Inicializando sistema RAG Simplificado...")
    rag_system = RAGSystem(config, logger)
    
    # Inicializa métricas
    print("📊 Inicializando coletor de métricas...")
    metrics = SimpleMetrics()
    metrics.reset_metrics()
    
    # Mostra informações do sistema
    system_info = rag_system.get_system_info()
    print(f"📊 Sistema - Recursos ativos:")
    print(f"   • Modelo: {system_info['model_name']}")
    print(f"   • Temperatura: {system_info['temperature']}")
    print(f"   • Modo teste: {system_info['test_mode']}")
    print(f"   • Vetorstore: {'✅' if system_info['vectorstore_available'] else '❌'}")
    print(f"   • Cross-Encoder: {'✅' if system_info['cross_encoder_available'] else '❌'}")
    
    # Queries de teste
    test_queries = [
        "O que é inteligência artificial?",
        "Explique machine learning",
        "Como funciona deep learning?",
        "O que é RAG?",
        "Explique LangChain",
        "Como funciona ChromaDB?",
        "O que são embeddings?",
        "Explique OpenAI",
        "Como funciona o sistema de recuperação?",
        "Qual é a capital do Brasil?",
        "Como fazer um bolo de chocolate?",
        "Qual é o melhor time de futebol?"
    ]
    
    print("\n🧪 Executando testes de validação...")
    print(f"📝 Executando {len(test_queries)} queries de teste...")
    
    # Executa testes
    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Teste {i}/{len(test_queries)}: {query}")
        
        start_time = time.time()
        result = rag_system.process_query(query)
        result["response_time"] = time.time() - start_time
        
        # Registra resultado
        metrics.record_query_result(result)
        results.append(result)
        
        # Mostra resultado
        if result["success"]:
            print(f"✅ Sucesso - Tempo: {result['response_time']:.2f}s")
            print(f"   Documentos usados: {result['documents_used']}")
            print(f"   Recall: {result['context_recall']:.2f}")
            print(f"   Precisão: {result['precision']:.2f}")
            if 'expanded_queries' in result:
                print(f"   🔍 Queries expandidas: {len(result['expanded_queries'])}")
        else:
            print(f"❌ Falha: {result.get('error_message', 'Erro desconhecido')}")
    
    print("\n✅ Testes concluídos!")
    
    # Calcula métricas finais
    print("\n📈 Calculando métricas finais...")
    
    summary = metrics.get_summary()
    final_score = metrics.calculate_final_score()
    
    # Mostra resultados
    print("\n📊 MÉTRICAS BÁSICAS DO SISTEMA")
    print("=" * 60)
    print(f"📊 Total de queries: {summary['total_queries']}")
    print(f"✅ Queries bem-sucedidas: {summary['total_queries'] - (summary['total_queries'] - int(summary['success_rate'] * summary['total_queries'] / 100))}")
    print(f"❌ Queries com falha: {summary['total_queries'] - int(summary['success_rate'] * summary['total_queries'] / 100)}")
    print(f"📈 Taxa de sucesso: {summary['success_rate']:.1f}%")
    print(f"⏱️ Tempo médio de resposta: {summary['avg_response_time']:.2f}s")
    print(f"📋 Recall médio: {summary['avg_context_recall']:.2f}")
    print(f"🎯 Precisão média: {summary['avg_precision']:.2f}")
    print(f"🔍 Taxa de uso RAG: {summary['rag_usage_rate']:.1f}%")
    
    # Score final
    print(f"\n🏆 SCORE FINAL: {final_score:.1f}%")
    
    # Avalia se passou nos critérios
    criteria_met = {
        "success_rate": summary['success_rate'] >= 90.0,
        "avg_response_time": summary['avg_response_time'] <= 5.0,
        "avg_context_recall": summary['avg_context_recall'] >= 0.7,
        "avg_precision": summary['avg_precision'] >= 0.7,
        "rag_usage_rate": summary['rag_usage_rate'] >= 70.0,
        "final_score": final_score >= 70.0
    }
    
    print("\n📋 CRITÉRIOS DE AVALIAÇÃO")
    print("=" * 60)
    print(f"✅ Taxa de sucesso ≥ 90%: {'✅' if criteria_met['success_rate'] else '❌'} ({summary['success_rate']:.1f}%)")
    print(f"✅ Tempo médio ≤ 5s: {'✅' if criteria_met['avg_response_time'] else '❌'} ({summary['avg_response_time']:.2f}s)")
    print(f"✅ Recall médio ≥ 70%: {'✅' if criteria_met['avg_context_recall'] else '❌'} ({summary['avg_context_recall']:.2f})")
    print(f"✅ Precisão média ≥ 70%: {'✅' if criteria_met['avg_precision'] else '❌'} ({summary['avg_precision']:.2f})")
    print(f"✅ Taxa uso RAG ≥ 70%: {'✅' if criteria_met['rag_usage_rate'] else '❌'} ({summary['rag_usage_rate']:.1f}%)")
    print(f"✅ Score final ≥ 70%: {'✅' if criteria_met['final_score'] else '❌'} ({final_score:.1f}%)")
    
    # Resultado final
    all_criteria_met = all(criteria_met.values())
    
    if all_criteria_met:
        print("\n🎉 LABORATÓRIO APROVADO!")
        print("✅ Todos os critérios foram atendidos.")
        return True
    else:
        print("\n❌ LABORATÓRIO REPROVADO")
        failed_criteria = [k for k, v in criteria_met.items() if not v]
        print(f"❌ Critérios não atendidos: {', '.join(failed_criteria)}")
        return False

if __name__ == "__main__":
    try:
        success = validate_rag_system()
        exit_code = 0 if success else 1
    except Exception as e:
        logger.error(f"Erro durante validação do sistema: {e}")
        exit_code = 1
    
    sys.exit(exit_code) 