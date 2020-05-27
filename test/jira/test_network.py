import pytest
import requests

from datetime import datetime
from dateutil.tz import tzutc
from unittest import mock

from jira_analysis.jira.network import (
    INetworkService,
    NetworkService,
    get_issues,
    get_project,
)
from jira_analysis.jira.auth import JiraConfig
from jira_analysis.jira.issue import JiraTicket
from jira_analysis.jira.project import JiraProject


class _MockNetwork(INetworkService):
    def __init__(self, return_values: list):
        self._index = 0
        self.return_values = return_values
        self.assigned_url = None
        self.assigned_auth = None

    def get(self, url, auth):
        self.assigned_url = url
        self.assigned_auth = auth
        value = self.return_values[self._index]
        self._index += 1
        return value

    def check_url(self, url):
        assert self.assigned_url == url

    def check_auth(self, auth):
        assert self.assigned_auth == auth


def mock_network(return_value):
    @pytest.fixture
    def network():
        return _MockNetwork(return_value)

    return network


issue_network = mock_network(
    [
        {
            "maxResults": 50,
            "total": 1,
            "issues": [
                {
                    "key": "KEY-123",
                    "fields": {
                        "created": "2020-01-10T09:01:10.000000",
                        "updated": "2020-01-30T15:01:05.000000",
                        "status": {"name": "Done"},
                        "description": {"type": "doc", "content": []},
                    },
                    "changelog": {"histories": []},
                }
            ],
        }
    ]
)

project_network = mock_network([{"id": 10, "key": "PROJ"}])

multiple_page_issues = mock_network(
    [
        {
            "maxResults": 1,
            "total": 2,
            "issues": [
                {
                    "key": "KEY-123",
                    "fields": {
                        "created": "2020-01-10T09:01:10.000000",
                        "updated": "2020-01-30T15:01:05.000000",
                        "status": {"name": "Done"},
                        "description": {"type": "doc", "content": []},
                    },
                    "changelog": {"histories": []},
                }
            ],
        },
        {
            "maxResults": 1,
            "total": 2,
            "issues": [
                {
                    "key": "KEY-456",
                    "fields": {
                        "created": "2020-01-20T09:01:10.000000",
                        "updated": "2020-02-10T15:01:05.000000",
                        "status": {"name": "To do"},
                        "description": {"type": "doc", "content": []},
                    },
                    "changelog": {"histories": []},
                }
            ],
        },
    ]
)


@pytest.fixture
def jira_project():
    return JiraProject(key="PROJ", id=10)


@pytest.fixture
def auth():
    return JiraConfig(email="test@example.com", token="123")


@pytest.fixture
def jira_ticket_key_123():
    return JiraTicket(
        key="KEY-123",
        created=datetime(2020, 1, 10, 9, 1, 10, tzinfo=tzutc()),
        updated=datetime(2020, 1, 30, 15, 1, 5, tzinfo=tzutc()),
        description="",
        status="Done",
        changelog=[],
    )


@pytest.fixture
def jira_ticket_key_456():
    return JiraTicket(
        key="KEY-456",
        created=datetime(2020, 1, 20, 9, 1, 10, tzinfo=tzutc()),
        updated=datetime(2020, 2, 10, 15, 1, 5, tzinfo=tzutc()),
        description="",
        status="To do",
        changelog=[],
    )


@pytest.fixture
def network_service():
    ns = NetworkService()

    network_response = mock.Mock()
    network_response.json.return_value = {}
    ns.requests = mock.Mock(spec_set=requests)
    ns.requests.get.return_value = network_response
    return ns


def test_get_issues(jira_project, jira_ticket_key_123, auth, issue_network):
    issues = get_issues(auth, jira_project, issue_network)
    assert issues == [jira_ticket_key_123]


def test_get_issues_uses_correct_endpoint(jira_project, auth, issue_network):
    get_issues(auth, jira_project, issue_network)

    issue_network.check_url(
        "https://hotjar.atlassian.net/rest/api/3/search?jql=project%3DPROJ&expand=changelog"
    )


def test_get_issues_multiple_pages(
    jira_project, jira_ticket_key_123, jira_ticket_key_456, auth, multiple_page_issues
):
    issues = get_issues(auth, jira_project, multiple_page_issues)
    assert issues == [jira_ticket_key_123, jira_ticket_key_456]


def test_get_issues_uses_auth(auth, project_network):
    get_project(auth, "PROJ", project_network)
    project_network.check_auth(auth)


def test_get_project(jira_project, auth, project_network):
    project = get_project(auth, "PROJ", project_network)
    assert project == jira_project


def test_get_project_uses_correct_endpoint(auth, project_network):
    get_project(auth, "PROJ", project_network)
    project_network.check_url("https://hotjar.atlassian.net/rest/api/3/project/PROJ")


def get_project_uses_auth(auth, project_network):
    get_project(auth, "PROJ", project_network)
    project_network.check_auth(auth)


def test_network_service_get(auth, network_service):
    assert network_service.get("https://example.com", auth) == {}


def test_network_service_get_calls_underlying_get(auth, network_service):
    network_service.get("https://example.com", auth)
    network_service.requests.get.assert_called_once_with(
        "https://example.com", auth=(auth.email, auth.token)
    )
