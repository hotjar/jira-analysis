import pytest

from unittest import mock

from jira_analysis.chart.base import IChart


class _MockChart(IChart):
    def __init__(self):
        self._wedge = mock.Mock()

    def render(self) -> None:
        pass

    @property
    def glyph(self):
        raise AssertionError("Not implemented")

    @property
    def line(self):
        raise AssertionError("Not implemented")

    @property
    def scatter(self):
        raise AssertionError("Not implemented")

    @property
    def vertical_bar(self):
        raise AssertionError("Not implemented")

    @property
    def wedge(self) -> None:
        return self._wedge


@pytest.fixture
def chart():
    return _MockChart()
