import json

import pytest


def create_work(authorized_client, project, duration=1.25):
    data = {"project": project["id"], "start_time": "2023-01-01T10:10:01", "duration": duration}
    return authorized_client.post("/work/", json.dumps(data), content_type="application/json")


@pytest.mark.smoke
@pytest.mark.django_db
def test_cannot_create_work(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has not been joined
    WHEN the /work/ endpoint receives a POST request
    THEN a 403 status code is returned
    """
    work_response = create_work(authorized_client, project)
    assert work_response.status_code == 403


@pytest.mark.smoke
@pytest.mark.django_db
def test_can_create_work(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has been joined
    WHEN the /work/ endpoint receives a POST request
    THEN the resulting work has been assigned a id
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    work_response = create_work(authorized_client, project)
    work = json.loads(work_response.content)
    assert work["id"] > 0


@pytest.mark.smoke
@pytest.mark.acceptance
@pytest.mark.django_db
def test_created_work_listed(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has been joined
        AND work has been created
    WHEN the project work endpoint is called
    THEN the created work is listed in the response
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    create_work_response = create_work(authorized_client, project)
    created_work = json.loads(create_work_response.content)

    work_response = authorized_client.get(f"/projects/{project['id']}/work/")
    works = json.loads(work_response.content)

    assert created_work["id"] in [work["id"] for work in works]


@pytest.mark.acceptance
@pytest.mark.django_db
def test_retrieve_work_duration(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has been joined
        AND work has been created
    WHEN the the work is retrieved from the API
    THEN the returned work has the correct duration
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    duration = 2.22
    create_work_response = create_work(authorized_client, project, duration=duration)
    created_work = json.loads(create_work_response.content)

    work_response = authorized_client.get(f"/work/{created_work['id']}/")
    work = json.loads(work_response.content)

    assert work["duration"] == duration


@pytest.mark.acceptance
@pytest.mark.django_db
def test_delete_work(authorized_client, project, user):
    """
    GIVEN a Project that has been created through the API
        AND the project has been joined
        AND work has been created
        AND work has been deleted
    WHEN the project work endpoint is called
    THEN the created work is not listed in the response
    """
    authorized_client.post(f"/projects/{project['id']}/join/")
    create_work_response = create_work(authorized_client, project)
    created_work = json.loads(create_work_response.content)

    authorized_client.delete(f"/work/{created_work['id']}/")

    work_response = authorized_client.get(f"/projects/{project['id']}/work/")
    works = json.loads(work_response.content)

    assert created_work["id"] not in [work["id"] for work in works]
