import pytest

from django.utils.timesince import timesince
from notifications.serializers import NotificationSerializer

pytestmark = pytest.mark.django_db


def test_notification_serializer(notification):
    serializer = NotificationSerializer(notification)
    assert serializer.data["title"] == "welcome"
    assert serializer.data["message"] == "Thanks for signing up"
    assert serializer.data["is_read"] is False
    assert serializer.data["created_at_human"]==timesince(notification.created_at)
