import pytest

from datetime import datetime

from jira_analysis.cycle_time.issue import Issue
from jira_analysis.conversions.cycle_time import convert_jira_to_cycle_time
from jira_analysis.jira.issue import JiraTicket, StatusChange

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


@pytest.fixture
def analysis_ticket():
    return Issue(
        key="PROJ-123",
        created=datetime(2020, 5, 10, 1, 2, 3),
        completed=datetime(2020, 5, 20, 5, 1, 2),
        started=datetime(2020, 5, 11, 2, 2, 2),
        status="Done",
    )


def test_convert_jira_to_cycle_time(config, jira_ticket, analysis_ticket):
    assert convert_jira_to_cycle_time(config, jira_ticket) == analysis_ticket
