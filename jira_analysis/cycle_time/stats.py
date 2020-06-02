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
    if len(cycle_times) < 5:
        return [func(cycle_times) for _ in cycle_times]
    window_size = max(int(len(cycle_times) * 0.2), 5)
    if window_size % 2 == 0:
        window_size += 1
    sliding_windows = [
        func(window) for window in it.sliding_window(window_size, cycle_times)
    ]
    subwindow = int(window_size // 2)
    return (
        [sliding_windows[0]] * subwindow
        + sliding_windows
        + [sliding_windows[-1]] * subwindow
    )


rolling_average_cycle_time = partial(padded_sliding_window, mean)
standard_deviations = partial(padded_sliding_window, std)
