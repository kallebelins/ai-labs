#!/usr/bin/env python3
"""
Métricas e coleta de dados para o laboratório
"""

import logging
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class TestResult:
    """Resultado de um teste individual"""
    query: str
    response: str
    success: bool
    response_time: float
    tokens_used: int
    confidence: float
    error_message: Optional[str] = None

@dataclass
class TestSummary:
    """Resumo dos resultados dos testes"""
    total_tests: int
    successful_tests: int
    failed_tests: int
    success_rate: float
    avg_response_time: float
    total_tokens_used: int
    avg_tokens_per_query: float
    avg_confidence: float

class MetricsCollector:
    """Coletor de métricas durante os testes"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.logger = logging.getLogger(__name__)
    
    def add_result(self, result: TestResult):
        """Adiciona um resultado de teste"""
        self.results.append(result)
        self.logger.info(f"Teste {'SUCESSO' if result.success else 'FALHA'}: {result.query[:50]}...")
    
    def get_summary(self) -> TestSummary:
        """Calcula resumo das métricas"""
        if not self.results:
            return TestSummary(0, 0, 0, 0.0, 0.0, 0, 0.0, 0.0)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests) * 100
        
        avg_response_time = sum(r.response_time for r in self.results) / total_tests
        total_tokens_used = sum(r.tokens_used for r in self.results)
        avg_tokens_per_query = total_tokens_used / total_tests
        avg_confidence = sum(r.confidence for r in self.results) / total_tests
        
        return TestSummary(
            total_tests=total_tests,
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            success_rate=success_rate,
            avg_response_time=avg_response_time,
            total_tokens_used=total_tokens_used,
            avg_tokens_per_query=avg_tokens_per_query,
            avg_confidence=avg_confidence
        ) 