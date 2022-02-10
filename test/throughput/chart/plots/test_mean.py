import pytest

from datetime import date, timedelta
from statistics import mean
from unittest import mock

from jira_analysis.chart.base import IChart
from jira_analysis.throughput.chart.plots.mean import AverageThroughputPlot


class _MockChart(IChart):
    def __init__(self):
        self._line = mock.Mock()

    def render(self) -> None:
        pass

    @property
    def scatter(self):
        raise AssertionError("Not implemented")

    @property
    def line(self):
        return self._line

    @property
    def glyph(self):
        raise AssertionError("Not implemented")

    @property
    def wedge(self):
        raise AssertionError("Not implemented")

    @property
    def vertical_bar(self):
        raise AssertionError("Not implemented")


@pytest.fixture
def chart():
    return _MockChart()


@pytest.fixture
def throughputs():
    return [1, 2, 4, 1, 4, 2]


@pytest.fixture
def mean_throughput(throughputs):
    return mean(throughputs)


@pytest.fixture
def weeks(throughputs):
    start_week = date(2021, 1, 4)
    DAYS_IN_WEEK = 7

    return [
        start_week + (i * timedelta(days=DAYS_IN_WEEK))
        for i, _ in enumerate(throughputs)
    ]


def test_render_throughput_plot(chart, throughputs, weeks):
    throughput_plot = AverageThroughputPlot(
        data_points=list(zip(weeks, throughputs)), data_source=mock.Mock()
    )
    throughput_plot.draw(chart)

    chart.line.assert_called_once_with(
        "x",
        "y",
        source=throughput_plot.to_data_source(),
        line_width=throughput_plot.width,
        name=throughput_plot.label,
        color=throughput_plot.color,
        alpha=throughput_plot.alpha,
    )


def test_throughput_plot_to_data_source(throughputs, weeks, mean_throughput):
    throughput_plot = AverageThroughputPlot(
        data_points=list(zip(weeks, throughputs)), data_source=mock.Mock()
    )

    throughput_plot.to_data_source()

    throughput_plot.data_source.assert_called_once_with(
        {
            "x": [w.strftime("%d/%m/%Y") for w in weeks],
            "y": [mean_throughput] * len(throughputs),
            'label': [throughput_plot.label] * len(throughputs)
        }
    )
