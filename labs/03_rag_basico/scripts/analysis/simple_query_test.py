#!/usr/bin/env python3
"""
Teste simples de queries do sistema RAG.

Este script permite testar queries individuais e ver as respostas.
"""

import os
import sys
import json
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.rag_system import RAGSystem
from src.utils.config import load_config

def test_simple_queries():
    """Testa queries simples do sistema RAG"""
    
    print("🧪 TESTE SIMPLES DE QUERIES")
    print("=" * 50)
    
    # Carrega configuração
    config = load_config()
    config["test_mode"] = True
    
    # Inicializa sistema RAG
    rag_system = RAGSystem(config)
    
    # Queries de teste
    test_queries = [
        "O que é inteligência artificial?",
        "Explique machine learning",
        "Como funciona deep learning?",
        "O que é RAG?",
        "Defina embeddings"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 50)
        
        result = rag_system.process_query(query)
        
        if result["success"]:
            print(f"✅ Resposta: {result['answer']}")
            print(f"⏱️ Tempo: {result['response_time']:.2f}s")
            print(f"📄 Documentos usados: {result['documents_used']}")
        else:
            print(f"❌ Erro: {result.get('error_message', 'Erro desconhecido')}")
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")

if __name__ == "__main__":
    test_simple_queries() 