"""
Orchestrateur principal qui coordonne tous les agents.
Gère la boucle itérative avec critères d'arrêt intelligents.
"""

from dataclasses import dataclass, field
from typing import Optional
import logging
import json
from pathlib import Path
from datetime import datetime

from ..agents import (
    ArchitectAgent,
    DeveloperAgent,
    ReviewerAgent,
    SecurityAgent,
    TesterAgent,
    DocumentationAgent,
    AgentOutput
)

logger = logging.getLogger(__name__)


@dataclass
class IterationMetrics:
    """Métriques pour une itération"""
    iteration: int
    timestamp: str
    architect_output: Optional[AgentOutput] = None
    developer_output: Optional[AgentOutput] = None
    reviewer_score: Optional[float] = None
    security_score: Optional[float] = None
    tester_output: Optional[AgentOutput] = None
    documentation_output: Optional[AgentOutput] = None
    overall_score: float = 0.0
    issues_count: int = 0
    improvements: list = field(default_factory=list)
    
    def to_dict(self):
        return {
            "iteration": self.iteration,
            "timestamp": self.timestamp,
            "overall_score": self.overall_score,
            "reviewer_score": self.reviewer_score,
            "security_score": self.security_score,
            "issues_count": self.issues_count,
            "improvements": self.improvements
        }


