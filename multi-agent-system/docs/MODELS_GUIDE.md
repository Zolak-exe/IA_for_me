# 🎯 Guide Modèles Recommandés

## Profils de Configuration

### 📱 Profil Léger (8GB GPU / CPU)

**Modèles:**
```bash
ollama pull mistral:7b
```

**Configuration `config/settings.py`:**
```python
AGENT_MODELS = {
    "architect": "mistral:7b",
    "developer": "mistral:7b",
    "reviewer": "mistral:7b",
    "security": "mistral:7b",
    "tester": "mistral:7b",
    "documentation": "mistral:7b"
}
```

**Caractéristiques:**
- ✅ Rapide (~1-2s par génération)
- ✅ Faible empreinte mémoire
- ✅ Qualité acceptable
- ❌ Peut manquer nuances

**Temps estimé:** 3-5 min par itération


### 💻 Profil Moyen (16GB GPU)

**Modèles:**
```bash
ollama pull mistral:7b
ollama pull neural-chat:7b
ollama pull codellama:13b
```

**Configuration optimale:**
```python
AGENT_MODELS = {
    "architect": "neural-chat:7b",      # Design créatif
    "developer": "codellama:13b",       # Code forte
    "reviewer": "neural-chat:7b",       # Analyse générale
    "security": "mistral:7b",          # Rapide, léger
    "tester": "codellama:13b",         # Syntaxe tests
    "documentation": "mistral:7b"      # Rapidité
}
```

**Caractéristiques:**
- ✅ Bon équilibre qualité/vitesse
- ✅ Qualité code très bonne
- ✅ Mémoire gérable
- ⚠️  ~5-10s par génération

**Temps estimé:** 8-15 min par itération


### 🚀 Profil Performance (24GB+ GPU)

**Modèles:**
```bash
ollama pull codellama:34b
ollama pull deepseek-coder:33b
ollama pull qwen2.5-coder:32b
ollama pull llama2:13b
ollama pull phind-coder:34b
```

**Configuration optimale:**
```python
AGENT_MODELS = {
    "architect": "codellama:34b",       # Excellente conception
    "developer": "deepseek-coder:33b",  # Code très bon
    "reviewer": "qwen2.5-coder:32b",    # Excellente analyse
    "security": "llama2:13b",           # Sécurité forte
    "tester": "phind-coder:34b",        # Tests excellents
    "documentation": "mistral:7b"       # Doc rapide
}
```

**Caractéristiques:**
- ✅✅ Qualité exceptionnelle
- ✅ Code très bon syntaxiquement
- ⚠️  Lent (~20-30s par génération)
- ⚠️  Très gourmand mémoire

**Temps estimé:** 30-60 min par itération


## Modèles Spécialisés Recommandés

### 👨‍💼 Architecture
| Modèle | Taille | Notes |
|--------|--------|-------|
| CodeLLaMA:34b | 19GB | 🏆 Meilleur design patterns |
| Mistral:7b | 4GB | Rapide, acceptable |
| Neural-Chat:7b | 4GB | Bon équilibre |

### 👨‍💻 Développement
| Modèle | Taille | Notes |
|--------|--------|-------|
| DeepSeek-Coder:33b | 19GB | 🏆 Meilleur code |
| CodeLLaMA:34b | 19GB | Très bon |
| Phind-Coder:34b | 19GB | Excellent |

### 🔍 Review/Qualité
| Modèle | Taille | Notes |
|--------|--------|-------|
| Qwen2.5-Coder:32b | 19GB | 🏆 Excellente analyse |
| CodeLLaMA:34b | 19GB | Très bon |
| Neural-Chat:7b | 4GB | Acceptable |

### 🔒 Sécurité
| Modèle | Taille | Notes |
|--------|--------|-------|
| Llama2:13b | 7GB | 🏆 Bon balance |
| Mistral:7b | 4GB | Rapide |
| Neural-Chat:7b | 4GB | Alternative |

### ✅ Testing
| Modèle | Taille | Notes |
|--------|--------|-------|
| Phind-Coder:34b | 19GB | 🏆 Excellents tests |
| CodeLLaMA:34b | 19GB | Très bon |
| DeepSeek-Coder:33b | 19GB | Bon |

### 📚 Documentation
| Modèle | Taille | Notes |
|--------|--------|-------|
| Mistral:7b | 4GB | 🏆 Rapide et clair |
| Neural-Chat:7b | 4GB | Bon |
| LLaMA2:7b | 4GB | Acceptable |


## Sélection Automatique

Si tu es indécis, utilise ce profil "intelligent":

```python
# config/settings.py
import os
import psutil

def get_available_gpu_memory():
    """Détecte la mémoire GPU disponible"""
    try:
        import torch
        if torch.cuda.is_available():
            return torch.cuda.get_device_properties(0).total_memory / 1e9
    except:
        pass
    return 0

gpu_mem = get_available_gpu_memory()

if gpu_mem < 10:  # < 10GB
    PROFILE = "LIGHT"
elif gpu_mem < 20:  # 10-20GB
    PROFILE = "MEDIUM"
else:  # > 20GB
    PROFILE = "HEAVY"

# Appliquer le profil approprié
```


## Installation Optimisée

### Télécharger avec script

**Windows:**
```powershell
# Profil léger
ollama pull mistral:7b

# Profil moyen
ollama pull mistral:7b; ollama pull neural-chat:7b; ollama pull codellama:13b

# Profil complet
ollama pull codellama:34b; ollama pull deepseek-coder:33b; ollama pull qwen2.5-coder:32b; ollama pull llama2:13b; ollama pull phind-coder:34b
```

**Linux/Mac:**
```bash
# Profil moyen
for model in mistral:7b neural-chat:7b codellama:13b; do
    ollama pull $model
done
```


## Benchmark Exemple

Temps pour générer une API simple (sur RTX 4090):

| Modèle | Architecture | Code | Review | Tests | Total |
|--------|--------------|------|--------|-------|-------|
| mistral:7b | 3s | 4s | 3s | 4s | 14s/iter |
| codellama:13b | 5s | 7s | 5s | 6s | 23s/iter |
| codellama:34b | 12s | 15s | 12s | 14s | 53s/iter |


## Conseil pour le Choix

```
Ai-je plus de 24GB GPU?
  → OUI: Utilise profil HEAVY (meilleure qualité)
  → NON
  
Ai-je plus de 16GB GPU?
  → OUI: Utilise profil MEDIUM (bon équilibre)
  → NON
  
Ai-je plus de 8GB GPU?
  → OUI: Utilise profil LIGHT (rapide)
  → NON: Utilise CPU uniquement (lent mais possible)
```

## Troubleshooting Modèles

**Modèle qui ne télécharge pas:**
```bash
ollama pull mistral:latest --insecure
```

**Vérifier téléchargement:**
```bash
ollama list
```

**Supprimer modèle:**
```bash
ollama rm mistral:latest
```

**Voir espace disque:**
```bash
ollama show mistral:latest
```

---

💡 **Conseil:** Commencez avec `mistral:7b` - c'est rapide et suffit pour tester!
