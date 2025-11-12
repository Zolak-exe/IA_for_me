"""
Implémentation des agents spécialisés.
"""

from .base_agent import BaseAgent, AgentOutput
import logging

logger = logging.getLogger(__name__)


class ArchitectAgent(BaseAgent):
    """Agent responsable de la conception architecture"""
    
    def __init__(self, ollama_client, model_name: str = "mistral"):
        super().__init__(ollama_client, model_name, "Architecte")
    
    def execute(self, requirements: str, iteration: int = 1) -> AgentOutput:
        """Crée l'architecture du projet"""
        
        prompt = f"""Tu es un architecte logiciel expert en conception système.

ITÉRATION: {iteration}

REQUIREMENTS CLIENT:
{requirements}

Génère une architecture détaillée complète avec:
1. **Diagramme composants** (en ASCII ou description textuelle)
2. **Patterns de design** appropriés (Hexagonale, Microservices, etc.)
3. **Stack technique** (langages, frameworks, databases)
4. **Modules principaux** et leur responsabilités
5. **Interfaces publiques** entre les modules
6. **Stratégie de scalabilité**
7. **Points de sécurité critiques** à prendre en compte

Format ta réponse en sections claires avec markdown.
"""
        
        content = self._call_llm(prompt, temperature=0.7)
        
        return AgentOutput(
            agent_name="ArchitectAgent",
            success=bool(content),
            content=content,
            score=100.0 if content else 0.0
        )


class DeveloperAgent(BaseAgent):
    """Agent responsable de la génération de code"""
    
    def __init__(self, ollama_client, model_name: str = "codellama"):
        super().__init__(ollama_client, model_name, "Développeur")
    
    def execute(
        self,
        architecture: str,
        requirements: str,
        language: str = "python",
        iteration: int = 1
    ) -> AgentOutput:
        """Génère le code selon l'architecture"""
        
        prompt = f"""Tu es un développeur expert en {language}.

ITÉRATION: {iteration}

ARCHITECTURE À IMPLÉMENTER:
{architecture[:2000]}...  # Limiter la longueur

REQUIREMENTS:
{requirements}

Génère du code professionnel:
- Code complet et fonctionnel (pas de pseudocode)
- Type hints stricts (mypy compatible)
- Docstrings Google style
- Gestion complète d'erreurs avec try/except
- Logging pertinent
- Pas de TODO ou commentaires TODO (code fini)
- Best practices {language}

Structure ta réponse:
1. **Fichiers à créer** (liste avec chemins)
2. **Code complet** (fichier par fichier)
3. **Dépendances** (requirements.txt si Python)
"""
        
        content = self._call_llm(prompt, temperature=0.5)
        
        return AgentOutput(
            agent_name="DeveloperAgent",
            success=bool(content),
            content=content,
            score=100.0 if content else 0.0
        )


class ReviewerAgent(BaseAgent):
    """Agent responsable du contrôle qualité"""
    
    def __init__(self, ollama_client, model_name: str = "deepseek-coder"):
        super().__init__(ollama_client, model_name, "Reviewer")
    
    def execute(
        self,
        code: str,
        architecture: str,
        iteration: int = 1
    ) -> AgentOutput:
        """Analyse et score la qualité du code"""
        
        prompt = f"""Tu es un expert en revue de code et qualité logicielle.

ITÉRATION: {iteration}

CODE À ANALYSER:
{code[:3000]}...

ARCHITECTURE CIBLE:
{architecture[:2000]}...

Effectue un audit complet:
1. **Conformité architecture** (0-100): Le code respecte-t-il l'architecture?
2. **Qualité du code** (0-100): Lisibilité, maintenabilité, best practices
3. **Gestion erreurs** (0-100): Complétude et pertinence
4. **Type hints** (0-100): Couverture et strictness
5. **Documentation** (0-100): Docstrings, commentaires utiles

Calcule un SCORE MOYEN final (0-100).

Format:
SCORE GLOBAL: [nombre]
PROBLÈMES DÉTECTÉS:
- [problème 1]
- [problème 2]
...

RECOMMANDATIONS:
- [recommandation 1]
- [recommandation 2]
...
"""
        
        content = self._call_llm(prompt, temperature=0.5)
        score = self.extract_score(content)
        
        return AgentOutput(
            agent_name="ReviewerAgent",
            success=bool(content),
            content=content,
            score=score,
            issues=self._extract_section(content, "PROBLÈMES"),
            recommendations=self._extract_section(content, "RECOMMANDATIONS")
        )
    
    def _extract_section(self, content: str, section_name: str) -> list:
        """Extrait les éléments d'une section"""
        import re
        pattern = f"{section_name}[:\\n]+(.*?)(?=\\n[A-Z]|$)"
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            items = re.findall(r"-\s*(.+?)(?=\n-|\n[A-Z]|$)", match.group(1), re.DOTALL)
            return [item.strip() for item in items if item.strip()]
        return []


