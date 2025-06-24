#!/usr/bin/env python3
"""
Coletor de métricas para o sistema RAG básico
"""

import json
import time
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

class MetricsCollector:
    """Coletor de métricas para o sistema RAG"""
    
    def __init__(self, metrics_file: str = "metrics/rag_metrics.json"):
        """
        Inicializa o coletor de métricas
        
        Args:
            metrics_file: Arquivo para salvar métricas
        """
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics = {
            "queries_processed": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "avg_response_time": 0.0,
            "total_tokens_used": 0,
            "avg_tokens_per_query": 0.0,
            "context_recall_scores": [],
            "precision_scores": [],
            "confidence_scores": [],
            "documents_used_count": [],
            "queries_with_context": 0,
            "queries_without_context": 0,
            "start_time": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat()
        }
        self._load_existing_metrics()
    
    def _load_existing_metrics(self):
        """Carrega métricas existentes do arquivo"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    existing_metrics = json.load(f)
                    self.metrics.update(existing_metrics)
            except Exception as e:
                print(f"Erro ao carregar métricas existentes: {e}")
    
    def record_query_result(self, result: Dict[str, Any]):
        """
        Registra resultado de uma query
        
        Args:
            result: Resultado da query processada
        """
        self.metrics["queries_processed"] += 1
        
        if result["success"]:
            self.metrics["successful_queries"] += 1
            
            # Métricas de tempo
            response_time = result["response_time"]
            self.metrics["total_response_time"] += response_time
            self.metrics["avg_response_time"] = (
                self.metrics["total_response_time"] / self.metrics["successful_queries"]
            )
            
            # Métricas de tokens
            tokens_used = result["tokens_used"]
            self.metrics["total_tokens_used"] += tokens_used
            self.metrics["avg_tokens_per_query"] = (
                self.metrics["total_tokens_used"] / self.metrics["successful_queries"]
            )
            
            # Métricas de qualidade
            if "context_recall" in result:
                self.metrics["context_recall_scores"].append(result["context_recall"])
            
            if "precision" in result:
                self.metrics["precision_scores"].append(result["precision"])
            
            if "confidence" in result:
                self.metrics["confidence_scores"].append(result["confidence"])
            
            # Métricas de documentos
            if "documents_used" in result:
                self.metrics["documents_used_count"].append(result["documents_used"])
                
                if result["documents_used"] > 0:
                    self.metrics["queries_with_context"] += 1
                else:
                    self.metrics["queries_without_context"] += 1
        else:
            self.metrics["failed_queries"] += 1
        
        self.metrics["last_update"] = datetime.now().isoformat()
        self._save_metrics()
    
    def _save_metrics(self):
        """Salva métricas no arquivo"""
        try:
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar métricas: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo das métricas
        
        Returns:
            Dict com resumo das métricas
        """
        total_queries = self.metrics["queries_processed"]
        if total_queries == 0:
            return {
                "status": "Nenhuma query processada",
                "total_queries": 0
            }
        
        # Calcula médias
        avg_context_recall = (
            sum(self.metrics["context_recall_scores"]) / len(self.metrics["context_recall_scores"])
            if self.metrics["context_recall_scores"] else 0.0
        )
        
        avg_precision = (
            sum(self.metrics["precision_scores"]) / len(self.metrics["precision_scores"])
            if self.metrics["precision_scores"] else 0.0
        )
        
        avg_confidence = (
            sum(self.metrics["confidence_scores"]) / len(self.metrics["confidence_scores"])
            if self.metrics["confidence_scores"] else 0.0
        )
        
        avg_documents_used = (
            sum(self.metrics["documents_used_count"]) / len(self.metrics["documents_used_count"])
            if self.metrics["documents_used_count"] else 0.0
        )
        
        # Taxa de uso de RAG
        rag_usage_rate = (
            self.metrics["queries_with_context"] / total_queries * 100
            if total_queries > 0 else 0.0
        )
        
        # Taxa de sucesso
        success_rate = (
            self.metrics["successful_queries"] / total_queries * 100
            if total_queries > 0 else 0.0
        )
        
        return {
            "total_queries": total_queries,
            "successful_queries": self.metrics["successful_queries"],
            "failed_queries": self.metrics["failed_queries"],
            "success_rate": success_rate,
            "avg_response_time": self.metrics["avg_response_time"],
            "avg_tokens_per_query": self.metrics["avg_tokens_per_query"],
            "avg_context_recall": avg_context_recall,
            "avg_precision": avg_precision,
            "avg_confidence": avg_confidence,
            "avg_documents_used": avg_documents_used,
            "rag_usage_rate": rag_usage_rate,
            "queries_with_context": self.metrics["queries_with_context"],
            "queries_without_context": self.metrics["queries_without_context"],
            "start_time": self.metrics["start_time"],
            "last_update": self.metrics["last_update"]
        }
    
    def calculate_final_score(self) -> float:
        """
        Calcula score final baseado nas métricas
        
        Returns:
            Score final (0-100)
        """
        summary = self.get_summary()
        
        if summary["total_queries"] == 0:
            return 0.0
        
        # Pesos para cada métrica
        weights = {
            "context_recall": 0.25,
            "precision": 0.20,
            "rag_usage": 0.20,
            "success_rate": 0.15,
            "response_time": 0.10,
            "confidence": 0.10
        }
        
        # Normaliza tempo de resposta (menor é melhor)
        response_time_score = max(0, 1 - (summary["avg_response_time"] / 5.0))  # 5s como referência
        
        # Calcula score ponderado
        score = (
            summary["avg_context_recall"] * weights["context_recall"] +
            summary["avg_precision"] * weights["precision"] +
            (summary["rag_usage_rate"] / 100) * weights["rag_usage"] +
            (summary["success_rate"] / 100) * weights["success_rate"] +
            response_time_score * weights["response_time"] +
            summary["avg_confidence"] * weights["confidence"]
        )
        
        return score * 100  # Converte para percentual
    
    def reset_metrics(self):
        """Reseta todas as métricas"""
        self.metrics = {
            "queries_processed": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_response_time": 0.0,
            "avg_response_time": 0.0,
            "total_tokens_used": 0,
            "avg_tokens_per_query": 0.0,
            "context_recall_scores": [],
            "precision_scores": [],
            "confidence_scores": [],
            "documents_used_count": [],
            "queries_with_context": 0,
            "queries_without_context": 0,
            "start_time": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat()
        }
        self._save_metrics() 