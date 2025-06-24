# Script de Validação do Laboratório
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VALIDACAO DO LABORATORIO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ativa o ambiente virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Ambiente virtual ativado" -ForegroundColor Green
} else {
    Write-Host "❌ Ambiente virtual não encontrado" -ForegroundColor Red
    exit 1
}

# Configura as variáveis de ambiente
$env:TEST_MODE = "true"
$env:PYTHONPATH = "."

Write-Host "✅ Variáveis de ambiente configuradas" -ForegroundColor Green
Write-Host ""

# Executa a validação
Write-Host "🚀 Executando validação..." -ForegroundColor Yellow
python scripts\validate_lab.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VALIDACAO CONCLUIDA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan 