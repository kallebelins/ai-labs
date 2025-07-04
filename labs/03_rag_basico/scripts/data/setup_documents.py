#!/usr/bin/env python3
"""
Script para configurar documentos no Sistema RAG Avançado
Carrega documentos de exemplo e os adiciona ao vetorstore
"""

import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem


def load_sample_documents():
    """Carrega documentos de exemplo"""
    documents = [
        {
            "content": """A inteligência artificial (IA) é um campo da computação que busca criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana. Isso inclui reconhecimento de fala, tomada de decisões, tradução entre idiomas e muito mais.

A IA pode ser dividida em várias subcategorias:
- Machine Learning: algoritmos que aprendem com dados
- Deep Learning: redes neurais com múltiplas camadas
- Processamento de Linguagem Natural: compreensão e geração de texto
- Visão Computacional: análise e interpretação de imagens

A IA está transformando diversos setores, desde saúde até finanças, e continua evoluindo rapidamente.""",
            "metadata": {"source": "ai_overview.txt", "topic": "Inteligência Artificial", "type": "overview"}
        },
        {
            "content": """Machine Learning é um subcampo da inteligência artificial que permite aos computadores aprenderem sem serem explicitamente programados para tarefas específicas. Em vez disso, os algoritmos de ML identificam padrões nos dados e fazem previsões ou decisões baseadas nesses padrões.

Tipos principais de Machine Learning:
1. Aprendizado Supervisionado: usa dados rotulados para treinar modelos
2. Aprendizado Não Supervisionado: encontra padrões em dados não rotulados
3. Aprendizado por Reforço: aprende através de tentativa e erro

Aplicações comuns incluem:
- Sistemas de recomendação
- Detecção de fraudes
- Análise de sentimentos
- Previsão de vendas
- Diagnóstico médico""",
            "metadata": {"source": "machine_learning.txt", "topic": "Machine Learning", "type": "explanation"}
        },
        {
            "content": """Deep Learning é uma subcategoria do machine learning que utiliza redes neurais artificiais com múltiplas camadas (por isso "deep") para processar dados complexos. Essas redes são inspiradas na estrutura do cérebro humano.

Características principais:
- Múltiplas camadas de neurônios artificiais
- Aprendizado hierárquico de características
- Requer grandes quantidades de dados
- Computação intensiva

Aplicações de sucesso:
- Reconhecimento de imagem e vídeo
- Processamento de linguagem natural
- Tradução automática
- Reconhecimento de fala
- Jogos e robótica

Frameworks populares incluem TensorFlow, PyTorch e Keras.""",
            "metadata": {"source": "deep_learning.txt", "topic": "Deep Learning", "type": "explanation"}
        },
        {
            "content": """RAG (Retrieval-Augmented Generation) é uma técnica que combina recuperação de informações com geração de texto para produzir respostas mais precisas e fundamentadas. Em vez de gerar respostas apenas com o conhecimento pré-treinado do modelo, o RAG primeiro recupera documentos relevantes e depois usa essas informações para gerar a resposta.

Vantagens do RAG:
- Reduz alucinações (informações falsas)
- Permite acesso a informações atualizadas
- Melhora a precisão das respostas
- Facilita a verificação de fontes
- Permite personalização com dados específicos

Componentes típicos:
1. Sistema de recuperação (vectorstore)
2. Gerador de texto (LLM)
3. Pipeline de processamento
4. Sistema de rankeamento""",
            "metadata": {"source": "rag_system.txt", "topic": "RAG", "type": "explanation"}
        },
        {
            "content": """LangChain é um framework para desenvolvimento de aplicações com grandes modelos de linguagem (LLMs). Ele oferece ferramentas e abstrações para construir aplicações complexas de IA de forma mais fácil e estruturada.

Principais componentes:
- Chains: sequências de operações
- Agents: sistemas autônomos que tomam decisões
- Memory: persistência de informações entre interações
- Tools: integração com APIs e serviços externos
- Prompts: gerenciamento de prompts de forma eficiente

Casos de uso:
- Chatbots inteligentes
- Agentes de automação
- Sistemas de análise de dados
- Aplicações de processamento de documentos
- Integração com bases de dados

LangChain suporta múltiplos provedores de LLM, incluindo OpenAI, Anthropic, e modelos open-source.""",
            "metadata": {"source": "langchain.txt", "topic": "LangChain", "type": "explanation"}
        },
        {
            "content": """ChromaDB é uma base de dados vetorial open-source projetada especificamente para aplicações de inteligência artificial e machine learning. Ela é otimizada para armazenar e buscar embeddings (representações vetoriais de texto, imagens ou outros dados).

Características principais:
- Armazenamento de embeddings de alta dimensionalidade
- Busca por similaridade eficiente
- Suporte a metadados
- Persistência de dados
- API Python simples
- Escalabilidade horizontal

Aplicações típicas:
- Sistemas de recomendação
- Busca semântica
- Detecção de duplicatas
- Análise de similaridade
- Sistemas RAG

Vantagens:
- Fácil de usar
- Performance otimizada
- Código aberto
- Comunidade ativa
- Integração com frameworks populares""",
            "metadata": {"source": "chromadb.txt", "topic": "ChromaDB", "type": "explanation"}
        },
        {
            "content": """Embeddings são representações vetoriais de dados (texto, imagens, áudio) que capturam o significado semântico em um espaço vetorial de alta dimensionalidade. Esses vetores permitem que computadores compreendam e comparem o significado de diferentes elementos.

Como funcionam:
- Texto é convertido em vetores numéricos
- Vetores similares representam conceitos similares
- Distância entre vetores indica similaridade semântica
- Permitem operações matemáticas com significado

Tipos de embeddings:
- Word embeddings (Word2Vec, GloVe)
- Sentence embeddings (BERT, USE)
- Document embeddings
- Multimodal embeddings

Aplicações:
- Busca semântica
- Clustering de documentos
- Análise de sentimentos
- Tradução automática
- Sistemas de recomendação
- RAG e chatbots""",
            "metadata": {"source": "embeddings.txt", "topic": "Embeddings", "type": "explanation"}
        },
        {
            "content": """OpenAI é uma empresa de pesquisa em inteligência artificial que desenvolve e oferece APIs de linguagem natural de ponta. Sua missão é garantir que a inteligência artificial geral beneficie toda a humanidade.

Principais produtos:
- GPT-4: modelo de linguagem mais avançado
- GPT-3.5: modelo mais rápido e econômico
- DALL-E: geração de imagens a partir de texto
- Whisper: reconhecimento de fala
- Embeddings: representações vetoriais de texto

APIs disponíveis:
- Chat Completions: para conversas interativas
- Completions: para geração de texto
- Embeddings: para conversão de texto em vetores
- Fine-tuning: para personalização de modelos

Casos de uso:
- Chatbots e assistentes virtuais
- Geração de conteúdo
- Análise de texto
- Tradução automática
- Programação assistida
- Educação e treinamento""",
            "metadata": {"source": "openai.txt", "topic": "OpenAI", "type": "explanation"}
        }
    ]
    
    return documents


