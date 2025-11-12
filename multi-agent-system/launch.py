#!/usr/bin/env python3
"""
🚀 LANCEUR PRINCIPAL - Système Multi-Agents Auto-Correctif

Interface utilisateur complète pour lancer le système avec des paramètres personnalisés.
"""

import sys
import logging
import argparse
import tempfile
import subprocess
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core import OllamaClient, OllamaConfig, MultiAgentOrchestrator
from src.utils.exporters import SolutionExporter, ReportGenerator
from src.config.settings import OLLAMA_CONFIG, SYSTEM_CONFIG

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('system.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class ProjectLauncher:
    """Interface de lancement du projet"""

    def __init__(self):
        self.client = None
        self.project_name = ""
        self.requirements = ""
        self.max_iterations = 15
        self.quality_threshold = 90.0
        self.output_dir = "./outputs"
        
    def display_banner(self):
        """Affiche le banneau principal"""
        print("\n" + "="*70)
        print("╔" + "="*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  🤖 SYSTÈME MULTI-AGENTS AUTO-CORRECTIF 🤖".center(68) + "║")
        print("║" + "  Génération de projets IA autonome avec 6 agents spécialisés".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "="*68 + "╝")
        print("="*70 + "\n")

    def check_ollama(self) -> bool:
        """Vérifie la connexion à Ollama"""
        logger.info("🔌 Vérification de la connexion à Ollama...")
        try:
            config = OllamaConfig(**OLLAMA_CONFIG)
            self.client = OllamaClient(config)
            
            if not self.client.check_connection():
                logger.error("❌ Impossible de se connecter à Ollama")
                logger.error(f"   URL: {OLLAMA_CONFIG['base_url']}")
                logger.error("   Solution: Lancez 'ollama serve' dans un autre terminal")
                return False
            
            logger.info("✅ Ollama connecté avec succès")
            
            # Afficher les modèles disponibles
            models = self.client.get_available_models()
            logger.info(f"📦 {len(models)} modèle(s) disponible(s):")
            for i, model in enumerate(models[:5], 1):
                print(f"   {i}. {model}")
            if len(models) > 5:
                print(f"   ... et {len(models) - 5} autre(s)")
            
            return True
        except Exception as e:
            logger.error(f"❌ Erreur connexion Ollama: {e}")
            return False

    def get_project_name(self) -> str:
        """Demande le nom du projet"""
        print("\n" + "="*70)
        print("📝 ÉTAPE 1: NOM DU PROJET")
        print("="*70)
        
        while True:
            name = input("\n👉 Nom du projet (sans espaces, ex: my-api, web-scraper): ").strip()
            
            if not name:
                print("❌ Le nom ne peut pas être vide")
                continue
            
            if any(c in name for c in [' ', '/', '\\', ':']):
                print("❌ Le nom ne peut pas contenir: espaces, /, \\, :")
                continue
            
            logger.info(f"✅ Projet: {name}")
            return name

    def get_requirements(self) -> str:
        """Demande les requirements du projet.

        Améliorations UX :
        - Permet d'ouvrir l'éditeur système (Notepad) pour saisir un long prompt.
        - Permet de charger depuis un fichier.
        - Permet de saisir une entrée simple sur une ligne.
        - Termine la saisie multiligne par une ligne contenant uniquement ".END"
        """
        print("\n" + "="*70)
        print("📋 ÉTAPE 2: DESCRIPTION DU PROJET")
        print("="*70)

        print("\nOptions de saisie:")
        print("  [e] Ouvrir l'éditeur (Notepad) pour saisir un prompt long")
        print("  [f] Charger depuis un fichier (chemin)")
        print("  [s] Saisie simple (une seule ligne)")
        print("  [p] Coller multiligne et terminer par une ligne contenant uniquement '.END'")

        choice = input('\nChoix (e/f/s/p) [e]: ').strip().lower() or 'e'

        if choice == 'f':
            path = input('Chemin vers le fichier: ').strip()
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    requirements = fh.read().strip()
            except Exception as e:
                print(f"❌ Impossible de lire le fichier: {e}")
                return self.get_requirements()

        elif choice == 's':
            requirements = input('\nEntrez la description (une ligne): ').strip()
            if not requirements:
                print('❌ La description ne peut pas être vide')
                return self.get_requirements()

        elif choice == 'p':
            print("\n📝 Collez votre texte. Terminez la saisie par une ligne contenant uniquement '.END' and press Enter:")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line.strip() == '.END':
                    break
                lines.append(line)
            requirements = '\n'.join(lines).strip()
            if not requirements:
                print('❌ La description ne peut pas être vide')
                return self.get_requirements()

        else:
            # Open system editor (Notepad on Windows)
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w+', encoding='utf-8') as tf:
                    tf.write('# Tapez votre description ci-dessous. Enregistrez et fermez Notepad pour continuer.\n')
                    tf.flush()
                    tmp_path = tf.name

                # Open notepad (Windows). On non-Windows, try $EDITOR
                if os.name == 'nt':
                    subprocess.run(['notepad.exe', tmp_path])
                else:
                    editor = os.environ.get('EDITOR', 'vi')
                    subprocess.run([editor, tmp_path])

                with open(tmp_path, 'r', encoding='utf-8') as fh:
                    contents = fh.read()
                # Remove comment lines we inserted
                requirements = '\n'.join([l for l in contents.splitlines() if not l.startswith('#')]).strip()
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

                if not requirements:
                    print('❌ Aucun contenu détecté dans l\'éditeur')
                    return self.get_requirements()

            except Exception as e:
                print(f"❌ Erreur éditeur: {e}")
                return self.get_requirements()

        # Afficher un résumé
        preview = requirements[:200] + '...' if len(requirements) > 200 else requirements
        logger.info(f"✅ Description reçue ({len(requirements)} caractères)")
        print(f"   Aperçu: {preview}")
        return requirements

    def get_parameters(self):
        """Demande les paramètres avancés"""
        print("\n" + "="*70)
        print("⚙️  ÉTAPE 3: PARAMÈTRES AVANCÉS")
        print("="*70)
        
        print("\n🔧 Options disponibles:")
        print("   • Max itérations: nombre maximal d'améliorations (1-20, défaut: 15)")
        print("   • Seuil qualité: score cible pour arrêt (50-100, défaut: 90)")
        print("   • Dossier résultats: où sauvegarder les fichiers (défaut: ./outputs)")
        
        # Max itérations
        print("\n👉 Max itérations [1-20, défaut 15]:")
        while True:
            try:
                val = input("   > ").strip()
                if not val:
                    self.max_iterations = 15
                    break
                val = int(val)
                if 1 <= val <= 20:
                    self.max_iterations = val
                    break
                print("   ❌ Entrez un nombre entre 1 et 20")
            except ValueError:
                print("   ❌ Entrez un nombre valide")
        
        logger.info(f"✅ Max itérations: {self.max_iterations}")
        
        # Seuil qualité
        print("\n👉 Seuil qualité [50-100, défaut 90]:")
        while True:
            try:
                val = input("   > ").strip()
                if not val:
                    self.quality_threshold = 90.0
                    break
                val = float(val)
                if 50 <= val <= 100:
                    self.quality_threshold = val
                    break
                print("   ❌ Entrez un nombre entre 50 et 100")
            except ValueError:
                print("   ❌ Entrez un nombre valide")
        
        logger.info(f"✅ Seuil qualité: {self.quality_threshold}%")
        
        # Dossier résultats
        print("\n👉 Dossier résultats [défaut ./outputs]:")
        val = input("   > ").strip()
        if val:
            self.output_dir = val
        
        logger.info(f"✅ Dossier résultats: {self.output_dir}")

    def get_confirmation(self) -> bool:
        """Demande une confirmation avant de lancer"""
        print("\n" + "="*70)
        print("✅ RÉSUMÉ DE LA CONFIGURATION")
        print("="*70)
        
        print(f"""
Projet:            {self.project_name}
Requirements:      {self.requirements[:50]}...
Max itérations:    {self.max_iterations}
Seuil qualité:     {self.quality_threshold}%
Dossier résultats: {self.output_dir}
        """)
        
        print("\n❓ Lancer le système? [o/N]:")
        response = input("  > ").strip().lower()
        
        return response in ['o', 'oui', 'y', 'yes']

    def run_system(self):
        """Lance le système multi-agents"""
        print("\n" + "="*70)
        print("🚀 LANCEMENT DU SYSTÈME")
        print("="*70 + "\n")
        
        try:
            # Créer l'orchestrateur
            orchestrator = MultiAgentOrchestrator(
                ollama_client=self.client,
                max_iterations=self.max_iterations,
                quality_threshold=self.quality_threshold,
                output_dir=self.output_dir
            )
            
            logger.info(f"🏗️  Orchestrateur initialisé")
            logger.info(f"✅ {len(orchestrator.agents)} agents prêts")
            
            # Lancer le système
            logger.info("\n" + "="*70)
            logger.info("🔄 EXÉCUTION MULTI-AGENTS")
            logger.info("="*70)
            
            solution = orchestrator.run(self.requirements)
            
            # Exporter la solution
            logger.info("\n📤 Export de la solution...")
            exporter = SolutionExporter(self.output_dir)
            result = exporter.export_all(solution, self.project_name)
            
            # Afficher le résumé final
            self.display_final_summary(solution, result)
            
            return True
            
        except KeyboardInterrupt:
            logger.warning("\n⚠️  Arrêt par utilisateur")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur: {e}", exc_info=True)
            return False

    def display_final_summary(self, solution: dict, export_result: dict):
        """Affiche le résumé final"""
        print("\n" + "="*70)
        print("🎉 EXÉCUTION TERMINÉE")
        print("="*70)
        
        score = solution.get('score', 0)
        iteration = solution.get('iteration', 0)
        
        print(f"""
✅ Score final:        {score:.1f}%
✅ Itération gagnante: {iteration}
✅ Fichiers générés:   {len(export_result.get('files', []))}
✅ Dossier résultats:  {export_result.get('output_dir', self.output_dir)}

📋 Fichiers créés:
        """)
        
        for file_path in export_result.get('files', [])[:5]:
            file_name = Path(file_path).name
            print(f"   ✓ {file_name}")
        
        if len(export_result.get('files', [])) > 5:
            print(f"   ... et {len(export_result.get('files', [])) - 5} autre(s)")
        
        print("\n📊 Résultats disponibles:")
        print("   • solution.json  - Données complètes en JSON")
        print("   • solution.html  - Rapport HTML formaté")
        print("   • solution.md    - Documentation Markdown")
        print("   • solution.txt   - Rapport texte simple")
        print("\n" + "="*70)

    def main(self):
        """Point d'entrée principal"""
        try:
            self.display_banner()
            
            # Étape 1: Vérifier Ollama
            if not self.check_ollama():
                print("❌ Impossible de continuer sans Ollama")
                return 1
            
            # Étape 2: Récupérer les paramètres
            self.project_name = self.get_project_name()
            self.requirements = self.get_requirements()
            self.get_parameters()
            
            # Étape 3: Confirmation
            if not self.get_confirmation():
                logger.info("⚠️  Lancement annulé par l'utilisateur")
                return 0
            
            # Étape 4: Exécuter
            if self.run_system():
                logger.info("\n✅ Système exécuté avec succès!")
                return 0
            else:
                logger.error("\n❌ Erreur lors de l'exécution")
                return 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Programme interrompu par l'utilisateur")
            return 0
        except Exception as e:
            logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
            return 1


def main():
    """Point d'entrée du script"""
    launcher = ProjectLauncher()
    return launcher.main()


if __name__ == "__main__":
    sys.exit(main())
