import pytest
from django.contrib.auth import get_user_model
from notifications.models import Notification
from notifications.services import NotificationService
from rest_framework.test import APIClient
User=get_user_model()



@pytest.fixture
def user():
    return User.objects.create_user(phone='09353045287', password='shahrivar1380')

@pytest.fixture
def notification(user):
    return NotificationService.create_notification(recipient_id=user.id,title="welcome",message="Thanks for signing up")
