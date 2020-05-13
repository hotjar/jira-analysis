import attr

from arrow import Arrow
from bokeh.plotting import figure, output_file, show
from datetime import date, datetime, timedelta
from enum import Enum
from numpy import busday_count
from operator import attrgetter
from typing import List, Optional

from .issue import Issue


def generate_control_chart(tickets: List[Issue], file_out: str) -> None:
    output_file(file_out)

    completed_tickets = (
        ticket
        for ticket in tickets
        if ticket.completed is not None and ticket.started is not None
    )
    completed_cycle_times = [
        (ticket.completed, get_cycle_time(ticket))
        for ticket in sorted(completed_tickets, key=attrgetter("completed"))
    ]
    completions, cycle_times = list(zip(*completed_cycle_times))

    p = figure(
        plot_width=1200,
        plot_height=800,
        x_range=[
            d[0].date().isoformat()
            for d in Arrow.span_range("day", completions[0], completions[-1])
        ],
    )
    p.circle(
        [c.date() for c in completions], cycle_times, size=5, color="red", alpha=0.9,
    )
    show(p)


def get_cycle_time(ticket: Issue) -> Optional[int]:
    if ticket.started is None or ticket.completed is None:
        return None

    return busday_count(ticket.started.date(), ticket.completed.date())
