import json

import pytest


@pytest.mark.smoke
@pytest.mark.django_db
def test_create_project(project):
    """
    GIVEN a Project that has been created through the API
    THEN the id field is set
    """
    assert project["id"] > 0


@pytest.mark.smoke
@pytest.mark.django_db
def test_join_project(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
    WHEN the project is joined
    THEN the authenticated user is a member of the project
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    members_response = authorized_client.get(f"/projects/{project['id']}/members/")
    members = json.loads(members_response.content)
    assert user["id"] in [member["user"]["id"] for member in members]


@pytest.mark.smoke
@pytest.mark.django_db
def test_leave_project(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the authenticated user has joined the project
    WHEN the project is left
    THEN the authenticated user is not a member of the project
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    authorized_client.post(f"/projects/{project['id']}/leave/")
    members_response = authorized_client.get(f"/projects/{project['id']}/members/")
    members = json.loads(members_response.content)
    assert user["id"] not in [member["user"]["id"] for member in members]


@pytest.mark.acceptance
@pytest.mark.django_db
def test_work_cannot_be_viewed(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has not been joined
    WHEN the project work endpoint is called
    THEN a 403 response code is returned
    """
    response = authorized_client.get(f"/projects/{project['id']}/work/")
    assert response.status_code == 403


@pytest.mark.acceptance
@pytest.mark.django_db
def test_work_can_be_viewed(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has been joined
    WHEN the project work endpoint is called
    THEN a 200 response code is returned
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    response = authorized_client.get(f"/projects/{project['id']}/work/")
    assert response.status_code == 200
