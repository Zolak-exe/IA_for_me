#!/usr/bin/env python3
"""Script d'exemple simple pour tester le système"""
import sys, logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

from src.core import OllamaClient, OllamaConfig, MultiAgentOrchestrator
from src.utils.exporters import SolutionExporter


def main():
    """Exemple d'utilisation minimal"""
    
    logger.info("🤖 Démo Système Multi-Agents")
    logger.info("="*50)
    
    # 1. Connecter à Ollama
    logger.info("\n1️⃣  Connexion à Ollama...")
    config = OllamaConfig(base_url="http://localhost:11434")
    client = OllamaClient(config)
    
    if not client.check_connection():
        logger.error("❌ Ollama non trouvé sur http://localhost:11434")
        logger.error("   Lancez: ollama serve")
        return 1
    
    logger.info("✅ Ollama connecté")
    models = client.get_available_models()
    logger.info(f"   {len(models)} modèle(s) disponible(s): {models[:3]}")
    
    # 2. Créer l'orchestrateur
    logger.info("\n2️⃣  Initialisation orchestrateur...")
    orchestrator = MultiAgentOrchestrator(
        ollama_client=client,
        max_iterations=3,  # Limiter pour démo
        quality_threshold=75.0,
        output_dir="./outputs"
    )
    logger.info(f"✅ {len(orchestrator.agents)} agents prêts")
    
    # 3. Lancer le système
    logger.info("\n3️⃣  Lancement du système...")
    requirements = """
    Créer une simple API REST avec:
    - Endpoint GET /hello
    - Endpoint POST /items
    - Documentation API
    """
    
    logger.info(f"   Requirements: {requirements.strip()}")
    logger.info("\n" + "="*50)
    
    try:
        solution = orchestrator.run(requirements)
        
        logger.info("\n4️⃣  Export de la solution...")
        exporter = SolutionExporter("./outputs")
        result = exporter.export_all(solution, "demo-project")
        
        logger.info(f"✅ Résultats dans: {result['output_dir']}")
        logger.info(f"   {len(result['files'])} fichiers générés")
        
        logger.info(f"\n🎉 Score final: {solution.get('score', 0):.1f}%")
        logger.info(f"   Itération: {solution.get('iteration', 0)}")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
