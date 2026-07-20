from django.contrib.auth import get_user_model
import pytest
from notifications.models import Notification

User = get_user_model()

pytestmark=pytest.mark.django_db


def test_create_user(user):
    assert user.phone=="09353045287"
    assert user.is_active==True


def test_number(sample_num):
    assert sample_num==5

def test_name(sample_name):
    assert sample_name == "alireza"

def test_notification_is_unread_by_default(user):
    notification= Notification.objects.create(recipient=user,title="welcome",message="Thanks for signing up")
    assert notification.is_read is False
    assert str(notification)=="notification for 09353045287"

