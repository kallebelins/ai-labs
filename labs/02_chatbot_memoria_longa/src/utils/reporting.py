#!/usr/bin/env python3
"""
Relatórios para o laboratório de chatbot com memória de longo prazo
"""

import json
import statistics
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.utils.metrics import MemoryMetricsCollector, OverallMetrics, SessionMetrics

class MemoryReportGenerator:
    """Gerador de relatórios para métricas de memória"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_memory_retention_report(self, metrics_collector: MemoryMetricsCollector) -> Dict[str, Any]:
        """
        Gera relatório de retenção de memória
        
        Args:
            metrics_collector: Coletor de métricas
            
        Returns:
            Relatório de retenção
        """
        overall_metrics = metrics_collector.calculate_overall_metrics()
        
        # Calcula métricas específicas de retenção
        memory_metrics = [m for m in metrics_collector.metrics if m.memory_context_used]
        retention_analysis = {
            "total_memory_usage": len(memory_metrics),
            "total_queries": len(metrics_collector.metrics),
            "retention_rate": overall_metrics.overall_memory_retention,
            "avg_memory_context_length": statistics.mean([m.memory_context_length for m in memory_metrics]) if memory_metrics else 0,
            "memory_utilization_rate": overall_metrics.memory_utilization_rate
        }
        
        # Análise por sessão
        session_retention = {}
        session_ids = list(set(m.session_id for m in metrics_collector.metrics))
        
        for session_id in session_ids:
            session_metric = metrics_collector.calculate_session_metrics(session_id)
            session_retention[session_id] = {
                "memory_retention_rate": session_metric.memory_retention_rate,
                "total_memory_contexts_used": session_metric.total_memory_contexts_used,
                "total_queries": session_metric.total_queries,
                "summary_generated": session_metric.summary_generated
            }
        
        report = {
            "report_type": "memory_retention",
            "timestamp": datetime.now().isoformat(),
            "overall_analysis": retention_analysis,
            "session_analysis": session_retention,
            "recommendations": self._generate_retention_recommendations(retention_analysis)
        }
        
        return report
    
    def generate_context_coherence_report(self, metrics_collector: MemoryMetricsCollector) -> Dict[str, Any]:
        """
        Gera relatório de coerência de contexto
        
        Args:
            metrics_collector: Coletor de métricas
            
        Returns:
            Relatório de coerência
        """
        overall_metrics = metrics_collector.calculate_overall_metrics()
        
        # Análise de coerência por sessão
        session_coherence = {}
        session_ids = list(set(m.session_id for m in metrics_collector.metrics))
        
        for session_id in session_ids:
            session_metric = metrics_collector.calculate_session_metrics(session_id)
            session_coherence[session_id] = {
                "context_coherence_score": session_metric.context_coherence_score,
                "avg_confidence": session_metric.avg_confidence,
                "conversation_length": session_metric.total_queries,
                "memory_contexts_used": session_metric.total_memory_contexts_used
            }
        
        # Análise temporal de coerência
        temporal_analysis = self._analyze_temporal_coherence(metrics_collector.metrics)
        
        report = {
            "report_type": "context_coherence",
            "timestamp": datetime.now().isoformat(),
            "overall_coherence": overall_metrics.overall_context_coherence,
            "session_coherence": session_coherence,
            "temporal_analysis": temporal_analysis,
            "recommendations": self._generate_coherence_recommendations(overall_metrics)
        }
        
        return report
    
    def generate_performance_report(self, metrics_collector: MemoryMetricsCollector) -> Dict[str, Any]:
        """
        Gera relatório de performance
        
        Args:
            metrics_collector: Coletor de métricas
            
        Returns:
            Relatório de performance
        """
        overall_metrics = metrics_collector.calculate_overall_metrics()
        
        # Análise de performance
        response_times = [m.response_time for m in metrics_collector.metrics]
        tokens_used = [m.tokens_used for m in metrics_collector.metrics]
        confidences = [m.confidence for m in metrics_collector.metrics]
        
        performance_analysis = {
            "avg_response_time": overall_metrics.avg_response_time,
            "response_time_stats": {
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
                "median": statistics.median(response_times) if response_times else 0,
                "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0
            },
            "avg_tokens_used": overall_metrics.avg_tokens_used,
            "tokens_stats": {
                "min": min(tokens_used) if tokens_used else 0,
                "max": max(tokens_used) if tokens_used else 0,
                "median": statistics.median(tokens_used) if tokens_used else 0,
                "total": sum(tokens_used)
            },
            "avg_confidence": overall_metrics.avg_confidence,
            "confidence_stats": {
                "min": min(confidences) if confidences else 0,
                "max": max(confidences) if confidences else 0,
                "median": statistics.median(confidences) if confidences else 0
            }
        }
        
        # Análise de performance por sessão
        session_performance = {}
        session_ids = list(set(m.session_id for m in metrics_collector.metrics))
        
        for session_id in session_ids:
            session_metric = metrics_collector.calculate_session_metrics(session_id)
            session_performance[session_id] = {
                "avg_response_time": session_metric.avg_response_time,
                "avg_tokens_used": session_metric.avg_tokens_used,
                "avg_confidence": session_metric.avg_confidence,
                "total_queries": session_metric.total_queries
            }
        
        report = {
            "report_type": "performance",
            "timestamp": datetime.now().isoformat(),
            "overall_performance": performance_analysis,
            "session_performance": session_performance,
            "recommendations": self._generate_performance_recommendations(performance_analysis)
        }
        
        return report
    
    def generate_comprehensive_report(self, metrics_collector: MemoryMetricsCollector) -> Dict[str, Any]:
        """
        Gera relatório abrangente
        
        Args:
            metrics_collector: Coletor de métricas
            
        Returns:
            Relatório abrangente
        """
        overall_metrics = metrics_collector.calculate_overall_metrics()
        
        # Gera relatórios específicos
        retention_report = self.generate_memory_retention_report(metrics_collector)
        coherence_report = self.generate_context_coherence_report(metrics_collector)
        performance_report = self.generate_performance_report(metrics_collector)
        
        # Análise de correlação
        correlation_analysis = self._analyze_correlations(metrics_collector.metrics)
        
        # Score geral do sistema
        system_score = self._calculate_system_score(overall_metrics)
        
        comprehensive_report = {
            "report_type": "comprehensive",
            "timestamp": datetime.now().isoformat(),
            "system_score": system_score,
            "overall_metrics": {
                "total_sessions": overall_metrics.total_sessions,
                "total_queries": overall_metrics.total_queries,
                "memory_retention": overall_metrics.overall_memory_retention,
                "context_coherence": overall_metrics.overall_context_coherence,
                "memory_utilization": overall_metrics.memory_utilization_rate,
                "avg_response_time": overall_metrics.avg_response_time,
                "avg_confidence": overall_metrics.avg_confidence
            },
            "detailed_reports": {
                "memory_retention": retention_report,
                "context_coherence": coherence_report,
                "performance": performance_report
            },
            "correlation_analysis": correlation_analysis,
            "recommendations": self._generate_comprehensive_recommendations(overall_metrics)
        }
        
        return comprehensive_report
    
    def save_report(self, report: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """
        Salva relatório em arquivo JSON
        
        Args:
            report: Relatório a ser salvo
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if filename is None:
            report_type = report.get("report_type", "report")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _analyze_temporal_coherence(self, metrics: List) -> Dict[str, Any]:
        """Analisa coerência temporal"""
        # Agrupa por timestamp (simplificado)
        return {
            "analysis_type": "temporal_coherence",
            "note": "Análise temporal simplificada - em produção implementar análise mais detalhada"
        }
    
    def _analyze_correlations(self, metrics: List) -> Dict[str, Any]:
        """Analisa correlações entre métricas"""
        if len(metrics) < 2:
            return {"note": "Dados insuficientes para análise de correlação"}
        
        # Correlação entre confiança e uso de memória
        confidences = [m.confidence for m in metrics]
        memory_usage = [1 if m.memory_context_used else 0 for m in metrics]
        
        try:
            correlation = statistics.correlation(confidences, memory_usage)
        except:
            correlation = 0.0
        
        return {
            "confidence_memory_correlation": correlation,
            "note": "Correlação entre confiança e uso de memória"
        }
    
    def _calculate_system_score(self, overall_metrics: OverallMetrics) -> float:
        """Calcula score geral do sistema"""
        # Score baseado em múltiplos fatores
        memory_score = overall_metrics.overall_memory_retention * 0.3
        coherence_score = overall_metrics.overall_context_coherence * 0.3
        performance_score = min(1.0, 3.0 / overall_metrics.avg_response_time) * 0.2
        utilization_score = overall_metrics.memory_utilization_rate * 0.2
        
        total_score = memory_score + coherence_score + performance_score + utilization_score
        return min(1.0, total_score)
    
    def _generate_retention_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera recomendações para retenção de memória"""
        recommendations = []
        
        if analysis["retention_rate"] < 0.7:
            recommendations.append("Considerar aumentar o tamanho da janela de memória")
            recommendations.append("Revisar estratégia de armazenamento de contexto")
        
        if analysis["memory_utilization_rate"] < 0.5:
            recommendations.append("Otimizar busca de contexto relevante")
            recommendations.append("Ajustar parâmetros de similaridade")
        
        return recommendations
    
    def _generate_coherence_recommendations(self, overall_metrics: OverallMetrics) -> List[str]:
        """Gera recomendações para coerência de contexto"""
        recommendations = []
        
        if overall_metrics.overall_context_coherence < 0.7:
            recommendations.append("Melhorar estratégia de resumo de conversa")
            recommendations.append("Ajustar prompt do sistema para maior coerência")
        
        return recommendations
    
    def _generate_performance_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera recomendações para performance"""
        recommendations = []
        
        if analysis["avg_response_time"] > 2.0:
            recommendations.append("Otimizar processamento de queries")
            recommendations.append("Considerar cache de respostas frequentes")
        
        if analysis["tokens_stats"]["total"] > 10000:
            recommendations.append("Otimizar uso de tokens")
            recommendations.append("Implementar estratégia de truncamento")
        
        return recommendations
    
    def _generate_comprehensive_recommendations(self, overall_metrics: OverallMetrics) -> List[str]:
        """Gera recomendações abrangentes"""
        recommendations = []
        
        # Recomendações baseadas no score geral
        if overall_metrics.overall_memory_retention < 0.8:
            recommendations.append("Priorizar melhorias na retenção de memória")
        
        if overall_metrics.overall_context_coherence < 0.7:
            recommendations.append("Focar em melhorias de coerência de contexto")
        
        if overall_metrics.avg_response_time > 2.0:
            recommendations.append("Otimizar performance do sistema")
        
        recommendations.append("Monitorar métricas continuamente")
        recommendations.append("Implementar testes automatizados regulares")
        
        return recommendations 