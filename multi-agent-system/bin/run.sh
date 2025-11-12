#!/bin/bash

# Script de lancement rapide sur Linux/Mac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé. Installez Python 3.10+"
    exit 1
fi

# Créer virtualenv si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création virtualenv..."
    python3 -m venv venv
fi

echo "🔧 Activation virtualenv..."
source venv/bin/activate

# Installer dépendances
if ! python -c "import requests" 2>/dev/null; then
    echo "📥 Installation dépendances..."
    pip install -q -r requirements.txt
fi

# Vérifier Ollama
echo ""
echo "🔌 Vérification Ollama..."
if ! timeout 2 python -c "import requests; requests.get('http://localhost:11434/api/tags', timeout=2)" 2>/dev/null; then
    echo "⚠️  Ollama ne répond pas sur http://localhost:11434"
    echo "   Démarrez Ollama: ollama serve"
    echo ""
fi

# Lancer le système
echo ""
read -p "📋 Décrivez votre projet (exemple 'API REST en FastAPI'): " REQ
if [ -z "$REQ" ]; then
    REQ="Créer une simple API REST"
fi

echo ""
python main.py --requirements "$REQ" --verbose
