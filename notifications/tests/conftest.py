import pytest
from django.contrib.auth import get_user_model
from notifications.models import Notification
User=get_user_model()



@pytest.fixture
def user():
    return User.objects.create_user(phone='09353045287', password='shahrivar1380')

@pytest.fixture
def notification():
    return Notification.objects.create(recipient=user,title="welcome")


@pytest.fixture
def sample_num():
    return 5

@pytest.fixture
def sample_name():
    return "alireza"