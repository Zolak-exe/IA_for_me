#!/usr/bin/env python3
"""Démo interactive avec plusieurs projets pré-définis"""
import sys, logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

from src.core import OllamaClient, OllamaConfig, MultiAgentOrchestrator
from src.utils.exporters import SolutionExporter, ReportGenerator


# Projets pré-définis pour tester
DEMO_PROJECTS = {
    "1": {
        "name": "API REST Simple",
        "description": """
API REST avec:
- Endpoint GET /items
- Endpoint POST /items/{id}
- Validation données
- Documentation OpenAPI
"""
    },
    "2": {
        "name": "CLI Task Manager",
        "description": """
Application CLI pour gérer des tâches avec:
- Commande add, list, delete, complete
- Stockage en fichier JSON
- Formatage terminal coloré
- Configuration fichier
"""
    },
    "3": {
        "name": "WebScraper",
        "description": """
Web scraper robuste avec:
- Scraping multiples pages
- Stockage en base données
- Logging détaillé
- Gestion d'erreurs
- Tests unitaires
"""
    },
    "4": {
        "name": "Data Processing Pipeline",
        "description": """
Pipeline traitement données avec:
- Lecture CSV
- Transformation données
- Aggregation et statistiques
- Export résultats
- Documentation API
"""
    },
    "5": {
        "name": "Chat Bot Simple",
        "description": """
Chat bot avec:
- Interface utilisateur
- Historique conversations
- Logging interactions
- Gestion d'erreurs
- Configuration flexible
"""
    },
    "0": {
        "name": "Custom",
        "description": "Saisissez votre propre description"
    }
}


def display_menu():
    """Affiche le menu de sélection"""
    print("\n" + "="*60)
    print("🤖 SYSTÈME MULTI-AGENTS - DÉMO INTERACTIVE")
    print("="*60)
    print("\n📋 Projets pré-définis:\n")
    
    for key, project in DEMO_PROJECTS.items():
        if key != "0":
            print(f"  [{key}] {project['name']}")
    
    print(f"\n  [0] {DEMO_PROJECTS['0']['name']}")
    print("\n" + "="*60)


def get_project_selection():
    """Récupère la sélection utilisateur"""
    while True:
        display_menu()
        choice = input("\n👉 Choisissez un projet (0-5): ").strip()
        
        if choice in DEMO_PROJECTS:
            return choice
        
        print("❌ Choix invalide")


def get_project_requirements(choice):
    """Récupère les requirements du projet sélectionné"""
    if choice == "0":
        description = input("\n📝 Décrivez votre projet: ").strip()
        if not description:
            description = "Créer une application simple et utile"
        return description
    
    project = DEMO_PROJECTS[choice]
    return project['description']


def get_execution_options():
    """Récupère les options d'exécution"""
    print("\n⚙️  OPTIONS D'EXÉCUTION")
    print("-"*40)
    
    while True:
        try:
            iterations = input("Max itérations [1-15, défaut 5]: ").strip()
            if not iterations:
                iterations = 5
            else:
                iterations = int(iterations)
                if not 1 <= iterations <= 15:
                    print("❌ Entre 1 et 15")
                    continue
            break
        except ValueError:
            print("❌ Nombre invalide")
    
    while True:
        try:
            threshold = input("Seuil qualité [50-100, défaut 85]: ").strip()
            if not threshold:
                threshold = 85.0
            else:
                threshold = float(threshold)
                if not 50 <= threshold <= 100:
                    print("❌ Entre 50 et 100")
                    continue
            break
        except ValueError:
            print("❌ Nombre invalide")
    
    verbose = input("\nMode verbeux/DEBUG? [y/N]: ").strip().lower() == 'y'
    
    return {
        "max_iterations": iterations,
        "quality_threshold": threshold,
        "verbose": verbose
    }


def main():
    """Fonction principale"""
    
    print("\n" + "╔"+"═"*58+"╗")
    print("║" + " 🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖 ".center(58) + "║")
    print("╚"+"═"*58+"╝\n")
    
    # Étape 1: Connexion Ollama
    logger.info("🔌 Vérification Ollama...")
    config = OllamaConfig(base_url="http://localhost:11434")
    client = OllamaClient(config)
    
    if not client.check_connection():
        logger.error("❌ Ollama non disponible")
        logger.error("   Lancez: ollama serve")
        return 1
    
    logger.info("✅ Ollama connecté")
    
    # Étape 2: Sélectionner projet
    choice = get_project_selection()
    project_name = DEMO_PROJECTS[choice]['name']
    requirements = get_project_requirements(choice)
    
    logger.info(f"\n✅ Projet sélectionné: {project_name}")
    logger.info(f"   {requirements[:100]}...")
    
    # Étape 3: Options d'exécution
    options = get_execution_options()
    
    if options['verbose']:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Étape 4: Initialiser le système
    logger.info("\n🏗️  Initialisation orchestrateur...")
    orchestrator = MultiAgentOrchestrator(
        ollama_client=client,
        max_iterations=options['max_iterations'],
        quality_threshold=options['quality_threshold'],
        output_dir="./outputs"
    )
    logger.info(f"✅ {len(orchestrator.agents)} agents initialisés")
    
    # Étape 5: Exécuter
    print("\n" + "="*60)
    print("🚀 LANCEMENT DU SYSTÈME")
    print("="*60)
    
    try:
        solution = orchestrator.run(requirements)
        
        # Export
        logger.info("\n💾 Export de la solution...")
        exporter = SolutionExporter("./outputs")
        result = exporter.export_all(solution, f"demo-{choice}")
        
        logger.info(f"✅ Résultats: {result['output_dir']}")
        
        # Rapport
        report = ReportGenerator.generate_text_report(solution)
        print("\n" + report)
        
        logger.info(f"\n🎉 Score final: {solution.get('score', 0):.1f}%")
        
        # Ouvrir résultats?
        import webbrowser
        import time
        
        html_file = Path(result['output_dir']) / "REPORT.html"
        if html_file.exists():
            open_html = input("\n🌐 Ouvrir rapport HTML? [Y/n]: ").strip().lower() != 'n'
            if open_html:
                logger.info(f"   Ouverture {html_file}...")
                webbrowser.open(f"file://{html_file.absolute()}")
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Arrêt par utilisateur")
        return 130
    
    except Exception as e:
        logger.error(f"❌ Erreur: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
