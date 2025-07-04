#!/usr/bin/env python3
"""
Script de limpeza do ambiente do Sistema RAG Avançado
Remove bancos ChromaDB, métricas, relatórios, logs e documentos de exemplo
"""

import shutil
from pathlib import Path

# Diretórios e arquivos a serem removidos
TARGETS = [
    'data/chroma_db',
    'data/chroma_db_advanced',
    'data/chroma_db_real',
    'metrics/rag_metrics.json',
    'logs',
    'reports',
    'data/real_documents.txt',
]

def remove_path(path_str):
    path = Path(path_str)
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
        print(f'Removido diretório: {path}')
    elif path.is_file():
        path.unlink(missing_ok=True)
        print(f'Removido arquivo: {path}')
    else:
        # Pode ser um glob pattern
        for p in path.parent.glob(path.name):
            if p.is_file():
                p.unlink(missing_ok=True)
                print(f'Removido arquivo: {p}')
            elif p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
                print(f'Removido diretório: {p}')

def main():
    print('🧹 Limpando ambiente do Sistema RAG Avançado...')
    for target in TARGETS:
        remove_path(target)
    print('✅ Limpeza concluída!')

if __name__ == '__main__':
    main() 