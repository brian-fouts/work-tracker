import uuid

import requests


class UserClient:
    def __init__(self, client):
        self.client = client
        self.url_path = "user/"

    def create(self, username, password, email, first_name, last_name):
        payload = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
        return self.client.post(self.url_path, payload)

    def get(self, user_id):
        return self.client.get(f"{self.url_path}{user_id}")


class ProjectClient:
    def __init__(self, client):
        self.client = client
        self.url_path = "project/"

    def create(self, name):
        payload = {
            "name": username,
        }
        return self.client.post(self.url_path, payload)

    def get(self, project_id):
        return self.client.get(f"{self.url_path}{project_id}/")

    def list(self):
        return self.client.get(f"projects")

    def get_members(self, project_id):
        return self.client.get(f"{self.url_path}{project_id}/members/")

    def join_project(self, project_id):
        return self.client.post(f"{self.url_path}{project_id}/join/")

    def leave_project(self, project_id):
        return self.client.post(f"{self.url_path}{project_id}/leave/")


class Client:
    def __init__(self, host="localhost", port=8080):
        self.user = UserClient(self)
        self.project = ProjectClient(self)
        self._host = host
        self._port = port
        self._access_token = None
        self._refresh_token = None

    @property
    def base_url(self):
        return f"http://{self._host}:{self._port}/"

    @property
    def headers(self):
        if not self._access_token:
            return None

        return {"Authorization": f"Bearer {self._access_token}"}

    def post(self, url_path, payload=None):
        if payload is None:
            payload = {}
        return requests.post(f"{self.base_url}{url_path}", json=payload, headers=self.headers)

    def get(self, url_path):
        return requests.get(f"{self.base_url}{url_path}", headers=self.headers)

    def auth(self, username, password):
        payload = {
            "username": username,
            "password": password,
        }
        response = self.post("token/", payload)
        body = response.json()
        self._access_token = body["access"]
        self._refresh_token = body["refresh"]


client = Client()

username = f"test-{uuid.uuid4()}"
password = str(uuid.uuid4())
email = f"test-{uuid.uuid4()}@test.com"
first_name = "test-first"
last_name = "test-last"

response = client.user.create(username, password, email, first_name, last_name)

print(response.json())
user_id = response.json()["user"]["id"]

response = client.user.get(user_id)
print(response.json())

client.auth(username, password)


response = client.project.list()
print(response.json())

response = client.project.create(f"project-{uuid.uuid4()}")
print(response.json())
project_id = response.json()["project"]["id"]
response = client.project.get(project_id)
print(response.json())

response = client.project.list()
print(response.json())

response = client.project.get_members(project_id)
print(response.json())

response = client.project.join_project(project_id)
print(response.json())

response = client.project.get_members(project_id)
print(response.json())

response = client.project.leave_project(project_id)
print(response.status_code)

response = client.project.get_members(project_id)
print(response.json())
