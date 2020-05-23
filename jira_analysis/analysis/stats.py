from numpy import mean, std
from toolz import itertoolz as it
from typing import List, Optional

from .issue import Issue


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
