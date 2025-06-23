#!/usr/bin/env python3
"""
Exemplo de uso real do Chatbot LangChain - Interface Interativa
"""

import logging
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para que os imports funcionem
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.chatbot import ChatbotEngine

def get_user_input():
    """Obtém entrada do usuário de forma interativa"""
    try:
        print("\n" + "="*60)
        print("🤖 CHATBOT LANGCHAIN - INTERFACE INTERATIVA")
        print("="*60)
        print("💡 Digite sua pergunta (ou 'sair' para encerrar):")
        print("-" * 60)
        
        user_input = input("👤 Você: ").strip()
        
        if not user_input:
            print("⚠️  Por favor, digite uma pergunta válida.")
            return get_user_input()
            
        return user_input
        
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando chatbot...")
        sys.exit(0)
    except EOFError:
        print("\n\n👋 Encerrando chatbot...")
        sys.exit(0)

def display_response(pergunta, resultado):
    """Exibe a resposta do chatbot de forma formatada"""
    print("\n" + "🤖 Chatbot: " + "="*50)
    print(resultado["response"])
    print("="*60)
    
    # Exibe métricas de forma amigável
    print(f"📊 Métricas:")
    print(f"   ⏱️  Tempo de resposta: {resultado['response_time']:.3f}s")
    print(f"   🔤 Tokens utilizados: {resultado['tokens_used']}")
    print(f"   🎯 Confiança: {resultado['confidence']:.2f}")
    
    if not resultado["success"]:
        print(f"   ❌ Erro: {resultado['error_message']}")

def main():
    # Configura logging estruturado (JSON)
    logger = setup_logging("logs/app.log")
    logger.info("Iniciando chatbot interativo.")

    # Carrega configurações e inicializa chatbot
    try:
        config = load_config()
        chatbot = ChatbotEngine(config)
        logger.info("Chatbot inicializado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao inicializar chatbot: {e}")
        logger.error(f"Erro na inicialização: {e}")
        return

    print("🚀 Chatbot LangChain iniciado!")
    print("📝 As conversas serão salvas em logs/app.log")
    
    # Loop principal de interação
    while True:
        try:
            # Obtém entrada do usuário
            pergunta = get_user_input()
            
            # Verifica se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("👋 Obrigado por usar o Chatbot LangChain!")
                logger.info("Usuário encerrou a sessão.")
                break
            
            # Log da pergunta
            logger.info(f"Pergunta do usuário: {pergunta}")
            
            # Processa a pergunta
            print("🔄 Processando...")
            resultado = chatbot.process_query(pergunta)
            
            # Exibe resposta
            display_response(pergunta, resultado)
            
            # Log da resposta e métricas
            logger.info(f"Resposta: {resultado['response']}")
            logger.info(f"Métricas: tempo={resultado['response_time']:.3f}s, tokens={resultado['tokens_used']}, confiança={resultado['confidence']:.2f}")
            
            if not resultado["success"]:
                logger.error(f"Erro no processamento: {resultado['error_message']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando chatbot...")
            logger.info("Sessão interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            logger.error(f"Erro inesperado: {e}")
            continue

if __name__ == "__main__":
    main() 