import pytest

pytestmark=pytest.mark.django_db



def test_notification_list_requires_authentication(api_client):
    response = api_client.get("/api/notifications/")
    assert response.status_code == 401


def test_notification_list(api_client,user,notification):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/notifications/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"]=="welcome"
    assert response.data[0]["message"]=="Thanks for signing up"
    assert response.data[0]["is_read"]==False


def test_user_can_only_see_own_notifications(api_client,user,other_user,notification):
    api_client.force_authenticate(user=other_user)
    response = api_client.get("/api/notifications/")

    assert response.status_code == 200
    assert len(response.data) == 0

def test_mark_as_read(api_client,user,notification):
    api_client.force_authenticate(user=user)
    assert notification.is_read is False
    response = api_client.patch(f"/api/notifications/{notification.id}/mark_as_read/")
    assert response.status_code == 200
    assert response.data["message"]=="notification marked as read"
    notification.refresh_from_db()
    assert notification.is_read is True

def test_all_marks_as_read(api_client,user,notification,notification_factory):
    api_client.force_authenticate(user=user)
    n2=notification_factory(recipient=user)
    response = api_client.patch(f"/api/notifications/all_marks_as_read/")
    assert response.status_code == 200
    notification.refresh_from_db()
    n2.refresh_from_db()
    assert notification.is_read is True
    assert n2.is_read is True

def test_can_only_mark_own_notifications(api_client,other_user,notification):
    api_client.force_authenticate(user=other_user)
    response = api_client.patch(f"/api/notifications/{notification.id}/mark_as_read/")
    assert response.status_code == 404
    notification.refresh_from_db()
    assert notification.is_read is False


def test_all_marks_as_read_only_updates_current_user_notifications(api_client,user,other_user,notification_factory,):
    own=notification_factory(recipient=user)
    other=notification_factory(recipient=other_user)
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/api/notifications/all_marks_as_read/")
    own.refresh_from_db()
    other.refresh_from_db()
    assert response.status_code == 200
    assert own.is_read is True
    assert other.is_read is False


def test_mark_as_read_on_already_read_notification(api_client,user,notification):
    api_client.force_authenticate(user=user)
    notification.is_read=True
    notification.save()
    response = api_client.patch(f"/api/notifications/{notification.id}/mark_as_read/")
    assert response.status_code == 200
    assert notification.is_read is True


def test_mark_as_read_returns_404_for_non_existing_notification(api_client,user):
    api_client.force_authenticate(user=user)
    response = api_client.patch("/api/notifications/999999/mark_as_read/")
    assert response.status_code == 404
