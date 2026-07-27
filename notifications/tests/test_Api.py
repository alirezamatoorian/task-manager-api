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
    response = api_client.patch(f"/api/notifications/{notification.id}/mark_as_read/")
    assert response.status_code == 200
    notification.refresh_from_db()
    assert notification.is_read is True
