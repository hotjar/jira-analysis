import pytest

from datetime import date
from unittest import mock

from jira_analysis.chart.base import Chart
from jira_analysis.throughput.issue import Issue
from jira_analysis.throughput.chart.exceptions import NoTicketsProvided
from jira_analysis.throughput.chart.throughput import generate_throughput_chart


@pytest.fixture
def chart():
    render_func = mock.Mock()

    def get_chart(*args, **kwargs):
        return Chart(*args, **kwargs, render=render_func)

    return get_chart, render_func


@pytest.fixture
def issues():
    return [
        Issue(key="PROJ-123", completed=date(2021, 2, 1)),
        Issue(key="PROJ-123", completed=date(2021, 2, 3)),
        Issue(key="PROJ-123", completed=date(2021, 2, 3)),
        Issue(key="PROJ-123", completed=date(2021, 2, 10)),
        Issue(key="PROJ-123", completed=date(2021, 2, 10)),
        Issue(key="PROJ-123", completed=date(2021, 2, 11)),
    ]


def test_generate_throughput_chart(issues, chart):
    create_chart, render_func = chart
    generate_throughput_chart(issues, create_chart)

    assert render_func.call_count == 1


@pytest.mark.parametrize(
    "issues, exception", (pytest.param([], NoTicketsProvided, id="no-tickets"),)
)
def test_generate_throughput_chart_errors(issues, exception, chart):
    create_chart, render_func = chart
    with pytest.raises(NoTicketsProvided):
        generate_throughput_chart(issues, create_chart)

    assert not render_func.called
