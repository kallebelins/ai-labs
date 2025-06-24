#!/usr/bin/env python3
"""
Script para testar o parameter tuning dos pesos do re-ranking
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.rag_system import RAGSystem
from src.utils.config import load_config
from src.utils.logging_config import setup_logging
import time

def test_parameter_tuning():
    """Testa o sistema de parameter tuning dos pesos"""
    print("🔧 TESTE DE PARAMETER TUNING DOS PESOS DO RE-RANKING")
    print("=" * 60)
    
    try:
        # Configura logging
        logger = setup_logging("logs/parameter_tuning_test.log")
        
        # Carrega configuração
        config = load_config()
        config["test_mode"] = True
        
        # Inicializa sistema RAG
        rag_system = RAGSystem(config, logger)
        
        # Queries de teste para demonstrar parameter tuning
        test_queries = [
            "O que é inteligência artificial?",
            "Como funciona machine learning?",
            "Explique deep learning",
            "O que é RAG?",
            "Como usar LangChain?",
            "O que é ChromaDB?",
            "Explique embeddings",
            "Como funciona OpenAI?",
            "O que é processamento de linguagem natural?",
            "Como implementar um chatbot RAG?"
        ]
        
        print(f"📝 Executando {len(test_queries)} queries para parameter tuning...")
        print()
        
        # Executa queries e observa evolução dos pesos
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 Query {i}/{len(test_queries)}: {query}")
            
            # Obtém pesos antes da query
            weights_before = rag_system.get_rerank_weights()
            
            # Processa query
            start_time = time.time()
            result = rag_system.process_query(query)
            end_time = time.time()
            
            # Obtém pesos depois da query
            weights_after = rag_system.get_rerank_weights()
            
            # Mostra evolução dos pesos
            print(f"   ⏱️  Tempo: {end_time - start_time:.2f}s")
            print(f"   📊 Documentos usados: {result['documents_used']}")
            print(f"   🎯 Recall: {result['context_recall']:.2%}")
            print(f"   📈 Precisão: {result['precision']:.2%}")
            
            # Mostra mudanças nos pesos
            print("   🔧 Evolução dos pesos:")
            for key in weights_before:
                change = weights_after[key] - weights_before[key]
                if abs(change) > 0.001:  # Só mostra mudanças significativas
                    print(f"      {key}: {weights_before[key]:.3f} → {weights_after[key]:.3f} ({change:+.3f})")
                else:
                    print(f"      {key}: {weights_before[key]:.3f} (sem mudança)")
            
            print()
            
            # Pequena pausa para visualização
            time.sleep(0.5)
        
        # Mostra informações finais do sistema
        system_info = rag_system.get_system_info()
        print("📊 INFORMAÇÕES FINAIS DO SISTEMA:")
        print(f"   - Documentos no sistema: {system_info['documents_count']}")
        print(f"   - Histórico de performance: {system_info['performance_history_size']} queries")
        print(f"   - Parameter tuning habilitado: {system_info['parameter_tuning_enabled']}")
        print(f"   - Pesos finais: {system_info['rerank_weights']}")
        
        print(f"\n✅ Teste de parameter tuning concluído!")
        return 0
        
    except Exception as e:
        error_msg = f"Erro durante teste de parameter tuning: {e}"
        print(f"❌ {error_msg}")
        if 'logger' in locals():
            logger.error(error_msg)
        return 1

if __name__ == "__main__":
    exit_code = test_parameter_tuning()
    sys.exit(exit_code) 