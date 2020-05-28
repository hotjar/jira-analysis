import pytest

from unittest import mock

from jira_analysis.analysis.chart.base import Axis, Chart


@pytest.fixture
def chart():
    return Chart(x=Axis(), y=Axis(), label="Test", create_chart=mock.Mock())


def test_chart_render(chart):
    chart.render()
