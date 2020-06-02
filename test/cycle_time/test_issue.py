import pytest

from datetime import datetime

from jira_analysis.cycle_time.config import Config
from jira_analysis.cycle_time.issue import Issue, TicketStatus, create_issue_with_config


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In Progress", "Review"},
        analyse_issue_types=None,
    )


def completed_issue():
    return Issue(
        key="PROJ-123",
        created=datetime(2020, 5, 2, 12, 4, 1),
        started=datetime(2020, 5, 10, 9, 1, 0),
        completed=datetime(2020, 5, 16, 14, 10, 30),
        status=TicketStatus.DONE,
    )


def in_progress_issue():
    return Issue(
        key="PROJ-111",
        created=datetime(2020, 5, 2, 12, 4, 1),
        started=datetime(2020, 5, 9, 9, 1, 0),
        completed=None,
        status=TicketStatus.IN_PROGRESS,
    )


def issue_props():
    return [
        {
            "key": "PROJ-123",
            "created": datetime(2020, 5, 2, 12, 4, 1),
            "status": "Done",
            "changelog": [
                ("In Progress", datetime(2020, 5, 10, 9, 1, 0)),
                ("Done", datetime(2020, 5, 16, 14, 10, 30)),
            ],
        },
        {
            "key": "PROJ-111",
            "created": datetime(2020, 5, 2, 12, 4, 1),
            "status": "In Progress",
            "changelog": [("In Progress", datetime(2020, 5, 9, 9, 1, 0)),],
        },
    ]


@pytest.mark.parametrize(
    "issue_props,issue",
    list(zip(issue_props(), [completed_issue(), in_progress_issue()],)),
)
def test_create_issue_with_config(issue_props, issue, config):
    assert create_issue_with_config(config, **issue_props) == issue
