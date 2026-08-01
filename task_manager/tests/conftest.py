import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from task_manager.models import Task,WorkSpace,WorkSpaceMembership
import tempfile
import shutil
from unittest.mock import MagicMock
from ..serializers import TaskSerializer


User = get_user_model()


@pytest.fixture
def apiclient():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(phone="09353045287",password="shahrivar1380")

@pytest.fixture
def other_user():
    return User.objects.create_user(phone="09120473601",password="shahrivar1380")

@pytest.fixture
def workspace(user):
    workspace=WorkSpace.objects.create(title="workspace1",owner=user)
    WorkSpaceMembership.objects.create(workspace=workspace,user=user,role=WorkSpaceMembership.RoleChoices.OWNER)
    return workspace

@pytest.fixture
def task(workspace,user):
    return Task.objects.create(title="task1",description="this is task 1",created_by=user,workspace=workspace)

@pytest.fixture(autouse=True)
def use_temp_media_root(settings):
    temp_dir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_dir
    yield
    shutil.rmtree(temp_dir)


@pytest.fixture
def make_task_serializer(workspace,user):
    def _make(data=None, **context_overrides):
        if data is None:
            data = {"title": "New Task", "description": "task description"}

        request = MagicMock()
        request.user = context_overrides.get("request_user", user)

        view = MagicMock()
        view.kwargs = {"workspaces_pk": workspace.id}

        serializer = TaskSerializer(data=data, context={"request": request, "view": view})
        serializer.is_valid(raise_exception=True)
        return serializer
    return _make
