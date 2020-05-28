from datetime import date
from functools import partial
from numpy import busday_count, mean, std
from toolz import itertoolz as it
from typing import Callable, Iterable, List


def cycle_time(start: date, end: date) -> float:
    return busday_count(start, end)


def padded_sliding_window(
    func: Callable[[Iterable[int]], float], cycle_times: List[int]
) -> List[float]:
    sliding_windows = [func(window) for window in it.sliding_window(5, cycle_times)]
    return [sliding_windows[0]] * 2 + sliding_windows + [sliding_windows[-1]] * 2


rolling_average_cycle_time = partial(padded_sliding_window, mean)
standard_deviations = partial(padded_sliding_window, std)
