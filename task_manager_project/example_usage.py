#!/usr/bin/env python3
"""
Exemple d'utilisation pratique du gestionnaire de tâches
"""

import sys
import os

# Ajouter le dossier src au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import Task, Priority, Status, TaskManager


def main():
    """Exemple d'utilisation du gestionnaire de tâches"""
    
    print("🚀 Exemple d'utilisation du gestionnaire de tâches\n")
    
    # Créer un gestionnaire avec stockage persistant
    manager = TaskManager("exemple_taches.json")
    
    print("=== Création de tâches ===")
    
    # Créer plusieurs tâches pour un projet
    tasks = [
        Task(
            title="Concevoir l'interface utilisateur",
            description="Créer les maquettes et wireframes pour l'application",
            priority=Priority.HIGH,
            status=Status.IN_PROGRESS,
            project="Application Web",
            assignee="Alice",
            due_date="2024-12-15T23:59:59"
        ),
        Task(
            title="Implémenter l'authentification",
            description="Système d'authentification JWT avec OAuth2",
            priority=Priority.URGENT,
            status=Status.TODO,
            project="Application Web",
            assignee="Bob",
            due_date="2024-12-10T23:59:59"
        ),
        Task(
            title="Écrire les tests unitaires",
            description="Tests pour les modules principaux",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            project="Application Web",
            assignee="Charlie",
            due_date="2024-12-20T23:59:59"
        ),
        Task(
            title="Déployer en production",
            description="Configuration du serveur et déploiement",
            priority=Priority.HIGH,
            status=Status.REVIEW,
            project="Application Web",
            assignee="David",
            due_date="2024-12-25T23:59:59"
        ),
        Task(
            title="Documentation utilisateur",
            description="Rédiger le manuel utilisateur",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            project="Application Web",
            assignee="Eve",
            due_date="2024-12-05T23:59:59"
        )
    ]
    
    # Ajouter toutes les tâches
    task_ids = []
    for task in tasks:
        task_id = manager.add_task(task)
        task_ids.append(task_id)
        print(f"✅ Tâche ajoutée: {task.title} (ID: {task_id})")
    
    print(f"\nTotal de tâches: {len(manager)}")
    
    print("\n=== Filtrage des tâches ===")
    
    # Filtrer par statut
    todo_tasks = manager.get_tasks_by_status(Status.TODO)
    print(f"📋 Tâches à faire: {len(todo_tasks)}")
    for task in todo_tasks:
        print(f"  - {task.title} (assigné à {task.assignee})")
    
    in_progress_tasks = manager.get_tasks_by_status(Status.IN_PROGRESS)
    print(f"🔄 Tâches en cours: {len(in_progress_tasks)}")
    for task in in_progress_tasks:
        print(f"  - {task.title} (assigné à {task.assignee})")
    
    # Filtrer par priorité
    urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
    print(f"🚨 Tâches urgentes: {len(urgent_tasks)}")
    for task in urgent_tasks:
        print(f"  - {task.title} (statut: {task.status.value})")
    
    # Filtrer par assigné
    alice_tasks = manager.get_tasks_by_assignee("Alice")
    print(f"👤 Tâches d'Alice: {len(alice_tasks)}")
    for task in alice_tasks:
        print(f"  - {task.title} (priorité: {task.priority.value})")
    
    print("\n=== Mise à jour des tâches ===")
    
    # Marquer une tâche comme terminée
    if todo_tasks:
        task_to_complete = todo_tasks[0]
        manager.update_task(task_to_complete.id, status=Status.COMPLETED)
        print(f"✅ Tâche marquée comme terminée: {task_to_complete.title}")
    
    # Changer la priorité d'une tâche
    if urgent_tasks:
        task_to_update = urgent_tasks[0]
        manager.update_task(task_to_update.id, priority=Priority.HIGH)
        print(f"📊 Priorité mise à jour: {task_to_update.title}")
    
    print("\n=== Statistiques ===")
    
    stats = manager.get_statistics()
    print(f"📊 Statistiques du projet:")
    print(f"  Total de tâches: {stats['total_tasks']}")
    print(f"  Par statut: {stats['by_status']}")
    print(f"  Par priorité: {stats['by_priority']}")
    print(f"  Par projet: {stats['by_project']}")
    print(f"  Par assigné: {stats['by_assignee']}")
    
    print("\n=== Sauvegarde et chargement ===")
    
    # Sauvegarder dans un fichier de backup
    backup_file = "backup_taches.json"
    manager.save_to_file(backup_file)
    print(f"💾 Sauvegarde créée: {backup_file}")
    
    # Créer un nouveau gestionnaire et charger depuis le backup
    new_manager = TaskManager("nouveau_gestionnaire.json")
    new_manager.load_from_file(backup_file)
    print(f"📂 Chargement depuis le backup: {len(new_manager)} tâches")
    
    print("\n=== Suppression de tâche ===")
    
    # Supprimer une tâche
    if task_ids:
        task_to_delete = manager.get_task(task_ids[0])
        if task_to_delete:
            success = manager.delete_task(task_ids[0])
            if success:
                print(f"🗑️ Tâche supprimée: {task_to_delete.title}")
                print(f"📊 Nouvelles statistiques: {len(manager)} tâches")
    
    print("\n=== Gestion des erreurs ===")
    
    # Tester la récupération d'une tâche inexistante
    non_existent_task = manager.get_task("tâche-inexistante")
    if non_existent_task is None:
        print("✅ Gestion correcte des tâches inexistantes")
    
    # Tester la suppression d'une tâche inexistante
    delete_success = manager.delete_task("tâche-inexistante")
    if not delete_success:
        print("✅ Gestion correcte de la suppression de tâches inexistantes")
    
    print("\n🎉 Exemple terminé avec succès!")
    print(f"📁 Fichier de données: {manager.storage_file}")
    print(f"📊 Tâches finales: {len(manager)}")


if __name__ == "__main__":
    main() 