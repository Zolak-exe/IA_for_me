
"""
Configuration du système multi-agents
"""

# Configuration Ollama
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "timeout": 300,  # 5 minutes
    "max_retries": 3,
    "retry_delay": 2.0
}

# Modèles LLM pour chaque agent
# Adapte selon les modèles installés sur ton système
AGENT_MODELS = {
    "architect": "mistral",              # Généraliste
    "developer": "codellama",            # Spécialisé code
    "reviewer": "deepseek-coder",        # Spécialisé code
    "security": "mistral",               # Généraliste
    "tester": "qwen2.5-coder",           # Spécialisé code
    "documentation": "mistral"           # Modèle léger pour doc
}

# Alternativement, si tu as peu de modèles, utilise les mêmes partout:
# AGENT_MODELS_FALLBACK = {
#     "architect": "mistral:latest",
#     "developer": "mistral:latest",
#     "reviewer": "mistral:latest",
#     "security": "mistral:latest",
#     "tester": "mistral:latest",
#     "documentation": "mistral:latest"
# }

# Paramètres du système
SYSTEM_CONFIG = {
    "max_iterations": 15,
    "quality_threshold": 90.0,  # Seuil de sortie (%)
    "output_dir": "./outputs",
    "log_level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "enable_streaming": True,  # Afficher la génération en temps réel
}

# Paramètres de génération LLM
GENERATION_PARAMS = {
    "architect": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40
    },
    "developer": {
        "temperature": 0.5,  # Plus bas pour code déterministe
        "top_p": 0.9,
        "top_k": 40
    },
    "reviewer": {
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 40
    },
    "security": {
        "temperature": 0.3,  # Très bas pour sécurité stricte
        "top_p": 0.9,
        "top_k": 40
    },
    "tester": {
        "temperature": 0.6,
        "top_p": 0.9,
        "top_k": 40
    },
    "documentation": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40
    }
}

# Configuration pondérations pour score global
SCORE_WEIGHTS = {
    "review_quality": 0.35,      # Qualité du code
    "security": 0.25,            # Sécurité (très important!)
    "testing": 0.20,             # Tests et couverture
    "documentation": 0.20        # Documentation
}

# Critères d'arrêt
STOP_CRITERIA = {
    "quality_threshold": 90.0,           # % global à atteindre
    "stagnation_threshold": 3,           # N itérations sans amélioration
    "security_min_score": 80.0,          # Score minimum sécurité
    "review_min_score": 85.0             # Score minimum qualité
}

PROMPT_LIMITS = {
    "architecture_context": 2000,
    "code_context": 3000,
    "requirements_context": 1000
}
