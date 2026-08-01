import pytest
from unittest.mock import patch
from task_manager.models import Task
from task_manager.services import TaskService


pytestmark = pytest.mark.django_db


def test_create_task(user,workspace,make_task_serializer):
    serializer = make_task_serializer()
    task=TaskService.create_task(user=user,workspace=workspace,serializer=serializer)

    assert task.created_by == user
    assert task.workspace == workspace
    assert task.title == "New Task"
    assert Task.objects.count() == 1