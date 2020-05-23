import attr

from datetime import date

from .issue import Issue
from .stats import cycle_time


@attr.s(frozen=True)
class CycleTime:
    issue: str = attr.ib()
    completed: date = attr.ib()
    cycle_time: float = attr.ib()


def get_cycle_time(issue: Issue) -> CycleTime:
    """Return a CycleTime for a given Issue.

    :param issue: Issue to convert. Both started and completed must be set.
    :raises IssueNotComplete: If the issue is not a completed issue.
    :return: The completed CycleTime
    """
    if issue.started is None or issue.completed is None:
        raise IssueNotComplete(issue)

    return CycleTime(
        issue=issue.key,
        completed=issue.completed.date(),
        cycle_time=cycle_time(issue.started.date(), issue.completed.date()),
    )


class IssueNotComplete(Exception):
    """The given ticket is not complete.
    """

    def __init__(self, issue: Issue):
        self.issue = Issue
        message = f"Incomplete issue: {issue.key}"
        super().__init__(message)
