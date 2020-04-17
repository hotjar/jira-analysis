import attr
import requests

from jira.auth import get_config
from jira.issue import Changelog, JiraTicket


def get_issue(key: str) -> JiraTicket:
    config = get_config("./credentials.yaml")
    response = requests.get(
        "https://hotjar.atlassian.net/rest/api/3/issue/{key}?expand=changelog".format(
            key=key
        ),
        auth=attr.astuple(config),
    )
    return JiraTicket.from_jira_ticket(response.json())
