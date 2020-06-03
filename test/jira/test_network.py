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
from jira_analysis.jira.issue import JiraTicket, StatusChange

from .fixtures import jira_config, jira_project, jira_ticket  # flake8: ignore


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


def mock_network(return_value, asfixture=True):
    def network():
        return _MockNetwork(return_value)

    return pytest.fixture(network) if asfixture else network


_issues_for_mock_network = [
    {
        "maxResults": 50,
        "total": 1,
        "issues": [
            {
                "key": "PROJ-123",
                "fields": {
                    "created": "2020-01-10T09:01:10.000000",
                    "updated": "2020-01-30T15:01:05.000000",
                    "status": {"name": "Done"},
                    "description": {
                        "type": "doc",
                        "content": [{"type": "text", "text": "Test description"}],
                    },
                    "issuetype": {"name": "Story"},
                    "issuelinks": [],
                },
                "changelog": {"histories": []},
            }
        ],
    }
]

issue_network = mock_network(_issues_for_mock_network)
issue_network_direct = mock_network(_issues_for_mock_network, asfixture=False)

project_network = mock_network([{"id": 10, "key": "PROJ"}])

multiple_page_issues = mock_network(
    [
        {
            "maxResults": 1,
            "total": 2,
            "issues": [
                {
                    "key": "PROJ-123",
                    "fields": {
                        "created": "2020-01-10T09:01:10.000000",
                        "updated": "2020-01-30T15:01:05.000000",
                        "status": {"name": "Done"},
                        "description": {
                            "type": "doc",
                            "content": [{"type": "text", "text": "Test description"}],
                        },
                        "issuetype": {"name": "Story"},
                        "issuelinks": [],
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
                    "key": "PROJ-456",
                    "fields": {
                        "created": "2020-01-20T09:01:10.000000",
                        "updated": "2020-02-10T15:01:05.000000",
                        "status": {"name": "To do"},
                        "description": {
                            "type": "doc",
                            "content": [{"type": "text", "text": "Test description"}],
                        },
                        "issuetype": {"name": "Bug"},
                        "issuelinks": [],
                    },
                    "changelog": {"histories": []},
                }
            ],
        },
    ],
    asfixture=False,
)


def get_jira_ticket(asfixture=True, **overrides):
    ticket_attrs = {
        "key": "PROJ-123",
        "created": datetime(2020, 1, 10, 9, 1, 10, tzinfo=tzutc()),
        "updated": datetime(2020, 1, 30, 15, 1, 5, tzinfo=tzutc()),
        "description": "Test description",
        "issue_type": "Story",
        "status": "Done",
        "changelog": [
            {
                "status_from": "To do",
                "status_to": "Done",
                "created": datetime(2020, 1, 30, 15, 1, 5, tzinfo=tzutc()),
            }
        ],
        "related_issues": [],
    }
    ticket_attrs.update(overrides)

    def inner():
        statuses = [StatusChange(**c) for c in ticket_attrs.pop("changelog")]
        return JiraTicket(changelog=statuses, **ticket_attrs)

    return pytest.fixture(inner) if asfixture else inner


jira_ticket_key_123 = get_jira_ticket()
jira_ticket_key_456 = get_jira_ticket(
    key="PROJ-456",
    changelog=[],
    issue_type="Bug",
    updated=datetime(2020, 2, 10, 15, 1, 5, tzinfo=tzutc()),
)


@pytest.fixture
def network_service():
    ns = NetworkService()

    network_response = mock.Mock()
    network_response.json.return_value = {}
    ns.requests = mock.Mock(spec_set=requests)
    ns.requests.get.return_value = network_response
    return ns


@pytest.mark.parametrize(
    "network,expected_output",
    [
        (issue_network_direct(), [get_jira_ticket(changelog=[], asfixture=False)()]),
        (
            multiple_page_issues(),
            [
                get_jira_ticket(asfixture=False, changelog=[])(),
                get_jira_ticket(
                    asfixture=False,
                    key="PROJ-456",
                    changelog=[],
                    issue_type="Bug",
                    created=datetime(2020, 1, 20, 9, 1, 10, tzinfo=tzutc()),
                    updated=datetime(2020, 2, 10, 15, 1, 5, tzinfo=tzutc()),
                    status="To do",
                )(),
            ],
        ),
    ],
)
def test_get_issues(network, expected_output, jira_project, jira_config):
    issues = get_issues(jira_config, jira_project, network)
    assert issues == expected_output


def test_get_issues_uses_correct_endpoint(jira_project, jira_config, issue_network):
    get_issues(jira_config, jira_project, issue_network)

    issue_network.check_url(
        "https://jira.example.com/rest/api/3/search?"
        "jql=project%3DPROJ&expand=changelog"
    )


def test_get_issues_uses_auth(jira_config, project_network):
    get_project(jira_config, "PROJ", project_network)
    project_network.check_auth(jira_config)


def test_get_project(jira_project, jira_config, project_network):
    project = get_project(jira_config, "PROJ", project_network)
    assert project == jira_project


def test_get_project_uses_correct_endpoint(jira_config, project_network):
    get_project(jira_config, "PROJ", project_network)
    project_network.check_url("https://hotjar.atlassian.net/rest/api/3/project/PROJ")


def get_project_uses_auth(jira_config, project_network):
    get_project(jira_config, "PROJ", project_network)
    project_network.check_auth(jira_config)


def test_network_service_get(jira_config, network_service):
    assert network_service.get("https://example.com", jira_config) == {}


def test_network_service_get_calls_underlying_get(jira_config, network_service):
    network_service.get("https://example.com", jira_config)
    network_service.requests.get.assert_called_once_with(
        "https://example.com", auth=(jira_config.email, jira_config.token)
    )
