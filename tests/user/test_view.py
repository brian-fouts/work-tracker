import json

import jwt
import pytest


@pytest.mark.django_db
def test_create_user(user):
    """
    WHEN the /users/ endpoint receives a valid POST request
    THEN a user is created
    """
    assert user["id"] > 0


@pytest.mark.django_db
def test_fetch_user(client, user):
    """
    GIVEN a user that has been created
    WHEN the /users/:id endpoint receives a valid GET request
    THEN the correct user is returned
    """
    get_response = client.get(f"/users/{user['id']}/")
    fetched_user = json.loads(get_response.content)
    assert fetched_user["id"] == user["id"]


@pytest.mark.django_db
def test_access_token_claims_for_correct_user(access_token, user):
    """
    GIVEN a user that has been created
        AND an access token has been created for that user
    WHEN the claims are extracted from the access token
    THEN the user_id matches the user it was generated for
    """
    claims = jwt.decode(access_token, options={"verify_signature": False})
    assert claims["user_id"] == user["id"]
