import logging
import os
import sys

from dotenv import load_dotenv

from api.atlassian_api import AtlassianApi, AtlassianApiError
from config import (
    confluence_default_permissions,
    confluence_full_permissions,
    default_confluence_group,
    default_admin_group,
    default_account_lead,
)
from gha_logging import setup_logging


def jira_project_creation():
    # Load required environment variables for Jira
    jira_url = os.getenv("JIRA_URL")
    username = os.getenv("ATLASSIAN_USERNAME")
    token = os.getenv("ATLASSIAN_TOKEN")
    project_key = os.getenv("PROJECT_KEY")
    project_name = os.getenv("PROJECT_NAME")
    project_type = os.getenv("PROJECT_TYPE")

    # Initialize API client
    jira = AtlassianApi(jira_url, username, token)

    # Define project creation payload
    payload = {
        "assigneeType": "PROJECT_LEAD",
        "key": project_key,
        "leadAccountId": default_account_lead,  # fixed accountId of the project lead
        "name": project_name,
        "projectTypeKey": project_type,
    }

    try:
        logging.info(
            f"Creating project {project_key} with following payload - {payload}"
        )
        jira.create_project(payload)
        logging.info(f"Project successfully created {jira_url}/browse/{project_key} ")
    except AtlassianApiError as e:
        logging.error(e)
        sys.exit(2)  # Exit with non-zero code to fail CI/CD pipeline


def confluence_space_creation():
    # Load required environment variables for Confluence
    jira_url = os.getenv(
        "JIRA_URL"
    )  # same URL used for Jira and Confluence (cloud base URL)
    username = os.getenv("ATLASSIAN_USERNAME")
    token = os.getenv("ATLASSIAN_TOKEN")
    space_key = os.getenv("SPACE_KEY")
    space_name = os.getenv("SPACE_NAME")
    visibility = os.getenv("VISIBILITY")
    owner = os.getenv("OWNER")

    # Private flag depends on VISIBILITY
    private = visibility == "private"

    # Initialize API client
    confluence = AtlassianApi(jira_url, username, token)

    # Define space creation payload
    payload = {
        "name": space_name,
        "key": space_key,
    }

    try:
        # Resolve accountId of the owner (username/email → Atlassian accountId)
        owner_account_id = confluence.get_account_id(owner)
        payload["ownerId"] = owner_account_id

        logging.info(f"Creating space {space_key} with following payload - {payload}")
        confluence.create_space(payload, private)
        logging.info(
            f"Project successfully created {jira_url}/wiki/spaces/{space_key}/overview"
        )

        # Assign default group permissions if space is not private
        if not private:
            for permission in confluence_default_permissions:
                permission_key, permission_target = permission
                confluence.add_space_permissions(
                    space_key,
                    "group",
                    default_confluence_group,
                    permission_key,
                    permission_target,
                )
            logging.info(
                f"Permission for public group - {confluence_default_permissions} granted"
            )

        # Grant full permissions to owner and admin group
        for permission in confluence_full_permissions:
            permission_key, permission_target = permission
            confluence.add_space_permissions(
                space_key, "user", owner_account_id, permission_key, permission_target
            )
            confluence.add_space_permissions(
                space_key,
                "group",
                default_admin_group,
                permission_key,
                permission_target,
            )
        logging.info(
            f"Permission for owner - {owner} and admin group - {default_admin_group} granted"
        )

    except AtlassianApiError as e:
        logging.error(e)
        sys.exit(2)


if __name__ == "__main__":
    # Load .env file values into environment
    load_dotenv()

    # Configure logging format and level
    setup_logging(level=logging.INFO)

    # Select target (jira or confluence) based on environment variable
    target = (os.getenv("TARGET") or "").strip().lower()
    if target == "jira":
        jira_project_creation()
    elif target == "confluence":
        confluence_space_creation()
    else:
        logging.error(f"Unknown target - {target} please choose jira or confluence")
        sys.exit(2)
