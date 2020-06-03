from arrow import Arrow
from bokeh.models.sources import ColumnDataSource
from operator import attrgetter
from typing import List

from jira_analysis.cycle_time.cycle_time import CycleTime, get_cycle_time
from jira_analysis.cycle_time.issue import Issue

from .base import Axis, Chart, IChart
from .cycle_time.deviation import CycleTimeDeviationPlot
from .cycle_time.line import AverageCycleTimePlot, RollingAverageCycleTimePlot
from .cycle_time.scatter import CycleTimeScatterPlot


def generate_control_chart(tickets: List[Issue], chart_class: IChart = Chart) -> None:
    completed_cycle_times: List[CycleTime] = list(
        sorted(
            (
                get_cycle_time(ticket)
                for ticket in tickets
                if ticket.completed is not None and ticket.started is not None
            ),
            key=attrgetter("completed"),
        )
    )
    cycle_time_plot = CycleTimeScatterPlot(
        cycle_times=completed_cycle_times, data_source=ColumnDataSource
    )
    average_cycle_time_plot = AverageCycleTimePlot(
        cycle_times=completed_cycle_times, data_source=ColumnDataSource
    )
    rolling_cycle_time_plot = RollingAverageCycleTimePlot(
        cycle_times=completed_cycle_times, data_source=ColumnDataSource
    )
    cycle_time_deviation_plot = CycleTimeDeviationPlot(
        cycle_times=completed_cycle_times, data_source=ColumnDataSource
    )

    start_date, end_date = (
        completed_cycle_times[0].completed,
        completed_cycle_times[-1].completed,
    )

    chart = chart_class(
        x=Axis(
            label="Closed (date)",
            values=[
                d[0].date().isoformat()
                for d in Arrow.span_range(
                    "day",
                    Arrow(start_date.year, start_date.month, start_date.day),
                    Arrow(end_date.year, end_date.month, end_date.day),
                )
            ],
            size=1800,
        ),
        y=Axis(label="Cycle time (days)", values=None, size=900),
        label="Ticket",
    )
    cycle_time_plot.draw(chart)
    average_cycle_time_plot.draw(chart)
    rolling_cycle_time_plot.draw(chart)
    cycle_time_deviation_plot.draw(chart)

    chart.render()
