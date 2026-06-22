@echo off
echo.
echo ====================================
echo   PÁDEL TRACKER - Test Local
echo ====================================
echo.
echo Iniciando servidor local...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado
    pause
    exit /b 1
)

REM Start server
cd /d "%~dp0"
start http://localhost:8000/padel-tracker.html
python -m http.server 8000

pause
