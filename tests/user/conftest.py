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
