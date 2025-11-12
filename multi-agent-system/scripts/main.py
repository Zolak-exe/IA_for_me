#!/usr/bin/env python3
"""Système Multi-Agents Auto-Correctif - Point d'entrée optimisé"""
import logging, sys, argparse, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('system.log')])
logger = logging.getLogger(__name__)

from src.core import OllamaClient, OllamaConfig, MultiAgentOrchestrator
from src.utils.exporters import SolutionExporter, ReportGenerator
from src.config.settings import OLLAMA_CONFIG, AGENT_MODELS, SYSTEM_CONFIG


def setup_ollama_client():
    """Initialise et teste le client Ollama"""
    logger.info("🔌 Initialisation client Ollama...")
    
    config = OllamaConfig(**OLLAMA_CONFIG)
    client = OllamaClient(config)
    
    # Vérifier la connexion
    if not client.check_connection():
        logger.error("❌ Impossible de se connecter à Ollama")
        logger.error(f"   Vérifiez que Ollama est running sur {OLLAMA_CONFIG['base_url']}")
        logger.error("   Commande: ollama serve")
        return None
    
    logger.info("✅ Connexion à Ollama établie")
    
    # Afficher l'état de santé
    health = client.health_check()
    logger.info(f"   Status: {health['status']}")
    logger.info(f"   Modèles disponibles: {health.get('models_available', 0)}")
    if health.get('models'):
        logger.info(f"   Exemples: {', '.join(health['models'])}")
    
    return client


def check_models_available(client):
    """Vérifie que les modèles requis sont disponibles"""
    logger.info("🔍 Vérification des modèles requis...")
    
    available = client.get_available_models()
    
    if not available:
        logger.warning("   ⚠️  Aucun modèle trouvé")
        logger.info("   Télécharge au moins un modèle avec: ollama pull mistral")
        return False
    
    logger.info(f"   ✓ {len(available)} modèle(s) disponible(s)")
    
    # Vérifier les modèles spécifiques
    missing = []
    for agent, model in AGENT_MODELS.items():
        model_base = model.split(':')[0]
        if not any(m.startswith(model_base) for m in available):
            missing.append(f"{agent} ({model})")
    
    if missing:
        logger.warning(f"   ⚠️  Modèles manquants:")
        for m in missing:
            logger.warning(f"      - {m}")
        logger.info("   Le système utilisera les modèles disponibles")
    
    return True


def parse_arguments():
    """Parse les arguments en ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Système Multi-Agents pour génération de projet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py --requirements "API REST avec FastAPI"
  python main.py --requirements "CLI tool en Python" --max-iterations 10
  python main.py --requirements "Microservice" --threshold 85
        """
    )
    
    parser.add_argument(
        '--requirements',
        required=True,
        help='Description des requirements du projet'
    )
    
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=SYSTEM_CONFIG.get('max_iterations', 15),
        help='Nombre maximum d\'itérations (défaut: 15)'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=SYSTEM_CONFIG.get('quality_threshold', 90.0),
        help='Seuil de qualité pour arrêt (défaut: 90)'
    )
    
    parser.add_argument(
        '--output',
        default=SYSTEM_CONFIG.get('output_dir', './outputs'),
        help='Répertoire de sortie (défaut: ./outputs)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Affichage détaillé (DEBUG)'
    )
    
    return parser.parse_args()


def main():
    """Fonction principale"""
    
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("🔧 Mode DEBUG activé")
    
    logger.info("╔════════════════════════════════════════════════════════════╗")
    logger.info("║      🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖            ║")
    logger.info("╚════════════════════════════════════════════════════════════╝")
    
    # Initialiser Ollama
    ollama_client = setup_ollama_client()
    if not ollama_client:
        logger.error("❌ Impossible de démarrer sans Ollama")
        sys.exit(1)
    
    # Vérifier les modèles
    if not check_models_available(ollama_client):
        logger.warning("⚠️  Continuant sans tous les modèles...")
    
    # Créer l'orchestrateur
    logger.info("\n🏗️  Initialisation du système multi-agents...")
    orchestrator = MultiAgentOrchestrator(
        ollama_client=ollama_client,
        max_iterations=args.max_iterations,
        quality_threshold=args.threshold,
        output_dir=args.output
    )
    
    logger.info(f"   ✓ {len(orchestrator.agents)} agents initialisés")
    for name, agent in orchestrator.agents.items():
        logger.info(f"     • {agent.role} ({agent.model_name})")
    
    # Afficher les requirements
    logger.info("\n📋 REQUIREMENTS:")
    for line in args.requirements.split('\n'):
        logger.info(f"   {line}")
    
    logger.info("\n" + "="*60)
    
    # Lancer le système
    try:
        solution = orchestrator.run(args.requirements)
        
        # Exporter la solution
        logger.info("\n💾 Export de la solution...")
        exporter = SolutionExporter(args.output)
        export_result = exporter.export_all(solution, "project")
        
        logger.info(f"✅ Solution exportée dans: {export_result['output_dir']}")
        
        # Générer les rapports
        logger.info("\n📊 Génération des rapports...")
        report_text = ReportGenerator.generate_text_report(solution)
        logger.info(report_text)
        
        # Sauvegarder le rapport text
        report_file = Path(export_result['output_dir']) / "REPORT.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        logger.info(f"   ✓ Rapport: {report_file}")
        
        # Sauvegarder le rapport HTML
        html_report = ReportGenerator.generate_html_report(solution)
        html_file = Path(export_result['output_dir']) / "REPORT.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        logger.info(f"   ✓ Rapport HTML: {html_file}")
        
        logger.info("\n" + "="*60)
        logger.info("🎉 EXÉCUTION COMPLÉTÉE AVEC SUCCÈS!")
        logger.info(f"   Score final: {solution.get('score', 0):.1f}%")
        logger.info(f"   Dossier résultats: {export_result['output_dir']}")
        logger.info("="*60 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Exécution interrompue par l'utilisateur")
        return 130
    
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
