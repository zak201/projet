# 🚀 Gestionnaire de Tâches - Projet TESSTS

[![Tests](https://github.com/your-username/task-manager/actions/workflows/test.yml/badge.svg)](https://github.com/your-username/task-manager/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/your-username/task-manager)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📋 Description

Projet de gestionnaire de tâches complet avec stockage persistant, services externes simulés et couverture de tests maximale. Développé dans le cadre du cours TESSTS (Tests et Qualité Logicielle).

## 🏗️ Architecture

```
projet/
├── .github/workflows/test.yml    # CI/CD GitHub Actions
├── pytest.ini                   # Configuration pytest
├── requirements.txt              # Dépendances Python
├── Makefile                     # Automatisation
├── task_manager_project/         # Code source
│   ├── src/task_manager/
│   │   ├── __init__.py
│   │   ├── task.py             # Classe Task
│   │   ├── manager.py          # TaskManager
│   │   └── services.py         # EmailService & ReportService
│   ├── tests/
│   │   └── test_services.py    # Tests des services
│   ├── test_task.py            # Tests Task
│   ├── test_manager.py         # Tests TaskManager
│   └── example_usage.py        # Exemple d'utilisation
└── README.md                   # Documentation
```

## 🚀 Installation

```bash
# Cloner le projet
git clone https://github.com/your-username/task-manager.git
cd task-manager

# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
pytest

# Voir la couverture
pytest --cov=task_manager_project/src/task_manager --cov-report=html
```

## 🧪 Tests

### Couverture actuelle : **98%** ✅

- **Task** : 100% (49 lignes)
- **TaskManager** : 95% (110 lignes)
- **Services** : 100% (44 lignes)
- **Total** : 98% (207 lignes)

### Commandes de test

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=task_manager_project/src/task_manager --cov-report=html

# Tests unitaires uniquement
pytest -m unit

# Tests d'intégration
pytest -m integration
```

## 📊 Fonctionnalités

### ✅ Sprint 1 - Initialisation
- Structure du projet
- Classe `Task` avec UUID et timestamps
- Énumérations `Priority` et `Status`
- Méthodes de base (`mark_completed`, `update_priority`, etc.)

### ✅ Sprint 2 - Gestionnaire
- Classe `TaskManager` avec stockage JSON
- Méthodes CRUD complètes
- Filtrage par statut, priorité, projet, assigné
- Statistiques détaillées
- Gestion d'erreurs robuste

### ✅ Sprint 3 - Services externes
- `EmailService` avec simulation d'envoi
- `ReportService` avec export CSV
- Validation des emails
- Gestion d'erreurs d'écriture

### ✅ Sprint 4 - Couverture maximale
- **98% de couverture de code**
- Tests de tous les cas d'erreur
- Mocks pour les dépendances externes
- Tests de limites et cas extrêmes

### ✅ Sprint 5 - Automatisation
- Configuration pytest complète
- GitHub Actions CI/CD
- Makefile pour automatisation
- Badges de qualité

## 🎯 Utilisation

```python
from task_manager_project.src.task_manager import Task, Priority, Status, TaskManager

# Créer un gestionnaire
manager = TaskManager("mes_taches.json")

# Ajouter une tâche
task = Task(
    title="Implémenter l'authentification",
    description="Système JWT avec OAuth2",
    priority=Priority.HIGH,
    assignee="Alice",
    project="Backend"
)
task_id = manager.add_task(task)

# Filtrer les tâches
urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
alice_tasks = manager.get_tasks_by_assignee("Alice")

# Obtenir les statistiques
stats = manager.get_statistics()
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

# Nettoyer
make clean

# Tout en une fois
make all
```

## 📈 CI/CD

Le projet utilise GitHub Actions pour l'intégration continue :

- ✅ Tests sur Python 3.8, 3.9, 3.10, 3.11
- ✅ Installation automatique des dépendances
- ✅ Exécution des tests et couverture
- ✅ Validation sur push et pull request

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Développé dans le cadre du cours TESSTS - Tests et Qualité Logicielle.

---

⭐ **Star ce projet si il vous a été utile !** 