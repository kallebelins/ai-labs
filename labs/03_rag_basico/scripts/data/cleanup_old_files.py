#!/usr/bin/env python3
"""
Script de limpeza para remover arquivos antigos e desnecessários.

Este script identifica e remove:
- Relatórios antigos (mantém apenas os 5 mais recentes)
- Arquivos .pyc antigos
- Caches de teste desnecessários
- Logs antigos
- Arquivos temporários
"""

import os
import glob
import json
import shutil
from datetime import datetime
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectCleaner:
    """Classe para limpeza do projeto."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.removed_files = []
        self.removed_dirs = []
        
    def cleanup_reports(self, keep_recent: int = 5):
        """Remove relatórios antigos, mantendo apenas os mais recentes."""
        reports_dir = self.project_root / "reports"
        if not reports_dir.exists():
            logger.info("Pasta reports não encontrada")
            return
            
        # Encontra todos os arquivos de relatório
        report_files = list(reports_dir.glob("lab_report_*.json"))
        
        if len(report_files) <= keep_recent:
            logger.info(f"Mantendo todos os {len(report_files)} relatórios")
            return
            
        # Ordena por data de modificação (mais recente primeiro)
        report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove os arquivos antigos
        files_to_remove = report_files[keep_recent:]
        for file_path in files_to_remove:
            try:
                file_path.unlink()
                self.removed_files.append(str(file_path))
                logger.info(f"Removido relatório antigo: {file_path.name}")
            except Exception as e:
                logger.error(f"Erro ao remover {file_path}: {e}")
                
    def cleanup_pycache(self):
        """Remove arquivos .pyc e pastas __pycache__."""
        # Remove arquivos .pyc
        pyc_files = list(self.project_root.rglob("*.pyc"))
        for pyc_file in pyc_files:
            try:
                pyc_file.unlink()
                self.removed_files.append(str(pyc_file))
                logger.info(f"Removido arquivo .pyc: {pyc_file}")
            except Exception as e:
                logger.error(f"Erro ao remover {pyc_file}: {e}")
        
        # Remove pastas __pycache__
        pycache_dirs = list(self.project_root.rglob("__pycache__"))
        for pycache_dir in pycache_dirs:
            try:
                shutil.rmtree(pycache_dir)
                self.removed_dirs.append(str(pycache_dir))
                logger.info(f"Removida pasta __pycache__: {pycache_dir}")
            except Exception as e:
                logger.error(f"Erro ao remover {pycache_dir}: {e}")
                
    def cleanup_test_cache(self):
        """Remove cache de testes desnecessário."""
        test_cache_dir = self.project_root / "data" / "test_cache"
        if test_cache_dir.exists():
            try:
                shutil.rmtree(test_cache_dir)
                self.removed_dirs.append(str(test_cache_dir))
                logger.info(f"Removido cache de testes: {test_cache_dir}")
            except Exception as e:
                logger.error(f"Erro ao remover {test_cache_dir}: {e}")
                
    def cleanup_old_logs(self, days_old: int = 7):
        """Remove logs antigos."""
        logs_dir = self.project_root / "logs"
        if not logs_dir.exists():
            logger.info("Pasta logs não encontrada")
            return
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        log_files = list(logs_dir.glob("*.log"))
        for log_file in log_files:
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    self.removed_files.append(str(log_file))
                    logger.info(f"Removido log antigo: {log_file.name}")
                except Exception as e:
                    logger.error(f"Erro ao remover {log_file}: {e}")
                    
    def cleanup_temp_files(self):
        """Remove arquivos temporários."""
        temp_patterns = [
            "*.tmp",
            "*.temp",
            "*.bak",
            "*.swp",
            "*.swo",
            "*~"
        ]
        
        for pattern in temp_patterns:
            temp_files = list(self.project_root.rglob(pattern))
            for temp_file in temp_files:
                try:
                    temp_file.unlink()
                    self.removed_files.append(str(temp_file))
                    logger.info(f"Removido arquivo temporário: {temp_file}")
                except Exception as e:
                    logger.error(f"Erro ao remover {temp_file}: {e}")
                    
    def cleanup_empty_dirs(self):
        """Remove diretórios vazios."""
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.removed_dirs.append(str(dir_path))
                        logger.info(f"Removido diretório vazio: {dir_path}")
                except Exception as e:
                    logger.error(f"Erro ao remover diretório vazio {dir_path}: {e}")
                    
    def generate_cleanup_report(self):
        """Gera relatório de limpeza."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "removed_files": self.removed_files,
            "removed_directories": self.removed_dirs,
            "total_files_removed": len(self.removed_files),
            "total_dirs_removed": len(self.removed_dirs)
        }
        
        # Salva relatório
        report_file = self.project_root / "reports" / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Relatório de limpeza salvo: {report_file}")
        
        # Exibe resumo
        print(f"\n{'='*50}")
        print("RELATÓRIO DE LIMPEZA")
        print(f"{'='*50}")
        print(f"Arquivos removidos: {len(self.removed_files)}")
        print(f"Diretórios removidos: {len(self.removed_dirs)}")
        print(f"Total de itens removidos: {len(self.removed_files) + len(self.removed_dirs)}")
        print(f"Relatório salvo em: {report_file}")
        print(f"{'='*50}")
        
    def run_full_cleanup(self):
        """Executa limpeza completa do projeto."""
        logger.info("Iniciando limpeza completa do projeto...")
        
        # Executa todas as operações de limpeza
        self.cleanup_reports(keep_recent=5)
        self.cleanup_pycache()
        self.cleanup_test_cache()
        self.cleanup_old_logs(days_old=7)
        self.cleanup_temp_files()
        self.cleanup_empty_dirs()
        
        # Gera relatório
        self.generate_cleanup_report()
        
        logger.info("Limpeza completa finalizada!")

def main():
    """Função principal."""
    print("🧹 Script de Limpeza do Projeto RAG")
    print("=" * 40)
    
    # Confirmação do usuário
    response = input("Deseja executar a limpeza? (y/N): ").strip().lower()
    if response not in ['y', 'yes', 's', 'sim']:
        print("Limpeza cancelada.")
        return
    
    # Executa limpeza
    cleaner = ProjectCleaner()
    cleaner.run_full_cleanup()

if __name__ == "__main__":
    main() 