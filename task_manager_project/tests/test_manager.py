#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement du TaskManager
"""

import sys
import os
import tempfile
import shutil
import json
import pytest

# Ajouter le dossier src au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from task_manager import Task, Priority, Status, TaskManager


def test_task_manager_creation():
    """Test de création du TaskManager"""
    print("=== Test de création du TaskManager ===")
    
    # Créer un gestionnaire avec un fichier temporaire
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    print(f"Gestionnaire créé: {manager}")
    print(f"Nombre de tâches: {len(manager)}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_add_and_get_task():
    """Test d'ajout et de récupération de tâches"""
    print("=== Test d'ajout et récupération ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer et ajouter une tâche
    task = Task(
        title="Tâche de test",
        description="Description de test",
        priority=Priority.HIGH,
        assignee="Alice"
    )
    
    task_id = manager.add_task(task)
    print(f"Tâche ajoutée avec l'ID: {task_id}")
    
    # Récupérer la tâche
    retrieved_task = manager.get_task(task_id)
    print(f"Tâche récupérée: {retrieved_task}")
    
    # Vérifier que c'est la même tâche
    print(f"Tâches identiques: {task.id == retrieved_task.id}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_filtering_methods():
    """Test des méthodes de filtrage"""
    print("=== Test des méthodes de filtrage ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer plusieurs tâches avec différents statuts et priorités
    tasks = [
        Task("Tâche 1", priority=Priority.HIGH, status=Status.TODO, assignee="Alice"),
        Task("Tâche 2", priority=Priority.MEDIUM, status=Status.IN_PROGRESS, assignee="Bob"),
        Task("Tâche 3", priority=Priority.LOW, status=Status.COMPLETED, assignee="Alice"),
        Task("Tâche 4", priority=Priority.HIGH, status=Status.TODO, assignee="Charlie"),
        Task("Tâche 5", priority=Priority.URGENT, status=Status.IN_PROGRESS, assignee="Bob")
    ]
    
    # Ajouter toutes les tâches
    for task in tasks:
        manager.add_task(task)
    
    print(f"Total de tâches: {len(manager)}")
    
    # Test filtrage par statut
    todo_tasks = manager.get_tasks_by_status(Status.TODO)
    print(f"Tâches TODO: {len(todo_tasks)}")
    
    in_progress_tasks = manager.get_tasks_by_status(Status.IN_PROGRESS)
    print(f"Tâches EN COURS: {len(in_progress_tasks)}")
    
    # Test filtrage par priorité
    high_priority_tasks = manager.get_tasks_by_priority(Priority.HIGH)
    print(f"Tâches haute priorité: {len(high_priority_tasks)}")
    
    urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
    print(f"Tâches urgentes: {len(urgent_tasks)}")
    
    # Test filtrage par assigné
    alice_tasks = manager.get_tasks_by_assignee("Alice")
    print(f"Tâches d'Alice: {len(alice_tasks)}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_delete_task():
    """Test de suppression de tâches"""
    print("=== Test de suppression ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Ajouter une tâche
    task = Task("Tâche à supprimer")
    task_id = manager.add_task(task)
    
    print(f"Tâches avant suppression: {len(manager)}")
    
    # Supprimer la tâche
    success = manager.delete_task(task_id)
    print(f"Suppression réussie: {success}")
    print(f"Tâches après suppression: {len(manager)}")
    
    # Essayer de supprimer une tâche inexistante
    success = manager.delete_task("tâche-inexistante")
    print(f"Suppression tâche inexistante: {success}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_statistics():
    """Test des statistiques"""
    print("=== Test des statistiques ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer des tâches avec différents paramètres
    tasks = [
        Task("Tâche 1", priority=Priority.HIGH, status=Status.TODO, project="Projet A", assignee="Alice"),
        Task("Tâche 2", priority=Priority.MEDIUM, status=Status.IN_PROGRESS, project="Projet A", assignee="Bob"),
        Task("Tâche 3", priority=Priority.LOW, status=Status.COMPLETED, project="Projet B", assignee="Alice"),
        Task("Tâche 4", priority=Priority.HIGH, status=Status.TODO, project="Projet B", assignee="Charlie"),
        Task("Tâche 5", priority=Priority.URGENT, status=Status.IN_PROGRESS, project="Projet A", assignee="Bob")
    ]
    
    for task in tasks:
        manager.add_task(task)
    
    # Obtenir les statistiques
    stats = manager.get_statistics()
    
    print("Statistiques:")
    print(f"  Total de tâches: {stats['total_tasks']}")
    print(f"  Par statut: {stats['by_status']}")
    print(f"  Par priorité: {stats['by_priority']}")
    print(f"  Par projet: {stats['by_project']}")
    print(f"  Par assigné: {stats['by_assignee']}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_persistence():
    """Test de persistance des données"""
    print("=== Test de persistance ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    
    # Créer un gestionnaire et ajouter des tâches
    manager1 = TaskManager(storage_file=temp_file)
    
    tasks = [
        Task("Tâche persistante 1", priority=Priority.HIGH),
        Task("Tâche persistante 2", priority=Priority.MEDIUM),
        Task("Tâche persistante 3", priority=Priority.LOW)
    ]
    
    for task in tasks:
        manager1.add_task(task)
    
    print(f"Tâches dans le premier gestionnaire: {len(manager1)}")
    
    # Créer un nouveau gestionnaire avec le même fichier
    manager2 = TaskManager(storage_file=temp_file)
    
    print(f"Tâches dans le deuxième gestionnaire: {len(manager2)}")
    
    # Vérifier que les tâches sont les mêmes
    tasks1 = manager1.get_all_tasks()
    tasks2 = manager2.get_all_tasks()
    
    print(f"Tâches identiques: {len(tasks1) == len(tasks2)}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_error_handling():
    """Test de gestion des erreurs"""
    print("=== Test de gestion des erreurs ===")
    
    # Test avec un fichier JSON invalide
    temp_file = tempfile.mktemp(suffix='.json')
    
    # Créer un fichier JSON invalide
    with open(temp_file, 'w') as f:
        f.write('{"invalid": json}')
    
    try:
        manager = TaskManager(storage_file=temp_file)
        print("Gestionnaire créé malgré le JSON invalide (fichier ignoré)")
    except Exception as e:
        print(f"Erreur lors de la création: {e}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_update_task():
    """Test de mise à jour de tâches"""
    print("=== Test de mise à jour ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer et ajouter une tâche
    task = Task("Tâche à mettre à jour", priority=Priority.LOW, status=Status.TODO)
    task_id = manager.add_task(task)
    
    print(f"Tâche initiale: {manager.get_task(task_id)}")
    
    # Mettre à jour la tâche
    success = manager.update_task(task_id, priority=Priority.HIGH, status=Status.IN_PROGRESS)
    print(f"Mise à jour réussie: {success}")
    
    updated_task = manager.get_task(task_id)
    print(f"Tâche mise à jour: {updated_task}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_add_task_with_existing_id():
    """Test d'ajout d'une tâche avec un ID déjà présent"""
    print("=== Test d'ajout avec ID existant ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer une tâche
    task1 = Task("Tâche 1")
    task_id = manager.add_task(task1)
    
    # Créer une autre tâche avec le même ID
    task2 = Task("Tâche 2")
    task2.id = task_id  # Forcer le même ID
    
    # Doit lever une ValueError
    try:
        manager.add_task(task2)
        print("❌ Erreur: ValueError attendue mais non levée")
    except ValueError as e:
        print(f"✅ ValueError levée correctement: {e}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_update_task_with_invalid_attributes():
    """Test de mise à jour avec des attributs invalides/non existants"""
    print("=== Test de mise à jour avec attributs invalides ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer et ajouter une tâche
    task = Task("Tâche Test")
    task_id = manager.add_task(task)
    
    # Mettre à jour avec des attributs valides et invalides
    success = manager.update_task(
        task_id, 
        title="Nouveau titre",  # Valide
        invalid_attr="valeur",   # Invalide
        another_invalid=123      # Invalide
    )
    
    # Doit réussir malgré les attributs invalides
    print(f"Mise à jour réussie: {success}")
    
    # Vérifier que seuls les attributs valides ont été mis à jour
    updated_task = manager.get_task(task_id)
    assert updated_task.title == "Nouveau titre"
    assert not hasattr(updated_task, 'invalid_attr')
    assert not hasattr(updated_task, 'another_invalid')
    print("✅ Seuls les attributs valides ont été mis à jour")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_save_to_file_with_custom_filename():
    """Test de sauvegarde avec un nom de fichier personnalisé"""
    print("=== Test de sauvegarde avec nom personnalisé ===")
    
    manager = TaskManager("temp_tasks.json")
    
    # Ajouter quelques tâches
    task1 = Task("Tâche 1")
    task2 = Task("Tâche 2")
    manager.add_task(task1)
    manager.add_task(task2)
    
    # Sauvegarder avec un nom personnalisé
    custom_file = "custom_backup.json"
    manager.save_to_file(custom_file)
    
    # Vérifier que le fichier existe
    assert os.path.exists(custom_file)
    print(f"✅ Fichier sauvegardé: {custom_file}")
    
    # Nettoyer
    if os.path.exists(custom_file):
        os.remove(custom_file)
    print()


def test_load_from_file_with_corrupted_json():
    """Test de chargement d'un fichier JSON corrompu"""
    print("=== Test de chargement JSON corrompu ===")
    
    # Créer un fichier JSON corrompu
    corrupted_file = "corrupted.json"
    with open(corrupted_file, 'w') as f:
        f.write('{"invalid": json, "format":}')
    
    # Créer un gestionnaire et essayer de charger le fichier corrompu
    manager = TaskManager("temp_tasks.json")
    
    try:
        manager.load_from_file(corrupted_file)
        print("❌ Erreur: ValueError attendue mais non levée")
    except ValueError as e:
        print(f"✅ ValueError levée correctement: {e}")
    
    # Nettoyer
    if os.path.exists(corrupted_file):
        os.remove(corrupted_file)
    print()


def test_load_from_file_with_valid_json():
    """Test de chargement d'un fichier JSON valide"""
    print("=== Test de chargement JSON valide ===")
    
    # Créer un fichier JSON valide
    valid_file = "valid_tasks.json"
    valid_data = [
        {
            'id': 'test-id-1',
            'title': 'Tâche Test 1',
            'description': 'Description test',
            'priority': 'high',
            'status': 'todo',
            'project': 'Projet Test',
            'assignee': 'Alice',
            'due_date': '2024-12-31T23:59:59',
            'created_at': '2024-01-01T10:00:00',
            'updated_at': '2024-01-01T10:00:00'
        }
    ]
    
    with open(valid_file, 'w') as f:
        json.dump(valid_data, f)
    
    # Charger le fichier
    manager = TaskManager("temp_tasks.json")
    manager.load_from_file(valid_file)
    
    # Vérifier que la tâche a été chargée
    task = manager.get_task('test-id-1')
    assert task is not None
    assert task.title == 'Tâche Test 1'
    assert task.assignee == 'Alice'
    print("✅ Fichier JSON valide chargé correctement")
    
    # Nettoyer
    if os.path.exists(valid_file):
        os.remove(valid_file)
    print()


def test_clear_all_tasks():
    """Test de suppression de toutes les tâches"""
    print("=== Test de suppression de toutes les tâches ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Ajouter quelques tâches
    task1 = Task("Tâche 1")
    task2 = Task("Tâche 2")
    manager.add_task(task1)
    manager.add_task(task2)
    
    print(f"Tâches avant suppression: {len(manager)}")
    
    # Supprimer toutes les tâches
    manager.clear_all_tasks()
    
    print(f"Tâches après suppression: {len(manager)}")
    assert len(manager) == 0
    print("✅ Toutes les tâches supprimées")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_manager_len_and_str():
    """Test des méthodes __len__ et __str__"""
    print("=== Test de __len__ et __str__ ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Test __len__
    assert len(manager) == 0
    print(f"Longueur initiale: {len(manager)}")
    
    # Ajouter une tâche
    task = Task("Tâche Test")
    manager.add_task(task)
    
    assert len(manager) == 1
    print(f"Longueur après ajout: {len(manager)}")
    
    # Test __str__
    str_repr = str(manager)
    assert "TaskManager" in str_repr
    assert "1 tâches" in str_repr
    print(f"Représentation string: {str_repr}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_manager_repr():
    """Test de la méthode __repr__"""
    print("=== Test de __repr__ ===")
    
    manager = TaskManager("test_file.json")
    
    repr_str = repr(manager)
    assert "TaskManager" in repr_str
    assert "storage_file='test_file.json'" in repr_str
    assert "tasks_count=0" in repr_str
    print(f"Représentation détaillée: {repr_str}")
    print()


def test_get_tasks_by_project():
    """Test de filtrage par projet"""
    print("=== Test de filtrage par projet ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer des tâches avec différents projets
    task1 = Task("Tâche 1", project="Projet A")
    task2 = Task("Tâche 2", project="Projet B")
    task3 = Task("Tâche 3", project="Projet A")
    
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)
    
    # Filtrer par projet
    projet_a_tasks = manager.get_tasks_by_project("Projet A")
    assert len(projet_a_tasks) == 2
    print(f"Tâches Projet A: {len(projet_a_tasks)}")
    
    projet_b_tasks = manager.get_tasks_by_project("Projet B")
    assert len(projet_b_tasks) == 1
    print(f"Tâches Projet B: {len(projet_b_tasks)}")
    
    # Projet inexistant
    inexistant_tasks = manager.get_tasks_by_project("Projet Inexistant")
    assert len(inexistant_tasks) == 0
    print(f"Tâches projet inexistant: {len(inexistant_tasks)}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_get_tasks_by_assignee():
    """Test de filtrage par assigné"""
    print("=== Test de filtrage par assigné ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Créer des tâches avec différents assignés
    task1 = Task("Tâche 1", assignee="Alice")
    task2 = Task("Tâche 2", assignee="Bob")
    task3 = Task("Tâche 3", assignee="Alice")
    
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)
    
    # Filtrer par assigné
    alice_tasks = manager.get_tasks_by_assignee("Alice")
    assert len(alice_tasks) == 2
    print(f"Tâches d'Alice: {len(alice_tasks)}")
    
    bob_tasks = manager.get_tasks_by_assignee("Bob")
    assert len(bob_tasks) == 1
    print(f"Tâches de Bob: {len(bob_tasks)}")
    
    # Assigné inexistant
    inexistant_tasks = manager.get_tasks_by_assignee("Charlie")
    assert len(inexistant_tasks) == 0
    print(f"Tâches assigné inexistant: {len(inexistant_tasks)}")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_update_task_with_nonexistent_task():
    """Test de mise à jour d'une tâche inexistante"""
    print("=== Test de mise à jour tâche inexistante ===")
    
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(storage_file=temp_file)
    
    # Essayer de mettre à jour une tâche qui n'existe pas
    success = manager.update_task("tâche-inexistante", title="Nouveau titre")
    
    # Doit retourner False
    assert success is False
    print("✅ Mise à jour d'une tâche inexistante retourne False")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print()


def test_load_from_file_with_task_loading_error():
    """Test de chargement avec erreur lors du chargement d'une tâche"""
    print("=== Test de chargement avec erreur de tâche ===")
    
    # Créer un fichier JSON avec une tâche invalide
    invalid_file = "invalid_task.json"
    invalid_data = [
        {
            'id': 'test-id-1',
            'title': 'Tâche Test 1',
            'description': 'Description test',
            'priority': 'high',
            'status': 'todo',
            'project': 'Projet Test',
            'assignee': 'Alice',
            'due_date': '2024-12-31T23:59:59',
            'created_at': '2024-01-01T10:00:00',
            'updated_at': '2024-01-01T10:00:00'
        },
        {
            'id': 'test-id-2',
            'title': 'Tâche Invalide',
            # Manque des champs requis
            'priority': 'invalid_priority',  # Priorité invalide
            'status': 'invalid_status'      # Statut invalide
        }
    ]
    
    with open(invalid_file, 'w') as f:
        json.dump(invalid_data, f)
    
    # Charger le fichier - doit gérer l'erreur gracieusement
    manager = TaskManager("temp_tasks.json")
    manager.load_from_file(invalid_file)
    
    # Vérifier que la première tâche a été chargée mais pas la seconde
    task1 = manager.get_task('test-id-1')
    task2 = manager.get_task('test-id-2')
    
    assert task1 is not None
    assert task2 is None
    print("✅ Gestion correcte des erreurs de chargement de tâches")
    
    # Nettoyer
    if os.path.exists(invalid_file):
        os.remove(invalid_file)
    print()


if __name__ == "__main__":
    print("🚀 Démarrage des tests du TaskManager\n")
    
    test_task_manager_creation()
    test_add_and_get_task()
    test_filtering_methods()
    test_delete_task()
    test_statistics()
    test_persistence()
    test_error_handling()
    test_update_task()
    test_add_task_with_existing_id()
    test_update_task_with_invalid_attributes()
    test_save_to_file_with_custom_filename()
    test_load_from_file_with_corrupted_json()
    test_load_from_file_with_valid_json()
    test_clear_all_tasks()
    test_manager_len_and_str()
    test_manager_repr()
    test_get_tasks_by_project()
    test_get_tasks_by_assignee()
    test_update_task_with_nonexistent_task()
    test_load_from_file_with_task_loading_error()
    
    print("✅ Tous les tests du TaskManager ont été exécutés avec succès!") 