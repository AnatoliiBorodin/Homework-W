import logging
import os
import sys

from dotenv import load_dotenv

from api.atlassian_api import AtlassianApi, AtlassianApiError
from config import confluence_default_permissions, confluence_full_permissions, default_confluence_group, \
    default_admin_group
from gha_logging import setup_logging


def jira_project_creation():
    jira_url = os.getenv("JIRA_URL")
    username = os.getenv("ATLASSIAN_USERNAME")
    token = os.getenv("ATLASSIAN_TOKEN")
    project_key = os.getenv("PROJECT_KEY")
    project_name = os.getenv("PROJECT_NAME")
    project_type = os.getenv("PROJECT_TYPE")
    jira = AtlassianApi(jira_url, username, token)
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
    except AtlassianApiError as e:
        logging.error(e)


def confluence_space_creation():
    jira_url = os.getenv("JIRA_URL")
    username = os.getenv("ATLASSIAN_USERNAME")
    token = os.getenv("ATLASSIAN_TOKEN")
    space_key = os.getenv("SPACE_KEY")
    space_name = os.getenv("SPACE_NAME")
    visibility = os.getenv("VISIBILITY")
    owner = os.getenv("OWNER")
    private = False
    if visibility == "private":
        private = True

    confluence = AtlassianApi(jira_url, username, token)
    payload = {
        "name": space_name,
        "key": space_key,
    }

    try:
        owner_account_id = confluence.get_account_id(owner)
        payload["ownerId"] = owner_account_id
        logging.info(f"Creating space {space_key} with following payload - {payload}")
        confluence.create_space(payload, private)
        logging.info(f"Project successfully created {jira_url}/wiki/spaces/{space_key}/overview")

        if not private:
            for permission in confluence_default_permissions:
                permission_key, permission_target = permission
                confluence.add_space_permissions(space_key, "group", default_confluence_group, permission_key,
                                                 permission_target)
            logging.info(f"Permission for public group - {confluence_default_permissions} granted")

        for permission in confluence_full_permissions:
            permission_key, permission_target = permission
            confluence.add_space_permissions(space_key, "user", owner_account_id, permission_key, permission_target)
            confluence.add_space_permissions(space_key, "group", default_admin_group, permission_key,
                                             permission_target)
        logging.info(f"Permission for owner - {owner} and admin group - {default_admin_group} granted")

    except AtlassianApiError as e:
        logging.error(e)


if __name__ == '__main__':
    load_dotenv()
    setup_logging(level=logging.INFO)
    target = (os.getenv("TARGET") or "").strip().lower()
    if target == "jira":
        jira_project_creation()
    elif target == "confluence":
        confluence_space_creation()
    else:
        logging.error(f"Unknown target - {target} please choose jira or confluence")
        sys.exit(2)
