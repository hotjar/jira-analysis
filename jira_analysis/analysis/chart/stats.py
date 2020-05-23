from datetime import date
from numpy import busday_count, mean, std
from toolz import itertoolz as it
from typing import List, Optional

from jira_analysis.analysis.issue import Issue


def cycle_time(start: date, end: date) -> float:
    return busday_count(start, end)


def rolling_average_cycle_time(cycle_times: List[int]) -> List[float]:
    cycle_window = [mean(window) for window in it.sliding_window(5, cycle_times)]
    return ([cycle_window[0]] * 2) + cycle_window + (cycle_window[-1] * 2)


def standard_deviations(cycle_times: List[int]) -> List[float]:
    std_deviation_window = [std(window) for window in it.sliding_window(5, cycle_times)]
    return (
        ([std_deviation_window[0]] * 2)
        + std_deviation_window
        + ([std_deviation_window[-1]] * 2)
    )
