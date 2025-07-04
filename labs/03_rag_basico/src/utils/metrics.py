#!/usr/bin/env python3
"""
Sistema de métricas simplificado para RAG.

Este módulo fornece coleta básica de métricas para o sistema RAG:
- Taxa de sucesso
- Tempo de resposta médio
- Recall e precisão básicos
- Armazenamento simples em JSON
"""

import json
import time
from typing import Dict, Any, List
from pathlib import Path

class SimpleMetrics:
    """Coletor de métricas simplificado para o sistema RAG"""
    
    def __init__(self, metrics_file: str = "metrics/rag_metrics.json"):
        """
        Inicializa o coletor de métricas
        
        Args:
            metrics_file: Caminho para o arquivo de métricas
        """
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(exist_ok=True)
        
        # Carrega métricas existentes ou inicializa
        self.data = self._load_metrics()
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Carrega métricas do arquivo ou inicializa estrutura básica"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "queries_processed": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "context_recall_scores": [],
            "precision_scores": [],
            "last_updated": None
        }
    
    def record_query_result(self, result: Dict[str, Any]):
        """
        Registra resultado de uma query
        
        Args:
            result: Dicionário com resultado da query
        """
        self.data["queries_processed"] += 1
        
        if result.get("success", False):
            self.data["successful_queries"] += 1
            self.data["total_response_time"] += result.get("response_time", 0)
            
            # Registra métricas de qualidade se disponíveis
            if "context_recall" in result:
                self.data["context_recall_scores"].append(result["context_recall"])
            if "precision" in result:
                self.data["precision_scores"].append(result["precision"])
        else:
            self.data["failed_queries"] += 1
        
        self.data["last_updated"] = time.time()
        self._save_metrics()
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo das métricas"""
        total = self.data["queries_processed"]
        if total == 0:
            return {
                "total_queries": 0,
                "success_rate": 0.0,
                "avg_response_time": 0.0,
                "avg_context_recall": 0.0,
                "avg_precision": 0.0
            }
        
        # Calcula médias
        avg_response_time = (
            self.data["total_response_time"] / self.data["successful_queries"]
            if self.data["successful_queries"] > 0 else 0.0
        )
        
        recall_scores = self.data["context_recall_scores"]
        avg_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0.0
        
        precision_scores = self.data["precision_scores"]
        avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0.0
        
        return {
            "total_queries": total,
            "success_rate": (self.data["successful_queries"] / total) * 100,
            "avg_response_time": avg_response_time,
            "avg_context_recall": avg_recall,
            "avg_precision": avg_precision,
            "queries_with_context": len(recall_scores),
            "rag_usage_rate": (len(recall_scores) / total) * 100 if total > 0 else 0.0
        }
    
    def calculate_final_score(self) -> float:
        """Calcula score final baseado nas métricas principais"""
        summary = self.get_summary()
        
        if summary["total_queries"] == 0:
            return 0.0
        
        # Score baseado em: success_rate (40%) + avg_recall (30%) + avg_precision (30%)
        success_weight = 0.4
        recall_weight = 0.3
        precision_weight = 0.3
        
        score = (
            (summary["success_rate"] / 100) * success_weight +
            summary["avg_context_recall"] * recall_weight +
            summary["avg_precision"] * precision_weight
        ) * 100
        
        return min(score, 100.0)  # Máximo de 100%
    
    def _save_metrics(self):
        """Salva métricas no arquivo"""
        try:
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar métricas: {e}")
    
    def reset_metrics(self):
        """Reseta todas as métricas"""
        self.data = {
            "queries_processed": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "context_recall_scores": [],
            "precision_scores": [],
            "last_updated": None
        }
        self._save_metrics()

# Alias para compatibilidade
MetricsCollector = SimpleMetrics 