import pytest

from datetime import date

from jira_analysis.analysis.stats import (
    cycle_time,
    padded_sliding_window,
    rolling_average_cycle_time,
    standard_deviations,
)


@pytest.mark.parametrize(
    "start,end,ct",
    [
        (date(2020, 5, 25), date(2020, 5, 27), 2),
        (date(2020, 5, 20), date(2020, 5, 25), 3),  # Run over a weekend
    ],
)
def test_cycle_time(start, end, ct):
    assert cycle_time(start, end) == ct


def test_padded_sliding_window():
    assert padded_sliding_window(sum, [1, 1, 1, 1, 1, 2, 2, 2]) == [
        5,
        5,
        5,
        6,
        7,
        8,
        8,
        8,
    ]


@pytest.mark.parametrize(
    "cycle_times,expected_windows",
    [([1, 1, 1, 1, 1, 5, 5, 5], [1, 1, 1, 1.8, 2.6, 3.4, 3.4, 3.4])],
)
def test_rolling_average_cycle_time(cycle_times, expected_windows):
    assert rolling_average_cycle_time(cycle_times) == expected_windows


@pytest.mark.parametrize(
    "cycle_times,expected_windows",
    [
        (
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
        )
    ],
)
def test_standard_deviations(
    cycle_times, expected_windows
):  # Sanity check as we just pulled the numbers from std
    assert standard_deviations(cycle_times) == expected_windows
