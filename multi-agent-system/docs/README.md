# 🤖 Système Multi-Agents Auto-Correctif

Un système autonome qui orchestre 6 agents IA spécialisés pour générer, vérifier, tester, sécuriser et documenter un projet complet.

## ✨ Caractéristiques

- **6 agents spécialisés**: Architecte, Développeur, Reviewer, Sécurité, Testeur, Documentation
- **Boucle d'amélioration continue**: Jusqu'à 15 itérations pour atteindre la qualité cible
- **Exécution 100% locale**: Utilise Ollama pour les modèles LLM locaux
- **Critères d'arrêt intelligents**: Détecte stagnation, qualité atteinte, etc.
- **Export complet**: Architecture, code, tests, sécurité, documentation
- **Rapports détaillés**: Métriques, scores, problèmes détectés

## 🏗️ Architecture

```
Multi-Agent System
├── 👨‍💼 ArchitectAgent: Conception architecture hexagonale
├── 👨‍💻 DeveloperAgent: Génération de code professionnel
├── 🔍 ReviewerAgent: Audit qualité et best practices
├── 🔒 SecurityAgent: Audit OWASP et vulnérabilités
├── ✅ TesterAgent: Génération tests unitaires
└── 📚 DocumentationAgent: Documentation complète

Orchestrateur
├── Gère le workflow itératif
├── Calcule score global pondéré
├── Détecte critères d'arrêt
└── Sauvegarde meilleure solution
```

## 📋 Prérequis

### 1. Installer Ollama

**Windows:**
```powershell
# Télécharger depuis https://ollama.ai
# Ou utiliser winget
winget install Ollama.Ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Télécharger des modèles

```bash
# Modèles recommandés
ollama pull mistral:latest          # Léger et performant
ollama pull neural-chat:latest      # Bon rapport qualité/taille
ollama pull codellama:13b           # Pour la génération code

# OU si tu as de la VRAM disponible
ollama pull codellama:34b
ollama pull deepseek-coder:33b
ollama pull qwen2.5-coder:32b
```

Vérifier les modèles:
```bash
ollama list
```

### 3. Lancer Ollama

```bash
# Par défaut sur http://localhost:11434
ollama serve

# Windows: Ollama lance un service en arrière-plan
```

### 4. Python 3.10+

```bash
python --version  # Vérifier
```

## 🚀 Installation

### 1. Cloner/Copier le projet

```bash
cd h:\DevAI\multi-agent-system
```

### 2. Créer un environnement virtuel

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Utilisation simple

```bash
python main.py --requirements "Créer une API REST en Python avec FastAPI"
```

### Avec options avancées

```bash
python main.py \
  --requirements "Créer un CLI tool pour gérer des tâches" \
  --max-iterations 10 \
  --threshold 85 \
  --output ./mon-projet \
  --verbose
```

### Options disponibles

```
--requirements TEXT         ✓ Description du projet (obligatoire)
--max-iterations INT        Nombre max d'itérations (défaut: 15)
--threshold FLOAT          Seuil de qualité 0-100 (défaut: 90)
--output PATH              Dossier résultats (défaut: ./outputs)
--verbose                  Affichage DEBUG détaillé
```

## 📊 Résultats

La sortie sera dans `./outputs/project_YYYYMMDD_HHMMSS/`:

```
project_20240315_143022/
├── SUMMARY.json           # Résumé exécution
├── METRICS.json           # Métriques itérations
├── ARCHITECTURE.md        # Design et patterns
├── CODE.md               # Code source généré
├── TESTS.md              # Suite tests unitaires
├── DOCUMENTATION.md      # Guide complet
├── REPORT.txt            # Rapport texte
└── REPORT.html           # Rapport HTML
```

## 🎯 Exemple d'exécution

```bash
$ python main.py --requirements "API REST pour gestion de tâches avec authentification JWT"

╔════════════════════════════════════════════════════════════╗
║      🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖            ║
╚════════════════════════════════════════════════════════════╝

🔌 Initialisation client Ollama...
✅ Connexion à Ollama établie
   Status: ok
   Modèles disponibles: 5

🏗️  Initialisation du système multi-agents...
   ✓ 6 agents initialisés
     • Architecte (codellama:34b)
     • Développeur (deepseek-coder:33b)
     • Reviewer (qwen2.5-coder:32b)
     • Sécurité (llama2:13b)
     • Testeur (phind-coder:34b)
     • Documentation (mistral:7b)

📋 REQUIREMENTS:
   API REST pour gestion de tâches avec authentification JWT

============================================================

