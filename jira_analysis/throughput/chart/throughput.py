from collections import OrderedDict
from datetime import date
from typing import List, Type

from toolz.itertoolz import pluck

from jira_analysis.chart.base import Axis, IChart, Chart

from jira_analysis.throughput.issue import Issue
from jira_analysis.throughput.stats import group_issues_by_week_commence

from .exceptions import NoTicketsProvided
from .plots.throughput import ThroughputPlot


def generate_throughput_chart(
    issues: List[Issue], chart_class: Type[IChart] = Chart
) -> None:
    """Generate a throughput bar chart for the given list of issues.

    :param issues: The list of issues to calculate the weekly throughput for.
    :param chart: The chart_class to draw on, defaults to Chart
    :raises NoTicketsProvided: If the list of issues is empty.
    """
    if not issues:
        raise NoTicketsProvided

    grouped_issues = group_issues_by_week_commence(issues)
    throughputs: OrderedDict[date, int] = OrderedDict(
        ((wc, len(completed)) for (wc, completed) in grouped_issues.items())
    )

    throughput_plot = ThroughputPlot(
        weeks=list(throughputs.keys()), throughputs=list(throughputs.values())
    )

    chart = chart_class(
        x=Axis(
            label="Week Start",
            values=[d.strftime("%d/%m/%Y") for d in throughput_plot.weeks],
            size=1500,
        ),
        y=Axis(
            label="Issues Completed",
            values=None,
            size=800,
        ),
        label="Throughput by week",
        tooltips=[
            ("Week", "@x"),
            ("Issues Completed", "@y"),
        ],
    )

    throughput_plot.draw(chart)

    chart.render()
