import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from task_manager.models import Task,WorkSpace,WorkSpaceMembership
import tempfile
import shutil


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
