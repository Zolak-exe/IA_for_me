#!/usr/bin/env python3
"""Script de validation simple - Vérifie que tout fonctionne"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Teste les imports"""
    print("🔍 Test 1: Imports Python...")
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError:
        print("  ✗ requests (pip install -r requirements.txt)")
        return False
    
    try:
        from src.core import OllamaClient
        print("  ✓ core.OllamaClient")
    except ImportError as e:
        print(f"  ✗ core.OllamaClient ({e})")
        return False
    
    try:
        from src.agents import ArchitectAgent
        print("  ✓ agents.ArchitectAgent")
    except ImportError as e:
        print(f"  ✗ agents.ArchitectAgent ({e})")
        return False
    
    print("  ✅ Tous les imports OK\n")
    return True


def test_structure():
    """Teste la structure des fichiers"""
    print("🔍 Test 2: Structure fichiers...")
    
    required_files = [
        "scripts/main.py",
        "scripts/demo.py",
        "scripts/test_ollama.py",
        "requirements.txt",
        "docs/README.md",
        "src/config/settings.py",
        "src/agents/base_agent.py",
        "src/agents/specialized_agents.py",
        "src/core/ollama_client.py",
        "src/core/orchestrator.py",
        "src/utils/exporters.py",
    ]
    
    missing = []
    for file in required_files:
        path = Path(file)
        if not path.exists():
            missing.append(file)
            print(f"  ✗ {file}")
        else:
            print(f"  ✓ {file}")
    
    if missing:
        print(f"\n  ❌ {len(missing)} fichier(s) manquant(s)")
        return False
    
    print("  ✅ Tous les fichiers présents\n")
    return True


def test_config():
    """Teste la configuration"""
    print("🔍 Test 3: Configuration...")
    
    try:
        from src.config.settings import OLLAMA_CONFIG, AGENT_MODELS, SYSTEM_CONFIG
        
        assert OLLAMA_CONFIG, "OLLAMA_CONFIG vide"
        print(f"  ✓ OLLAMA_CONFIG: {OLLAMA_CONFIG.get('base_url')}")
        
        assert len(AGENT_MODELS) >= 6, f"Seulement {len(AGENT_MODELS)} agents"
        print(f"  ✓ AGENT_MODELS: {len(AGENT_MODELS)} agents")
        
        assert SYSTEM_CONFIG, "SYSTEM_CONFIG vide"
        print(f"  ✓ SYSTEM_CONFIG: {SYSTEM_CONFIG.get('max_iterations')} itérations max")
        
        print("  ✅ Configuration OK\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur config: {e}\n")
        return False


def test_agents():
    """Teste que les agents sont importables"""
    print("🔍 Test 4: Agents...")
    
    try:
        from src.agents import (
            ArchitectAgent,
            DeveloperAgent,
            ReviewerAgent,
            SecurityAgent,
            TesterAgent,
            DocumentationAgent
        )
        
        agents = [
            ("Architect", ArchitectAgent),
            ("Developer", DeveloperAgent),
            ("Reviewer", ReviewerAgent),
            ("Security", SecurityAgent),
            ("Tester", TesterAgent),
            ("Documentation", DocumentationAgent),
        ]
        
        for name, agent_class in agents:
            print(f"  ✓ {name}Agent")
        
        print("  ✅ Tous les agents importables\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur agents: {e}\n")
        return False


def test_export():
    """Teste que les exporters sont importables"""
    print("🔍 Test 5: Exporters...")
    
    try:
        from src.utils.exporters import SolutionExporter, ReportGenerator, Dashboard
        
        print(f"  ✓ SolutionExporter")
        print(f"  ✓ ReportGenerator")
        print(f"  ✓ Dashboard")
        
        print("  ✅ Exporters OK\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur exporters: {e}\n")
        return False


def main():
    """Exécute tous les tests"""
    
    print("\n" + "="*50)
    print("🧪 VALIDATION INSTALLATION")
    print("="*50 + "\n")
    
    results = [
        ("Imports", test_imports()),
        ("Structure", test_structure()),
        ("Configuration", test_config()),
        ("Agents", test_agents()),
        ("Exporters", test_export()),
    ]
    
    print("="*50)
    print("📊 RÉSUMÉ")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nScore: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS PASSÉS!")
        print("\n✅ L'installation est correcte.")
        print("✅ Vous pouvez lancer: python main.py --requirements \"...\"\n")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) échoué(s)")
        print("\nVérifiez:")
        print("  1. pip install -r requirements.txt")
        print("  2. Tous les fichiers présents")
        print("  3. Répertoires agents/, core/, utils/\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