class MultiAgentOrchestrator:
    """
    Orchestrateur principal coordonnant tous les agents.
    Gère la boucle itérative avec 15 itérations max.
    """
    
    def __init__(
        self,
        ollama_client,
        max_iterations: int = 15,
        quality_threshold: float = 90.0,
        output_dir: str = "./outputs"
    ):
        self.ollama_client = ollama_client
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialiser les agents
        self.agents = {
            'architect': ArchitectAgent(ollama_client),
            'developer': DeveloperAgent(ollama_client),
            'reviewer': ReviewerAgent(ollama_client),
            'security': SecurityAgent(ollama_client),
            'tester': TesterAgent(ollama_client),
            'documentation': DocumentationAgent(ollama_client)
        }
        
        # State tracking
        self.iteration_count = 0
        self.best_score = 0.0
        self.best_solution = None
        self.best_iteration = 0
        self.metrics_history = []
        self.architecture = ""
        self.code = ""
        self.all_issues = []
        
    def run(self, requirements: str) -> dict:
        """
        Lance la boucle principale d'amélioration continue.
        Retourne la meilleure solution trouvée.
        """
        logger.info("🚀 Démarrage du système multi-agents")
        logger.info(f"📋 Requirement: {requirements[:100]}...")
        logger.info(f"⚙️  Max itérations: {self.max_iterations}")
        
        for iteration in range(1, self.max_iterations + 1):
            self.iteration_count = iteration
            logger.info(f"\n{'='*60}")
            logger.info(f"🔄 ITÉRATION {iteration}/{self.max_iterations}")
            logger.info(f"{'='*60}")
            
            try:
                metrics = self._run_iteration(requirements, iteration)
                self.metrics_history.append(metrics)
                
                # Afficher les métriques
                self._display_iteration_summary(metrics)
                
                # Vérifier critères d'arrêt
                should_stop, reason = self._check_stop_criteria(metrics)
                
                if should_stop:
                    logger.info(f"\n✅ {reason}")
                    logger.info(f"🏆 Meilleure solution trouvée itération {self.best_iteration}")
                    break
                    
            except Exception as e:
                logger.error(f"❌ Erreur itération {iteration}: {e}", exc_info=True)
                continue
        
        logger.info(f"\n{'='*60}")
        logger.info("🎯 RÉSUMÉ FINAL")
        logger.info(f"{'='*60}")
        self._display_final_summary()
        
        return self._package_solution()
    
    def _run_iteration(self, requirements: str, iteration: int) -> IterationMetrics:
        """Exécute une itération complète"""
        
        metrics = IterationMetrics(
            iteration=iteration,
            timestamp=datetime.now().isoformat()
        )
        
        # Phase 1: Architecture
        logger.info("👨‍💼 Phase 1: Architecture...")
        arch_output = self.agents['architect'].execute(requirements, iteration)
        self.architecture = arch_output.content
        metrics.architect_output = arch_output
        
        # Phase 2: Développement
        logger.info("👨‍💻 Phase 2: Développement...")
        dev_output = self.agents['developer'].execute(
            self.architecture,
            requirements,
            iteration=iteration
        )
        self.code = dev_output.content
        metrics.developer_output = dev_output
        
        # Phase 3: Revue Qualité
        logger.info("🔍 Phase 3: Revue qualité...")
        review_output = self.agents['reviewer'].execute(
            self.code,
            self.architecture,
            iteration=iteration
        )
        metrics.reviewer_score = review_output.score or 0.0
        metrics.issues_count = len(review_output.issues)
        metrics.improvements.extend(review_output.recommendations)
        
        # Phase 4: Sécurité
        logger.info("🔒 Phase 4: Audit sécurité...")
        security_output = self.agents['security'].execute(
            self.code,
            requirements,
            iteration=iteration
        )
        metrics.security_score = security_output.score or 0.0
        self.all_issues.extend(security_output.issues)
        
        # Phase 5: Tests
        logger.info("✅ Phase 5: Génération tests...")
        test_output = self.agents['tester'].execute(
            self.code,
            requirements,
            iteration=iteration
        )
        metrics.tester_output = test_output
        
        # Phase 6: Documentation
        logger.info("📚 Phase 6: Documentation...")
        doc_output = self.agents['documentation'].execute(
            self.architecture,
            self.code,
            requirements,
            iteration=iteration
        )
        metrics.documentation_output = doc_output
        
        # Calculer score global
        metrics.overall_score = self._calculate_overall_score(metrics)
        
        # Mise à jour meilleure solution
        if metrics.overall_score > self.best_score:
            self.best_score = metrics.overall_score
            self.best_iteration = iteration
            self.best_solution = {
                'architecture': self.architecture,
                'code': self.code,
                'tests': test_output.content,
                'documentation': doc_output.content,
                'metrics': metrics,
                'iteration': iteration
            }
            logger.info(f"🏆 NOUVELLE MEILLEURE SOLUTION! Score: {self.best_score:.1f}%")
        
        return metrics
    
    def _calculate_overall_score(self, metrics: IterationMetrics) -> float:
        """Calcule un score global pondéré"""
        weights = {
            'review': 0.35,      # Qualité code
            'security': 0.25,    # Sécurité (important!)
            'tester': 0.20,      # Tests
            'documentation': 0.20  # Documentation
        }
        
        score = (
            (metrics.reviewer_score or 0) * weights['review'] +
            (metrics.security_score or 0) * weights['security'] +
            (100.0 if metrics.tester_output else 0) * weights['tester'] +
            (100.0 if metrics.documentation_output else 0) * weights['documentation']
        )
        
        return min(100.0, max(0.0, score))
    
    def _check_stop_criteria(self, metrics: IterationMetrics) -> tuple[bool, str]:
        """Vérifie les critères d'arrêt"""
        
        # Critère 1: Qualité atteinte
        if metrics.overall_score >= self.quality_threshold:
            return True, f"✅ Qualité {metrics.overall_score:.1f}% atteinte (seuil: {self.quality_threshold}%)"
        
        # Critère 2: Stagnation (3 itérations sans amélioration)
        if len(self.metrics_history) >= 3:
            recent = self.metrics_history[-3:]
            if all(m.overall_score <= self.best_score for m in recent):
                return True, "✅ Stagnation détectée: 3 itérations sans amélioration"
        
        # Critère 3: Max itérations atteint
        if self.iteration_count >= self.max_iterations:
            return True, f"✅ Max itérations ({self.max_iterations}) atteint"
        
        return False, ""
    
    def _display_iteration_summary(self, metrics: IterationMetrics):
        """Affiche un résumé de l'itération"""
        logger.info(f"""
        📊 ITÉRATION {metrics.iteration}:
        ├─ Score global: {metrics.overall_score:.1f}% 
        ├─ Qualité code: {metrics.reviewer_score:.1f}%
        ├─ Sécurité: {metrics.security_score:.1f}%
        ├─ Problèmes détectés: {metrics.issues_count}
        ├─ Améliorations: {len(metrics.improvements)}
        └─ Meilleur: {self.best_score:.1f}% (itération {self.best_iteration})
        """)
    
    def _display_final_summary(self):
        """Affiche le résumé final"""
        if not self.best_solution:
            logger.error("❌ Aucune solution trouvée")
            return
        
        logger.info(f"""
        🎉 RÉSUMÉ FINAL:
        ├─ Itérations exécutées: {self.iteration_count}/{self.max_iterations}
        ├─ Meilleur score: {self.best_score:.1f}%
        ├─ Itération gagnante: {self.best_iteration}
        ├─ Agents utilisés: {len(self.agents)}
        ├─ Fichiers générés: Voir {self.output_dir}
        └─ Temps total: {self._get_total_time()}
        """)
        
        # Afficher les agents stats
        logger.info("\n🤖 STATISTIQUES AGENTS:")
        for name, agent in self.agents.items():
            logger.info(f"  {agent}: {agent.total_tokens} tokens")
    
    def _get_total_time(self) -> str:
        """Calcule le temps total d'exécution"""
        if not self.metrics_history:
            return "N/A"
        
        first_time = datetime.fromisoformat(self.metrics_history[0].timestamp)
        last_time = datetime.fromisoformat(self.metrics_history[-1].timestamp)
        duration = last_time - first_time
        
        return f"{duration.total_seconds():.0f}s"
    
    def _package_solution(self) -> dict:
        """Prépare la solution pour export"""
        if not self.best_solution:
            return {"status": "failed", "error": "Aucune solution générée"}
        
        solution = {
            "status": "success",
            "iteration": self.best_solution['iteration'],
            "score": self.best_score,
            "artifacts": {
                "architecture": self.best_solution['architecture'],
                "code": self.best_solution['code'],
                "tests": self.best_solution['tests'],
                "documentation": self.best_solution['documentation']
            },
            "metrics": [m.to_dict() for m in self.metrics_history]
        }
        
        return solution
