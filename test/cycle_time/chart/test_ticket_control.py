import pytest

from datetime import datetime
from unittest import mock

from jira_analysis.cycle_time.issue import Issue
from jira_analysis.chart.base import Chart
from jira_analysis.cycle_time.chart.ticket_control import generate_control_chart
from jira_analysis.cycle_time.chart.exceptions import ChartError, NoTicketsProvided


@pytest.fixture
def chart():
    render_func = mock.Mock()

    def get_chart(*args, **kwargs):
        return Chart(*args, **kwargs, render=render_func)

    return get_chart, render_func


@pytest.fixture
def issues():
    return [
        Issue(
            key="PROJ-123",
            created=datetime(2020, 1, 10, 15, 1, 1),
            completed=datetime(2020, 5, 10, 14, 41, 10),
            started=datetime(2020, 4, 30, 9, 10, 11),
            status="Done",
        ),
        Issue(
            key="PROJ-111",
            created=datetime(2020, 1, 10, 15, 1, 1),
            completed=datetime(2020, 5, 10, 14, 41, 10),
            started=datetime(2020, 4, 30, 9, 10, 11),
            status="Done",
        ),
        Issue(
            key="PROJ-4",
            created=datetime(2020, 3, 10, 15, 1, 1),
            completed=datetime(2020, 4, 10, 14, 41, 10),
            started=datetime(2020, 2, 29, 9, 10, 11),
            status="Done",
        ),
        Issue(
            key="PROJ-123",
            created=datetime(2020, 1, 10, 15, 1, 1),
            completed=datetime(2020, 5, 10, 14, 41, 10),
            started=datetime(2020, 4, 30, 9, 10, 11),
            status="Done",
        ),
        Issue(
            key="PROJ-111",
            created=datetime(2020, 1, 10, 15, 1, 1),
            completed=datetime(2020, 5, 10, 14, 41, 10),
            started=datetime(2020, 4, 30, 9, 10, 11),
            status="Done",
        ),
        Issue(
            key="PROJ-4",
            created=datetime(2020, 3, 10, 15, 1, 1),
            completed=datetime(2020, 4, 10, 14, 41, 10),
            started=datetime(2020, 2, 29, 9, 10, 11),
            status="Done",
        ),
    ]


def test_generate_control_chart(issues, chart):
    create_chart, render_func = chart
    generate_control_chart(issues, create_chart)

    assert render_func.call_count == 1


@pytest.mark.parametrize(
    "tickets, exception",
    (
        pytest.param([], NoTicketsProvided, id="no-tickets"),
        pytest.param(
            [
                Issue(
                    key="PROJ-4",
                    created=datetime(2020, 3, 10, 15, 1, 1),
                    completed=None,
                    started=None,
                    status="To Do",
                )
            ],
            ChartError,
            id="no-completed-issues",
        ),
    ),
)
def test_generate_control_chart_errors(tickets, exception, chart):
    create_chart, render_func = chart
    with pytest.raises(exception):
        generate_control_chart(tickets, create_chart)

    assert not render_func.called
