"""
Classe de base pour tous les agents.
Définit l'interface commune et les utilitaires.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentOutput:
    """Structure de sortie uniforme pour tous les agents"""
    agent_name: str
    success: bool
    content: str
    score: Optional[float] = None
    issues: list = None
    recommendations: list = None
    token_count: Optional[int] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.recommendations is None:
            self.recommendations = []
    
    def to_dict(self):
        return asdict(self)


class BaseAgent(ABC):
    """Classe de base pour tous les agents"""
    
    def __init__(self, ollama_client, model_name: str, role: str):
        self.ollama_client = ollama_client
        self.model_name = model_name
        self.role = role
        self.call_count = 0
        self.total_tokens = 0
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> AgentOutput:
        """Exécute la tâche spécifique de l'agent"""
        pass
    
    def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        instruction_prefix: str = ""
    ) -> str:
        """Appelle le LLM avec gestion d'erreur"""
        self.call_count += 1
        
        full_prompt = f"{instruction_prefix}\n\n{prompt}" if instruction_prefix else prompt
        
        logger.debug(f"🤖 [{self.role}] Appel #{self.call_count} avec {self.model_name}")
        
        response = self.ollama_client.generate(
            model=self.model_name,
            prompt=full_prompt,
            temperature=temperature
        )
        
        # Estimation tokens (approximation: ~4 chars = 1 token)
        self.total_tokens += len(full_prompt) // 4 + len(response) // 4
        
        return response
    
    def extract_score(self, content: str) -> float:
        """Extrait un score (0-100) du contenu"""
        import re
        # Cherche patterns comme "score: 85", "qualité: 92%", etc.
        patterns = [
            r"score[:\s]+(\d+)",
            r"qualité[:\s]+(\d+)",
            r"(\d+)\s*%",
            r"(\d+)/100"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(100, max(0, score))
        
        return 0.0
    
    def __str__(self) -> str:
        return f"🤖 {self.role} ({self.model_name}) - {self.call_count} appels"