🔄 ITÉRATION 1/15
============================================================
👨‍💼 Phase 1: Architecture...
👨‍💻 Phase 2: Développement...
🔍 Phase 3: Revue qualité...
🔒 Phase 4: Audit sécurité...
✅ Phase 5: Génération tests...
📚 Phase 6: Documentation...

📊 ITÉRATION 1:
├─ Score global: 72.3% 
├─ Qualité code: 68.5%
├─ Sécurité: 75.2%
├─ Problèmes détectés: 5
├─ Améliorations: 3
└─ Meilleur: 72.3% (itération 1)

[Itérations 2-8: amélioration progressive...]

🔄 ITÉRATION 9/15
============================================================
📊 ITÉRATION 9:
├─ Score global: 92.1% 
├─ Qualité code: 91.0%
├─ Sécurité: 93.5%
├─ Problèmes détectés: 1
├─ Améliorations: 0
└─ Meilleur: 92.1% (itération 9)

✅ Qualité 92.1% atteinte (seuil: 90%)

============================================================
🎉 RÉSUMÉ FINAL:
============================================================
✅ Itérations exécutées: 9/15
✅ Meilleur score: 92.1%
✅ Itération gagnante: 9
✅ Solution exportée dans: ./outputs/project_20240315_143022
✅ EXÉCUTION COMPLÉTÉE AVEC SUCCÈS!
```

## ⚙️ Configuration

Voir `config/settings.py` pour personnaliser:

- **Modèles LLM** utilisés par chaque agent
- **Paramètres génération** (température, top_p, etc.)
- **Critères d'arrêt** (seuil qualité, stagnation, etc.)
- **Pondérations** du score global

## 📈 Métriques et Scoring

### Score Global (pondéré)

```
Score = (0.35 × Qualité) + (0.25 × Sécurité) + (0.20 × Tests) + (0.20 × Docs)
```

### Critères de qualité

- **Qualité Code (0-100)**: Conformité architecture, lisibilité, best practices
- **Sécurité (0-100)**: Absence vulnérabilités OWASP
- **Tests (0-100)**: Présence tests unitaires, couverture
- **Documentation (0-100)**: Complétude, clarté

### Arrêt automatique

Le système s'arrête si:
1. **Score ≥ 90%** (seuil par défaut)
2. **3 itérations sans amélioration** (stagnation)
3. **Max 15 itérations atteintes**

## 🔍 Dépannage

### Ollama ne répond pas

```
❌ Impossible de se connecter à Ollama
   Vérifiez que Ollama est running sur http://localhost:11434
```

**Solution:**
```bash
ollama serve
```

### Aucun modèle disponible

```
⚠️  Aucun modèle trouvé
   Télécharge au moins un modèle avec: ollama pull mistral
```

**Solution:**
```bash
ollama pull mistral:latest
ollama list  # Vérifier
```

### Timeout (génération trop lente)

Augmente le timeout dans `config/settings.py`:
```python
OLLAMA_CONFIG = {
    "timeout": 600,  # 10 minutes au lieu de 5
}
```

Ou utilise des modèles plus légers:
```python
AGENT_MODELS = {
    "architect": "mistral:7b",
    "developer": "mistral:7b",
    # ...
}
```

### Mémoire insuffisante

Si le GPU manque de VRAM:

1. Réduire la taille des modèles
2. Utiliser modèles 7B au lieu de 34B
3. Laisser plus de mémoire libre avant lancement

## 📚 Documentation technique

### Structure agents

Tous les agents héritent de `BaseAgent`:

```python
class ArchitectAgent(BaseAgent):
    def execute(self, requirements: str) -> AgentOutput:
        # Implémentation spécifique
        pass
```

### Workflow itératif

1. **Architecte** → Conception architecture
2. **Développeur** → Code selon architecture
3. **Reviewer** → Score qualité
4. **Sécurité** → Vulnérabilités
5. **Testeur** → Tests unitaires
6. **Documentation** → Docs
7. **Orchestrateur** → Score global + décision arrêt

### Sortie `AgentOutput`

```python
@dataclass
class AgentOutput:
    agent_name: str
    success: bool
    content: str
    score: Optional[float] = None
    issues: list = None
    recommendations: list = None
```

## 🎓 Améliorations futures

- [ ] Support GPU ROCm/CUDA pour accélération
- [ ] Cache persistant des résultats
- [ ] Parallel execution d'agents indépendants
- [ ] Web UI pour suivi en temps réel
- [ ] Intégration CI/CD
- [ ] Support multiples langages (Go, Rust, etc.)
- [ ] Analyse de coût en tokens
- [ ] Fine-tuning des prompts adaptatifs

## 📝 License

MIT

## 👨‍💻 Support

Pour problèmes ou suggestions, voir les logs dans `system.log`
