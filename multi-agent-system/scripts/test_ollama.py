#!/usr/bin/env python3
"""Script pour tester la connexion à Ollama et vérifier les modèles"""
import sys, logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

from src.core import OllamaClient, OllamaConfig


def test_ollama_connection():
    """Test la connexion à Ollama"""
    
    logger.info("🔍 TEST CONNEXION OLLAMA")
    logger.info("=" * 50)
    
    config = OllamaConfig(base_url="http://localhost:11434")
    client = OllamaClient(config)
    
    logger.info("\n1️⃣  Test de connexion...")
    if not client.check_connection():
        logger.error("❌ ÉCHOUÉ: Ollama ne répond pas")
        logger.error("   URL: http://localhost:11434")
        logger.error("   Solution: Lancez 'ollama serve'")
        return False
    
    logger.info("✅ SUCCÈS: Ollama en ligne")
    
    # 2. Modèles disponibles
    logger.info("\n2️⃣  Modèles disponibles...")
    models = client.get_available_models()
    
    if not models:
        logger.warning("⚠️  AUCUN MODÈLE TROUVÉ")
        logger.info("   Téléchargez un modèle:")
        logger.info("   $ ollama pull mistral:latest")
        return False
    
    logger.info(f"✅ SUCCÈS: {len(models)} modèle(s)")
    for i, model in enumerate(models, 1):
        logger.info(f"   {i}. {model}")
    
    # 3. Test de génération
    logger.info("\n3️⃣  Test de génération...")
    
    if not models:
        logger.warning("⚠️  Pas de modèle pour tester")
        return True
    
    model = models[0]
    logger.info(f"   Test avec: {model}")
    
    response = client.generate(
        model=model,
        prompt="Réponds simplement: Ollama fonctionne!",
        temperature=0.5
    )
    
    if response:
        logger.info("✅ SUCCÈS: Génération OK")
        logger.info(f"   Réponse: {response[:100]}...")
    else:
        logger.error("❌ ÉCHOUÉ: Aucune réponse")
        return False
    
    # Résumé
    logger.info("\n" + "=" * 50)
    logger.info("✅ TOUT EST OK - Prêt à lancer le système!")
    logger.info("=" * 50)
    logger.info("\nProchaine étape:")
    logger.info("$ python main.py --requirements \"Votre projet\"")
    
    return True


if __name__ == "__main__":
    try:
        success = test_ollama_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        sys.exit(1)
