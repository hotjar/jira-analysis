import pytest

from datetime import date, datetime

from jira_analysis.conversions.throughput import convert_jira_to_throughput
from jira_analysis.jira.issue import JiraTicket, StatusChange
from jira_analysis.throughput.issue import Issue

from .fixtures import config


@pytest.fixture
def jira_ticket():
    return JiraTicket(
        key="PROJ-123",
        created=datetime(2020, 5, 10, 1, 2, 3),
        updated=datetime(2020, 5, 20, 5, 1, 2),
        description="Test issue",
        status="Done",
        issue_type="Story",
        changelog=[
            StatusChange(
                created=datetime(2020, 5, 11, 2, 2, 2),
                status_from="Backlog",
                status_to="In progress",
            ),
            StatusChange(
                created=datetime(2020, 5, 20, 5, 1, 2),
                status_from="In progress",
                status_to="Done",
            ),
        ],
        related_issues=[],
    )


def test_convert_jira_to_throughput(jira_ticket, config):
    assert convert_jira_to_throughput(jira_ticket=jira_ticket, config=config) == Issue(
        key=jira_ticket.key, completed=date(2020, 5, 20)
    )
