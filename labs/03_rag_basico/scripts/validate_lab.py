#!/usr/bin/env python3
"""
Script de validação do Laboratório 3: RAG Básico
Executa testes automatizados e gera relatório de validação
"""

import sys
import os
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem
from src.utils.metrics import MetricsCollector
from src.utils.reporting import ReportGenerator


def run_validation_tests(rag_system, metrics_collector):
    """
    Executa testes de validação do sistema RAG
    
    Args:
        rag_system: Sistema RAG inicializado
        metrics_collector: Coletor de métricas
    """
    print("🧪 Executando testes de validação...")
    
    # Queries de teste para validar diferentes aspectos
    test_queries = [
        # Testes de recall de contexto
        "O que é inteligência artificial?",
        "Explique machine learning",
        "Como funciona deep learning?",
        
        # Testes de precisão
        "O que é RAG?",
        "Explique LangChain",
        "Como funciona ChromaDB?",
        
        # Testes de uso de documentos
        "O que são embeddings?",
        "Explique OpenAI",
        "Como funciona o sistema de recuperação?",
        
        # Testes de queries sem contexto
        "Qual é a capital do Brasil?",
        "Como fazer um bolo de chocolate?",
        "Qual é o melhor time de futebol?"
    ]
    
    print(f"📝 Executando {len(test_queries)} queries de teste...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Teste {i}/{len(test_queries)}: {query}")
        
        # Processa query
        result = rag_system.process_query(query)
        
        # Registra métricas
        metrics_collector.record_query_result(result)
        
        # Exibe resultado
        if result["success"]:
            print(f"✅ Sucesso - Tempo: {result['response_time']:.2f}s")
            print(f"   Documentos usados: {result['documents_used']}")
            print(f"   Recall: {result['context_recall']:.2f}")
            print(f"   Precisão: {result['precision']:.2f}")
        else:
            print(f"❌ Falha: {result['error_message']}")
        
        # Pequena pausa entre testes
        time.sleep(0.5)
    
    print(f"\n✅ Testes concluídos!")


def main():
    """Função principal de validação"""
    print("🔍 LABORATÓRIO 3: VALIDAÇÃO DO SISTEMA RAG BÁSICO")
    print("=" * 60)
    
    # Configura logging
    logger = setup_logging("logs/validation.log")
    logger.info("Iniciando validação do Laboratório 3")
    
    try:
        # Carrega configuração
        print("🔧 Carregando configurações...")
        config = load_config()
        
        # Inicializa sistema RAG
        print("🤖 Inicializando sistema RAG...")
        rag_system = RAGSystem(config, logger)
        
        # Inicializa coletor de métricas
        print("📊 Inicializando coletor de métricas...")
        metrics_collector = MetricsCollector()
        
        # Executa testes de validação
        run_validation_tests(rag_system, metrics_collector)
        
        # Obtém resumo das métricas
        print("\n📈 Calculando métricas finais...")
        metrics_summary = metrics_collector.get_summary()
        system_info = rag_system.get_system_info()
        
        # Gera relatório
        print("📋 Gerando relatório...")
        report_generator = ReportGenerator()
        report_file = report_generator.generate_lab_report(metrics_summary, system_info)
        
        # Exibe resumo no console
        report_generator.print_summary(metrics_summary, system_info)
        
        # Calcula score final
        final_score = metrics_collector.calculate_final_score()
        
        print(f"\n🎯 RESULTADO DA VALIDAÇÃO:")
        print(f"   - Score Final: {final_score:.1f}%")
        
        if final_score >= 90:
            print("   - Status: ✅ LABORATÓRIO APROVADO")
        elif final_score >= 80:
            print("   - Status: ⚠️ LABORATÓRIO APROVADO COM RESERVAS")
        elif final_score >= 70:
            print("   - Status: 🔄 LABORATÓRIO EM REVISÃO")
        else:
            print("   - Status: ❌ LABORATÓRIO REPROVADO")
        
        if report_file:
            print(f"\n📄 Relatório salvo em: {report_file}")
        
        logger.info(f"Validação concluída - Score: {final_score:.1f}%")
        return 0
        
    except Exception as e:
        error_msg = f"Erro durante validação: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 