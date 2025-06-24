#!/usr/bin/env python3
"""
Script de configuração automática do ambiente para o Chatbot com Memória Longa
"""

import os
import sys
import subprocess
from pathlib import Path

LAB_ROOT = Path(__file__).parent.parent.resolve()
VENV_DIR = LAB_ROOT / ".venv"
REQUIREMENTS = LAB_ROOT / "requirements.txt"
ENV_FILE = LAB_ROOT / ".env"

EXAMPLE_ENV = """
OPENAI_API_KEY=sua_chave_api_aqui
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_RESPONSE_TIME=3.0
MIN_SUCCESS_RATE=95.0
MEMORY_WINDOW=10
MAX_SUMMARY_TOKENS=2000
MEMORY_PERSISTENCE_PATH=data/chroma_db
MEMORY_SEARCH_K=3
MEMORY_CHUNK_SIZE=1000
MEMORY_CHUNK_OVERLAP=200
"""

def create_venv():
    if not VENV_DIR.exists():
        print(f"[INFO] Criando ambiente virtual em {VENV_DIR}...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)])
    else:
        print(f"[INFO] Ambiente virtual já existe em {VENV_DIR}.")

def install_requirements():
    pip_exec = VENV_DIR / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    print(f"[INFO] Instalando dependências do requirements.txt...")
    subprocess.run([str(pip_exec), "install", "-r", str(REQUIREMENTS)])

def create_env_file():
    if not ENV_FILE.exists():
        print(f"[INFO] Criando arquivo .env de exemplo...")
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write(EXAMPLE_ENV.strip())
        print(f"[INFO] Edite o arquivo .env e adicione sua chave da API OpenAI.")
    else:
        print(f"[INFO] Arquivo .env já existe.")

def create_dirs():
    for d in [LAB_ROOT / "logs", LAB_ROOT / "metrics", LAB_ROOT / "data", LAB_ROOT / "reports"]:
        d.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Diretório garantido: {d}")

def main():
    print("🚀 Configuração automática do ambiente - Chatbot Memória Longa")
    create_venv()
    install_requirements()
    create_env_file()
    create_dirs()
    print("✅ Ambiente configurado! Siga as instruções no README para rodar o laboratório.")

if __name__ == "__main__":
    main() 