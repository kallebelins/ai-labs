#!/usr/bin/env python3
"""
Script para análise detalhada das queries que perdem pontos
Identifica padrões e oportunidades de melhoria no sistema RAG
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logging_config import setup_logging
from src.utils.config import load_config
from src.core.rag_system import RAGSystem


class QueryAnalyzer:
    """Analisador de queries para identificar problemas e oportunidades de melhoria"""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
        self.analysis_results = []
        
    def analyze_query_performance(self, query: str, expected_response: str = None) -> Dict[str, Any]:
        """
        Analisa performance detalhada de uma query
        
        Args:
            query: Query para analisar
            expected_response: Resposta esperada (opcional)
            
        Returns:
            Dicionário com análise detalhada
        """
        # Processa query
        result = self.rag_system.process_query(query)
        
        # Analisa documentos recuperados
        doc_analysis = self._analyze_retrieved_documents(query, result.get('relevant_documents', []))
        
        # Analisa resposta gerada
        response_analysis = self._analyze_response(query, result.get('response', ''), expected_response)
        
        # Calcula scores de qualidade
        quality_scores = self._calculate_quality_scores(query, result, doc_analysis, response_analysis)
        
        analysis = {
            'query': query,
            'success': result.get('success', False),
            'response_time': result.get('response_time', 0),
            'documents_used': result.get('documents_used', 0),
            'context_recall': result.get('context_recall', 0),
            'precision': result.get('precision', 0),
            'doc_analysis': doc_analysis,
            'response_analysis': response_analysis,
            'quality_scores': quality_scores,
            'rerank_weights': result.get('rerank_weights', {}),
            'timestamp': time.time()
        }
        
        self.analysis_results.append(analysis)
        return analysis
    
    def _analyze_retrieved_documents(self, query: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa os documentos recuperados"""
        if not documents:
            return {'relevance_score': 0, 'coverage_score': 0, 'diversity_score': 0, 'issues': ['Nenhum documento recuperado']}
        
        # Calcula relevância dos documentos
        relevance_scores = []
        query_words = set(query.lower().split())
        
        for doc in documents:
            content = doc['content'].lower()
            doc_words = set(content.split())
            
            # Overlap de palavras-chave
            overlap = len(query_words.intersection(doc_words)) / len(query_words) if query_words else 0
            
            # Densidade de palavras-chave
            density = len(query_words.intersection(doc_words)) / len(doc_words) if doc_words else 0
            
            # Comprimento do documento
            length_score = min(1.0, len(doc_words) / 50.0)  # Normaliza para documentos de ~50 palavras
            
            relevance_score = (overlap * 0.5 + density * 0.3 + length_score * 0.2)
            relevance_scores.append(relevance_score)
        
        # Calcula cobertura (quantos aspectos da query são cobertos)
        all_content = ' '.join([doc['content'].lower() for doc in documents])
        coverage_score = len(query_words.intersection(set(all_content.split()))) / len(query_words) if query_words else 0
        
        # Calcula diversidade (quão diferentes são os documentos)
        unique_words = set()
        for doc in documents:
            unique_words.update(doc['content'].lower().split())
        diversity_score = len(unique_words) / sum(len(doc['content'].split()) for doc in documents) if documents else 0
        
        # Identifica problemas
        issues = []
        if max(relevance_scores) < 0.3:
            issues.append('Baixa relevância dos documentos')
        if coverage_score < 0.5:
            issues.append('Baixa cobertura da query')
        if diversity_score < 0.3:
            issues.append('Baixa diversidade de documentos')
        if len(documents) < 3:
            issues.append('Poucos documentos recuperados')
        
        return {
            'relevance_score': sum(relevance_scores) / len(relevance_scores),
            'coverage_score': coverage_score,
            'diversity_score': diversity_score,
            'avg_doc_length': sum(len(doc['content'].split()) for doc in documents) / len(documents),
            'issues': issues
        }
    
    def _analyze_response(self, query: str, response: str, expected_response: str = None) -> Dict[str, Any]:
        """Analisa a resposta gerada"""
        if not response:
            return {'completeness': 0, 'relevance': 0, 'structure': 0, 'issues': ['Resposta vazia']}
        
        # Análise de completude
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        completeness = len(query_words.intersection(response_words)) / len(query_words) if query_words else 0
        
        # Análise de relevância (simplificada)
        relevance = min(1.0, len(response.split()) / 20.0)  # Respostas com pelo menos 20 palavras
        
        # Análise de estrutura
        structure_score = 0
        if 'baseado nos documentos' in response.lower() or 'segundo os documentos' in response.lower():
            structure_score += 0.5
        if response.count('"') >= 2:  # Citações
            structure_score += 0.3
        if len(response.split('.')) >= 2:  # Múltiplas frases
            structure_score += 0.2
        
        # Identifica problemas
        issues = []
        if completeness < 0.3:
            issues.append('Resposta não aborda a query adequadamente')
        if relevance < 0.5:
            issues.append('Resposta muito curta ou vaga')
        if structure_score < 0.5:
            issues.append('Resposta não segue formato esperado')
        if 'não encontrei' in response.lower():
            issues.append('Sistema não encontrou informações relevantes')
        
        return {
            'completeness': completeness,
            'relevance': relevance,
            'structure': structure_score,
            'response_length': len(response.split()),
            'issues': issues
        }
    
    def _calculate_quality_scores(self, query: str, result: Dict[str, Any], 
                                doc_analysis: Dict[str, Any], 
                                response_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calcula scores de qualidade geral"""
        # Score de recuperação (baseado nos documentos)
        retrieval_score = (
            doc_analysis['relevance_score'] * 0.4 +
            doc_analysis['coverage_score'] * 0.3 +
            doc_analysis['diversity_score'] * 0.3
        )
        
        # Score de geração (baseado na resposta)
        generation_score = (
            response_analysis['completeness'] * 0.4 +
            response_analysis['relevance'] * 0.3 +
            response_analysis['structure'] * 0.3
        )
        
        # Score geral
        overall_score = (retrieval_score * 0.6 + generation_score * 0.4)
        
        return {
            'retrieval_score': retrieval_score,
            'generation_score': generation_score,
            'overall_score': overall_score
        }
    
    def analyze_query_patterns(self) -> Dict[str, Any]:
        """Analisa padrões nas queries analisadas"""
        if not self.analysis_results:
            return {}
        
        # Agrupa queries por performance
        high_performance = []
        medium_performance = []
        low_performance = []
        
        for analysis in self.analysis_results:
            score = analysis['quality_scores']['overall_score']
            if score >= 0.8:
                high_performance.append(analysis)
            elif score >= 0.6:
                medium_performance.append(analysis)
            else:
                low_performance.append(analysis)
        
        # Analisa padrões
        patterns = {
            'total_queries': len(self.analysis_results),
            'high_performance_count': len(high_performance),
            'medium_performance_count': len(medium_performance),
            'low_performance_count': len(low_performance),
            'avg_overall_score': sum(a['quality_scores']['overall_score'] for a in self.analysis_results) / len(self.analysis_results),
            'common_issues': self._identify_common_issues(),
            'query_types': self._categorize_queries(),
            'recommendations': self._generate_recommendations()
        }
        
        return patterns
    
    def _identify_common_issues(self) -> List[str]:
        """Identifica problemas comuns"""
        all_issues = []
        for analysis in self.analysis_results:
            all_issues.extend(analysis['doc_analysis']['issues'])
            all_issues.extend(analysis['response_analysis']['issues'])
        
        # Conta frequência
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Retorna problemas mais frequentes
        return sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _categorize_queries(self) -> Dict[str, List[str]]:
        """Categoriza queries por tipo"""
        categories = {
            'definition': [],
            'explanation': [],
            'how_to': [],
            'comparison': [],
            'factual': []
        }
        
        for analysis in self.analysis_results:
            query = analysis['query'].lower()
            
            if any(word in query for word in ['o que é', 'defina', 'significa']):
                categories['definition'].append(analysis['query'])
            elif any(word in query for word in ['explique', 'como funciona', 'funciona']):
                categories['explanation'].append(analysis['query'])
            elif any(word in query for word in ['como fazer', 'como', 'passos']):
                categories['how_to'].append(analysis['query'])
            elif any(word in query for word in ['melhor', 'diferença', 'comparar']):
                categories['comparison'].append(analysis['query'])
            else:
                categories['factual'].append(analysis['query'])
        
        return categories
    
    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        # Analisa problemas comuns
        common_issues = self._identify_common_issues()
        
        if any('Baixa relevância' in issue for issue, count in common_issues):
            recommendations.append("Melhorar algoritmo de re-ranking para priorizar documentos mais relevantes")
        
        if any('Baixa cobertura' in issue for issue, count in common_issues):
            recommendations.append("Expandir base de conhecimento com mais documentos sobre tópicos específicos")
        
        if any('Resposta não segue formato' in issue for issue, count in common_issues):
            recommendations.append("Refinar prompt do sistema para garantir formato consistente de respostas")
        
        if any('Sistema não encontrou informações' in issue for issue, count in common_issues):
            recommendations.append("Adicionar documentos de fallback para queries sem contexto específico")
        
        return recommendations


def main():
    """Função principal de análise"""
    print("🔍 ANÁLISE DETALHADA DE QUERIES - SISTEMA RAG")
    print("=" * 60)
    
    # Configura logging
    logger = setup_logging("logs/query_analysis.log")
    
    try:
        # Carrega configuração
        config = load_config()
        
        # Inicializa sistema RAG
        rag_system = RAGSystem(config, logger)
        
        # Inicializa analisador
        analyzer = QueryAnalyzer(rag_system)
        
        # Queries de teste para análise detalhada
        test_queries = [
            "O que é inteligência artificial?",
            "Explique machine learning",
            "Como funciona deep learning?",
            "O que é RAG?",
            "Explique LangChain",
            "Como funciona ChromaDB?",
            "O que são embeddings?",
            "Explique OpenAI",
            "Como funciona o sistema de recuperação?",
            "Qual é a capital do Brasil?",
            "Como fazer um bolo de chocolate?",
            "Qual é o melhor time de futebol?",
            "Defina inteligência artificial de forma técnica",
            "O que significa machine learning?",
            "Defina deep learning de forma técnica",
            "O que é processamento de linguagem natural?",
            "Como funciona um sistema de recomendação?",
            "Explique o conceito de overfitting em machine learning",
            "Qual é a diferença entre IA e machine learning?",
            "Como implementar um chatbot usando RAG?"
        ]
        
        print(f"📝 Analisando {len(test_queries)} queries...")
        print()
        
        # Analisa cada query
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 Análise {i}/{len(test_queries)}: {query}")
            
            analysis = analyzer.analyze_query_performance(query)
            
            if analysis['success']:
                overall_score = analysis['quality_scores']['overall_score']
                print(f"   ✅ Score geral: {overall_score:.2f}")
                print(f"   📊 Recuperação: {analysis['quality_scores']['retrieval_score']:.2f}")
                print(f"   🎯 Geração: {analysis['quality_scores']['generation_score']:.2f}")
                
                if analysis['doc_analysis']['issues']:
                    print(f"   ⚠️ Problemas de recuperação: {', '.join(analysis['doc_analysis']['issues'])}")
                
                if analysis['response_analysis']['issues']:
                    print(f"   ⚠️ Problemas de resposta: {', '.join(analysis['response_analysis']['issues'])}")
            else:
                print(f"   ❌ Falha na análise")
            
            print()
        
        # Analisa padrões
        print("📈 ANÁLISE DE PADRÕES")
        print("=" * 40)
        
        patterns = analyzer.analyze_query_patterns()
        
        print(f"📊 Estatísticas Gerais:")
        print(f"   - Total de queries: {patterns['total_queries']}")
        print(f"   - Alta performance: {patterns['high_performance_count']}")
        print(f"   - Performance média: {patterns['medium_performance_count']}")
        print(f"   - Baixa performance: {patterns['low_performance_count']}")
        print(f"   - Score médio: {patterns['avg_overall_score']:.2f}")
        
        print(f"\n🔍 Problemas Mais Comuns:")
        for issue, count in patterns['common_issues']:
            print(f"   - {issue}: {count} ocorrências")
        
        print(f"\n📋 Categorias de Queries:")
        for category, queries in patterns['query_types'].items():
            print(f"   - {category}: {len(queries)} queries")
        
        print(f"\n💡 Recomendações:")
        for i, recommendation in enumerate(patterns['recommendations'], 1):
            print(f"   {i}. {recommendation}")
        
        # Salva análise detalhada
        analysis_file = f"reports/query_analysis_{int(time.time())}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                'patterns': patterns,
                'detailed_analysis': analyzer.analysis_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Análise detalhada salva em: {analysis_file}")
        print(f"\n✅ Análise concluída!")
        
        return 0
        
    except Exception as e:
        error_msg = f"Erro durante análise: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 