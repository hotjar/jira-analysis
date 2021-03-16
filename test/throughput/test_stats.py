import pytest
from datetime import date
from collections import OrderedDict
from operator import attrgetter

from jira_analysis.throughput.issue import Issue
from jira_analysis.throughput.stats import group_issues_by_week_commence

from .helpers import get_config


@pytest.fixture
def config():
    return get_config()


@pytest.fixture
def issues():
    return [
        Issue(key="PROJ-123", completed=date(2021, 2, 3)),
        Issue(key="PROJ-422", completed=date(2021, 2, 19)),
        Issue(key="PROJ-41", completed=date(2021, 2, 17)),
        Issue(key="PROJ-111", completed=date(2021, 2, 2)),
        Issue(key="PROJ-91", completed=date(2021, 2, 17)),
    ]


def test_group_issues_by_week_commence(issues):
    sorted_issues = list(sorted(issues, key=attrgetter("completed")))
    group_1 = sorted_issues[:2]
    group_2 = sorted_issues[2:]

    assert group_issues_by_week_commence(issues=issues) == OrderedDict(
        (
            (date(2021, 2, 1), group_1),
            (date(2021, 2, 8), []),
            (date(2021, 2, 15), group_2),
        )
    )
