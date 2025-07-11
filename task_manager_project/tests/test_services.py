import pytest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import os
import tempfile

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from task_manager import Task, Priority, Status, EmailService, ReportService

# --- FIXTURE DE TÂCHES SIMULÉES ---
@pytest.fixture
def sample_tasks():
    now = datetime.now()
    return [
        Task(
            title="Tâche 1",
            description="Desc 1",
            priority=Priority.HIGH,
            status=Status.TODO,
            assignee="Alice",
            due_date=(now + timedelta(days=1)).isoformat(),
        ),
        Task(
            title="Tâche 2",
            description="Desc 2",
            priority=Priority.URGENT,
            status=Status.IN_PROGRESS,
            assignee="Bob",
            due_date=(now + timedelta(days=2)).isoformat(),
        ),
        Task(
            title="Tâche 3",
            description="Desc 3",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            assignee="Alice",
            due_date=(now + timedelta(days=3)).isoformat(),
        ),
    ]

# --- TESTS EMAILSERVICE ---
def test_send_task_reminder_valid():
    service = EmailService()
    result = service.send_task_reminder("test@example.com", "Tâche Test", "2024-12-31")
    assert "RAPPEL" in result
    assert "Tâche Test" in result


def test_send_task_reminder_invalid():
    service = EmailService()
    with pytest.raises(ValueError):
        service.send_task_reminder("invalid_email", "Tâche Test", "2024-12-31")


def test_send_completion_notification_valid():
    service = EmailService()
    result = service.send_completion_notification("user@domaine.fr", "Tâche Complétée")
    assert "CONFIRMATION" in result
    assert "Tâche Complétée" in result


def test_send_completion_notification_invalid():
    service = EmailService()
    with pytest.raises(ValueError):
        service.send_completion_notification("pasdemail", "Tâche Complétée")

# --- TESTS AVEC PATCH SMTP (simulation, pas d'envoi réel) ---
def test_emailservice_init_params():
    service = EmailService(smtp_server="smtp.test.com", port=2525)
    assert service.smtp_server == "smtp.test.com"
    assert service.port == 2525


@patch('smtplib.SMTP')
def test_emailservice_with_smtp_mock(mock_smtp):
    """Test avec mock SMTP pour simuler l'envoi d'email"""
    service = EmailService(smtp_server="smtp.test.com", port=2525)
    
    # Configurer le mock SMTP
    mock_smtp_instance = mock_smtp.return_value
    mock_smtp_instance.starttls.return_value = None
    mock_smtp_instance.login.return_value = None
    mock_smtp_instance.sendmail.return_value = None
    mock_smtp_instance.quit.return_value = None
    
    # Test d'envoi de rappel
    result = service.send_task_reminder("test@example.com", "Tâche Test", "2024-12-31")
    
    # Vérifier que le message contient les bonnes informations
    assert "RAPPEL" in result
    assert "Tâche Test" in result
    assert "2024-12-31" in result

# --- TESTS REPORTSERVICE ---
def test_generate_daily_report(sample_tasks):
    service = ReportService()
    today = datetime.now().date().isoformat()
    # On force la date de création/MAJ de toutes les tâches à aujourd'hui
    for t in sample_tasks:
        t.created_at = today + "T10:00:00"
        t.updated_at = today + "T10:00:00"
    stats = service.generate_daily_report(sample_tasks, date_=today)
    assert stats['date'] == today
    assert stats['total'] == len(sample_tasks)
    assert stats['completed'] == 1
    assert stats['in_progress'] == 1
    assert stats['todo'] == 1
    assert stats['urgent'] == 1
    assert stats['by_assignee']['Alice'] == 2
    assert stats['by_assignee']['Bob'] == 1


def test_generate_daily_report_empty():
    service = ReportService()
    stats = service.generate_daily_report([], date_="2024-01-01")
    assert stats['total'] == 0
    assert stats['completed'] == 0
    assert stats['in_progress'] == 0
    assert stats['todo'] == 0
    assert stats['urgent'] == 0
    assert stats['by_assignee'] == {}


def test_generate_daily_report_with_default_date():
    service = ReportService()
    stats = service.generate_daily_report([])
    assert 'date' in stats
    assert stats['total'] == 0

# --- TEST EXPORT CSV ---
def test_export_tasks_csv_success(sample_tasks, tmp_path):
    service = ReportService()
    csv_file = tmp_path / "export.csv"
    service.export_tasks_csv(sample_tasks, str(csv_file))
    assert os.path.exists(csv_file)
    with open(csv_file, encoding='utf-8') as f:
        content = f.read()
        assert "id,title,description,priority,status" in content
        assert "Tâche 1" in content
        assert "Tâche 2" in content


def test_export_tasks_csv_error(sample_tasks):
    service = ReportService()
    # Simuler une erreur d'écriture avec open patché
    with patch("builtins.open", mock_open()) as m:
        m.side_effect = IOError("Erreur simulée")
        with pytest.raises(IOError):
            service.export_tasks_csv(sample_tasks, "/chemin/invalide/export.csv")


@patch('builtins.open', new_callable=mock_open)
def test_export_tasks_csv_with_mock_open(mock_file, sample_tasks):
    """Test d'export CSV avec mock open pour vérifier l'écriture"""
    service = ReportService()
    service.export_tasks_csv(sample_tasks, "test_export.csv")
    
    # Vérifier que open a été appelé
    mock_file.assert_called_once_with("test_export.csv", 'w', newline='', encoding='utf-8') 