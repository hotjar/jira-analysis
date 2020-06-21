import pytest

from unittest import mock

from jira_analysis.chart.base import Axis, Chart


@pytest.fixture
def chart_constructor():
    create_chart = mock.Mock()
    render = mock.Mock()
    return (
        Chart(
            x=Axis(label="X", values=[1, 2, 3], size=1000),
            y=Axis(label="Y", values=[1, 2, 6], size=800),
            label="Test",
            create_chart=create_chart,
            render=render,
            tooltips="Tooltip",
        ),
        create_chart,
        render,
    )


def test_chart_construct(chart_constructor):
    _, create_chart, _ = chart_constructor
    create_chart.assert_called_once_with(
        plot_width=1000,
        plot_height=800,
        x_range=[1, 2, 3],
        y_range=[1, 2, 6],
        tooltips="Tooltip",
    )
    assert create_chart.return_value.xaxis.axis_label == "X"
    assert create_chart.return_value.xaxis.major_label_orientation == "vertical"
    assert create_chart.return_value.yaxis.axis_label == "Y"
    assert create_chart.return_value.y_range.start == 0


def test_chart_render(chart_constructor):
    chart, create_chart, render = chart_constructor
    chart.render()
    render.assert_called_once_with(create_chart.return_value)


def test_chart_line(chart_constructor):
    chart, create_chart, _ = chart_constructor
    assert chart.line == create_chart.return_value.line


def test_chart_scatter(chart_constructor):
    chart, create_chart, _ = chart_constructor
    assert chart.scatter == create_chart.return_value.scatter


def test_chart_glyph(chart_constructor):
    chart, create_chart, _ = chart_constructor
    assert chart.glyph == create_chart.return_value.add_glyph
