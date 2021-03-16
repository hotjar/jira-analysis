from dataclasses import dataclass
from datetime import date

from jira_analysis.config.config import Config

from .exceptions import IssueNotComplete


@dataclass(frozen=True)
class Issue:
    key: str
    completed: date


def create_issue_with_config(
    key: str, completed: date, status: str, config: Config
) -> Issue:
    """Create an issue from the given key and completed date.

    The config is used to determine if the issue is complete. If the issue
    is not complete, this raises an exception.

    :param key: The issue key.
    :param completed: The date the issue was completed.
    :param config: The config.
    :return: The new issue.
    :raises IssueNotComplete: If the given status is not a completed status.
    """
    if not config.is_completed_status(status) or completed is None:
        raise IssueNotComplete(key, status)
    return Issue(key=key, completed=completed)
