import attr

from arrow import Arrow
from bokeh.models import VArea
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from collections import Counter
from datetime import date, datetime, timedelta
from enum import Enum
from numpy import busday_count, mean, std
from operator import attrgetter
from typing import List, Optional
from toolz import itertoolz as it

from .issue import Issue


def generate_control_chart(tickets: List[Issue], file_out: str) -> None:
    output_file(file_out)

    completed_tickets = [
        ticket
        for ticket in tickets
        if ticket.completed is not None and ticket.started is not None
    ]
    completed_cycle_times = [
        (ticket.completed, get_cycle_time(ticket))
        for ticket in sorted(completed_tickets, key=attrgetter("completed"))
    ]
    completions, cycle_times = list(zip(*completed_cycle_times))
    completion_dates = [c.date() for c in completions]
    cycle_time_heatmap = Counter(((t.date(), c) for t, c in completed_cycle_times))
    cycle_time_data_source = ColumnDataSource(
        {
            "x": completion_dates,
            "y": cycle_times,
            "sizes": [
                cycle_time_heatmap[(c.date(), t)] * 3 + 2
                for c, t in completed_cycle_times
            ],
        }
    )
    date_span = [
        d[0].date().isoformat()
        for d in Arrow.span_range("day", completions[0], completions[-1])
    ]

    rolling_cycle_times = rolling_average_cycle_time(cycle_times)
    zipped_deviations = zip(rolling_cycle_times, standard_deviations(cycle_times))
    upper_deviation, lower_deviation = list(
        zip(*((ct + sd, ct - sd) for ct, sd in zipped_deviations))
    )

    deviation_source = ColumnDataSource(
        {"x": completion_dates, "y1": upper_deviation, "y2": lower_deviation}
    )

    p = figure(plot_width=1800, plot_height=900, x_range=date_span)
    p.xaxis.axis_label = "Ticket closed (date)"
    p.xaxis.major_label_orientation = "vertical"
    p.yaxis.axis_label = "Cycle time (days)"

    p.scatter("x", "y", marker="circle", source=cycle_time_data_source, size="sizes")
    p.line(
        completion_dates,
        mean(cycle_times),
        line_width=1,
        name="Average cycle time",
        color="red",
        alpha=0.8,
    )
    p.line(
        completion_dates,
        rolling_cycle_times,
        line_width=3,
        name="Cycle time sliding window",
        color="green",
        alpha=0.9,
    )
    p.line(
        completion_dates,
        upper_deviation,
        line_width=1,
        name="Upper bound",
        color="green",
        alpha=0.3,
    )

    p.line(
        completion_dates,
        lower_deviation,
        line_width=1,
        name="Lower bound",
        color="green",
        alpha=0.3,
    )
    deviation_glyph = VArea(x="x", y1="y1", y2="y2", fill_color="green", fill_alpha=0.3)
    p.add_glyph(deviation_source, deviation_glyph)
    show(p)


def get_cycle_time(ticket: Issue) -> Optional[int]:
    if ticket.started is None or ticket.completed is None:
        return None

    return busday_count(ticket.started.date(), ticket.completed.date())


def rolling_average_cycle_time(cycle_times: List[int]) -> List[float]:
    cycle_window = [mean(window) for window in it.sliding_window(5, cycle_times)]
    return ([cycle_window[0]] * 4) + cycle_window


def standard_deviations(cycle_times: List[int]) -> List[float]:
    std_deviation_window = [std(window) for window in it.sliding_window(5, cycle_times)]
    return ([std_deviation_window[0]] * 4) + std_deviation_window
