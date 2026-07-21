from django.contrib.auth import get_user_model
import pytest
from notifications.models import Notification
from notifications.services import NotificationService

User = get_user_model()

pytestmark=pytest.mark.django_db



def test_create_notification(user,notification):
    assert notification.recipient==user
    assert notification.title == "welcome"
    assert notification.message == "Thanks for signing up"
    assert Notification.objects.count() == 1

def test_create_notification_unread_by_default(notification):
    assert notification.is_read==False

def test_create_two_notifications(user):
    NotificationService.create_notification(recipient_id=user.id, title="first", message="first")
    NotificationService.create_notification(recipient_id=user.id, title="second", message="second")
    assert Notification.objects.count() == 2
