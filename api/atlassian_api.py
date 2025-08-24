import requests
from requests.auth import HTTPBasicAuth


class AtlassianApiError(Exception):
    """Raised when Jira project creation fails."""


class AtlassianApi:
    def __init__(self, url, username, token):
        self.auth = HTTPBasicAuth(username, token)
        self.url = url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_space(self, payload, private=False):
        url = f"{self.url}/wiki/rest/api/space"
        if private:
            url += "/_private"
        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth
        )
        try:
            response.raise_for_status()
        except requests.RequestException:
            raise AtlassianApiError(f"Failed to create space - {response.text}")
        return response.json()

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
            raise AtlassianApiError(f"Failed to create project - {response.text}")
        return response.json()

    def get_account_id(self, email):
        response = requests.get(
            f"{self.url}/rest/api/3/user/search?query={email}",
            headers=self.headers,
            auth=self.auth
        )
        try:
            response.raise_for_status()
        except requests.RequestException:
            raise AtlassianApiError(f"Failed to get account_id for user - {email} with error - {response.text}")
        users = response.json()
        if len(users) == 0 or len(users) > 1:
            raise AtlassianApiError(f"Failed to get account_id for user - {email} found - {len(users)} users with this email")
        return users[0]['accountId']

    def add_space_permissions(self, space_key, subject_type, group_user_name, operation_key, operation_target):
        payload = {
            "subject": {
                "type": subject_type,
                "identifier": group_user_name,
            },
            "operation": {
                "key": operation_key,
                "target": operation_target
            }
        }
        response = requests.post(
            f"{self.url}/wiki/rest/api/space/{space_key}/permission",
            json=payload,
            headers=self.headers,
            auth=self.auth
        )
        try:
            response.raise_for_status()
        except requests.RequestException:
            if "Permission already exists" in response.text:
                # It's okay if user or group already have permission
                return
            raise AtlassianApiError(f"Failed to grant permissions for group - {group_user_name} to space {space_key} with error - {response.text}")
