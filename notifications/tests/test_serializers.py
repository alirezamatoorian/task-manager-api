import pytest

from django.utils.timesince import timesince
from notifications.serializers import NotificationSerializer

pytestmark = pytest.mark.django_db


def test_notification_serializer(notification):
    serializer = NotificationSerializer(notification)

    assert set(serializer.data.keys()) == {
        "id",
        "recipient"
        ,"title"
        ,"message"
        ,"is_read"
        ,"created_at"
        ,"created_at_human"
    }

    assert serializer.data["title"] == "welcome"
    assert serializer.data["message"] == "Thanks for signing up"
    assert serializer.data["is_read"] is False
    assert serializer.data["created_at_human"]==timesince(notification.created_at)


def test_cannot_mark_read_notification_as_unread(notification):
    notification.is_read = True
    notification.save()
    serializer = NotificationSerializer(instance=notification,data={"is_read":False},partial=True)

    assert serializer.is_valid() is False
    assert "is_read" in serializer.errors


def test_can_mark_unread_notification_as_read(notification):
    serializer = NotificationSerializer(instance=notification,data={"is_read":True},partial=True)
    assert serializer.is_valid() is True
    assert serializer.validated_data["is_read"] is True


