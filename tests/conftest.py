import pytest


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
