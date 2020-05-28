import pytest

from unittest import mock

from jira_analysis.analysis.chart.base import IChart


class _MockChart(IChart):
    def __init__(self):
        self._scatter = mock.Mock()
        self._line = mock.Mock()
        self._glyph = mock.Mock()

    def render(self) -> None:
        pass

    @property
    def scatter(self):
        return self._scatter

    @property
    def line(self):
        return self._line

    @property
    def glyph(self):
        return self._glyph


@pytest.fixture
def chart():
    return _MockChart()
