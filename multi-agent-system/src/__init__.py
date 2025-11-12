"""
Système Multi-Agents Auto-Correctif pour Génération de Projets

Un système autonome orchestrant 6 agents IA spécialisés:
- Architecte: Conception et design patterns
- Développeur: Génération de code
- Reviewer: Contrôle qualité
- Sécurité: Audit sécurité OWASP
- Testeur: Génération de tests
- Documentation: Documentation complète

Capable de:
✓ Générer un projet complet
✓ Vérifier qualité et sécurité
✓ Corriger automatiquement
✓ S'améliorer en boucle (15 itérations max)
✓ Exporter tous les artefacts
"""

__version__ = "1.0.0"
__author__ = "Multi-Agent System"

from .core import OllamaClient, MultiAgentOrchestrator
from .agents import BaseAgent, ArchitectAgent, DeveloperAgent

__all__ = [
    "OllamaClient",
    "MultiAgentOrchestrator",
    "BaseAgent",
    "ArchitectAgent",
    "DeveloperAgent"
]
