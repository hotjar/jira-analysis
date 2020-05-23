import attr

from bokeh.models.sources import DataSource
from collections import Counter
from datetime import date
from numpy import busday_count
from operator import attrgetter
from typing import Dict, List, Type, TypeVar

from jira_analysis.analysis.issue import Issue

from .base import BaseDataConverter


@attr.s(frozen=True)
class CycleTime:
    issue: str = attr.ib()
    completed: date = attr.ib()
    cycle_time: float = attr.ib()


@attr.s
class CycleTimeDataSource(BaseDataConverter):

    cycle_times: List[CycleTime] = attr.ib()

    def to_data_source(self, data_source: Type[DataSource]) -> DataSource:
        sorted_cycle_times = list(sorted(self.cycle_times, key=attrgetter("completed")))

        keys, completions, cycle_times = list(
            zip(*(attr.astuple(sct) for sct in sorted_cycle_times))
        )

        completion_cycle_times = list(zip(completions, cycle_times))
        cycle_time_heatmap = Counter(completion_cycle_times)

        return data_source(
            {
                "x": completions,
                "y": cycle_times,
                "sizes": [
                    cycle_time_heatmap[(c, t)] * 3 + 2
                    for c, t in completion_cycle_times
                ],
                "label": keys,
            }
        )


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
        cycle_time=busday_count(issue.started.date(), issue.completed.date()),
    )


class IssueNotComplete(Exception):
    """The given ticket is not complete.
    """

    def __init__(self, issue: Issue):
        self.issue = Issue
        message = f"Incomplete issue: {issue.key}"
        super().__init__(message)