def main():
    """Função principal"""
    print("📄 CONFIGURANDO DOCUMENTOS PARA O SISTEMA RAG AVANÇADO")
    print("=" * 60)
    
    # Configura logging
    logger = setup_logging("logs/setup_documents.log")
    logger.info("Iniciando configuração de documentos")
    
    try:
        # Carrega configuração
        print("🔧 Carregando configurações...")
        config = load_config()
        
        # Inicializa sistema RAG avançado
        print("🚀 Inicializando sistema RAG avançado...")
        rag_system = RAGSystem(config, logger)
        
        # Carrega documentos de exemplo
        print("📚 Carregando documentos de exemplo...")
        documents = load_sample_documents()
        
        print(f"✅ {len(documents)} documentos carregados")
        
        # Nota: O sistema avançado não tem método add_documents implementado
        # Os documentos são carregados automaticamente no modo de teste
        print("\n⚠️ Nota: O sistema avançado carrega documentos automaticamente")
        print("   Para adicionar documentos personalizados, modifique o código")
        
        # Mostra informações do sistema
        system_info = rag_system.get_system_info()
        print(f"\n📊 Status do sistema:")
        print(f"   - Documentos disponíveis: {system_info['documents_count']}")
        print(f"   - Vetorstore: {'Disponível' if system_info['vectorstore_available'] else 'Não disponível'}")
        print(f"   - Cross-Encoder: {'Disponível' if system_info['cross_encoder_available'] else 'Não disponível'}")
        print(f"   - BM25: {'Disponível' if system_info['bm25_available'] else 'Não disponível'}")
        
        print("\n✅ Configuração concluída!")
        logger.info("Configuração de documentos concluída com sucesso")
        
    except Exception as e:
        error_msg = f"Erro durante configuração: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 