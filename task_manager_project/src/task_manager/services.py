import smtplib
import os
import csv
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from .task import Task


class EmailService:
    """Service simulé d'envoi d'emails pour les rappels et notifications de tâches."""
    def __init__(self, smtp_server: str = "smtp.gmail.com", port: int = 587):
        self.smtp_server = smtp_server
        self.port = port

    def send_task_reminder(self, email: str, task_title: str, due_date: str) -> str:
        if "@" not in email:
            raise ValueError(f"Adresse email invalide : {email}")
        # Simulation d'envoi
        message = f"[RAPPEL] La tâche '{task_title}' est à rendre pour le {due_date}."
        print(f"[SIMULATION EMAIL] Envoi à {email} via {self.smtp_server}:{self.port} : {message}")
        return message

    def send_completion_notification(self, email: str, task_title: str) -> str:
        if "@" not in email:
            raise ValueError(f"Adresse email invalide : {email}")
        # Simulation d'envoi
        message = f"[CONFIRMATION] La tâche '{task_title}' a été complétée avec succès."
        print(f"[SIMULATION EMAIL] Envoi à {email} via {self.smtp_server}:{self.port} : {message}")
        return message


class ReportService:
    """Service de génération de rapports et d'export CSV pour les tâches."""
    def generate_daily_report(self, tasks: List[Task], date_: Optional[str] = None) -> Dict[str, Any]:
        if date_ is None:
            date_ = date.today().isoformat()
        # Filtrer les tâches créées ou modifiées à la date donnée
        filtered = [t for t in tasks if (t.created_at.startswith(date_) or t.updated_at.startswith(date_))]
        stats = {
            'date': date_,
            'total': len(filtered),
            'completed': sum(1 for t in filtered if t.status.value == 'completed'),
            'in_progress': sum(1 for t in filtered if t.status.value == 'in_progress'),
            'todo': sum(1 for t in filtered if t.status.value == 'todo'),
            'urgent': sum(1 for t in filtered if t.priority.value == 'urgent'),
            'by_assignee': {}
        }
        for t in filtered:
            if t.assignee:
                stats['by_assignee'][t.assignee] = stats['by_assignee'].get(t.assignee, 0) + 1
        return stats

    def export_tasks_csv(self, tasks: List[Task], filename: str) -> None:
        try:
            dirname = os.path.dirname(filename)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'id', 'title', 'description', 'priority', 'status',
                    'project', 'assignee', 'due_date', 'created_at', 'updated_at'
                ])
                for t in tasks:
                    writer.writerow([
                        t.id, t.title, t.description, t.priority.value, t.status.value,
                        t.project, t.assignee, t.due_date, t.created_at, t.updated_at
                    ])
        except Exception as e:
            raise IOError(f"Erreur lors de l'export CSV : {e}") 