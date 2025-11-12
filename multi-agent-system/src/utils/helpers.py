"""
Utilitaires généraux
"""

import time
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    **kwargs
) -> Any:
    """Retry une fonction avec backoff exponentiel"""
    
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func(**kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            logger.warning(f"Tentative {attempt + 1} échouée: {e}. Retry dans {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor
    
    return None


def format_tokens(token_count: int) -> str:
    """Formate un nombre de tokens lisiblement"""
    if token_count < 1000:
        return f"{token_count}"
    elif token_count < 1_000_000:
        return f"{token_count/1000:.1f}K"
    else:
        return f"{token_count/1_000_000:.1f}M"


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """Tronque le texte à une longueur max"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
