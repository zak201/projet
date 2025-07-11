import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class Priority(Enum):
    """Énumération des niveaux de priorité pour les tâches"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(Enum):
    """Énumération des statuts possibles pour les tâches"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task:
    """Classe représentant une tâche dans le gestionnaire de tâches"""
    
    def __init__(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM, 
                 status: Status = Status.TODO, project: Optional[str] = None, 
                 assignee: Optional[str] = None, due_date: Optional[str] = None):
        """
        Initialise une nouvelle tâche
        
        Args:
            title: Titre de la tâche
            description: Description détaillée de la tâche
            priority: Niveau de priorité (LOW, MEDIUM, HIGH, URGENT)
            status: Statut actuel de la tâche
            project: Projet associé à la tâche
            assignee: Personne assignée à la tâche
            due_date: Date d'échéance au format ISO
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.project = project
        self.assignee = assignee
        self.due_date = due_date
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def mark_completed(self) -> None:
        """Marque la tâche comme terminée"""
        self.status = Status.COMPLETED
        self.updated_at = datetime.now().isoformat()
    
    def update_priority(self, new_priority: Priority) -> None:
        """
        Met à jour la priorité de la tâche
        
        Args:
            new_priority: Nouvelle priorité à assigner
        """
        self.priority = new_priority
        self.updated_at = datetime.now().isoformat()
    
    def assign_to_project(self, project_name: str) -> None:
        """
        Assigne la tâche à un projet
        
        Args:
            project_name: Nom du projet
        """
        self.project = project_name
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la tâche en dictionnaire pour la sérialisation
        
        Returns:
            Dictionnaire contenant toutes les propriétés de la tâche
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'project': self.project,
            'assignee': self.assignee,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Crée une instance de Task à partir d'un dictionnaire
        
        Args:
            data: Dictionnaire contenant les données de la tâche
            
        Returns:
            Instance de Task
        """
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data['priority']),
            status=Status(data['status']),
            project=data.get('project'),
            assignee=data.get('assignee'),
            due_date=data.get('due_date')
        )
        task.id = data['id']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        return task
    
    def __str__(self) -> str:
        """Représentation string de la tâche"""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value}, priority={self.priority.value})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de la tâche"""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status={self.status.value}, priority={self.priority.value}, project={self.project}, assignee={self.assignee})" 