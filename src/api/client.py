from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class Project:
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None  # Assuming ISO format date string


class TestomatAPI:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.jwt = None
        self.session = requests.Session()

    def login(self) -> str:
        """
        Authenticates using the API token and stores the JWT.
        """
        url = f"{self.base_url}/api/login"
        # Perform the request directly via session to avoid circular calls with _request
        response = self.session.post(url, json={"api_token": self.api_token})
        response.raise_for_status()

        result = response.json()
        self.jwt = result.get("jwt")

        if self.jwt:
            self.session.headers.update({"Authorization": self.jwt})

        return self.jwt

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Internal method for executing requests with automatic authorization check.
        """
        if not self.jwt:
            self.login()

        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        # If the token has expired (401 Unauthorized), try to re-login and repeat the request
        if response.status_code == 401:
            self.login()
            response = self.session.request(method, url, **kwargs)

        response.raise_for_status()
        return response

    def get_projects(self) -> List[Project]:
        """
        Retrieves all projects for the authenticated user.
        """
        response = self._request("GET", "/api/projects")
        data = response.json().get("data", [])

        return [
            Project(
                id=item.get("id"),
                name=item.get("attributes", {}).get("title"),
                description=item.get("attributes", {}).get("description"),
                created_at=item.get("attributes", {}).get("created-at"),
            )
            for item in data
        ]
