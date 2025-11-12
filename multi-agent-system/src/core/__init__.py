"""
__init__ pour le package core
"""

from .ollama_client import OllamaClient, OllamaConfig
from .orchestrator import MultiAgentOrchestrator, IterationMetrics

__all__ = [
    "OllamaClient",
    "OllamaConfig",
    "MultiAgentOrchestrator",
    "IterationMetrics"
]
