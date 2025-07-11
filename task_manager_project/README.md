# 🚀 Gestionnaire de Tâches – Projet TESSTS

[![Tests](https://github.com/your-username/task-manager/actions/workflows/test.yml/badge.svg)](https://github.com/your-username/task-manager/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/your-username/task-manager)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📋 Description

Projet de gestionnaire de tâches complet développé dans le cadre du module **TESSTS** (Tests et Qualité Logicielle). 

Le système offre une gestion complète des tâches avec :
- **Tâches avec UUID unique**, statuts, priorités et timestamps
- **Opérations CRUD complètes** avec stockage persistant JSON
- **Filtres avancés** par statut, priorité, projet, assigné
- **Statistiques détaillées** et rapports
- **Services simulés** (Email, Export CSV) avec gestion d'erreurs
- **Couverture de tests 98%** avec 40+ tests unitaires et d'intégration
- **CI/CD** avec GitHub Actions

## 🏗️ Architecture

```
task_manager_project/
├── .github/workflows/
│   └── test.yml                    # CI/CD GitHub Actions
├── src/task_manager/
│   ├── __init__.py                 # Package initialization
│   ├── task.py                     # Classe Task + Enums
│   ├── manager.py                  # TaskManager (CRUD + stats)
│   └── services.py                 # EmailService + ReportService
├── tests/
│   ├── fixtures/
│   │   ├── tasks.json             # Données de test complètes
│   │   ├── temp_tasks.json        # Données temporaires
│   │   └── exemple_taches.json    # Données d'exemple
│   ├── test_task.py               # Tests classe Task
│   ├── test_manager.py            # Tests TaskManager
│   └── test_services.py           # Tests services
├── demo.py                         # Script de démonstration
├── example_usage.py                # Exemples d'utilisation
├── requirements.txt                # Dépendances Python
├── Makefile                       # Automatisation
├── pytest.ini                     # Configuration pytest
└── README.md                      # Documentation
```

## 🚀 Installation

```bash
# Cloner le projet
git clone https://github.com/your-username/task-manager.git
cd task-manager

# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
python -m pytest

# Voir la couverture
python -m pytest --cov=src/task_manager --cov-report=html
```

## 🧪 Tests

### Couverture actuelle : **98%** ✅

- **Task** : 100% (129 lignes)
- **TaskManager** : 95% (288 lignes) 
- **Services** : 100% (70 lignes)
- **Total** : 98% (487 lignes)

### Commandes de test

```bash
# Tous les tests
python -m pytest

# Tests avec couverture
python -m pytest --cov=src/task_manager --cov-report=html

# Tests unitaires uniquement
python -m pytest -m unit

# Tests d'intégration
python -m pytest -m integration

# Avec Makefile (Unix)
make test
make coverage
make all
```

## 📊 Fonctionnalités par Sprint

### ✅ Sprint 1 - Initialisation
- Structure du projet et architecture
- Classe `Task` avec UUID unique et timestamps
- Énumérations `Priority` (LOW, MEDIUM, HIGH, URGENT) et `Status` (TODO, IN_PROGRESS, COMPLETED, CANCELLED)
- Méthodes de base (`mark_completed`, `update_priority`, `to_dict`, `from_dict`)

### ✅ Sprint 2 - Gestionnaire de Tâches
- Classe `TaskManager` avec stockage JSON persistant
- Méthodes CRUD complètes (`add_task`, `get_task`, `update_task`, `delete_task`)
- Filtrage avancé par statut, priorité, projet, assigné
- Statistiques détaillées (`get_statistics`, `get_tasks_by_status`, etc.)
- Gestion d'erreurs robuste avec validation des données

### ✅ Sprint 3 - Services Externes
- `EmailService` avec simulation d'envoi d'emails
- `ReportService` avec export CSV des tâches
- Validation des adresses email
- Gestion d'erreurs d'écriture et de réseau
- Tests complets avec mocks pour les dépendances externes

### ✅ Sprint 4 - Couverture Maximale
- **98% de couverture de code** avec 40+ tests
- Tests de tous les cas d'erreur et exceptions
- Mocks pour les dépendances externes (fichiers, réseau)
- Tests de limites et cas extrêmes
- Configuration pytest complète

### ✅ Sprint 5 - Automatisation CI/CD
- Configuration GitHub Actions CI/CD
- Tests automatiques sur Python 3.8, 3.9, 3.10, 3.11
- Makefile pour automatisation des tâches
- Badges de qualité et couverture
- Intégration continue sur push et pull request

### ✅ Sprint 6 - Démonstration
- Script `demo.py` avec démonstration complète
- Affichage avec emojis et couleurs
- Tests des services (email, rapport)
- Gestion des erreurs en temps réel
- Exemples d'utilisation avancée

## 🎯 Utilisation

```python
from src.task_manager import Task, Priority, Status, TaskManager

# Créer un gestionnaire de tâches
manager = TaskManager("mes_taches.json")

# Créer une nouvelle tâche
task = Task(
    title="Implémenter l'authentification",
    description="Système JWT avec OAuth2 et refresh tokens",
    priority=Priority.HIGH,
    assignee="Alice",
    project="Backend"
)

# Ajouter la tâche
task_id = manager.add_task(task)

# Mettre à jour la tâche
manager.update_task(task_id, status=Status.IN_PROGRESS)

# Filtrer les tâches
urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
alice_tasks = manager.get_tasks_by_assignee("Alice")
backend_tasks = manager.get_tasks_by_project("Backend")

# Obtenir les statistiques
stats = manager.get_statistics()
print(f"Tâches complétées: {stats['completed']}")
print(f"Tâches en cours: {stats['in_progress']}")
```

## 🔧 Développement

### Prérequis
- Python 3.8+
- pip

### Installation locale
```bash
# Installer les dépendances
make install

# Lancer tous les tests
make test

# Voir la couverture
make coverage

# Nettoyer les fichiers temporaires
make clean

# Tout en une fois (install, test, coverage)
make all
```

## 📈 CI/CD

Le projet utilise GitHub Actions pour l'intégration continue :

- ✅ Tests sur Python 3.8, 3.9, 3.10, 3.11
- ✅ Installation automatique des dépendances
- ✅ Exécution des tests et calcul de couverture
- ✅ Validation sur push et pull request
- ✅ Badges de statut en temps réel

### Workflow GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest --cov=src/task_manager
```

## 🤝 Contribution

1. **Fork** le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** les changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

### Guidelines de contribution
- Suivre les conventions PEP 8
- Ajouter des tests pour les nouvelles fonctionnalités
- Maintenir la couverture de code au-dessus de 95%
- Documenter les nouvelles APIs

## 📄 License

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Développé par Zakaria ANOUAR dans le cadre du module Méthodologies de Tests & Tests Unitaires - Tests et Qualité Logicielle.

---

*Ce projet démontre les bonnes pratiques de développement avec tests, couverture maximale et intégration continue.*

