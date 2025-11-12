# Configuration Ollama pour le système multi-agents

## Modèles recommandés par rôle

### Budget mémoire faible (8GB GPU)
- mistral:7b (tous les agents)
- neural-chat:7b

### Budget moyen (12-16GB GPU)
- mistral:7b ou neural-chat:7b (architecture, security, doc)
- codellama:13b (developer, reviewer, tester)

### Budget élevé (24GB+ GPU)
- codellama:34b (architect, developer, tester)
- deepseek-coder:33b (developer)
- qwen2.5-coder:32b (reviewer)
- llama2:13b (security)
- phind-coder:34b (tester)

## Installation sur Windows PowerShell

```powershell
# 1. Installer Ollama
winget install Ollama.Ollama

# 2. Lancer Ollama (démarre le service)
ollama serve

# 3. Dans une autre terminal, télécharger modèles
ollama pull mistral:latest
ollama pull neural-chat:7b

# 4. Vérifier les modèles
ollama list
```

## Installation sur Linux

```bash
# 1. Installer
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Lancer
ollama serve &

# 3. Télécharger modèles
ollama pull mistral:latest
ollama pull neural-chat:7b

# 4. Vérifier
ollama list
```

## Tester la connexion

```bash
curl http://localhost:11434/api/tags
```

Doit retourner du JSON avec les modèles.

## Performance

Si ralentissement, ajuster:

1. **Timeout** dans `config/settings.py`
   - Augmenter si timeouts fréquents
   - Diminuer si réponses rapides

2. **Température** (0.0-1.0)
   - Basse (0.3) = déterministe, rapide
   - Haute (0.9) = créatif, plus lent

3. **Taille modèles**
   - 7B < 13B < 34B (taille mémoire)
   - Taille ∝ qualité mais aussi temps/mémoire
