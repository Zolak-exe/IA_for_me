# 📦 Structure du Projet - Multi-Agent System

## 🎯 Architecture Optimisée

Le projet a été réorganisé pour **performance maximale** et **facilité de maintenance** :

```
multi-agent-system/
├── bin/                          # Scripts de lancement
│   ├── run.bat                  # Windows PowerShell
│   └── run.sh                   # Linux/macOS bash
│
├── scripts/                      # Points d'entrée (exécutables)
│   ├── main.py                  # 🚀 Point d'entrée principal
│   ├── demo.py                  # Démo interactive
│   ├── example.py               # Exemple simple
│   ├── test_ollama.py           # Test connexion Ollama
│   └── validate_installation.py # Validation installation
│
├── src/                          # 🔒 Code source principal
│   ├── agents/                  # 6 agents IA spécialisés
│   │   ├── base_agent.py        # Classe de base abstraite
│   │   ├── specialized_agents.py # Implémentations (Architect, Developer, etc)
│   │   └── __init__.py          # Exports agents
│   │
│   ├── core/                    # Orchestration & Ollama
│   │   ├── ollama_client.py     # Client HTTP Ollama
│   │   ├── orchestrator.py      # Orchestrateur multi-agent
│   │   ├── logging_config.py    # Configuration logging
│   │   └── __init__.py          # Exports core
│   │
│   ├── utils/                   # Utilitaires
│   │   ├── exporters.py         # Export des solutions
│   │   ├── helpers.py           # Fonctions utiles
│   │   └── __init__.py          # Exports utils
│   │
│   ├── config/                  # Configuration système
│   │   ├── settings.py          # Paramètres globaux
│   │   └── __init__.py          # Exports config
│   │
│   └── __init__.py              # Package src
│
├── docs/                         # 📖 Documentation
│   ├── README.md                # Guide complet
│   ├── TROUBLESHOOTING.md       # Dépannage
│   ├── MODELS_GUIDE.md          # Modèles disponibles
│   ├── OLLAMA_SETUP.md          # Setup Ollama
│   └── STRUCTURE.md             # Ce fichier
│
├── outputs/                      # 📤 Résultats générés
│   └── (dossiers projets créés)
│
├── requirements.txt             # 📋 Dépendances Python
├── .gitignore                   # Config Git
└── README.md                    # (symlink vers docs/README.md)
```

## ✨ Optimisations Apportées

### 📊 Réductions de Fichiers
| Catégorie | Avant | Après | Réduction |
|-----------|-------|-------|-----------|
| **Fichiers doc** | 12 | 4 | **-67%** |
| **Dossiers racine** | 4 | 5 | Organisés |
| **Structure** | Plate | Hiérarchique | ✅ |

### 🚀 Performance
- ✅ Imports optimisés (chemins relatifs dans src/)
- ✅ Code consolidé dans scripts/ pour accès facile
- ✅ Documentation dédupliquée (docs/ unique)
- ✅ Configuration centralisée (src/config/)

### 📁 Organisation Logique
1. **src/** = Code production (immuable)
2. **scripts/** = Points d'entrée (exécutables)
3. **docs/** = Documentation complète
4. **bin/** = Launchers OS-spécifiques
5. **outputs/** = Résultats des générations

## 🚀 Comment Utiliser

### Installation
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Vérifier l'installation
python scripts/validate_installation.py
```

### Lancer le système
```bash
# Depuis Windows
python scripts\main.py --requirements "Créer une API REST"

# Depuis Linux/macOS
python scripts/main.py --requirements "Créer une API REST"

# Ou avec le launcher
./bin/run.sh  # Linux/macOS
.\bin\run.bat # Windows PowerShell
```

### Options disponibles
```bash
python scripts/main.py \
    --requirements "Description du projet" \
    [--max-iterations 15] \
    [--model codellama:34b] \
    [--output-dir ./outputs]
```

### Tester la démo
```bash
python scripts/demo.py
```

### Valider Ollama
```bash
python scripts/test_ollama.py
```

## 📂 Détails des Répertoires

### `/src/agents/`
Contient les 6 agents IA spécialisés :
- **ArchitectAgent** : Conception et patterns
- **DeveloperAgent** : Génération de code
- **ReviewerAgent** : Contrôle qualité
- **SecurityAgent** : Audit OWASP
- **TesterAgent** : Génération de tests
- **DocumentationAgent** : Documentation

### `/src/core/`
Système d'orchestration :
- **OllamaClient** : Communication HTTP avec Ollama
- **MultiAgentOrchestrator** : Gestion de la boucle itérative (max 15 itérations)
- **logging_config** : Configuration logging colorisé

### `/src/utils/`
Utilitaires de support :
- **SolutionExporter** : Export JSON, HTML, Markdown, Text
- **ReportGenerator** : Génération de rapports
- **helpers** : Fonctions utiles (retry, truncate, format)

### `/src/config/`
Configuration centralisée :
- Paramètres Ollama (URL, timeout)
- Modèles par agent
- Paramètres système (max_iterations, seuils)
- Poids de scoring (35% Qualité, 25% Sécurité, 20% Tests, 20% Documentation)

### `/scripts/`
Points d'entrée executables :
- Import depuis `../src/` via `sys.path.insert(0, ...)`
- Utilisation facile : `python main.py --requirements "..."`
- Scripts helpers pour démo, test, validation

### `/bin/`
Launchers OS-spécifiques :
- **run.bat** : PowerShell Windows
- **run.sh** : Bash Linux/macOS

### `/docs/`
Documentation réduite (4 fichiers essentiels) :
- **README.md** : Guide complet avec tous les détails
- **TROUBLESHOOTING.md** : Solutions aux problèmes
- **MODELS_GUIDE.md** : Modèles disponibles
- **OLLAMA_SETUP.md** : Installation Ollama

### `/outputs/`
Résultats générés par le système :
- Structure : `outputs/{project_name}/`
- Formats : `solution.json`, `solution.html`, `solution.md`, `solution.txt`

## 🔧 Chemins Relatifs

Tous les imports utilisent maintenant les chemins corrects :

```python
# Dans scripts/main.py :
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.core import OllamaClient, MultiAgentOrchestrator
from src.utils.exporters import SolutionExporter
from src.config.settings import OLLAMA_CONFIG

# Dans src/core/orchestrator.py :
from ..agents import (ArchitectAgent, DeveloperAgent, ...)
```

## 📊 Statistiques Finales

| Métrique | Valeur |
|----------|--------|
| **Fichiers Python** | 18 |
| **Fichiers documentation** | 4 |
| **Total fichiers** | 25 |
| **Dossiers** | 5 principaux |
| **Agents** | 6 |
| **Max itérations** | 15 |

## ✅ Checklist d'Utilisation

- [ ] `pip install -r requirements.txt`
- [ ] `python scripts/validate_installation.py`
- [ ] `python scripts/test_ollama.py` (Ollama doit tourner)
- [ ] `python scripts/demo.py` (pour tester)
- [ ] `python scripts/main.py --requirements "Votre projet"`

## 🎉 Résultat Final

**Système optimisé, organisé et prêt pour la production !**

- ✅ Structure logique et claire
- ✅ Imports corrigés et fonctionnels
- ✅ Documentation dédupliquée
- ✅ Performance maximale
- ✅ Facile à maintenir et étendre
