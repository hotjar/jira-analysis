import pytest

from datetime import date
from unittest import mock

from jira_analysis.cycle_time.cycle_time import CycleTime
from jira_analysis.cycle_time.chart.cycle_time.deviation import CycleTimeDeviationPlot

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
def standard_deviations():
    return (
        (
            7.270540018881466,
            7.270540018881466,
            7.270540018881466,
            7.259411708155671,
            7.259411708155671,
            7.259411708155671,
        ),
        (
            1.5294599811185354,
            1.5294599811185354,
            1.5294599811185354,
            1.1405882918443293,
            1.1405882918443293,
            1.1405882918443293,
        ),
    )


@pytest.fixture
def cycle_time_deviation_plot():
    return CycleTimeDeviationPlot(
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


def test_to_data_source(
    cycle_time_deviation_plot, sorted_completions, standard_deviations
):
    upper_deviations, lower_deviations = standard_deviations
    cycle_time_deviation_plot.to_data_source()
    cycle_time_deviation_plot.data_source.assert_called_once_with(
        {"x": sorted_completions, "y1": upper_deviations, "y2": lower_deviations,}
    )


def test_draw(
    cycle_time_deviation_plot, chart, sorted_completions, standard_deviations
):
    upper_deviations, lower_deviations = standard_deviations
    cycle_time_deviation_plot.draw(chart)
    chart.glyph.assert_called_once_with(
        cycle_time_deviation_plot.to_data_source(), mock.ANY
    )
    assert chart.line.call_count == 2
    first_call, second_call = chart.line.call_args_list
    _assert_called(
        first_call,
        "x",
        "y",
        source=mock.ANY,
        line_width=1,
        name="Upper bound",
        color="green",
        alpha=0.3,
    )
    _assert_called(
        second_call,
        "x",
        "y",
        source=mock.ANY,
        line_width=1,
        name="Lower bound",
        color="green",
        alpha=0.3,
    )


def _assert_called(call, *expected_args, **expected_kwargs):
    call_args, call_kwargs = call
    assert call_args == expected_args
    assert call_kwargs == expected_kwargs
