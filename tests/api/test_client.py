import pytest

from src.api.client import TestomatAPI


@pytest.fixture
def api_client():
    return TestomatAPI(base_url="http://localhost", api_token="test_token")


def test_login(api_client: TestomatAPI, requests_mock):
    jwt_token = "test_jwt"
    requests_mock.post(f"{api_client.base_url}/api/login", json={"jwt": jwt_token})

    jwt = api_client.login()

    assert jwt == jwt_token
    assert api_client.jwt == jwt_token
    assert api_client.session.headers["Authorization"] == jwt_token


def test_get_projects(api_client: TestomatAPI, requests_mock):
    jwt_token = "test_jwt"
    projects_data = {
        "data": [
            {"id": "1", "attributes": {"title": "Project 1", "description": "desc", "created-at": "date"}},
            {"id": "2", "attributes": {"title": "Project 2", "description": "desc", "created-at": "date"}},
        ]
    }

    requests_mock.post(f"{api_client.base_url}/api/login", json={"jwt": jwt_token})
    requests_mock.get(f"{api_client.base_url}/api/projects", json=projects_data)

    projects = api_client.get_projects()

    assert len(projects) == 2
    assert projects[0].name == "Project 1"
    assert projects[1].id == "2"
    assert requests_mock.call_count == 2
    assert requests_mock.request_history[0].url == f"{api_client.base_url}/api/login"
    assert requests_mock.request_history[1].url == f"{api_client.base_url}/api/projects"


def test_get_projects_already_logged_in(api_client: TestomatAPI, requests_mock):
    jwt_token = "test_jwt"
    projects_data = {
        "data": [
            {"id": "1", "attributes": {"title": "Project 1", "description": "desc", "created-at": "date"}},
            {"id": "2", "attributes": {"title": "Project 2", "description": "desc", "created-at": "date"}},
        ]
    }

    requests_mock.post(f"{api_client.base_url}/api/login", json={"jwt": jwt_token})
    requests_mock.get(f"{api_client.base_url}/api/projects", json=projects_data)

    api_client.login()
    projects = api_client.get_projects()

    assert len(projects) == 2
    assert projects[0].name == "Project 1"
    assert projects[1].id == "2"
    assert requests_mock.call_count == 2  # login() + get_projects()
    assert requests_mock.request_history[0].url == f"{api_client.base_url}/api/login"
    assert requests_mock.request_history[1].url == f"{api_client.base_url}/api/projects"
