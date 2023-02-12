import uuid

import pytest


@pytest.fixture
def username():
    return "test-user"


@pytest.fixture
def password():
    return str(uuid.uuid4())
