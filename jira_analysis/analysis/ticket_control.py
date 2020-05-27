import attr

from arrow import Arrow
from bokeh.models import VArea
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from collections import Counter
from datetime import date
from numpy import mean
from operator import attrgetter
from typing import List

from .chart.cycle_time import CycleTimeDataSource, CycleTimeDeviationDataSource
from .cycle_time import CycleTime, get_cycle_time
from .issue import Issue
from .stats import rolling_average_cycle_time


def generate_control_chart(tickets: List[Issue], file_out: str) -> None:
    output_file(file_out)

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
    completion_dates = [c.completed for c in completed_cycle_times]
    cycle_time_data_source = CycleTimeDataSource(
        cycle_times=completed_cycle_times
    ).to_data_source(ColumnDataSource)

    rolling_cycle_times = rolling_average_cycle_time(
        c.cycle_time for c in completed_cycle_times
    )

    deviation_source = CycleTimeDeviationDataSource(
        cycle_times=completed_cycle_times
    ).to_data_source(ColumnDataSource)

    p = _get_figure(
        completed_cycle_times[0].completed, completed_cycle_times[-1].completed
    )
    p.xaxis.axis_label = "Ticket closed (date)"
    p.xaxis.major_label_orientation = "vertical"
    p.yaxis.axis_label = "Cycle time (days)"
    p.y_range.start = 0

    p.scatter("x", "y", marker="circle", source=cycle_time_data_source, size="sizes")
    cycle_times = [c.cycle_time for c in completed_cycle_times]
    p.line(
        completion_dates,
        [mean(cycle_times) for _ in cycle_times],
        line_width=1,
        name="Average cycle time",
        color="red",
        alpha=0.8,
    )
    p.line(
        completion_dates,
        rolling_cycle_times,
        line_width=3,
        name="Rolling Average Cycle Time",
        color="green",
        alpha=0.9,
    )
    # p.line(
    #     completion_dates,
    #     upper_deviation,
    #     line_width=1,
    #     name="Upper bound",
    #     color="green",
    #     alpha=0.3,
    # )

    # p.line(
    #     completion_dates,
    #     lower_deviation,
    #     line_width=1,
    #     name="Lower bound",
    #     color="green",
    #     alpha=0.3,
    # )
    deviation_glyph = VArea(x="x", y1="y1", y2="y2", fill_color="green", fill_alpha=0.3)
    p.add_glyph(deviation_source, deviation_glyph)
    show(p)


def _get_figure(start_date: date, end_date: date):
    date_span = [
        d[0].date().isoformat()
        for d in Arrow.span_range(
            "day",
            Arrow(start_date.year, start_date.month, start_date.day),
            Arrow(end_date.year, end_date.month, end_date.day),
        )
    ]

    return figure(
        plot_width=1800,
        plot_height=900,
        x_range=date_span,
        tooltips=[("Ticket ID", "@label"), ("Date", "@x"), ("Cycle time", "@y")],
    )
