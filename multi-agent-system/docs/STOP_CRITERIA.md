# 🛑 Critères d'Arrêt du Système Multi-Agents

## 📋 Vue d'Ensemble

Le système **NE continue PAS jusqu'à 15 itérations automatiquement**. Il s'arrête dès qu'**UN des critères d'arrêt est atteint** :

## 🎯 3 Critères d'Arrêt

### 1️⃣ **Critère de Qualité Atteint** ✅
```
Condition: score_global >= seuil_qualité
Défaut: 90% (configurable)

Exemple:
- Seuil défini: 90%
- Score itération 5: 92%
→ ARRÊT à l'itération 5 ✅
```

**Impact**: Si la qualité cible est atteinte, on arrête immédiatement.

---

### 2️⃣ **Stagnation Détectée** ⏱️
```
Condition: 3 itérations consécutives sans amélioration
Format: Les 3 dernières itérations ont un score ≤ meilleur_score

Exemple:
- Itération 7: 87% ← Meilleur score
- Itération 8: 85% ← Pas d'amélioration
- Itération 9: 86% ← Pas d'amélioration
- Itération 10: 84% ← Pas d'amélioration (3ème sans amélioration)
→ ARRÊT à l'itération 10 ⏱️
```

**Impact**: Si le système stagne (pas de progrès pendant 3 itérations), on arrête pour économiser du temps de calcul.

---

### 3️⃣ **Max Itérations Atteint** 🔄
```
Condition: iteration_count >= max_iterations
Défaut: 15 itérations max

Exemple:
- Max itérations: 15
- Itération 15 complétée
→ ARRÊT à l'itération 15 (aucun autre critère atteint)
```

**Impact**: Limite absolue de sécurité pour éviter une exécution infinie.

---

## 📊 Tableau Récapitulatif

| Critère | Condition | Action | Priorité |
|---------|-----------|--------|----------|
| **Qualité** | Score ≥ seuil | Arrêt immédiat | Haute |
| **Stagnation** | 3 itérations sans amélioration | Arrêt immédiat | Moyenne |
| **Max itérations** | Itération 15 atteinte | Arrêt final | Basse |

---

## 🔄 Ordre de Vérification

À la fin de **CHAQUE itération**, le système vérifie dans cet ordre:

```
1. Score ≥ 90% ?
   ├─ OUI → ARRÊT ✅
   └─ NON → Continuer

2. 3 itérations consécutives sans amélioration ?
   ├─ OUI → ARRÊT ⏱️
   └─ NON → Continuer

3. Itération 15 atteinte ?
   ├─ OUI → ARRÊT 🔄
   └─ NON → Itération suivante
```

---

## 💡 Exemples Réels

### Exemple 1: Arrêt par Qualité
```
Itération 1: Score 45% → Continue
Itération 2: Score 67% → Continue
Itération 3: Score 78% → Continue
Itération 4: Score 85% → Continue
Itération 5: Score 92% → ARRÊT ✅ (Qualité atteinte!)

Total: 5 itérations exécutées (au lieu de 15)
Raison: Seuil de qualité (90%) dépassé
```

### Exemple 2: Arrêt par Stagnation
```
Itération 1: Score 45% → Continue
Itération 2: Score 62% → Continue (Meilleur: 62%)
Itération 3: Score 73% → Continue (Meilleur: 73%)
Itération 4: Score 79% → Continue (Meilleur: 79%)
Itération 5: Score 75% → Continue (Pas meilleur)
Itération 6: Score 76% → Continue (Pas meilleur)
Itération 7: Score 74% → ARRÊT ⏱️ (3ème consécutive sans amélioration)

Total: 7 itérations exécutées
Raison: Stagnation (pas de progrès depuis 3 itérations)
```

### Exemple 3: Arrêt par Max Itérations
```
Itération 1-8: Scores croissants (45% → 80%)
Itération 9: Score 82% → Meilleur, continue
Itération 10: Score 81% → Pas d'amélioration, continue
Itération 11: Score 80% → Pas d'amélioration, continue
Itération 12: Score 79% → Pas d'amélioration
...
Itération 15: Score 78% → ARRÊT 🔄 (Max itérations atteint)

Total: 15 itérations exécutées (cas rare)
Raison: Limite absolue de sécurité atteinte
```

---

## ⚙️ Configuration

### Modifier le Seuil de Qualité
```python
# Dans src/config/settings.py
SYSTEM_CONFIG = {
    "quality_threshold": 85.0,  # Réduire à 85% pour arrêter plus tôt
    "max_iterations": 15
}
```

### Modifier les Max Itérations
```python
# Dans src/config/settings.py
SYSTEM_CONFIG = {
    "quality_threshold": 90.0,
    "max_iterations": 10  # Réduire à 10 itérations max
}
```

### Au Lancement du Programme
```bash
# Depuis le script main.py
python scripts/main.py \
    --requirements "Votre projet" \
    --quality-threshold 85 \
    --max-iterations 10
```

---

## 📈 Stratégie Recommandée

### Pour Développement Rapide
```python
quality_threshold = 75.0   # Moins strict
max_iterations = 5         # Moins d'itérations
```
→ Résultat en 1-3 itérations généralement

### Pour Production
```python
quality_threshold = 90.0   # Strict
max_iterations = 15        # Maximum de sécurité
```
→ Résultat en 3-8 itérations généralement

### Pour Recherche/Optimisation
```python
quality_threshold = 95.0   # Très strict
max_iterations = 20        # Illimité presque
```
→ Résultat en 5-15 itérations

---

## 🎯 Résumé

**Question**: "Les agents s'arrêtent une fois que toutes les requêtes sont respectées ou font le max d'itération?"

**Réponse**: **Les deux!** 🎯

1. ✅ **S'arrêtent dès que la qualité est atteinte** (par défaut 90%)
2. ⏱️ **S'arrêtent si stagnation** (3 itérations sans amélioration)
3. 🔄 **S'arrêtent au max d'itérations** (15 par défaut, si aucun autre critère atteint)

Le système est **intelligent** et **optimisé**: il n'exécute que les itérations nécessaires, pas forcément les 15 d'office.

---

## 📊 Statistiques Typiques

| Configuration | Cas Moyen | Cas Rapide | Cas Lent |
|---------------|-----------|-----------|----------|
| **Itérations** | 4-6 | 1-3 | 10-15 |
| **Temps** | 2-5 min | 30s-2min | 10-30min |
| **Score final** | 85-92% | 75-85% | 92-98% |
| **Critère d'arrêt** | Qualité | Qualité | Stagnation/Max |
