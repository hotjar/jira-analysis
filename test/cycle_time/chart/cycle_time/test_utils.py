import pytest

from datetime import date

from jira_analysis.cycle_time.cycle_time import CycleTime
from jira_analysis.cycle_time.chart.cycle_time.utils import sort_cycle_times, unsplit


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        (
            [
                CycleTime(issue="PROJ-123", completed=date(2020, 5, 1), cycle_time=1.2),
                CycleTime(issue="PROJ-555", completed=date(2020, 2, 1), cycle_time=5.1),
            ],
            [
                CycleTime(issue="PROJ-555", completed=date(2020, 2, 1), cycle_time=5.1),
                CycleTime(issue="PROJ-123", completed=date(2020, 5, 1), cycle_time=1.2),
            ],
        )
    ],
)
def test_sort_cycle_times(test_input, expected_output):
    assert sort_cycle_times(test_input) == expected_output


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        (
            [
                CycleTime(issue="PROJ-555", completed=date(2020, 2, 1), cycle_time=5.1),
                CycleTime(issue="PROJ-123", completed=date(2020, 5, 1), cycle_time=1.2),
            ],
            (
                ("PROJ-555", "PROJ-123"),
                (date(2020, 2, 1), date(2020, 5, 1)),
                (5.1, 1.2),
            ),
        )
    ],
)
def test_unsplit(test_input, expected_output):
    assert unsplit(test_input) == expected_output
