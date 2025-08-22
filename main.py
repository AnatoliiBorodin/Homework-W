import logging
import os
import sys

from dotenv import load_dotenv

from api.jira_api import JiraApi, ProjectCreateError


def jira_project_creation():
    jira_url = os.getenv("JIRA_URL")
    username = os.getenv("ATLASSIAN_USERNAME")
    token = os.getenv("ATLASSIAN_TOKEN")
    project_key = os.getenv("PROJECT_KEY")
    project_name = os.getenv("PROJECT_NAME")
    project_type = os.getenv("PROJECT_TYPE")
    jira = JiraApi(jira_url, username, token)
    payload = {
        "assigneeType": "PROJECT_LEAD",
        "key": project_key,
        "leadAccountId": "557058:dc9ad4ec-abd5-4fe9-bf2c-1c02693fa1fb",
        "name": project_name,
        "projectTypeKey": project_type,
    }

    try:
        logging.info(f"Creating project {project_key} with following payload - {payload}")
        jira.create_project(payload)
        logging.info(f"Project successfully created {jira_url}/browse/{project_key} ")
    except ProjectCreateError as e:
        logging.error(e)


def confluence_space_creation():
    pass


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    target = (os.getenv("TARGET") or "").strip().lower()
    if target == "jira":
        jira_project_creation()
    elif target == "confluence":
        confluence_space_creation()
    else:
        logging.error(f"Unknown target - {target} please choose jira or confluence")
        sys.exit(2)
