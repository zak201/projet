#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement des classes Task, Priority et Status
"""

import sys
import os

# Ajouter le dossier src au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import Task, Priority, Status


def test_task_creation():
    """Test de création d'une tâche"""
    print("=== Test de création de tâche ===")
    
    # Créer une tâche simple
    task = Task(
        title="Tâche de test",
        description="Description de la tâche de test",
        priority=Priority.HIGH,
        assignee="John Doe"
    )
    
    print(f"Tâche créée: {task}")
    print(f"ID: {task.id}")
    print(f"Statut: {task.status.value}")
    print(f"Priorité: {task.priority.value}")
    print(f"Assigné à: {task.assignee}")
    print(f"Créé le: {task.created_at}")
    print()


def test_task_methods():
    """Test des méthodes de la classe Task"""
    print("=== Test des méthodes ===")
    
    task = Task(
        title="Tâche avec méthodes",
        description="Test des différentes méthodes",
        priority=Priority.MEDIUM
    )
    
    print(f"Tâche initiale: {task}")
    
    # Test mark_completed
    task.mark_completed()
    print(f"Après mark_completed: {task}")
    
    # Test update_priority
    task.update_priority(Priority.URGENT)
    print(f"Après update_priority: {task}")
    
    # Test assign_to_project
    task.assign_to_project("Projet Test")
    print(f"Après assign_to_project: {task}")
    print()


def test_serialization():
    """Test de sérialisation/désérialisation"""
    print("=== Test de sérialisation ===")
    
    # Créer une tâche
    original_task = Task(
        title="Tâche pour sérialisation",
        description="Test de to_dict et from_dict",
        priority=Priority.LOW,
        status=Status.IN_PROGRESS,
        project="Projet Sérialisation",
        assignee="Alice",
        due_date="2024-12-31T23:59:59"
    )
    
    print(f"Tâche originale: {original_task}")
    
    # Convertir en dictionnaire
    task_dict = original_task.to_dict()
    print(f"Dictionnaire: {task_dict}")
    
    # Recréer à partir du dictionnaire
    reconstructed_task = Task.from_dict(task_dict)
    print(f"Tâche reconstruite: {reconstructed_task}")
    
    # Vérifier que les objets sont identiques
    print(f"Les tâches sont identiques: {original_task.to_dict() == reconstructed_task.to_dict()}")
    print()


def test_enums():
    """Test des énumérations"""
    print("=== Test des énumérations ===")
    
    print("Priorités disponibles:")
    for priority in Priority:
        print(f"  - {priority.name}: {priority.value}")
    
    print("\nStatuts disponibles:")
    for status in Status:
        print(f"  - {status.name}: {status.value}")
    print()


def test_task_repr():
    """Test de la méthode __repr__ pour couvrir la ligne 129"""
    print("=== Test de __repr__ ===")
    
    task = Task(
        title="Tâche Test",
        description="Description de test",
        priority=Priority.HIGH,
        status=Status.IN_PROGRESS,
        project="Projet Test",
        assignee="Alice"
    )
    
    repr_str = repr(task)
    print(f"Représentation détaillée: {repr_str}")
    
    # Vérifier que tous les éléments sont présents
    assert "Task(" in repr_str
    assert "title='Tâche Test'" in repr_str
    assert "description='Description de test'" in repr_str
    assert "status=in_progress" in repr_str
    assert "priority=high" in repr_str
    assert "project=Projet Test" in repr_str
    assert "assignee=Alice" in repr_str
    print("✅ __repr__ fonctionne correctement")
    print()


def test_task_all_statuses():
    """Test de tous les statuts possibles"""
    print("=== Test de tous les statuts ===")
    
    for status in Status:
        task = Task("Tâche", status=status)
        assert task.status == status
        assert task.status.value == status.value
        print(f"✅ Statut {status.name} fonctionne")
    print()


def test_task_all_priorities():
    """Test de toutes les priorités possibles"""
    print("=== Test de toutes les priorités ===")
    
    for priority in Priority:
        task = Task("Tâche", priority=priority)
        assert task.priority == priority
        assert task.priority.value == priority.value
        print(f"✅ Priorité {priority.name} fonctionne")
    print()


def test_task_with_none_values():
    """Test avec des valeurs None"""
    print("=== Test avec valeurs None ===")
    
    task = Task(
        title="Tâche avec None",
        project=None,
        assignee=None,
        due_date=None
    )
    
    assert task.project is None
    assert task.assignee is None
    assert task.due_date is None
    
    # Test to_dict avec None
    task_dict = task.to_dict()
    assert task_dict['project'] is None
    assert task_dict['assignee'] is None
    assert task_dict['due_date'] is None
    
    print("✅ Gestion des valeurs None fonctionne")
    print()


if __name__ == "__main__":
    print("🚀 Démarrage des tests du gestionnaire de tâches\n")
    
    test_task_creation()
    test_task_methods()
    test_serialization()
    test_enums()
    test_task_repr()
    test_task_all_statuses()
    test_task_all_priorities()
    test_task_with_none_values()
    
    print("✅ Tous les tests ont été exécutés avec succès!") 