from abc import ABC, abstractmethod
import requests
from typing import List
from urllib.parse import urlencode, urljoin

from .auth import JiraConfig
from .issue import JiraTicket, parse_jira_ticket
from .project import JiraProject, parse_jira_project

_JIRA_URL_BASE = "https://hotjar.atlassian.net/rest/api/3/"


class INetworkService(ABC):
    @abstractmethod
    def get(self, url: str, auth: JiraConfig) -> dict:
        pass


class NetworkService(INetworkService):
    requests = requests

    def get(self, url: str, auth: JiraConfig) -> dict:
        return self.requests.get(url, auth=(auth.email, auth.token)).json()


_DEFAULT_NETWORK = NetworkService()


def get_issues(
    config: JiraConfig,
    project: JiraProject,
    network: INetworkService = _DEFAULT_NETWORK,
) -> List[JiraTicket]:
    issues = []
    jira_url = urljoin(
        config.jira_url
        if config.jira_url.startswith("http")
        else f"https://{config.jira_url}",
        "rest/api/3/search",
    )
    query = urlencode({"jql": "project={}".format(project.key), "expand": "changelog"})
    response = network.get("{}?{}".format(jira_url, query), auth=config)
    page_size, total = (
        response["maxResults"],
        response["total"],
    )
    if page_size > total:
        page_size = total
    issues.extend([parse_jira_ticket(t) for t in response["issues"]])

    for start in range(page_size, total, page_size):
        query = urlencode(
            {
                "jql": "project={}".format(project.key),
                "expand": "changelog",
                "startAt": start,
            }
        )
        response = network.get("{}?{}".format(jira_url, query), auth=config)
        issues.extend([parse_jira_ticket(t) for t in response["issues"]])
    return issues


def get_project(
    config: JiraConfig, key: str, network: INetworkService = _DEFAULT_NETWORK
) -> JiraProject:
    response = network.get(urljoin(_JIRA_URL_BASE, f"project/{key}"), auth=config)
    return parse_jira_project(response)
