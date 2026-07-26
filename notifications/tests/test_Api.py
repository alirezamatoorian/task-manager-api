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

def test_cannot_see_other_users_notifications(api_client,user,other_user,notification):
    api_client.force_authenticate(user=other_user)
    response = api_client.get("/api/notifications/")

    assert response.status_code == 200
    assert len(response.data) == 0
