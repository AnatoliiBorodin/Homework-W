import logging

import requests
from requests.auth import HTTPBasicAuth


class ProjectCreateError(Exception):
    """Raised when Jira project creation fails."""


class JiraApi:
    def __init__(self, url, username, token):
        self.auth = HTTPBasicAuth(username, token)
        self.url = url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_project(self, payload):
        response = requests.post(
            f"{self.url}/rest/api/3/project",
            json=payload,
            headers=self.headers,
            auth=self.auth
        )
        try:
            response.raise_for_status()
        except requests.RequestException:
            raise ProjectCreateError(f"Failed to create project - {response.text}")
        return response.json()

