#!/usr/bin/env python3
"""
Script simples para aplicar otimizações básicas ao sistema RAG
"""

import json
from pathlib import Path

def apply_basic_optimizations():
    """Aplica otimizações básicas ao sistema RAG"""
    
    print("🎯 APLICANDO OTIMIZAÇÕES BÁSICAS")
    print("=" * 40)
    
    # Configurações otimizadas básicas
    basic_config = {
        "chunk_size": 250,
        "chunk_overlap": 150,
        "vectorstore_search_k": 8,
        "similarity_threshold": 0.1,
        "expansion_count": 3,
        "temperature": 0.2
    }
    
    # Carrega configuração atual
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Aplica otimizações
    config.update(basic_config)
    
    # Salva configuração otimizada
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Otimizações básicas aplicadas:")
    print(f"   • Chunk size: {basic_config['chunk_size']}")
    print(f"   • Chunk overlap: {basic_config['chunk_overlap']}")
    print(f"   • Search K: {basic_config['vectorstore_search_k']}")
    print(f"   • Similarity threshold: {basic_config['similarity_threshold']}")
    print(f"   • Query expansion: {basic_config['expansion_count']}")
    print(f"   • Temperature: {basic_config['temperature']}")
    
    return True

if __name__ == "__main__":
    apply_basic_optimizations()
