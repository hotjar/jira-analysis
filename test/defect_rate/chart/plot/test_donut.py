import pytest
from datetime import date
from math import pi
from unittest.mock import Mock

from jira_analysis.defect_rate.chart.plot.donut import DefectRateDonut
from jira_analysis.defect_rate.issue import Issue

from test.defect_rate.fixtures import issue
from test.defect_rate.chart.fixtures import chart


@pytest.fixture
def defect_rate_donut(issue):
    fake_data_source = Mock()
    fake_data_source.side_effect = lambda x: x
    return DefectRateDonut(
        issues=[issue, Issue(key="PROJ-121", completed=date(2020, 3, 30), defects=[])],
        data_source=fake_data_source,
        no_defects_transform=Mock(),
        defects_transform=Mock(),
    )


def test_to_data_source(defect_rate_donut):
    assert defect_rate_donut.to_data_source() == {
        "issues": [2, 1],
        "defect_rate": [0.5, 0.5],
        "value": ["Issues", "Defect Rate"],
        "angle": [0.5 * pi, 0.5 * pi],
        "color": ["green", "red"],
    }


def test_draw(chart, defect_rate_donut):
    defect_rate_donut.draw(chart)
    chart.wedge.assert_called_once_with(
        x=0,
        y=0,
        inner_radius=0.65,
        outer_radius=0.95,
        start_angle=defect_rate_donut.no_defects_transform.return_value,
        end_angle=defect_rate_donut.defects_transform.return_value,
        line_color="white",
        fill_color="color",
        legend_field="value",
        source=defect_rate_donut.to_data_source(),
    )
    defect_rate_donut.no_defects_transform.assert_called_once_with("angle")
    defect_rate_donut.defects_transform.assert_called_once_with("angle")
