import pytest
from datetime import datetime, date

from jira_analysis.cycle_time.cycle_time import (
    CycleTime,
    IssueNotComplete,
    get_cycle_time,
)
from jira_analysis.cycle_time.issue import Issue


@pytest.fixture
def cycle_time():
    return CycleTime(issue="PROJ-123", completed=date(2020, 4, 6), cycle_time=2)


@pytest.fixture
def complete_issue():
    return Issue(
        key="PROJ-123",
        created=datetime(2020, 3, 1, 1, 4, 1),
        completed=datetime(2020, 4, 6, 12, 0, 12),
        started=datetime(2020, 4, 2, 12, 0, 12),
        status="Done",
    )


@pytest.fixture
def incomplete_issue():
    return Issue(
        key="PROJ-123",
        created=datetime(2020, 3, 1, 1, 4, 1),
        completed=None,
        started=datetime(2020, 4, 2, 12, 0, 12),
        status="In progress",
    )


def test_get_cycle_time(cycle_time, complete_issue):
    assert get_cycle_time(complete_issue) == cycle_time


def test_get_cycle_time_issue_not_complete(incomplete_issue):
    with pytest.raises(IssueNotComplete) as exc:
        get_cycle_time(incomplete_issue)

    assert exc.value.issue == incomplete_issue
