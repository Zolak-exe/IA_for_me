# 🆘 Guide Dépannage Complet

## ❌ Erreurs Communes et Solutions

### 1. "Ollama non disponible"

```
❌ Impossible de se connecter à Ollama
   Vérifiez que Ollama est running sur http://localhost:11434
```

**Causes possibles:**
- Ollama n'est pas lancé
- Port 11434 bloqué/utilisé par autre processus
- Ollama installé mais non configuré

**Solutions:**

```bash
# 1. Vérifier si Ollama est lancé
curl http://localhost:11434/api/tags

# 2. Si erreur, lancer Ollama
ollama serve

# 3. Sur Windows, vérifier le service
Get-Service Ollama

# 4. Si port occupé, trouver le processus
netstat -ano | findstr :11434  # Windows
lsof -i :11434                  # Linux/Mac

# 5. Redémarrer Ollama
# Windows: taskkill /PID <PID> /F
# Linux/Mac: kill -9 <PID>
```


### 2. "Aucun modèle trouvé"

```
⚠️  Aucun modèle trouvé
   Télécharge au moins un modèle avec: ollama pull mistral
```

**Causes:**
- Aucun modèle n'a été téléchargé
- Modèles corrompus/mal téléchargés
- Répertoire modèles inaccessible

**Solutions:**

```bash
# 1. Lister modèles disponibles
ollama list

# 2. Télécharger modèle (recommandé: mistral)
ollama pull mistral:latest

# 3. Ou choisir autre modèle
ollama pull neural-chat:7b
ollama pull llama2:7b

# 4. Vérifier espace disque
df -h  # Linux/Mac
Disk Usage  # Windows

# 5. Si corruption, supprimer et réinstaller
ollama rm mistral:latest
ollama pull mistral:latest
```


### 3. "Timeout" lors de la génération

```
Timeout tentative 1/3
Timeout tentative 2/3
❌ Impossible de générer après 3 tentatives
```

**Causes:**
- Modèle trop gros pour votre GPU
- Trop peu de VRAM disponible
- Réseau lent
- Modèle trop complexe

**Solutions:**

```python
# config/settings.py
OLLAMA_CONFIG = {
    "timeout": 600,  # Augmenter de 300 à 600 (10 min)
}

# OU utiliser un modèle plus léger:
AGENT_MODELS = {
    "architect": "mistral:7b",      # Léger
    "developer": "mistral:7b",
    # ...
}

# OU réduire les itérations:
# main.py --max-iterations 3
```

**Vérifier ressources:**

```bash
# GPU NVIDIA
nvidia-smi

# GPU AMD
rocm-smi

# Mémoire générale
free -h  # Linux/Mac
systeminfo | findstr Memory  # Windows
```


### 4. "Out of Memory" (OOM)

```
CUDA out of memory
RuntimeError: CUDA ran out of memory
```

**Causes:**
- GPU manque de VRAM
- Modèle trop gros
- Trop d'instances du modèle chargées

**Solutions:**

```bash
# 1. Vérifier VRAM disponible
nvidia-smi -q -d Memory | head -n 3

# 2. Libérer mémoire
# Fermer autres applications
# Redémarrer Ollama et les applications

# 3. Utiliser modèles plus petits
ollama pull mistral:7b  # 4GB
ollama rm codellama:34b  # Supprimer le gros

# 4. Changer configuration
# config/settings.py -> utiliser mistral partout
```

**Profil mémoire par modèle:**
- 7B: 4-6 GB VRAM
- 13B: 8-10 GB VRAM
- 34B: 18-24 GB VRAM


### 5. "Type error" ou "JSON decode error"

```
JSONDecodeError: Expecting value
AttributeError: 'NoneType' object has no attribute 'get'
```

**Causes:**
- Réponse malformée d'Ollama
- Modèle pas complètement lancé
- Problème réseau

**Solutions:**

```bash
# 1. Vérifier santé Ollama
curl http://localhost:11434/api/tags -v

# 2. Relancer Ollama
# Ctrl+C pour arrêter
# ollama serve pour relancer

# 3. Vérifier modèle
ollama list
ollama show mistral:latest

# 4. Activer logs détaillés
# main.py --verbose

# 5. Vérifier Python version
python --version  # Doit être 3.10+
```


### 6. "ModuleNotFoundError"

```
ModuleNotFoundError: No module named 'requests'
```

**Causes:**
- Dépendances non installées
- Virtualenv pas activé
- Mauvais Python utilisé

**Solutions:**

```bash
# 1. Vérifier virtualenv actif
which python  # Doit indiquer venv/bin/python

# 2. Activer virtualenv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Vérifier installation
pip list | grep requests

# 5. Réinstaller si besoin
pip install --upgrade requests
```


### 7. "Port already in use"

