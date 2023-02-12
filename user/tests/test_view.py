import json

import pytest


def create_user(client, username, password):
    """Creates a user by submitting a POST request to the API"""
    data = {
        "username": username,
        "password": password,
        "email": "test@test.com",
        "first_name": "Tester",
        "last_name": "Testy",
    }
    return client.post("/users/", json.dumps(data), content_type="application/json")


@pytest.mark.django_db
def test_create_user(client, username, password):
    """
    WHEN the /users/ endpoint receives a valid POST request
    THEN a user is created
    """
    response = create_user(client, username, password)
    assert response.status_code == 200
    user = json.loads(response.content)
    assert user["id"] > 0


@pytest.mark.django_db
def test_fetch_user(client, username, password):
    """
    GIVEN a user that has been created
    WHEN the /users/:id endpoint receives a valid GET request
    THEN the correct user is returned
    """
    create_response = create_user(client, username, password)
    created_user = json.loads(create_response.content)
    user_id = created_user["id"]
    get_response = client.get(f"/users/{user_id}/")
    fetched_user = json.loads(get_response.content)
    assert fetched_user["id"] == user_id
