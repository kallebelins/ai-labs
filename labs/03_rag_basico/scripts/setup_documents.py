#!/usr/bin/env python3
"""
Script para carregar documentos no sistema RAG
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem


def load_sample_documents():
    """Carrega documentos de exemplo no sistema RAG"""
    
    # Configura logging
    logger = setup_logging("logs/setup_documents.log")
    logger.info("Iniciando carregamento de documentos")
    
    try:
        # Carrega configuração
        print("🔧 Carregando configurações...")
        config = load_config()
        
        # Inicializa sistema RAG
        print("🤖 Inicializando sistema RAG...")
        rag_system = RAGSystem(config, logger)
        
        # Carrega documentos do arquivo
        documents_file = Path("input/sample_documents.txt")
        if not documents_file.exists():
            print("❌ Arquivo de documentos não encontrado")
            return False
        
        print("📄 Carregando documentos...")
        with open(documents_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Divide o conteúdo em documentos separados
        documents = [doc.strip() for doc in content.split("\n\n") if doc.strip()]
        
        # Metadados para cada documento
        metadata_list = []
        for i, doc in enumerate(documents):
            metadata = {
                "source": f"sample_doc_{i+1}",
                "type": "sample",
                "index": i
            }
            metadata_list.append(metadata)
        
        # Adiciona documentos ao sistema
        rag_system.add_documents(documents, metadata_list)
        
        print(f"✅ {len(documents)} documentos carregados com sucesso!")
        
        # Mostra informações do sistema
        system_info = rag_system.get_system_info()
        print(f"\n📊 Informações do sistema:")
        print(f"   - Modo de teste: {'Sim' if system_info['test_mode'] else 'Não'}")
        print(f"   - Vetorstore disponível: {'Sim' if system_info['vectorstore_available'] else 'Não'}")
        print(f"   - Documentos: {system_info['documents_count']}")
        
        logger.info(f"Carregamento concluído - {len(documents)} documentos")
        return True
        
    except Exception as e:
        error_msg = f"Erro ao carregar documentos: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return False


if __name__ == "__main__":
    success = load_sample_documents()
    sys.exit(0 if success else 1) 