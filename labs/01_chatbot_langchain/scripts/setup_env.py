#!/usr/bin/env python3
"""
Script para configurar automaticamente o ambiente virtual do projeto
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso!")
            if result.stdout.strip():
                print(f"   Saída: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Erro!")
            print(f"   Erro: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False
    return True

def check_python_version():
    """Verifica a versão do Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ Versão do Python compatível!")
        return True
    else:
        print("⚠️  Recomenda-se Python 3.11 ou superior")
        return False

def create_venv():
    """Cria o ambiente virtual"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("📁 Ambiente virtual já existe!")
        return True
    
    # Comando para criar ambiente virtual
    if platform.system() == "Windows":
        cmd = "python -m venv .venv"
    else:
        cmd = "python3 -m venv .venv"
    
    return run_command(cmd, "Criando ambiente virtual")

def install_dependencies():
    """Instala as dependências"""
    # Comando para ativar e instalar dependências
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip install -r requirements.txt"
    else:
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip install -r requirements.txt"
    
    # Instalar dependências
    return run_command(pip_cmd, "Instalando dependências")

def create_env_file():
    """Cria arquivo .env de exemplo"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("📄 Arquivo .env já existe!")
        return True
    
    env_content = """# Configurações da API OpenAI
OPENAI_API_KEY=sua_chave_api_aqui

# Configurações do modelo
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7

# Configurações de performance
MAX_RESPONSE_TIME=3.0
MIN_SUCCESS_RATE=95.0

# Configurações de arquivos
TEST_QUERIES_FILE=input/inputs.txt
LOG_FILE=logs/app.log
METRICS_FILE=metrics/metrics_report.json
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
        print("⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua chave da API OpenAI!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = ["logs", "reports", "metrics", "input"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Diretório {dir_name} criado!")
        else:
            print(f"📁 Diretório {dir_name} já existe!")

def show_next_steps():
    """Mostra os próximos passos"""
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    
    if platform.system() == "Windows":
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Ativar o ambiente virtual:")
        print("   .venv\\Scripts\\activate")
        print("\n2. Editar o arquivo .env e adicionar sua chave da API OpenAI")
        print("\n3. Executar o projeto:")
        print("   python main.py")
        print("\n4. Analisar logs:")
        print("   python run_analysis.py")
        print("\n5. Desativar o ambiente virtual:")
        print("   deactivate")
    else:
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Ativar o ambiente virtual:")
        print("   source .venv/bin/activate")
        print("\n2. Editar o arquivo .env e adicionar sua chave da API OpenAI")
        print("\n3. Executar o projeto:")
        print("   python main.py")
        print("\n4. Analisar logs:")
        print("   python run_analysis.py")
        print("\n5. Desativar o ambiente virtual:")
        print("   deactivate")

def main():
    """Função principal"""
    print("🚀 CONFIGURADOR DE AMBIENTE - Lab01 Chatbot LangChain")
    print("="*60)
    
    # Verificar versão do Python
    if not check_python_version():
        print("❌ Versão do Python incompatível!")
        return
    
    # Criar diretórios
    create_directories()
    
    # Criar ambiente virtual
    if not create_venv():
        print("❌ Falha ao criar ambiente virtual!")
        return
    
    # Instalar dependências
    if not install_dependencies():
        print("❌ Falha ao instalar dependências!")
        return
    
    # Criar arquivo .env
    create_env_file()
    
    # Mostrar próximos passos
    show_next_steps()

if __name__ == "__main__":
    main() 