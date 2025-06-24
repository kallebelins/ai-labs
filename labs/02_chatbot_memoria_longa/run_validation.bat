@echo off
echo ========================================
echo   VALIDACAO DO LABORATORIO
echo ========================================
echo.

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Configura as variáveis de ambiente
set TEST_MODE=true
set PYTHONPATH=.

REM Executa a validação
python scripts\validate_lab.py

echo.
echo ========================================
echo   VALIDACAO CONCLUIDA
echo ========================================
pause 