#!/usr/bin/env python3
"""
Script de teste do Chatbot LangChain com perguntas predefinidas
Útil para testes automatizados e demonstração
"""

import logging
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para que os imports funcionem
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.chatbot import ChatbotEngine

def run_test_queries():
    """Executa uma série de perguntas de teste predefinidas"""
    
    # Configura logging estruturado (JSON)
    logger = setup_logging("logs/test_chatbot.log")
    logger.info("Iniciando testes do chatbot com perguntas predefinidas.")

    # Carrega configurações e inicializa chatbot
    try:
        config = load_config()
        chatbot = ChatbotEngine(config)
        logger.info("Chatbot inicializado para testes.")
    except Exception as e:
        print(f"❌ Erro ao inicializar chatbot: {e}")
        logger.error(f"Erro na inicialização: {e}")
        return

    # Lista de perguntas de teste
    test_queries = [
        "Explique o que é inteligência artificial.",
        "Qual é a capital do Brasil?",
        "Conte uma piada curta.",
        "Quais são os benefícios do exercício físico?",
        "Como funciona a fotossíntese?",
        "Qual é a diferença entre Python e JavaScript?",
        "Explique o conceito de machine learning.",
        "Quais são as principais características do Python?"
    ]

    print("🧪 TESTE DO CHATBOT LANGCHAIN")
    print("="*60)
    print(f"📝 Executando {len(test_queries)} perguntas de teste...")
    print()

    total_tokens = 0
    total_time = 0
    successful_queries = 0

    for i, pergunta in enumerate(test_queries, 1):
        print(f"🔍 Teste {i}/{len(test_queries)}")
        print(f"👤 Pergunta: {pergunta}")
        
        try:
            # Processa a pergunta
            resultado = chatbot.process_query(pergunta)
            
            # Exibe resposta resumida
            response_preview = resultado["response"][:100] + "..." if len(resultado["response"]) > 100 else resultado["response"]
            print(f"🤖 Resposta: {response_preview}")
            
            # Exibe métricas
            print(f"📊 Tempo: {resultado['response_time']:.3f}s | Tokens: {resultado['tokens_used']} | Confiança: {resultado['confidence']:.2f}")
            
            if resultado["success"]:
                successful_queries += 1
                total_tokens += resultado['tokens_used']
                total_time += resultado['response_time']
            else:
                print(f"❌ Erro: {resultado['error_message']}")
            
            # Log da interação
            logger.info(f"Teste {i}: Pergunta='{pergunta}' | Sucesso={resultado['success']} | Tempo={resultado['response_time']:.3f}s | Tokens={resultado['tokens_used']}")
            
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            logger.error(f"Erro no teste {i}: {e}")
        
        print("-" * 60)

    # Resumo dos testes
    print("\n📈 RESUMO DOS TESTES")
    print("="*60)
    print(f"✅ Queries bem-sucedidas: {successful_queries}/{len(test_queries)}")
    print(f"📊 Taxa de sucesso: {(successful_queries/len(test_queries)*100):.1f}%")
    print(f"⏱️  Tempo total: {total_time:.3f}s")
    print(f"🔤 Total de tokens: {total_tokens}")
    print(f"📝 Logs salvos em: logs/test_chatbot.log")
    
    logger.info(f"Testes concluídos: {successful_queries}/{len(test_queries)} sucessos")

if __name__ == "__main__":
    run_test_queries() 