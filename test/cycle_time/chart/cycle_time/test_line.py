import pytest

from datetime import date
from unittest import mock

from jira_analysis.cycle_time.cycle_time import CycleTime
from jira_analysis.cycle_time.chart.cycle_time.line import (
    AverageCycleTimePlot,
    RollingAverageCycleTimePlot,
)

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


def _get_cycle_times():
    return [
        CycleTime(issue="PROJ-123", completed=date(2020, 5, 1), cycle_time=3),
        CycleTime(issue="PROJ-456", completed=date(2020, 5, 1), cycle_time=3),
        CycleTime(issue="PROJ-1", completed=date(2020, 1, 1), cycle_time=4),
        CycleTime(issue="PROJ-41", completed=date(2020, 10, 1), cycle_time=1),
        CycleTime(issue="PROJ-12", completed=date(2019, 12, 3), cycle_time=2),
        CycleTime(issue="PROJ-414", completed=date(2020, 4, 30), cycle_time=10),
    ]


@pytest.fixture
def average_cycle_time_plot():
    return AverageCycleTimePlot(cycle_times=_get_cycle_times(), data_source=mock.Mock())


@pytest.fixture
def rolling_average_cycle_time_plot():
    return RollingAverageCycleTimePlot(
        cycle_times=_get_cycle_times(), data_source=mock.Mock()
    )


def test_average_cycle_time_plot_draw(
    average_cycle_time_plot, chart, sorted_completions
):
    average_cycle_time_plot.draw(chart)
    chart.line.assert_called_once_with(
        "x",
        "y",
        source=average_cycle_time_plot.to_data_source(),
        line_width=1,
        name="Average cycle time (days)",
        color="red",
        alpha=0.9,
    )


def test_average_cycle_time_plot_to_data_source(
    average_cycle_time_plot, sorted_completions
):
    average_cycle_time_plot.to_data_source()
    average_cycle_time_plot.data_source.assert_called_once_with(
        {
            "x": sorted_completions,
            "y": [3.8333333333333335] * 6,
            "label": ["Average cycle time (days)"] * 6,
        }
    )


def test_rolling_average_cycle_time_plot_draw(
    rolling_average_cycle_time_plot, chart, sorted_completions
):
    rolling_average_cycle_time_plot.draw(chart)
    chart.line.assert_called_once_with(
        "x",
        "y",
        source=rolling_average_cycle_time_plot.to_data_source(),
        line_width=3,
        name="Rolling average cycle time (days)",
        color="green",
        alpha=0.9,
    )


def test_rolling_average_cycle_time_plot_to_data_source(
    rolling_average_cycle_time_plot, sorted_completions
):
    rolling_average_cycle_time_plot.to_data_source()
    rolling_average_cycle_time_plot.data_source.assert_called_once_with(
        {
            "x": sorted_completions,
            "y": [4.4, 4.4, 4.4, 4.2, 4.2, 4.2],
            "label": ["Rolling average cycle time (days)"] * 6,
        }
    )
