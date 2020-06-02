"""Helper functions for building up charts.
"""
import attr

from datetime import date
from operator import attrgetter
from typing import List, Tuple, cast

from jira_analysis.cycle_time.cycle_time import CycleTime


def sort_cycle_times(cycle_times: List[CycleTime]) -> List[CycleTime]:
    """Return a sorted list of cycle times.

    :param cycle_times: The cycle times to sort by created date.
    :return: The sorted list of cycle times.
    """
    return list(sorted(cycle_times, key=attrgetter("completed")))


def unsplit(
    cycle_times: List[CycleTime],
) -> Tuple[Tuple[str, ...], Tuple[date, ...], Tuple[float, ...]]:
    """Unsplit the cycle times into a tuple of three lists.

    :param cycle_times: The cycle times to split out.
    :return: Three tuples of: ticket_keys, completed_dates, cycle_times
    """
    return cast(
        Tuple[Tuple[str, ...], Tuple[date, ...], Tuple[float, ...]],
        tuple(zip(*(attr.astuple(ct) for ct in cycle_times))),
    )
