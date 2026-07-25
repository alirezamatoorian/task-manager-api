




def test_notification_list_requires_authentication(api_client):
    response = api_client.get("/api/notifications/")

    assert response.status_code == 401


def test_notification_list(api_client,user):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/notifications/")
    assert response.status_code == 200
