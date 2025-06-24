#!/usr/bin/env python3
"""
Script principal do Chatbot com Memória Longa
Interface de linha de comando para interagir com o chatbot
"""

import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.chatbot import LongTermMemoryChatbot


def print_banner():
    """Exibe banner de boas-vindas"""
    print("=" * 60)
    print("🤖 CHATBOT COM MEMÓRIA LONGA")
    print("=" * 60)
    print("💡 Comandos disponíveis:")
    print("   - Digite sua mensagem normalmente")
    print("   - '/help' - Mostra esta ajuda")
    print("   - '/clear' - Limpa a memória da conversa")
    print("   - '/status' - Mostra status da memória")
    print("   - '/summary' - Mostra resumo da conversa")
    print("   - '/quit' ou '/exit' - Sair do chatbot")
    print("=" * 60)
    print()


def print_status(chatbot):
    """Exibe status da memória do chatbot"""
    print("\n📊 STATUS DA MEMÓRIA:")
    print(f"   - Memória de conversa: {len(chatbot.conversation_memory.chat_memory.messages)} mensagens")
    print(f"   - Resumo disponível: {'Sim' if chatbot.summary_memory.buffer else 'Não'}")
    print(f"   - Documentos na memória longa: {chatbot.vectorstore._collection.count() if hasattr(chatbot.vectorstore, '_collection') else 'N/A'}")
    print()


def main():
    """Função principal"""
    # Configura logging
    logger = setup_logging("logs/main_chatbot.log")
    logger.info("Iniciando Chatbot com Memória Longa")
    
    try:
        # Carrega configuração
        print("🔧 Carregando configurações...")
        config = load_config()
        
        # Inicializa chatbot
        print("🤖 Inicializando chatbot...")
        chatbot = LongTermMemoryChatbot(config, logger)
        
        print("✅ Chatbot inicializado com sucesso!")
        print_banner()
        
        # Loop principal de conversa
        while True:
            try:
                # Obtém input do usuário
                user_input = input("👤 Você: ").strip()
                
                # Comandos especiais
                if user_input.lower() in ['/quit', '/exit']:
                    print("👋 Até logo! Obrigado por usar o Chatbot com Memória Longa!")
                    break
                
                elif user_input.lower() == '/help':
                    print_banner()
                    continue
                
                elif user_input.lower() == '/clear':
                    chatbot.clear_memory()
                    print("🧹 Memória da conversa limpa!")
                    continue
                
                elif user_input.lower() == '/status':
                    print_status(chatbot)
                    continue
                
                elif user_input.lower() == '/summary':
                    summary = chatbot.get_conversation_summary()
                    print(f"\n📝 RESUMO DA CONVERSA:\n{summary}\n")
                    continue
                
                elif not user_input:
                    continue
                
                # Processa mensagem do usuário
                print("🤖 Chatbot: ", end="", flush=True)
                result = chatbot.process_query(user_input)
                
                if result["success"]:
                    print(result["response"])
                    
                    # Log da interação
                    logger.info(f"Usuário: {user_input}")
                    logger.info(f"Chatbot: {result['response']}")
                    logger.info(f"Tempo de resposta: {result['response_time']:.2f}s")
                    logger.info(f"Tokens usados: {result['tokens_used']}")
                    logger.info(f"Confiança: {result['confidence']:.2f}")
                else:
                    print(f"❌ Erro: {result['error_message']}")
                    logger.error(f"Erro ao processar query: {result['error_message']}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrompido pelo usuário. Até logo!")
                break
                
            except Exception as e:
                print(f"❌ Erro durante a conversa: {e}")
                logger.error(f"Erro na conversa: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Erro fatal ao inicializar o chatbot: {e}")
        logger.error(f"Erro fatal na inicialização: {e}")
        return 1
    
    logger.info("Chatbot finalizado")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 