#!/usr/bin/env python3
"""
Script principal do Sistema RAG Avançado
Interface de linha de comando para interagir com o sistema RAG avançado
"""

import sys
import logging
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem


def print_banner():
    """Exibe banner de boas-vindas"""
    print("=" * 60)
    print("🚀 SISTEMA RAG AVANÇADO")
    print("=" * 60)
    print("💡 Comandos disponíveis:")
    print("   - Digite sua pergunta normalmente")
    print("   - '/help' - Mostra esta ajuda")
    print("   - '/status' - Mostra status do sistema")
    print("   - '/add' - Adiciona documentos ao sistema")
    print("   - '/metrics' - Mostra métricas atuais")
    print("   - '/features' - Mostra recursos avançados")
    print("   - '/quit' ou '/exit' - Sair do sistema")
    print("=" * 60)
    print()


def print_status(rag_system):
    """Exibe status do sistema RAG avançado"""
    system_info = rag_system.get_system_info()
    
    print("\n📊 STATUS DO SISTEMA RAG AVANÇADO:")
    print(f"   - Modelo: {system_info['model_name']}")
    print(f"   - Temperatura: {system_info['temperature']}")
    print(f"   - Modo de teste: {'Sim' if system_info['test_mode'] else 'Não'}")
    print(f"   - Vetorstore disponível: {'Sim' if system_info['vectorstore_available'] else 'Não'}")
    print(f"   - Cross-Encoder disponível: {'Sim' if system_info['cross_encoder_available'] else 'Não'}")
    print(f"   - BM25 disponível: {'Sim' if system_info['bm25_available'] else 'Não'}")
    print(f"   - Documentos: {system_info['documents_count']}")
    print(f"   - Histórico de feedback: {system_info['feedback_history_size']}")
    print()


def print_features(rag_system):
    """Exibe recursos avançados do sistema"""
    system_info = rag_system.get_system_info()
    
    print("\n🚀 RECURSOS AVANÇADOS:")
    advanced_features = system_info.get('advanced_features', {})
    for feature, enabled in advanced_features.items():
        status = "✅" if enabled else "❌"
        feature_name = feature.replace('_', ' ').title()
        print(f"   {status} {feature_name}")
    
    if 'performance_metrics' in system_info:
        perf = system_info['performance_metrics']
        print(f"\n📈 MÉTRICAS DE PERFORMANCE:")
        print(f"   - Recall médio: {perf.get('avg_recall', 0):.1%}")
        print(f"   - Precisão média: {perf.get('avg_precision', 0):.1%}")
    print()


def add_documents_interactive(rag_system):
    """Interface interativa para adicionar documentos"""
    print("\n📄 ADICIONAR DOCUMENTOS")
    print("Digite os documentos (digite 'fim' em uma linha vazia para terminar):")
    
    documents = []
    metadata_list = []
    
    doc_count = 1
    while True:
        print(f"\n--- Documento {doc_count} ---")
        print("Digite o conteúdo do documento:")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "fim":
                break
            lines.append(line)
        
        if not lines:
            break
        
        content = "\n".join(lines)
        documents.append(content)
        
        # Metadados simples
        metadata = {
            "source": f"user_input_{doc_count}",
            "added_by": "interactive"
        }
        metadata_list.append(metadata)
        
        doc_count += 1
    
    if documents:
        # Nota: O sistema avançado não tem método add_documents implementado
        print(f"\n⚠️ Adição de documentos não implementada no sistema avançado")
        print(f"   Use o script setup_documents.py para adicionar documentos")
    else:
        print("\n❌ Nenhum documento foi adicionado.")


def main():
    """Função principal"""
    # Configura logging
    logger = setup_logging("logs/rag_system_advanced.log")
    logger.info("Iniciando Sistema RAG Avançado")
    
    try:
        # Carrega configuração
        print("🔧 Carregando configurações...")
        config = load_config()
        
        # Inicializa sistema RAG avançado
        print("🚀 Inicializando sistema RAG avançado...")
        rag_system = RAGSystem(config, logger)
        
        print("✅ Sistema RAG avançado inicializado com sucesso!")
        print_banner()
        
        # Loop principal de interação
        while True:
            try:
                # Obtém input do usuário
                user_input = input("👤 Você: ").strip()
                
                # Comandos especiais
                if user_input.lower() in ['/quit', '/exit']:
                    print("👋 Até logo! Obrigado por usar o Sistema RAG Avançado!")
                    break
                
                elif user_input.lower() == '/help':
                    print_banner()
                    continue
                
                elif user_input.lower() == '/status':
                    print_status(rag_system)
                    continue
                
                elif user_input.lower() == '/features':
                    print_features(rag_system)
                    continue
                
                elif user_input.lower() == '/add':
                    add_documents_interactive(rag_system)
                    continue
                
                elif user_input.lower() == '/metrics':
                    # Aqui você poderia implementar exibição de métricas
                    print("📊 Métricas serão implementadas em versão futura")
                    continue
                
                elif not user_input:
                    continue
                
                # Processa query do usuário
                print("🤖 Sistema RAG Avançado: ", end="", flush=True)
                result = rag_system.process_query(user_input)
                
                if result["success"]:
                    print(result["answer"])
                    
                    # Log da interação
                    logger.info(f"Query: {user_input}")
                    logger.info(f"Resposta: {result['answer']}")
                    logger.info(f"Tempo de resposta: {result['response_time']:.2f}s")
                    logger.info(f"Documentos usados: {result['documents_used']}")
                    logger.info(f"Recall de contexto: {result['context_recall']:.2f}")
                    logger.info(f"Precisão: {result['precision']:.2f}")
                    
                    # Informações específicas do sistema avançado
                    if 'expanded_queries' in result:
                        logger.info(f"Queries expandidas: {len(result['expanded_queries'])}")
                    if 'query_context' in result:
                        context = result['query_context']
                        logger.info(f"Tipo de query: {context.get('type', 'N/A')}")
                    
                    # Mostra contexto usado (opcional)
                    if result["documents_used"] > 0:
                        print(f"\n📄 Contexto usado ({result['documents_used']} documentos):")
                        print("-" * 40)
                        print(result["context"][:200] + "..." if len(result["context"]) > 200 else result["context"])
                        print("-" * 40)
                else:
                    print(f"❌ Erro: {result['error_message']}")
                    logger.error(f"Erro ao processar query: {result['error_message']}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrompido pelo usuário. Até logo!")
                break
                
            except Exception as e:
                print(f"❌ Erro durante a interação: {e}")
                logger.error(f"Erro na interação: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Erro fatal ao inicializar o sistema RAG avançado: {e}")
        logger.error(f"Erro fatal na inicialização: {e}")
        return 1
    
    logger.info("Sistema RAG avançado finalizado")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 