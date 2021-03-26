import pytest

from dataclasses import dataclass
from unittest import mock
from typing import Any, List, Type

from jira_analysis.chart.mean import LinePlot

from .helpers import chart


@dataclass
class _ConcreteCycleTimeLinePlot(LinePlot):

    data_points: List[Any]
    data_source: Type[Any]

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
    return _ConcreteCycleTimeLinePlot(data_points=[], data_source=mock.Mock())


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
