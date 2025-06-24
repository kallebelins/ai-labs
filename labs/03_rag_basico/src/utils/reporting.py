#!/usr/bin/env python3
"""
Gerador de relatórios para o sistema RAG básico
"""

import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

class ReportGenerator:
    """Gerador de relatórios para o sistema RAG"""
    
    def __init__(self, reports_dir: str = "reports"):
        """
        Inicializa o gerador de relatórios
        
        Args:
            reports_dir: Diretório para salvar relatórios
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_lab_report(self, metrics_summary: Dict[str, Any], system_info: Dict[str, Any]) -> str:
        """
        Gera relatório completo do laboratório
        
        Args:
            metrics_summary: Resumo das métricas
            system_info: Informações do sistema
        
        Returns:
            Caminho do arquivo de relatório gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"lab_report_{timestamp}.json"
        
        # Calcula score final
        final_score = self._calculate_final_score(metrics_summary)
        
        # Determina status do laboratório
        status = self._determine_lab_status(final_score)
        
        # Cria relatório
        report = {
            "lab_info": {
                "name": "Lab 3: RAG Básico",
                "description": "Sistema RAG básico com recuperação e geração",
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "final_score": final_score
            },
            "system_info": system_info,
            "metrics_summary": metrics_summary,
            "detailed_metrics": {
                "context_recall": {
                    "value": metrics_summary.get("avg_context_recall", 0.0),
                    "target": 0.8,
                    "status": "✅" if metrics_summary.get("avg_context_recall", 0.0) >= 0.8 else "❌"
                },
                "precision": {
                    "value": metrics_summary.get("avg_precision", 0.0),
                    "target": 0.75,
                    "status": "✅" if metrics_summary.get("avg_precision", 0.0) >= 0.75 else "❌"
                },
                "rag_usage_rate": {
                    "value": metrics_summary.get("rag_usage_rate", 0.0),
                    "target": 90.0,
                    "status": "✅" if metrics_summary.get("rag_usage_rate", 0.0) >= 90.0 else "❌"
                },
                "response_time": {
                    "value": metrics_summary.get("avg_response_time", 0.0),
                    "target": 3.0,
                    "status": "✅" if metrics_summary.get("avg_response_time", 0.0) <= 3.0 else "❌"
                },
                "success_rate": {
                    "value": metrics_summary.get("success_rate", 0.0),
                    "target": 95.0,
                    "status": "✅" if metrics_summary.get("success_rate", 0.0) >= 95.0 else "❌"
                }
            },
            "recommendations": self._generate_recommendations(metrics_summary),
            "conclusion": self._generate_conclusion(final_score, status)
        }
        
        # Salva relatório
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Relatório gerado: {report_file}")
            return str(report_file)
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            return ""
    
    def _calculate_final_score(self, metrics_summary: Dict[str, Any]) -> float:
        """
        Calcula score final baseado nas métricas
        
        Args:
            metrics_summary: Resumo das métricas
        
        Returns:
            Score final (0-100)
        """
        if metrics_summary.get("total_queries", 0) == 0:
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
        response_time = metrics_summary.get("avg_response_time", 0.0)
        response_time_score = max(0, 1 - (response_time / 5.0))  # 5s como referência
        
        # Calcula score ponderado
        score = (
            metrics_summary.get("avg_context_recall", 0.0) * weights["context_recall"] +
            metrics_summary.get("avg_precision", 0.0) * weights["precision"] +
            (metrics_summary.get("rag_usage_rate", 0.0) / 100) * weights["rag_usage"] +
            (metrics_summary.get("success_rate", 0.0) / 100) * weights["success_rate"] +
            response_time_score * weights["response_time"] +
            metrics_summary.get("avg_confidence", 0.0) * weights["confidence"]
        )
        
        return score * 100  # Converte para percentual
    
    def _determine_lab_status(self, final_score: float) -> str:
        """
        Determina status do laboratório baseado no score
        
        Args:
            final_score: Score final do laboratório
        
        Returns:
            Status do laboratório
        """
        if final_score >= 90:
            return "LABORATÓRIO APROVADO"
        elif final_score >= 80:
            return "LABORATÓRIO APROVADO COM RESERVAS"
        elif final_score >= 70:
            return "LABORATÓRIO EM REVISÃO"
        else:
            return "LABORATÓRIO REPROVADO"
    
    def _generate_recommendations(self, metrics_summary: Dict[str, Any]) -> List[str]:
        """
        Gera recomendações baseadas nas métricas
        
        Args:
            metrics_summary: Resumo das métricas
        
        Returns:
            Lista de recomendações
        """
        recommendations = []
        
        # Análise de recall de contexto
        context_recall = metrics_summary.get("avg_context_recall", 0.0)
        if context_recall < 0.8:
            recommendations.append(
                "Melhorar recall de contexto: Considere ajustar threshold de similaridade ou expandir base de documentos"
            )
        
        # Análise de precisão
        precision = metrics_summary.get("avg_precision", 0.0)
        if precision < 0.75:
            recommendations.append(
                "Melhorar precisão das respostas: Otimize prompts e refine critérios de recuperação"
            )
        
        # Análise de uso de RAG
        rag_usage = metrics_summary.get("rag_usage_rate", 0.0)
        if rag_usage < 90.0:
            recommendations.append(
                "Aumentar taxa de uso de RAG: Verifique se documentos estão sendo recuperados adequadamente"
            )
        
        # Análise de tempo de resposta
        response_time = metrics_summary.get("avg_response_time", 0.0)
        if response_time > 3.0:
            recommendations.append(
                "Otimizar tempo de resposta: Considere cache de embeddings ou otimização de queries"
            )
        
        # Análise de taxa de sucesso
        success_rate = metrics_summary.get("success_rate", 0.0)
        if success_rate < 95.0:
            recommendations.append(
                "Melhorar taxa de sucesso: Verifique logs de erro e trate exceções adequadamente"
            )
        
        if not recommendations:
            recommendations.append("Sistema funcionando adequadamente - mantenha monitoramento")
        
        return recommendations
    
    def _generate_conclusion(self, final_score: float, status: str) -> str:
        """
        Gera conclusão do relatório
        
        Args:
            final_score: Score final
            status: Status do laboratório
        
        Returns:
            Conclusão do relatório
        """
        if final_score >= 90:
            return (
                f"Excelente - Solução muito bem implementada e validada. "
                f"Score final de {final_score:.1f}% demonstra alta efetividade do sistema RAG."
            )
        elif final_score >= 80:
            return (
                f"Bom - Solução implementada com sucesso. "
                f"Score final de {final_score:.1f}% indica boa performance, com espaço para melhorias."
            )
        elif final_score >= 70:
            return (
                f"Regular - Solução implementada mas requer melhorias. "
                f"Score final de {final_score:.1f}% indica necessidade de otimizações."
            )
        else:
            return (
                f"Insuficiente - Solução não atende aos requisitos mínimos. "
                f"Score final de {final_score:.1f}% indica necessidade de revisão completa."
            )
    
    def print_summary(self, metrics_summary: Dict[str, Any], system_info: Dict[str, Any]):
        """
        Imprime resumo das métricas no console
        
        Args:
            metrics_summary: Resumo das métricas
            system_info: Informações do sistema
        """
        print("\n" + "="*60)
        print("📊 RELATÓRIO DO SISTEMA RAG BÁSICO")
        print("="*60)
        
        # Informações do sistema
        print(f"\n🤖 INFORMAÇÕES DO SISTEMA:")
        print(f"   - Modelo: {system_info.get('model_name', 'N/A')}")
        print(f"   - Temperatura: {system_info.get('temperature', 'N/A')}")
        print(f"   - Modo de teste: {'Sim' if system_info.get('test_mode', False) else 'Não'}")
        print(f"   - Vetorstore disponível: {'Sim' if system_info.get('vectorstore_available', False) else 'Não'}")
        print(f"   - Documentos: {system_info.get('documents_count', 0)}")
        
        # Métricas principais
        print(f"\n📈 MÉTRICAS PRINCIPAIS:")
        print(f"   - Total de queries: {metrics_summary.get('total_queries', 0)}")
        print(f"   - Taxa de sucesso: {metrics_summary.get('success_rate', 0.0):.1f}%")
        print(f"   - Tempo médio de resposta: {metrics_summary.get('avg_response_time', 0.0):.2f}s")
        print(f"   - Tokens médios por query: {metrics_summary.get('avg_tokens_per_query', 0.0):.1f}")
        
        # Métricas de qualidade
        print(f"\n🎯 MÉTRICAS DE QUALIDADE:")
        print(f"   - Recall de contexto: {metrics_summary.get('avg_context_recall', 0.0):.1%}")
        print(f"   - Precisão: {metrics_summary.get('avg_precision', 0.0):.1%}")
        print(f"   - Confiança: {metrics_summary.get('avg_confidence', 0.0):.1%}")
        print(f"   - Taxa de uso de RAG: {metrics_summary.get('rag_usage_rate', 0.0):.1f}%")
        print(f"   - Documentos médios usados: {metrics_summary.get('avg_documents_used', 0.0):.1f}")
        
        # Score final
        final_score = self._calculate_final_score(metrics_summary)
        status = self._determine_lab_status(final_score)
        
        print(f"\n🏆 RESULTADO FINAL:")
        print(f"   - Score Final: {final_score:.1f}%")
        print(f"   - Status: {status}")
        
        print("="*60) 