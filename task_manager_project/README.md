# Gestionnaire de Tâches - Sprint 2

## Description

Ce projet implémente un gestionnaire de tâches complet avec stockage persistant et gestion avancée des tâches, priorités et statuts.

## Structure du projet

```
task_manager_project/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── task.py
│       └── manager.py
├── test_task.py
├── test_manager.py
└── README.md
```

## Classes implémentées

### Priority (Enum)
Énumération des niveaux de priorité :
- `LOW` : Priorité faible
- `MEDIUM` : Priorité moyenne
- `HIGH` : Priorité élevée
- `URGENT` : Priorité urgente

### Status (Enum)
Énumération des statuts possibles :
- `TODO` : À faire
- `IN_PROGRESS` : En cours
- `REVIEW` : En révision
- `COMPLETED` : Terminé
- `CANCELLED` : Annulé

### Task (Classe)
Classe principale représentant une tâche avec les propriétés suivantes :
- `id` : Identifiant unique (UUID)
- `title` : Titre de la tâche
- `description` : Description détaillée
- `priority` : Niveau de priorité
- `status` : Statut actuel
- `project` : Projet associé
- `assignee` : Personne assignée
- `due_date` : Date d'échéance
- `created_at` : Date de création
- `updated_at` : Date de dernière modification

### TaskManager (Classe)
Gestionnaire principal avec stockage persistant JSON :

#### Méthodes principales :
- `add_task(task)` : Ajoute une tâche
- `get_task(task_id)` : Récupère une tâche par ID
- `get_tasks_by_status(status)` : Filtre par statut
- `get_tasks_by_priority(priority)` : Filtre par priorité
- `delete_task(task_id)` : Supprime une tâche
- `update_task(task_id, **kwargs)` : Met à jour une tâche
- `get_statistics()` : Calcule les statistiques
- `save_to_file(filename)` : Sauvegarde dans un fichier
- `load_from_file(filename)` : Charge depuis un fichier

#### Méthodes de filtrage supplémentaires :
- `get_all_tasks()` : Récupère toutes les tâches
- `get_tasks_by_project(project)` : Filtre par projet
- `get_tasks_by_assignee(assignee)` : Filtre par assigné

## Utilisation

### Exemple d'utilisation basique

```python
from task_manager import Task, Priority, Status, TaskManager

# Créer un gestionnaire
manager = TaskManager("mes_taches.json")

# Créer et ajouter des tâches
task1 = Task(
    title="Implémenter l'authentification",
    description="Ajouter un système d'authentification JWT",
    priority=Priority.HIGH,
    assignee="Alice",
    project="Backend"
)

task_id = manager.add_task(task1)

# Récupérer une tâche
task = manager.get_task(task_id)

# Filtrer les tâches
todo_tasks = manager.get_tasks_by_status(Status.TODO)
urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
alice_tasks = manager.get_tasks_by_assignee("Alice")

# Mettre à jour une tâche
manager.update_task(task_id, status=Status.IN_PROGRESS, priority=Priority.URGENT)

# Obtenir les statistiques
stats = manager.get_statistics()
print(f"Total de tâches: {stats['total_tasks']}")
print(f"Par statut: {stats['by_status']}")
```

### Gestion des erreurs

Le TaskManager gère automatiquement les erreurs de sérialisation/désérialisation :

```python
# Gestion des erreurs de fichier
try:
    manager = TaskManager("fichier_inexistant.json")
    # Le gestionnaire se crée même si le fichier n'existe pas
except Exception as e:
    print(f"Erreur: {e}")

# Gestion des erreurs de format JSON
try:
    manager.load_from_file("fichier_corrompu.json")
except ValueError as e:
    print(f"Format JSON invalide: {e}")
except IOError as e:
    print(f"Erreur de lecture: {e}")
```

### Persistance des données

Les données sont automatiquement sauvegardées en JSON :

```python
# Sauvegarde automatique
manager = TaskManager("taches.json")
manager.add_task(Task("Nouvelle tâche"))  # Sauvegarde automatique

# Sauvegarde manuelle
manager.save_to_file("backup.json")

# Chargement depuis un fichier
manager.load_from_file("backup.json")
```

## Tests

Pour exécuter les tests :

```bash
# Tests des classes de base
python test_task.py

# Tests du gestionnaire
python test_manager.py
```

## Fonctionnalités implémentées

### Sprint 1 ✅
- ✅ Structure du projet créée
- ✅ Classe `Task` avec toutes les propriétés requises
- ✅ Énumérations `Priority` et `Status`
- ✅ Méthode `__init__` avec UUID et timestamps ISO
- ✅ Méthode `mark_completed()`
- ✅ Méthode `update_priority()`
- ✅ Méthode `assign_to_project()`
- ✅ Méthode `to_dict()` pour la sérialisation
- ✅ Méthode `from_dict()` pour la désérialisation
- ✅ Tests de validation
- ✅ Documentation complète

### Sprint 2 ✅
- ✅ Classe `TaskManager` avec stockage persistant
- ✅ Méthode `add_task()` avec gestion des erreurs
- ✅ Méthode `get_task()` pour récupération par ID
- ✅ Méthode `get_tasks_by_status()` pour filtrage
- ✅ Méthode `get_tasks_by_priority()` pour filtrage
- ✅ Méthode `delete_task()` avec retour booléen
- ✅ Méthode `save_to_file()` pour sauvegarde manuelle
- ✅ Méthode `load_from_file()` pour chargement manuel
- ✅ Méthode `get_statistics()` pour analyses
- ✅ Sérialisation/désérialisation JSON robuste
- ✅ Gestion complète des erreurs (IOError, ValueError)
- ✅ Tests complets du gestionnaire
- ✅ Méthodes de filtrage supplémentaires
- ✅ Mise à jour automatique des timestamps

## Prochaines étapes

- Sprint 3 : Interface utilisateur (CLI ou GUI)
- Sprint 4 : Fonctionnalités avancées (notifications, rapports)
- Sprint 5 : API REST et interface web 