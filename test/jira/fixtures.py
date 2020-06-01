import pytest

from datetime import datetime
from dateutil.tz import tzutc

from jira_analysis.jira.auth import JiraConfig
from jira_analysis.jira.issue import JiraTicket, StatusChange

from jira_analysis.jira.project import JiraProject


@pytest.fixture
def jira_config():
    return JiraConfig(
        email="test@example.com", token="abc123", jira_url="jira.example.com"
    )


@pytest.fixture
def jira_project():
    return JiraProject(key="PROJ", id=10)


@pytest.fixture
def jira_ticket(jira_json):
    return JiraTicket(
        key="PROJ-123",
        created=datetime(2020, 1, 10, 9, 1, 10, tzinfo=tzutc()),
        updated=datetime(2020, 1, 15, 9, 5, 10, tzinfo=tzutc()),
        description="Test description",
        status="Done",
        issue_type="Bug",
        changelog=[
            StatusChange(
                status_from="To do",
                status_to="Done",
                created=datetime(2020, 1, 15, 9, 5, 10, tzinfo=tzutc()),
            )
        ],
    )
