"""Configuration module"""
from .settings import (
    OLLAMA_CONFIG,
    AGENT_MODELS,
    SYSTEM_CONFIG,
    GENERATION_PARAMS,
    SCORE_WEIGHTS,
    STOP_CRITERIA
)

__all__ = [
    'OLLAMA_CONFIG',
    'AGENT_MODELS',
    'SYSTEM_CONFIG',
    'GENERATION_PARAMS',
    'SCORE_WEIGHTS',
    'STOP_CRITERIA'
]
