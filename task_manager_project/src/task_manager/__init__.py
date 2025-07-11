"""
Package task_manager - Gestionnaire de tâches

Ce package contient les classes principales pour la gestion des tâches.
"""

from .task import Task, Priority, Status
from .manager import TaskManager
from .services import EmailService, ReportService

__all__ = ['Task', 'Priority', 'Status', 'TaskManager', 'EmailService', 'ReportService'] 