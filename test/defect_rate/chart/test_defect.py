import pytest
from unittest.mock import Mock

from jira_analysis.chart.base import Chart
from jira_analysis.defect_rate.chart.defect import generate_defect_chart

from test.defect_rate.fixtures import issue


@pytest.fixture
def chart():
    render_func = Mock()

    def get_chart(*args, **kwargs):
        return Chart(*args, **kwargs, render=render_func)

    return get_chart, render_func


def test_generate_defect_chart(issue, chart):
    chart_class, render_func = chart
    generate_defect_chart([issue], chart_class)

    assert render_func.call_count == 1
