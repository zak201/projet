import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from .task import Task, Priority, Status


class TaskManager:
    """Gestionnaire de tâches avec stockage persistant"""
    
    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialise le gestionnaire de tâches
        
        Args:
            storage_file: Chemin vers le fichier de stockage JSON
        """
        self.storage_file = storage_file
        self.tasks: Dict[str, Task] = {}
        self._load_from_file()
    
    def add_task(self, task: Task) -> str:
        """
        Ajoute une tâche au gestionnaire
        
        Args:
            task: Tâche à ajouter
            
        Returns:
            ID de la tâche ajoutée
            
        Raises:
            ValueError: Si la tâche a déjà un ID existant
        """
        if task.id in self.tasks:
            raise ValueError(f"Une tâche avec l'ID {task.id} existe déjà")
        
        self.tasks[task.id] = task
        self._save_to_file()
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Récupère une tâche par son ID
        
        Args:
            task_id: ID de la tâche à récupérer
            
        Returns:
            Tâche trouvée ou None si non trouvée
        """
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """
        Récupère toutes les tâches avec un statut donné
        
        Args:
            status: Statut à filtrer
            
        Returns:
            Liste des tâches avec le statut spécifié
        """
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """
        Récupère toutes les tâches avec une priorité donnée
        
        Args:
            priority: Priorité à filtrer
            
        Returns:
            Liste des tâches avec la priorité spécifiée
        """
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def delete_task(self, task_id: str) -> bool:
        """
        Supprime une tâche par son ID
        
        Args:
            task_id: ID de la tâche à supprimer
            
        Returns:
            True si la tâche a été supprimée, False sinon
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_to_file()
            return True
        return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """
        Met à jour une tâche existante
        
        Args:
            task_id: ID de la tâche à mettre à jour
            **kwargs: Attributs à mettre à jour
            
        Returns:
            True si la tâche a été mise à jour, False sinon
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        for attr, value in kwargs.items():
            if hasattr(task, attr):
                setattr(task, attr, value)
        
        task.updated_at = datetime.now().isoformat()
        self._save_to_file()
        return True
    
    def get_all_tasks(self) -> List[Task]:
        """
        Récupère toutes les tâches
        
        Returns:
            Liste de toutes les tâches
        """
        return list(self.tasks.values())
    
    def get_tasks_by_project(self, project: str) -> List[Task]:
        """
        Récupère toutes les tâches d'un projet
        
        Args:
            project: Nom du projet
            
        Returns:
            Liste des tâches du projet
        """
        return [task for task in self.tasks.values() if task.project == project]
    
    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """
        Récupère toutes les tâches assignées à une personne
        
        Args:
            assignee: Nom de la personne assignée
            
        Returns:
            Liste des tâches assignées
        """
        return [task for task in self.tasks.values() if task.assignee == assignee]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcule les statistiques des tâches
        
        Returns:
            Dictionnaire contenant les statistiques
        """
        total_tasks = len(self.tasks)
        
        # Statistiques par statut
        status_stats = {}
        for status in Status:
            status_stats[status.value] = len(self.get_tasks_by_status(status))
        
        # Statistiques par priorité
        priority_stats = {}
        for priority in Priority:
            priority_stats[priority.value] = len(self.get_tasks_by_priority(priority))
        
        # Statistiques par projet
        project_stats = {}
        for task in self.tasks.values():
            if task.project:
                project_stats[task.project] = project_stats.get(task.project, 0) + 1
        
        # Statistiques par assigné
        assignee_stats = {}
        for task in self.tasks.values():
            if task.assignee:
                assignee_stats[task.assignee] = assignee_stats.get(task.assignee, 0) + 1
        
        return {
            'total_tasks': total_tasks,
            'by_status': status_stats,
            'by_priority': priority_stats,
            'by_project': project_stats,
            'by_assignee': assignee_stats
        }
    
    def _save_to_file(self) -> None:
        """
        Sauvegarde les tâches dans le fichier JSON
        
        Raises:
            IOError: En cas d'erreur d'écriture
        """
        try:
            tasks_data = [task.to_dict() for task in self.tasks.values()]
            
            # Créer le dossier parent si nécessaire (seulement si le chemin contient des dossiers)
            dirname = os.path.dirname(self.storage_file)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise IOError(f"Erreur lors de la sauvegarde dans {self.storage_file}: {str(e)}")
    
    def _load_from_file(self) -> None:
        """
        Charge les tâches depuis le fichier JSON
        
        Raises:
            IOError: En cas d'erreur de lecture
            ValueError: En cas d'erreur de format JSON
        """
        if not os.path.exists(self.storage_file):
            return  # Fichier n'existe pas encore, pas d'erreur
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            self.tasks.clear()
            for task_data in tasks_data:
                try:
                    task = Task.from_dict(task_data)
                    self.tasks[task.id] = task
                except (KeyError, ValueError) as e:
                    print(f"Erreur lors du chargement d'une tâche: {e}")
                    continue
                    
        except json.JSONDecodeError as e:
            raise ValueError(f"Format JSON invalide dans {self.storage_file}: {str(e)}")
        except Exception as e:
            raise IOError(f"Erreur lors du chargement depuis {self.storage_file}: {str(e)}")
    
    def save_to_file(self, filename: Optional[str] = None) -> None:
        """
        Sauvegarde les tâches dans un fichier spécifique
        
        Args:
            filename: Nom du fichier (utilise self.storage_file si None)
            
        Raises:
            IOError: En cas d'erreur d'écriture
        """
        if filename:
            original_file = self.storage_file
            self.storage_file = filename
            self._save_to_file()
            self.storage_file = original_file
        else:
            self._save_to_file()
    
    def load_from_file(self, filename: str) -> None:
        """
        Charge les tâches depuis un fichier spécifique
        
        Args:
            filename: Nom du fichier à charger
            
        Raises:
            IOError: En cas d'erreur de lecture
            ValueError: En cas d'erreur de format JSON
        """
        original_file = self.storage_file
        self.storage_file = filename
        self._load_from_file()
        self.storage_file = original_file
    
    def clear_all_tasks(self) -> None:
        """Supprime toutes les tâches"""
        self.tasks.clear()
        self._save_to_file()
    
    def __len__(self) -> int:
        """Retourne le nombre de tâches"""
        return len(self.tasks)
    
    def __str__(self) -> str:
        """Représentation string du gestionnaire"""
        return f"TaskManager({len(self.tasks)} tâches)"
    
    def __repr__(self) -> str:
        """Représentation détaillée du gestionnaire"""
        return f"TaskManager(storage_file='{self.storage_file}', tasks_count={len(self.tasks)})" 