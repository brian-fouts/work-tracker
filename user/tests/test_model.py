import pytest

from user.models import User


@pytest.mark.django_db
def test_create_user(username, password):
    """
    WHEN create is called
    THEN a User is returned with an id
    """
    user = User.objects.create(username=username, password=password)
    assert user.id > 0


@pytest.mark.django_db
def test_get_by_id(username, password):
    """
    GIVEN a user that has been created
    WHEN get is called with the id of the created user
    THEN the found user has the correct username
    """
    created_user = User.objects.create(username=username, password=password)
    user_id = created_user.id
    user = User.objects.get(id=user_id)
    assert user.username == created_user.username


@pytest.mark.django_db
@pytest.mark.parametrize("query_count", range(1, 3))
def test_query_count(query_count, username, password, django_assert_num_queries):
    """
    GIVEN a user that has been created
        AND a number of times to fetch the user
    WHEN get is called with the id of the created user
    THEN only 1 query is performed when fetching
    """
    created_user = User.objects.create(username=username, password=password)
    user_id = created_user.id

    with django_assert_num_queries(1):
        for _ in range(query_count):
            User.objects.get(id=user_id)
