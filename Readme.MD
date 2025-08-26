# Atlassian Project & Space Automation

This script automates the creation of **Jira projects** and **Confluence spaces** in Atlassian Cloud using REST API.  
It can be executed locally or triggered in CI/CD pipelines.

## Features

- Create a Jira project with key, name, and project type.
- Create a Confluence space (public or private) with an assigned owner.
- Assign default permissions:
  - Public spaces → default Confluence group.
  - Full permissions → space owner and admin group.
- Logging of all steps and API errors.

## Requirements

- Python 3.10+
- API Token for authentication.
- Dependencies:
  - `python-dotenv`
  - `requests`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
To run a script locally you need to set ENV variables, otherwise use Workflow
```
JIRA_URL=https://xxx.atlassian.net
ATLASSIAN_USERNAME=some_email@example.com
ATLASSIAN_TOKEN=TOKEN_FROM_YOUR_ATLASSIAN_PROFILE
PROJECT_KEY=TEST
PROJECT_NAME=Project Test Name
PROJECT_TYPE=software or business
TARGET=jira or confluence
SPACE_KEY=TEST
SPACE_NAME=Test Space
OWNER=some_email@example.com
VISIBILITY=private or public
```