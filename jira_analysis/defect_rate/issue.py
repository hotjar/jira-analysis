import attr

from datetime import date, datetime
from typing import List, Tuple

from jira_analysis.config.config import Config


@attr.s(frozen=True)
class Defect:
    key: str = attr.ib()


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    completed: date = attr.ib()
    defects: List[Defect] = attr.ib()


# Aliases to make the below type information more readable
_STATUS_TO = str
_STATUS_CHANGE = Tuple[_STATUS_TO, datetime]
_ISSUE_KEY = str
_ISSUE_TYPE = str
_RELATED_ISSUE = Tuple[_ISSUE_KEY, _ISSUE_TYPE]


def create_issue_with_config(
    config: Config, key, changelog: List[_STATUS_CHANGE], related: List[_RELATED_ISSUE],
) -> Issue:
    try:
        completed = min(t for c, t in changelog if config.is_completed_status(c))
    except ValueError:
        raise IssueNotComplete(key)
    return Issue(
        key=key,
        completed=completed.date(),
        defects=[Defect(key=k) for k, t in related if config.is_defect_type(t)],
    )


class IssueNotComplete(Exception):
    def __init__(self, issue_key: str):
        self.issue_key = issue_key
        super().__init__(f"Issue key {issue_key} is not a completed ticket.")
