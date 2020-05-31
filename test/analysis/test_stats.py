import pytest

from datetime import date

from jira_analysis.analysis.stats import (
    cycle_time,
    padded_sliding_window,
    rolling_average_cycle_time,
    standard_deviations,
)

from .helpers import integers


@pytest.mark.parametrize(
    "start,end,ct",
    [
        (date(2020, 5, 25), date(2020, 5, 27), 2),
        (date(2020, 5, 20), date(2020, 5, 25), 3),  # Run over a weekend
    ],
)
def test_cycle_time(start, end, ct):
    assert cycle_time(start, end) == ct


@pytest.mark.parametrize(
    "test_func,test_input,expected_output",
    [
        (sum, [1, 1, 1, 1, 1, 2, 2, 2, 2, 3], [5, 5, 5, 6, 7, 8, 9, 11, 11, 11]),
        (sum, [1, 2, 3], [6, 6, 6]),
        (sum, [1, 1, 1, 1, 1], [5, 5, 5, 5, 5]),
        (sum, list(integers(num_values=20)), [9, 9] + [9, 11, 10] * 5 + [9] * 3),
        (
            sum,
            list(integers(end=5, num_values=30)),
            [18] * 3 + [18, 20, 22, 24, 21] * 4 + [18, 20, 22] + [24] * 4,
        ),
    ],
)
def test_padded_sliding_window(test_func, test_input, expected_output):
    assert padded_sliding_window(test_func, test_input) == expected_output


@pytest.mark.parametrize(
    "test_func,cycle_times,expected_windows",
    [
        (
            rolling_average_cycle_time,
            [1, 1, 1, 1, 1, 5, 5, 5],
            [1, 1, 1, 1.8, 2.6, 3.4, 3.4, 3.4],
        ),
        (
            standard_deviations,
            [1, 1, 1, 1, 1, 5, 5, 5],
            [
                0.0,
                0.0,
                0.0,
                1.6,
                1.9595917942265426,
                1.9595917942265426,
                1.9595917942265426,
                1.9595917942265426,
            ],
        ),
    ],
)
def test_specific_padding_funcs(test_func, cycle_times, expected_windows):
    assert test_func(cycle_times) == expected_windows
