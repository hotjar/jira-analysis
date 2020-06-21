import pytest

from datetime import date, datetime

from jira_analysis.jira.issue import (
    JiraTicket,
    LinkDirection,
    LinkedTicket,
    StatusChange,
)
from jira_analysis.defect_rate.issue import Defect, Issue
from jira_analysis.conversions.defect_rate import convert_jira_to_defect

from .fixtures import config


@pytest.fixture
def jira_ticket():
    return JiraTicket(
        key="PROJ-123",
        created=datetime(2020, 4, 10, 13, 4, 40),
        updated=datetime(2020, 4, 20, 13, 4, 40),
        description="Test description",
        status="Done",
        issue_type="Story",
        changelog=[
            StatusChange(
                created=datetime(2020, 4, 20, 13, 4, 40),
                status_from="To do",
                status_to="Done",
            )
        ],
        related_issues=[
            LinkedTicket(
                key="PROJ-444",
                link_type="Cause",
                link_direction=LinkDirection.OUTBOUND,
                issue_type="Bug",
            ),
            LinkedTicket(
                key="PROJ-12",
                link_type="Blocked",
                link_direction=LinkDirection.INBOUND,
                issue_type="Story",
            ),
            LinkedTicket(
                key="PROJ-1211",
                link_type="Blocks",
                link_direction=LinkDirection.OUTBOUND,
                issue_type="Story",
            ),
            LinkedTicket(
                key="PROJ-931",
                link_type="Blocks",
                link_direction=LinkDirection.OUTBOUND,
                issue_type="Bug",
            ),
        ],
    )


@pytest.fixture
def defect_issue():
    return Issue(
        key="PROJ-123",
        completed=date(2020, 4, 20),
        defects=[Defect(key="PROJ-444"), Defect(key="PROJ-931")],
    )


def test_convert_jira_to_defect(config, jira_ticket, defect_issue):
    assert convert_jira_to_defect(jira_ticket, config) == defect_issue
