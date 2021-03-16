import pytest
from datetime import date


from jira_analysis.throughput.issue import Issue, create_issue_with_config
from jira_analysis.throughput.exceptions import IssueNotComplete

from .helpers import get_config


@pytest.fixture
def config():
    return get_config()


@pytest.mark.parametrize(
    "key, completed, status",
    (pytest.param("PROJ-123", date(2021, 1, 13), "Done", id="completed-issue"),),
)
def test_create_issue_with_config(key, completed, status, config):
    assert create_issue_with_config(
        key=key, completed=completed, status=status, config=config
    ) == Issue(key=key, completed=completed)


@pytest.mark.parametrize(
    "key, completed, status",
    (
        pytest.param("PROJ-123", date(2021, 1, 12), "To do", id="not-completed-status"),
        pytest.param("PROJ-123", None, "Done", id="completed-is-none"),
    ),
)
def test_create_issue_errors(key, completed, status, config):
    with pytest.raises(IssueNotComplete):
        create_issue_with_config(
            key=key, completed=completed, status=status, config=config
        )
