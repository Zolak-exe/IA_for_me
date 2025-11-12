"""
Configuration logging avancée pour le système multi-agents
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Formatter avec couleurs pour terminal"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Vert
        'WARNING': '\033[33m',    # Jaune
        'ERROR': '\033[31m',      # Rouge
        'CRITICAL': '\033[35m'    # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(name: str = "multi-agent", level=logging.INFO, verbose: bool = False):
    """Configure le logging complet du système"""
    
    if verbose:
        level = logging.DEBUG
    
    # Logger principal
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Éviter les doublons
    if logger.handlers:
        return logger
    
    # Format
    log_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Console handler (avec couleurs)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    colored_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)
    
    # File handler (sans couleurs)
    log_file = Path("system.log")
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Toujours DEBUG en fichier
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Impossible d'ouvrir fichier log: {e}")
    
    return logger


def get_logger(name: str):
    """Récupère un logger configuré"""
    return logging.getLogger(f"multi-agent.{name}")


if __name__ == "__main__":
    # Test
    logger = setup_logging(verbose=True)
    
    logger.debug("Message DEBUG")
    logger.info("Message INFO")
    logger.warning("Message WARNING")
    logger.error("Message ERROR")
    
    print(f"\n✓ Logs sauvegardés dans system.log")
