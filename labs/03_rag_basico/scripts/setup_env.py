#!/usr/bin/env python3
"""
Script de configuração do ambiente para o Sistema RAG Básico
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Configura o ambiente para o sistema RAG"""
    print("🔧 Configurando ambiente para Sistema RAG Básico...")
    
    # Define variáveis de ambiente
    os.environ["PYTHONPATH"] = "."
    os.environ["TEST_MODE"] = "true"
    
    # Cria diretórios necessários
    directories = ["logs", "metrics", "reports", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório criado: {directory}")
    
    # Verifica se existe ambiente virtual
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Criando ambiente virtual...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Ambiente virtual criado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar ambiente virtual: {e}")
            return False
    
    # Instala dependências
    print("📦 Instalando dependências...")
    try:
        # Determina o comando pip correto
        if os.name == 'nt':  # Windows
            pip_cmd = "venv\\Scripts\\pip"
        else:  # Unix/Linux/Mac
            pip_cmd = "venv/bin/pip"
        
        # Instala dependências
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    
    print("🎉 Ambiente configurado com sucesso!")
    print("\n📋 Para ativar o ambiente virtual:")
    if os.name == 'nt':  # Windows
        print("   .\\venv\\Scripts\\Activate.ps1")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n🚀 Para executar o sistema:")
    print("   python scripts/main.py")
    
    return True

def main():
    """Função principal"""
    success = setup_environment()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 