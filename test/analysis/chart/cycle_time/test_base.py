import pytest

from unittest import mock

from jira_analysis.analysis.chart.cycle_time.base import BaseCycleTimeLinePlot

from .helpers import chart


class _ConcreteCycleTimeLinePlot(BaseCycleTimeLinePlot):
    def __init__(self):
        super().__init__(cycle_times=[], data_source=mock.Mock())

    def to_data_source(self):
        return self.data_source()

    @property
    def label(self):
        return "Test"

    @property
    def color(self):
        return "red"

    @property
    def width(self):
        return 1


@pytest.fixture
def line_plot():
    return _ConcreteCycleTimeLinePlot()


def test_draw_calls_data_source(chart, line_plot):
    line_plot.draw(chart)
    line_plot.data_source.assert_called_once_with()


def test_draw_calls_line(chart, line_plot):
    line_plot.draw(chart)
    chart.line.assert_called_once_with(
        "x",
        "y",
        source=line_plot.data_source.return_value,
        line_width=1,
        name="Test",
        color="red",
        alpha=0.9,
    )
