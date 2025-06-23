#!/usr/bin/env python3
"""
Testes automatizados para o laboratório
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from ..core.chatbot import ChatbotEngine
from .metrics import MetricsCollector, TestResult, TestSummary

class TestRunner:
    """Executor de testes automatizados"""
    
    def __init__(self, config: Dict[str, Any], chatbot: ChatbotEngine, metrics: MetricsCollector):
        """
        Inicializa o test runner
        
        Args:
            config: Configurações
            chatbot: Instância do chatbot
            metrics: Coletor de métricas
        """
        self.config = config
        self.chatbot = chatbot
        self.metrics = metrics
        self.logger = logging.getLogger(__name__)
    
    def load_test_queries(self) -> List[str]:
        """
        Carrega queries de teste do arquivo de entrada
        
        Returns:
            Lista de queries para teste
        """
        queries_file = Path(self.config["test_queries_file"])
        
        if not queries_file.exists():
            # Cria arquivo de exemplo se não existir
            queries_file.parent.mkdir(parents=True, exist_ok=True)
            example_queries = [
                "Olá, como você está?",
                "Qual é a capital do Brasil?",
                "Explique o que é inteligência artificial",
                "Conte uma piada",
                "Quais são os benefícios do exercício físico?"
            ]
            
            with open(queries_file, 'w', encoding='utf-8') as f:
                for query in example_queries:
                    f.write(query + '\n')
            
            self.logger.info(f"Arquivo de queries criado: {queries_file}")
        
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]
        
        self.logger.info(f"Carregadas {len(queries)} queries de teste")
        return queries
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Executa todos os testes
        
        Returns:
            Dicionário com resultados e resumo
        """
        self.logger.info("Iniciando execução dos testes...")
        
        # Carrega queries
        queries = self.load_test_queries()
        
        # Executa testes
        for i, query in enumerate(queries, 1):
            self.logger.info(f"Executando teste {i}/{len(queries)}: {query[:50]}...")
            
            # Processa query
            result_data = self.chatbot.process_query(query)
            
            # Cria objeto de resultado
            result = TestResult(
                query=query,
                response=result_data["response"],
                success=result_data["success"],
                response_time=result_data["response_time"],
                tokens_used=result_data["tokens_used"],
                confidence=result_data["confidence"],
                error_message=result_data["error_message"]
            )
            
            # Adiciona às métricas
            self.metrics.add_result(result)
        
        # Calcula resumo
        summary = self.metrics.get_summary()
        
        # Verifica thresholds
        self._check_thresholds(summary)
        
        return {
            "tests": [result.__dict__ for result in self.metrics.results],
            "summary": summary.__dict__,
            "timestamp": datetime.now().isoformat()
        }
    
    def _check_thresholds(self, summary: TestSummary):
        """Verifica se os resultados atendem aos thresholds mínimos"""
        issues = []
        
        if summary.success_rate < self.config["min_success_rate"]:
            issues.append(f"Taxa de sucesso ({summary.success_rate:.1f}%) abaixo do mínimo ({self.config['min_success_rate']}%)")
        
        if summary.avg_response_time > self.config["max_response_time"]:
            issues.append(f"Tempo médio de resposta ({summary.avg_response_time:.3f}s) acima do máximo ({self.config['max_response_time']}s)")
        
        if issues:
            self.logger.warning("Thresholds não atendidos:")
            for issue in issues:
                self.logger.warning(f"  - {issue}") 