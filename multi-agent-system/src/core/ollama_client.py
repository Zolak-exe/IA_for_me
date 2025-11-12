"""
Client pour communiquer avec Ollama localement.
Gère les retries, erreurs et optimisation des prompts.
"""

import requests
import json
import time
from typing import Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Configuration pour Ollama"""
    base_url: str = "http://localhost:11434"
    timeout: int = 300
    max_retries: int = 3
    retry_delay: float = 2.0


class OllamaClient:
    """Client pour interagir avec Ollama"""
    
    def __init__(self, config: OllamaConfig = None):
        self.config = config or OllamaConfig()
        self.session = requests.Session()
        self.models_cache = {}
        
    def check_connection(self) -> bool:
        """Vérifie que Ollama est disponible"""
        try:
            response = self.session.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Ollama non disponible: {e}")
            return False
    
    def get_available_models(self) -> list[str]:
        """Récupère les modèles disponibles"""
        try:
            response = self.session.get(
                f"{self.config.base_url}/api/tags",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                models = [m["name"].split(":")[0] for m in data.get("models", [])]
                self.models_cache = models
                return models
            return []
        except Exception as e:
            logger.error(f"Erreur récupération modèles: {e}")
            return self.models_cache
    
    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
    ) -> str:
        """
        Génère du texte avec le modèle spécifié.
        Avec retry automatique en cas d'erreur.
        """
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.post(
                    f"{self.config.base_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "top_p": top_p,
                        "top_k": top_k,
                        "stream": False,
                    },
                    timeout=self.config.timeout,
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.warning(f"Status {response.status_code}: {response.text}")
                    
            except requests.Timeout:
                logger.warning(f"Timeout tentative {attempt + 1}/{self.config.max_retries}")
            except requests.ConnectionError:
                logger.warning(f"Connexion échouée tentative {attempt + 1}/{self.config.max_retries}")
            except Exception as e:
                logger.error(f"Erreur génération: {e}")
            
            if attempt < self.config.max_retries - 1:
                time.sleep(self.config.retry_delay)
        
        logger.error(f"❌ Impossible de générer après {self.config.max_retries} tentatives")
        return ""
    
    def stream_generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
    ):
        """Génère du texte en streaming (pour affichage progressif)"""
        try:
            response = self.session.post(
                f"{self.config.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": True,
                },
                timeout=self.config.timeout,
                stream=True,
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    full_response += chunk
                    yield chunk
                    
        except Exception as e:
            logger.error(f"Erreur streaming: {e}")
            yield ""
    
    def pull_model(self, model_name: str) -> bool:
        """Télécharge un modèle (si disponible)"""
        try:
            logger.info(f"📥 Téléchargement du modèle {model_name}...")
            response = self.session.post(
                f"{self.config.base_url}/api/pull",
                json={"name": model_name},
                timeout=3600,  # 1 heure max
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erreur téléchargement: {e}")
            return False
    
    def health_check(self) -> dict:
        """Vérifie l'état de santé d'Ollama"""
        try:
            # Test de connexion
            if not self.check_connection():
                return {
                    "status": "error",
                    "message": "Ollama non accessible",
                    "url": self.config.base_url
                }
            
            models = self.get_available_models()
            return {
                "status": "ok",
                "models_available": len(models),
                "models": models[:5] if models else [],
                "url": self.config.base_url
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
