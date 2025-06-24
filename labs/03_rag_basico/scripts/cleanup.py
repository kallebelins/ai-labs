#!/usr/bin/env python3
"""
Script de limpeza para o Sistema RAG Básico
Remove arquivos temporários e logs antigos
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def cleanup_files():
    """Remove arquivos temporários e logs antigos"""
    print("🧹 Iniciando limpeza do Sistema RAG Básico...")
    
    # Diretórios para limpar
    cleanup_dirs = ["logs", "metrics", "reports", "data"]
    
    for dir_name in cleanup_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"📁 Limpando diretório: {dir_name}")
            
            # Remove arquivos antigos (mais de 7 dias)
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    # Verifica se o arquivo é antigo
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        try:
                            file_path.unlink()
                            print(f"   🗑️ Removido: {file_path.name}")
                        except Exception as e:
                            print(f"   ❌ Erro ao remover {file_path.name}: {e}")
    
    # Remove ambiente virtual se existir
    venv_path = Path("venv")
    if venv_path.exists():
        print("📦 Removendo ambiente virtual...")
        try:
            shutil.rmtree(venv_path)
            print("   ✅ Ambiente virtual removido")
        except Exception as e:
            print(f"   ❌ Erro ao remover ambiente virtual: {e}")
    
    # Remove arquivos de cache Python
    cache_dirs = [".pytest_cache", "__pycache__"]
    for cache_dir in cache_dirs:
        cache_path = Path(cache_dir)
        if cache_path.exists():
            print(f"🗂️ Removendo cache: {cache_dir}")
            try:
                shutil.rmtree(cache_path)
                print(f"   ✅ Cache removido: {cache_dir}")
            except Exception as e:
                print(f"   ❌ Erro ao remover cache {cache_dir}: {e}")
    
    # Remove arquivos .pyc
    for pyc_file in Path(".").rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"   🗑️ Removido: {pyc_file.name}")
        except Exception as e:
            print(f"   ❌ Erro ao remover {pyc_file.name}: {e}")
    
    print("✅ Limpeza concluída!")

def main():
    """Função principal"""
    cleanup_files()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main()) 