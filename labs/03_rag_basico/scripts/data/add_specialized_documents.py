#!/usr/bin/env python3
"""
Script para adicionar documentos especializados ao sistema RAG
"""

import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem

def create_specialized_documents():
    """Cria documentos especializados e casos de uso específicos"""
    
    documents = [
        # Casos de uso práticos
        {
            "content": """
            CASO DE USO: CHATBOT DE ATENDIMENTO COM RAG
            Implementação prática de um chatbot usando RAG para atendimento ao cliente.
            
            Arquitetura:
            1. Base de conhecimento: FAQ, manuais, políticas da empresa
            2. Pipeline de ingestão: PDF → chunks → embeddings → ChromaDB
            3. Query processing: classificação de intenção + busca semântica
            4. Response generation: contexto + prompt template + LLM
            
            Código exemplo:
            ```python
            from langchain.vectorstores import Chroma
            from langchain.embeddings import OpenAIEmbeddings
            from langchain.llms import OpenAI
            from langchain.chains import RetrievalQA
            
            # Configuração
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
            llm = OpenAI(temperature=0.7)
            
            # Chain de QA
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
            )
            
            # Uso
            response = qa_chain.run("Como cancelar minha assinatura?")
            ```
            
            Métricas importantes:
            - Taxa de resolução: >85%
            - Tempo de resposta: <3s
            - Satisfação do usuário: >4.5/5
            """,
            "metadata": {
                "topic": "chatbot_case_study",
                "type": "practical_implementation",
                "difficulty": "intermediate",
                "category": "use_case"
            }
        },
        
        {
            "content": """
            CASO DE USO: SISTEMA DE BUSCA DOCUMENTAL CORPORATIVO
            Sistema RAG para busca inteligente em documentos corporativos.
            
            Desafios:
            - Múltiplos formatos: PDF, Word, PowerPoint, Excel
            - Diferentes idiomas e terminologias técnicas
            - Controle de acesso e permissões
            - Escalabilidade para milhões de documentos
            
            Solução implementada:
            1. Preprocessing: OCR + extração de texto + limpeza
            2. Chunking inteligente: preserva estrutura de seções
            3. Embeddings híbridos: dense + sparse (BM25)
            4. Indexação hierárquica: departamento → tipo → documento
            5. Re-ranking por relevância e permissões
            
            Resultados:
            - 40% redução no tempo de busca
            - 60% aumento na precisão
            - 95% satisfação dos usuários
            - ROI de 300% em 6 meses
            
            Tecnologias utilizadas:
            - LangChain para orchestração
            - ChromaDB para vector storage
            - Elasticsearch para busca híbrida
            - FastAPI para API REST
            - Streamlit para interface
            """,
            "metadata": {
                "topic": "document_search_case_study",
                "type": "practical_implementation",
                "difficulty": "advanced",
                "category": "enterprise"
            }
        },
        
        {
            "content": """
            TUTORIAL: IMPLEMENTAÇÃO RAG PASSO-A-PASSO
            Guia completo para implementar um sistema RAG do zero.
            
            PASSO 1: Preparação dos dados
            ```python
            from langchain.document_loaders import PyPDFLoader, TextLoader
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            
            # Carregamento
            loader = PyPDFLoader("documento.pdf")
            documents = loader.load()
            
            # Chunking
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_documents(documents)
            ```
            
            PASSO 2: Criação de embeddings
            ```python
            from langchain.embeddings import OpenAIEmbeddings
            from langchain.vectorstores import Chroma
            
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory="./chroma_db"
            )
            ```
            
            PASSO 3: Configuração do retriever
            ```python
            retriever = vectorstore.as_retriever(
                search_type="mmr",  # Maximum Marginal Relevance
                search_kwargs={
                    "k": 5,
                    "lambda_mult": 0.7,
                    "fetch_k": 20
                }
            )
            ```
            
            PASSO 4: Chain de QA
            ```python
            from langchain.chains import RetrievalQA
            from langchain.llms import OpenAI
            
            llm = OpenAI(temperature=0.3, max_tokens=1000)
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            ```
            
            PASSO 5: Implementação com streaming
            ```python
            from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
            
            llm = OpenAI(
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()],
                temperature=0.3
            )
            ```
            
            Dicas de otimização:
            - Use cache para embeddings
            - Implemente re-ranking
            - Monitore métricas de qualidade
            - Teste diferentes estratégias de chunking
            """,
            "metadata": {
                "topic": "rag_tutorial",
                "type": "tutorial",
                "difficulty": "beginner",
                "category": "implementation"
            }
        },
        
        {
            "content": """
            EMBEDDINGS AVANÇADOS PARA RAG
            Técnicas avançadas para melhorar a qualidade dos embeddings.
            
            1. EMBEDDINGS HÍBRIDOS
            Combina dense embeddings (semântica) com sparse embeddings (keywords):
            
            ```python
            from sentence_transformers import SentenceTransformer
            from sklearn.feature_extraction.text import TfidfVectorizer
            import numpy as np
            
            class HybridEmbeddings:
                def __init__(self):
                    self.dense_model = SentenceTransformer('all-MiniLM-L6-v2')
                    self.sparse_model = TfidfVectorizer(max_features=5000)
                
                def embed_documents(self, texts):
                    # Dense embeddings
                    dense_emb = self.dense_model.encode(texts)
                    
                    # Sparse embeddings
                    sparse_emb = self.sparse_model.fit_transform(texts).toarray()
                    
                    # Concatenação ponderada
                    alpha = 0.7  # peso para dense
                    beta = 0.3   # peso para sparse
                    
                    hybrid_emb = np.concatenate([
                        alpha * dense_emb,
                        beta * sparse_emb
                    ], axis=1)
                    
                    return hybrid_emb
            ```
            
            2. FINE-TUNING DE EMBEDDINGS
            Adapta embeddings para domínio específico:
            
            ```python
            from sentence_transformers import SentenceTransformer, InputExample, losses
            from torch.utils.data import DataLoader
            
            # Carrega modelo base
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Dados de treino (pares query-documento relevante)
            train_examples = [
                InputExample(texts=['query1', 'documento_relevante1']),
                InputExample(texts=['query2', 'documento_relevante2']),
            ]
            
            # DataLoader
            train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
            
            # Loss function
            train_loss = losses.MultipleNegativesRankingLoss(model)
            
            # Fine-tuning
            model.fit(
                train_objectives=[(train_dataloader, train_loss)],
                epochs=3,
                warmup_steps=100
            )
            ```
            
            3. EMBEDDINGS MULTIMODAIS
            Para documentos com texto e imagens:
            
            ```python
            from transformers import CLIPModel, CLIPProcessor
            
            class MultimodalEmbeddings:
                def __init__(self):
                    self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
                    self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
                
                def embed_text(self, text):
                    inputs = self.processor(text=text, return_tensors="pt")
                    return self.model.get_text_features(**inputs)
                
                def embed_image(self, image):
                    inputs = self.processor(images=image, return_tensors="pt")
                    return self.model.get_image_features(**inputs)
            ```
            
            Métricas de avaliação:
            - Semantic similarity: cosine similarity
            - Retrieval accuracy: MAP@k, NDCG@k
            - Domain adaptation: performance on domain-specific tasks
            """,
            "metadata": {
                "topic": "advanced_embeddings",
                "type": "technical_guide",
                "difficulty": "advanced",
                "category": "embeddings"
            }
        },
        
        {
            "content": """
            MÉTRICAS E AVALIAÇÃO DE SISTEMAS RAG
            Guia completo para avaliar a performance de sistemas RAG.
            
            1. MÉTRICAS DE RECUPERAÇÃO
            
            NDCG (Normalized Discounted Cumulative Gain):
            ```python
            import numpy as np
            
            def dcg_at_k(relevances, k):
                relevances = np.array(relevances)[:k]
                return np.sum(relevances / np.log2(np.arange(2, len(relevances) + 2)))
            
            def ndcg_at_k(relevances, k):
                dcg = dcg_at_k(relevances, k)
                idcg = dcg_at_k(sorted(relevances, reverse=True), k)
                return dcg / idcg if idcg > 0 else 0
            ```
            
            MAP (Mean Average Precision):
            ```python
            def average_precision(relevances):
                precisions = []
                relevant_count = 0
                
                for i, rel in enumerate(relevances):
                    if rel > 0:
                        relevant_count += 1
                        precision = relevant_count / (i + 1)
                        precisions.append(precision)
                
                return np.mean(precisions) if precisions else 0
            
            def mean_average_precision(all_relevances):
                return np.mean([average_precision(rel) for rel in all_relevances])
            ```
            
            2. MÉTRICAS DE GERAÇÃO
            
            BLEU Score para comparação com referência:
            ```python
            from nltk.translate.bleu_score import sentence_bleu
            
            def calculate_bleu(reference, candidate):
                reference_tokens = reference.split()
                candidate_tokens = candidate.split()
                return sentence_bleu([reference_tokens], candidate_tokens)
            ```
            
            ROUGE Score para summarização:
            ```python
            from rouge_score import rouge_scorer
            
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            scores = scorer.score(reference, candidate)
            ```
            
            3. MÉTRICAS CUSTOMIZADAS
            
            Faithfulness (fidelidade ao contexto):
            ```python
            def calculate_faithfulness(context, answer, llm):
                prompt = f'''
                Contexto: {context}
                Resposta: {answer}
                
                A resposta é fiel ao contexto? Responda apenas Sim ou Não.
                '''
                result = llm.predict(prompt)
                return "sim" in result.lower()
            ```
            
            Answer Relevancy (relevância da resposta):
            ```python
            def calculate_answer_relevancy(question, answer, embeddings):
                q_emb = embeddings.embed_query(question)
                a_emb = embeddings.embed_query(answer)
                
                # Similaridade coseno
                similarity = np.dot(q_emb, a_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(a_emb))
                return similarity
            ```
            
            4. FRAMEWORK DE AVALIAÇÃO AUTOMÁTICA
            ```python
            class RAGEvaluator:
                def __init__(self, embeddings, llm):
                    self.embeddings = embeddings
                    self.llm = llm
                
                def evaluate_retrieval(self, queries, retrieved_docs, ground_truth):
                    ndcg_scores = []
                    map_scores = []
                    
                    for query, docs, truth in zip(queries, retrieved_docs, ground_truth):
                        # Calcula relevância
                        relevances = self._calculate_relevances(docs, truth)
                        
                        # Métricas
                        ndcg_scores.append(ndcg_at_k(relevances, 5))
                        map_scores.append(average_precision(relevances))
                    
                    return {
                        'ndcg@5': np.mean(ndcg_scores),
                        'map': np.mean(map_scores)
                    }
                
                def evaluate_generation(self, questions, answers, contexts):
                    faithfulness_scores = []
                    relevancy_scores = []
                    
                    for q, a, c in zip(questions, answers, contexts):
                        faithfulness_scores.append(self.calculate_faithfulness(c, a))
                        relevancy_scores.append(self.calculate_answer_relevancy(q, a))
                    
                    return {
                        'faithfulness': np.mean(faithfulness_scores),
                        'answer_relevancy': np.mean(relevancy_scores)
                    }
            ```
            
            Benchmarks recomendados:
            - MS MARCO para retrieval
            - Natural Questions para QA
            - BEIR para retrieval cross-domain
            - RAGAs para avaliação end-to-end
            """,
            "metadata": {
                "topic": "rag_evaluation",
                "type": "technical_guide",
                "difficulty": "advanced",
                "category": "evaluation"
            }
        }
    ]
    
    return documents

