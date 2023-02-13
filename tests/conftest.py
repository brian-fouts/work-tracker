import json
import uuid

import pytest


@pytest.fixture
def username():
    return f"test-{uuid.uuid4()}"


@pytest.fixture
def password():
    return str(uuid.uuid4())


@pytest.fixture
def user(client, username, password):
    data = {
        "username": username,
        "password": password,
        "email": "test@test.com",
        "first_name": "Tester",
        "last_name": "Testy",
    }
    response = client.post("/users/", json.dumps(data), content_type="application/json")
    return json.loads(response.content)


@pytest.fixture
def access_token(client, user, username, password):
    data = {"username": username, "password": password}
    response = client.post("/token/", data)
    token_data = json.loads(response.content)
    return token_data["access"]


@pytest.fixture
def headers(access_token):
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def authorized_client(headers):
    from django.test import Client

    return Client(**headers)


@pytest.fixture(autouse=True)
def reset_cache():
    """
    Ensure that cache state does not persist between tests
    """
    from django.core.cache import cache

    cache.clear()


@pytest.fixture
def client():
    from django.test import Client

    return Client()


@pytest.fixture
def project(authorized_client):
    data = {
        "name": f"project-{uuid.uuid4()}",
    }
    response = authorized_client.post(
        "/projects/", json.dumps(data), content_type="application/json"
    )
    return json.loads(response.content)
