import pytest

from datetime import date, timedelta
from unittest import mock

from jira_analysis.chart.base import IChart
from jira_analysis.throughput.chart.plots.throughput import ThroughputPlot


class _MockChart(IChart):
    def __init__(self):
        self._vbar = mock.Mock()

    def render(self) -> None:
        pass

    @property
    def scatter(self):
        raise AssertionError("Not implemented")

    @property
    def line(self):
        raise AssertionError("Not implemented")

    @property
    def glyph(self):
        raise AssertionError("Not implemented")

    @property
    def wedge(self):
        raise AssertionError("Not implemented")

    @property
    def vertical_bar(self):
        return self._vbar


@pytest.fixture
def chart():
    return _MockChart()


@pytest.fixture
def throughputs():
    return [1, 2, 4, 1, 4, 2]


@pytest.fixture
def weeks(throughputs):
    start_week = date(2021, 1, 4)
    DAYS_IN_WEEK = 7

    return [
        start_week + (i * timedelta(days=DAYS_IN_WEEK))
        for i, _ in enumerate(throughputs)
    ]


def test_render_throughput_plot(chart, throughputs, weeks):
    throughput_plot = ThroughputPlot(
        weeks=weeks, throughputs=throughputs, data_source=mock.Mock()
    )
    throughput_plot.draw(chart)

    chart.vertical_bar.assert_called_once_with(
        x="weeks", top="throughputs", source=throughput_plot.to_data_source(), width=0.9
    )


def test_throughput_plot_to_data_source(throughputs, weeks):
    throughput_plot = ThroughputPlot(
        weeks=weeks, throughputs=throughputs, data_source=mock.Mock()
    )

    throughput_plot.to_data_source()

    throughput_plot.data_source.assert_called_once_with(
        data={
            "weeks": [w.strftime("%d/%m/%Y") for w in weeks],
            "throughputs": throughputs,
        }
    )