def main():
    """Adiciona documentos especializados ao sistema"""
    print("📚 ADICIONANDO DOCUMENTOS ESPECIALIZADOS")
    print("=" * 50)
    
    # Configura logging
    logger = setup_logging()
    
    # Carrega configuração
    config = load_config()
    
    # Inicializa sistema RAG
    print("🚀 Inicializando sistema RAG...")
    rag_system = RAGSystem(config, logger)
    
    # Cria documentos especializados
    print("📝 Criando documentos especializados...")
    documents = create_specialized_documents()
    
    # Adiciona ao sistema
    print(f"📖 Adicionando {len(documents)} documentos especializados...")
    
    # Converte para formato esperado pelo sistema
    formatted_docs = []
    for doc in documents:
        formatted_docs.append({
            "page_content": doc["content"],
            "metadata": doc["metadata"]
        })
    
    # Adiciona documentos
    try:
        rag_system.add_documents(formatted_docs)
        print(f"✅ {len(documents)} documentos especializados adicionados com sucesso!")
        
        # Mostra estatísticas
        print(f"\n📊 Estatísticas:")
        print(f"   • Casos de uso práticos: 2")
        print(f"   • Tutoriais técnicos: 1") 
        print(f"   • Guias avançados: 2")
        print(f"   • Total de documentos: {len(documents)}")
        
    except Exception as e:
        print(f"❌ Erro ao adicionar documentos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 