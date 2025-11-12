@echo off
REM Script de lancement rapide sur Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé. Installez Python 3.10+
    exit /b 1
)

REM Activer virtualenv si nécessaire
if not exist "venv\Scripts\activate.bat" (
    echo 📦 Création virtualenv...
    python -m venv venv
)

echo 🔧 Activation virtualenv...
call venv\Scripts\activate.bat

REM Installer dépendances
if not exist "venv\Lib\site-packages\requests" (
    echo 📥 Installation dépendances...
    pip install -q -r requirements.txt
)

REM Vérifier Ollama
echo.
echo 🔌 Vérification Ollama...
timeout /t 1 /nobreak >nul 2>&1
python -c "import requests; requests.get('http://localhost:11434/api/tags', timeout=2)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama ne répond pas sur http://localhost:11434
    echo    Démarrez Ollama: ollama serve
    echo.
)

REM Lancer le système
echo.
set /p REQ="📋 Décrivez votre projet (exemple 'API REST en FastAPI'): "
if "%REQ%"=="" (
    set REQ=Créer une simple API REST
)

echo.
python main.py --requirements "%REQ%" --verbose

pause
