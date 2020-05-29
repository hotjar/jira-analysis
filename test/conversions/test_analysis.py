import pytest

from datetime import datetime

from jira_analysis.analysis.config import Config
from jira_analysis.analysis.issue import Issue, TicketStatus
from jira_analysis.conversions.analysis import convert_jira_to_analysis
from jira_analysis.jira.issue import JiraTicket, StatusChange


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In progress"},
        analyse_issue_types=None,
    )


@pytest.fixture
def jira_ticket():
    return JiraTicket(
        key="PROJ-123",
        created=datetime(2020, 5, 10, 1, 2, 3),
        updated=datetime(2020, 5, 20, 5, 1, 2),
        description="Test issue",
        status="Done",
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
    )


@pytest.fixture
def analysis_ticket():
    return Issue(
        key="PROJ-123",
        created=datetime(2020, 5, 10, 1, 2, 3),
        completed=datetime(2020, 5, 20, 5, 1, 2),
        started=datetime(2020, 5, 11, 2, 2, 2),
        status=TicketStatus.DONE,
    )


def test_convert_jira_to_analysis(config, jira_ticket, analysis_ticket):
    assert convert_jira_to_analysis(config, jira_ticket) == analysis_ticket