class SecurityAgent(BaseAgent):
    """Agent responsable de l'audit sécurité"""
    
    def __init__(self, ollama_client, model_name: str = "mistral"):
        super().__init__(ollama_client, model_name, "Sécurité")
    
    def execute(
        self,
        code: str,
        requirements: str,
        iteration: int = 1
    ) -> AgentOutput:
        """Audit sécurité du code"""
        
        prompt = f"""Tu es un expert en sécurité logicielle et OWASP.

ITÉRATION: {iteration}

CODE À AUDITER:
{code[:3000]}...

REQUIREMENTS:
{requirements}

Analyse les risques sécurité (OWASP Top 10):
1. **Injection** (SQL, Command, etc.) - Risque 0-100
2. **Authentification faible** - Risque 0-100
3. **Exposition données sensibles** - Risque 0-100
4. **XXE/XML** - Risque 0-100
5. **Contrôle d'accès** - Risque 0-100
6. **Mauvaise configuration** - Risque 0-100

Score de sécurité final: 100 - RISQUE_MAXIMUM

VULNÉRABILITÉS TROUVÉES:
- [vulnérabilité]

CORRECTIONS RECOMMANDÉES:
- [correction]
"""
        
        content = self._call_llm(prompt, temperature=0.3)  # Température basse pour sécurité
        score = 100 - self.extract_score(content)  # Inverser le score (100 = secure)
        
        return AgentOutput(
            agent_name="SecurityAgent",
            success=bool(content),
            content=content,
            score=max(0, min(100, score)),
            issues=self._extract_section(content, "VULNÉRABILITÉS"),
        )
    
    def _extract_section(self, content: str, section_name: str) -> list:
        import re
        pattern = f"{section_name}[:\\n]+(.*?)(?=\\n[A-Z]|$)"
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            items = re.findall(r"-\s*(.+?)(?=\n-|\n[A-Z]|$)", match.group(1), re.DOTALL)
            return [item.strip() for item in items if item.strip()]
        return []


class TesterAgent(BaseAgent):
    """Agent responsable de la génération de tests"""
    
    def __init__(self, ollama_client, model_name: str = "qwen2.5-coder"):
        super().__init__(ollama_client, model_name, "Testeur")
    
    def execute(
        self,
        code: str,
        requirements: str,
        iteration: int = 1
    ) -> AgentOutput:
        """Génère les tests unitaires et intégration"""
        
        prompt = f"""Tu es un expert en tests logiciel et TDD.

ITÉRATION: {iteration}

CODE À TESTER:
{code[:3000]}...

REQUIREMENTS:
{requirements}

Génère une suite de tests complète:
1. **Tests unitaires** - 1 test par fonction/méthode
2. **Tests d'intégration** - Interaction entre composants
3. **Tests d'erreur** - Cas limites et exceptions
4. **Couverture** - Viser >90%

Format:
- Framework: pytest (Python) ou Jest (JS)
- Nommer les tests clairement: test_<fonction>_<cas>
- Inclure setup/teardown si nécessaire
- Documenter les cas de test

Génère le code complet des tests.
"""
        
        content = self._call_llm(prompt, temperature=0.5)
        
        return AgentOutput(
            agent_name="TesterAgent",
            success=bool(content),
            content=content,
            score=100.0 if content else 0.0
        )


class DocumentationAgent(BaseAgent):
    """Agent responsable de la documentation"""
    
    def __init__(self, ollama_client, model_name: str = "mistral"):
        super().__init__(ollama_client, model_name, "Documentation")
    
    def execute(
        self,
        architecture: str,
        code: str,
        requirements: str,
        iteration: int = 1
    ) -> AgentOutput:
        """Génère la documentation complète"""
        
        prompt = f"""Tu es un expert en documentation logicielle.

ITÉRATION: {iteration}

Génère la documentation complète du projet:

REQUIREMENTS:
{requirements}

ARCHITECTURE:
{architecture[:2000]}...

CODE:
{code[:2000]}...

Crée une documentation structurée en markdown:
1. **README.md** - Vue d'ensemble, installation, usage rapide
2. **ARCHITECTURE.md** - Détails architecture et design patterns
3. **API.md** - Documentation API/interfaces publiques
4. **SETUP.md** - Guide installation développeur
5. **TESTING.md** - Comment lancer les tests
6. **DEPLOYMENT.md** - Guide de déploiement
7. **TROUBLESHOOTING.md** - FAQ et problèmes courants

Chaque section doit être:
- Complète et auto-contenue
- Avec exemples concrets
- Bien formatée en markdown
"""
        
        content = self._call_llm(prompt, temperature=0.7)
        
        return AgentOutput(
            agent_name="DocumentationAgent",
            success=bool(content),
            content=content,
            score=100.0 if content else 0.0
        )
