import pytest

from datetime import date
from unittest import mock

from jira_analysis.analysis.cycle_time import CycleTime
from jira_analysis.analysis.chart.cycle_time.scatter import CycleTimeScatterPlot

from .helpers import chart


@pytest.fixture
def sorted_completions():
    return (
        date(2019, 12, 3),
        date(2020, 1, 1),
        date(2020, 4, 30),
        date(2020, 5, 1),
        date(2020, 5, 1),
        date(2020, 10, 1),
    )


@pytest.fixture
def cycle_times():
    return (
        2,
        4,
        10,
        3,
        3,
        1,
    )


@pytest.fixture
def keys():
    return (
        "PROJ-12",
        "PROJ-1",
        "PROJ-414",
        "PROJ-123",
        "PROJ-456",
        "PROJ-41",
    )


@pytest.fixture
def cycle_time_scatter_plot():
    return CycleTimeScatterPlot(
        cycle_times=[
            CycleTime(issue="PROJ-123", completed=date(2020, 5, 1), cycle_time=3),
            CycleTime(issue="PROJ-456", completed=date(2020, 5, 1), cycle_time=3),
            CycleTime(issue="PROJ-1", completed=date(2020, 1, 1), cycle_time=4),
            CycleTime(issue="PROJ-41", completed=date(2020, 10, 1), cycle_time=1),
            CycleTime(issue="PROJ-12", completed=date(2019, 12, 3), cycle_time=2),
            CycleTime(issue="PROJ-414", completed=date(2020, 4, 30), cycle_time=10),
        ],
        data_source=mock.Mock(),
    )


def test_to_data_source(cycle_time_scatter_plot, cycle_times, sorted_completions, keys):
    cycle_time_scatter_plot.to_data_source()
    cycle_time_scatter_plot.data_source.assert_called_once_with(
        {
            "x": sorted_completions,
            "y": cycle_times,
            "sizes": [5, 5, 5, 8, 8, 5],
            "label": keys,
        }
    )


def test_draw(cycle_time_scatter_plot, chart):
    cycle_time_scatter_plot.draw(chart)
    chart.scatter.assert_called_once_with(
        "x",
        "y",
        marker="circle",
        source=cycle_time_scatter_plot.to_data_source(),
        size="sizes",
    )