```
OSError: [Errno 48] Address already in use
Address 127.0.0.1:11434 is already in use
```

**Causes:**
- Port 11434 déjà utilisé
- Ollama en double
- Autre service sur ce port

**Solutions:**

```bash
# 1. Trouver le processus
netstat -ano | findstr :11434  # Windows
lsof -i :11434                  # Linux/Mac

# 2. Vérifier si c'est Ollama
ps aux | grep ollama

# 3. Tuer le processus
taskkill /PID 12345 /F  # Windows (remplacer 12345)
kill -9 12345           # Linux/Mac

# 4. OU changer le port (config/settings.py)
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11435",  # Nouveau port
}
```


### 8. Génération de code vide

```
✓ Génération terminée
   Réponse: ""
```

**Causes:**
- Modèle ne répond pas
- Prompt trop complexe
- Température trop basse

**Solutions:**

```python
# config/settings.py
GENERATION_PARAMS = {
    "developer": {
        "temperature": 0.7,  # Augmenter de 0.5 à 0.7
    }
}

# OU vérifier le modèle
# ollama show mistral:latest
# ollama list

# OU activer logs détaillés pour voir les prompts
# main.py --verbose

# OU utiliser modèle différent
AGENT_MODELS = {
    "developer": "neural-chat:7b",  # Essayer autre
}
```


### 9. "Connection refused"

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Causes:**
- Ollama pas lancé
- URL incorrecte
- Firewall bloque connexion

**Solutions:**

```bash
# 1. Lancer Ollama
ollama serve

# 2. Vérifier URL
# config/settings.py -> "http://localhost:11434"

# 3. Tester connexion manuelle
curl http://localhost:11434/api/tags

# 4. Vérifier firewall
# Windows: Windows Defender Firewall
# Linux: sudo ufw allow 11434
```


### 10. Performance lente

```
Phase 1: Architecture... (30s+ attente)
Très lent lors génération
```

**Causes:**
- GPU chargé
- Modèle trop gros
- CPU utilisé au lieu GPU

**Solutions:**

```bash
# 1. Vérifier GPU utilisé
nvidia-smi  # Doit voir CUDA
rocm-smi    # Doit voir ROCm

# 2. Libérer GPU
# Fermer applications gourmandes

# 3. Réduire taille modèle
ollama rm codellama:34b
ollama pull mistral:7b

# 4. Augmenter batch size (si config GPU avancée)

# 5. Réduire nombre itérations
main.py --max-iterations 3

# 6. Profiling (benchmark)
# Voir MODELS_GUIDE.md
```


═══════════════════════════════════════════════════════════════

## 🔍 DEBUGGING AVANCÉ

### Activer tous les logs

```bash
python main.py --requirements "..." --verbose
```

Génère logs détaillés dans `system.log`


### Tester composant par composant

```bash
# 1. Test Ollama seul
python test_ollama.py

# 2. Test avec petit modèle
python example.py

# 3. Test avec démo interactive
python demo.py

# 4. Test spécifique agent
python -c "
from core import OllamaClient
from agents import ArchitectAgent
# ...
"
```


### Profiling d'exécution

```bash
# Mesurer temps avec verbose
python -m cProfile -s cumtime main.py --requirements "..." --verbose | head -20

# Voir utilisation mémoire
python -m memory_profiler main.py --requirements "..." --verbose
```


### Vérifier les fichiers de log

```bash
# Affichage temps réel
tail -f system.log

# Rechercher erreurs
grep -i error system.log

# Dernières 50 lignes
tail -50 system.log
```


═══════════════════════════════════════════════════════════════

## 💡 CONSEILS

1. **Commencer simple**
   - Tester d'abord avec 3 itérations
   - Utiliser mistral:7b
   - Petit projet pour validation

2. **Surveiller ressources**
   - Ouvrir nvidia-smi avant lancement
   - Garder ~30% VRAM libre
   - Fermer applications lourdes

3. **Lire les logs**
   - system.log = meilleure source info
   - --verbose pour plus de détails
   - Chercher "Error" ou "Failed"

4. **Backup modèles**
   - Modèles téléchargés peuvent être volumineux
   - Sauvegarder ~/.ollama après setup
   - Ne réinstaller que si nécessaire

5. **Expérimenter**
   - Essayer différents modèles
   - Varier température/paramètres
   - Consulter MODELS_GUIDE.md


═══════════════════════════════════════════════════════════════

## 📞 SUPPORT

Si problème persiste:

1. Consulter les logs: `system.log`
2. Relire cette page
3. Vérifier `README.md`
4. Tester `test_ollama.py`
5. Essayer `demo.py` avec projet pré-défini

Informations utiles pour dépannage:
- `python --version`
- `ollama list`
- GPU disponible (`nvidia-smi`)
- OS (Windows/Linux/Mac)
- Messages d'erreur exacts
