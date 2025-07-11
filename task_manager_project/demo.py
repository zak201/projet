#!/usr/bin/env python3
"""
🎯 Démonstration du Gestionnaire de Tâches
===========================================

Ce script démontre toutes les fonctionnalités du gestionnaire de tâches :
- Création et gestion des tâches
- Filtrage et recherche
- Sauvegarde et chargement
- Gestion des erreurs
- Statistiques détaillées
"""

import sys
import os

# Ajouter le chemin du projet pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'task_manager_project', 'src'))

from task_manager import Task, TaskManager, Priority, Status, EmailService, ReportService


def print_header(title):
    """Affiche un en-tête stylisé"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")


def print_section(title):
    """Affiche une section avec style"""
    print(f"\n📋 {title}")
    print(f"{'-'*40}")


def print_task(task):
    """Affiche une tâche de manière formatée"""
    status_emoji = {
        Status.TODO: "⏳",
        Status.IN_PROGRESS: "🔄", 
        Status.COMPLETED: "✅",
        Status.CANCELLED: "❌"
    }
    
    priority_emoji = {
        Priority.LOW: "🟢",
        Priority.MEDIUM: "🟡", 
        Priority.HIGH: "🔴",
        Priority.URGENT: "🚨"
    }
    
    print(f"  {status_emoji[task.status]} {priority_emoji[task.priority]} {task.title}")
    print(f"     📝 {task.description}")
    print(f"     👤 Assigné à: {task.assignee}")
    print(f"     📁 Projet: {task.project}")
    print(f"     📅 Créée: {task.created_at}")
    if task.status == Status.COMPLETED:
        print(f"     ✅ Terminée: {task.updated_at}")
    print()


def print_statistics(manager):
    """Affiche les statistiques de manière détaillée"""
    stats = manager.get_statistics()
    
    print("📊 STATISTIQUES GLOBALES")
    print(f"   📈 Total de tâches: {stats['total_tasks']}")
    print("\n🎯 RÉPARTITION PAR STATUT:")
    status_emoji = {
        "todo": "⏳", "in_progress": "🔄", "review": "🧐", "completed": "✅", "cancelled": "❌"
    }
    for status, count in stats['by_status'].items():
        print(f"   {status_emoji.get(status, '•')} {status}: {count}")
    print("\n🎯 RÉPARTITION PAR PRIORITÉ:")
    priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴", "urgent": "🚨"}
    for priority, count in stats['by_priority'].items():
        print(f"   {priority_emoji.get(priority, '⚪')} {priority}: {count}")
    print("\n📁 RÉPARTITION PAR PROJET:")
    for project, count in stats['by_project'].items():
        print(f"   📂 {project}: {count}")
    print("\n👥 RÉPARTITION PAR ASSIGNÉ:")
    for assignee, count in stats['by_assignee'].items():
        print(f"   👤 {assignee}: {count}")


def main():
    """Fonction principale de démonstration"""
    print_header("DÉMONSTRATION DU GESTIONNAIRE DE TÂCHES")
    
    # 1. Création du gestionnaire
    print_section("1. INITIALISATION DU GESTIONNAIRE")
    manager = TaskManager()
    print("✅ Gestionnaire de tâches créé avec succès!")
    
    # 2. Création de tâches variées
    print_section("2. CRÉATION DE TÂCHES DIVERSES")
    
    tasks_data = [
        {
            "title": "Réviser la documentation API",
            "description": "Mettre à jour la documentation de l'API REST",
            "priority": Priority.HIGH,
            "status": Status.IN_PROGRESS,
            "assignee": "Alice Martin",
            "project": "Documentation"
        },
        {
            "title": "Corriger le bug de connexion",
            "description": "Résoudre le problème de timeout sur la page de login",
            "priority": Priority.URGENT,
            "status": Status.TODO,
            "assignee": "Bob Dupont",
            "project": "Frontend"
        },
        {
            "title": "Optimiser les requêtes SQL",
            "description": "Améliorer les performances de la base de données",
            "priority": Priority.MEDIUM,
            "status": Status.COMPLETED,
            "assignee": "Claire Dubois",
            "project": "Backend"
        },
        {
            "title": "Créer les tests unitaires",
            "description": "Ajouter des tests pour les nouvelles fonctionnalités",
            "priority": Priority.HIGH,
            "status": Status.TODO,
            "assignee": "David Leroy",
            "project": "Tests"
        },
        {
            "title": "Réunion d'équipe hebdomadaire",
            "description": "Planifier les objectifs de la semaine",
            "priority": Priority.LOW,
            "status": Status.COMPLETED,
            "assignee": "Emma Rousseau",
            "project": "Management"
        },
        {
            "title": "Mise à jour des dépendances",
            "description": "Mettre à jour les packages npm et pip",
            "priority": Priority.MEDIUM,
            "status": Status.IN_PROGRESS,
            "assignee": "François Moreau",
            "project": "DevOps"
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(tasks_data, 1):
        task = Task(
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data["priority"],
            status=task_data["status"],
            assignee=task_data["assignee"],
            project=task_data["project"]
        )
        manager.add_task(task)
        created_tasks.append(task)
        print(f"✅ Tâche {i} créée: {task.title}")
    
    # 3. Affichage de toutes les tâches
    print_section("3. AFFICHAGE DE TOUTES LES TÂCHES")
    all_tasks = manager.get_all_tasks()
    for task in all_tasks:
        print_task(task)
    
    # 4. Modification de certaines tâches
    print_section("4. MODIFICATION DES TÂCHES")
    
    # Marquer une tâche comme terminée
    if all_tasks:
        task_to_complete = all_tasks[0]
        print(f"🔄 Marquage de '{task_to_complete.title}' comme terminée...")
        task_to_complete.mark_completed()
        print("✅ Tâche marquée comme terminée!")
    
    # Changer la priorité d'une tâche
    if len(all_tasks) > 1:
        task_to_update = all_tasks[1]
        print(f"🔄 Changement de priorité pour '{task_to_update.title}'...")
        task_to_update.update_priority(Priority.URGENT)
        print("✅ Priorité mise à jour!")
    
    # 5. Filtrage des tâches
    print_section("5. FILTRAGE DES TÂCHES")
    
    # Par statut
    print("📋 Tâches à faire:")
    todo_tasks = manager.get_tasks_by_status(Status.TODO)
    for task in todo_tasks:
        print(f"  ⏳ {task.title}")
    
    print("\n🔄 Tâches en cours:")
    in_progress_tasks = manager.get_tasks_by_status(Status.IN_PROGRESS)
    for task in in_progress_tasks:
        print(f"  🔄 {task.title}")
    
    print("\n✅ Tâches terminées:")
    completed_tasks = manager.get_tasks_by_status(Status.COMPLETED)
    for task in completed_tasks:
        print(f"  ✅ {task.title}")
    
    # Par priorité
    print("\n🚨 Tâches urgentes:")
    urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
    for task in urgent_tasks:
        print(f"  🚨 {task.title}")
    
    # Par projet
    print("\n📁 Tâches du projet 'Frontend':")
    frontend_tasks = [t for t in all_tasks if t.project == "Frontend"]
    for task in frontend_tasks:
        print(f"  📁 {task.title}")
    
    # Par assigné
    print("\n👤 Tâches assignées à 'Alice Martin':")
    alice_tasks = [t for t in all_tasks if t.assignee == "Alice Martin"]
    for task in alice_tasks:
        print(f"  👤 {task.title}")
    
    # 6. Statistiques
    print_section("6. STATISTIQUES DÉTAILLÉES")
    print_statistics(manager)
    
    # 7. Sauvegarde et chargement
    print_section("7. SAUVEGARDE ET CHARGEMENT")
    
    # Sauvegarde
    filename = "demo_tasks.json"
    print(f"💾 Sauvegarde des tâches dans '{filename}'...")
    try:
        manager.save_to_file(filename)
        print("✅ Sauvegarde réussie!")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    # Création d'un nouveau gestionnaire et chargement
    print("🔄 Création d'un nouveau gestionnaire...")
    new_manager = TaskManager()
    
    print(f"📂 Chargement des tâches depuis '{filename}'...")
    try:
        new_manager.load_from_file(filename)
        print("✅ Chargement réussi!")
        print(f"📊 {len(new_manager.get_all_tasks())} tâches chargées")
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
    
    # 8. Gestion des erreurs
    print_section("8. GESTION DES ERREURS")
    
    # Tentative de récupération d'une tâche inexistante
    print("🔍 Tentative de récupération d'une tâche inexistante...")
    try:
        non_existent_task = manager.get_task("task-inexistante")
        print("❌ Erreur: la tâche aurait dû ne pas exister")
    except ValueError as e:
        print(f"✅ Erreur gérée correctement: {e}")
    
    # Tentative de suppression d'une tâche inexistante
    print("\n🗑️ Tentative de suppression d'une tâche inexistante...")
    try:
        manager.delete_task("task-inexistante")
        print("❌ Erreur: la suppression aurait dû échouer")
    except ValueError as e:
        print(f"✅ Erreur gérée correctement: {e}")
    
    # 9. Suppression d'une tâche existante
    print_section("9. SUPPRESSION DE TÂCHE")
    if all_tasks:
        task_to_delete = all_tasks[0]
        task_id = task_to_delete.id
        print(f"🗑️ Suppression de la tâche: {task_to_delete.title}")
        try:
            manager.delete_task(task_id)
            print("✅ Tâche supprimée avec succès!")
            
            # Vérification de la suppression
            try:
                manager.get_task(task_id)
                print("❌ Erreur: la tâche existe encore")
            except ValueError:
                print("✅ Vérification: la tâche a bien été supprimée")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
    
    # 10. Services externes (simulation)
    print_section("10. SERVICES EXTERNES")
    
    # Service email
    email_service = EmailService()
    print("📧 Test du service email...")
    try:
        result = email_service.send_completion_notification("test@example.com", "Test de notification")
        print(f"✅ Email envoyé: {result}")
    except Exception as e:
        print(f"❌ Erreur email: {e}")
    
    # Service de rapports
    report_service = ReportService()
    print("\n📊 Test du service de rapports...")
    try:
        report = report_service.generate_daily_report(all_tasks)
        print(f"✅ Rapport généré: {report}")
    except Exception as e:
        print(f"❌ Erreur rapport: {e}")
    
    # 11. Finalisation
    print_section("11. FINALISATION")
    print("🎉 Démonstration terminée avec succès!")
    print("📈 Toutes les fonctionnalités ont été testées:")
    print("   ✅ Création et gestion des tâches")
    print("   ✅ Filtrage et recherche")
    print("   ✅ Sauvegarde et chargement")
    print("   ✅ Gestion des erreurs")
    print("   ✅ Services externes")
    print("   ✅ Statistiques détaillées")
    
    # Nettoyage
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"🧹 Fichier temporaire '{filename}' supprimé")
        except Exception as e:
            print(f"⚠️ Impossible de supprimer le fichier temporaire: {e}")


if __name__ == "__main__":
    main() 