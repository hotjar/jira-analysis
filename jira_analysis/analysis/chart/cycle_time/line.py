import attr

from datetime import date
from numpy import mean
from typing import List, Tuple, cast

from jira_analysis.analysis.chart.base import IChart, Plot
from jira_analysis.analysis.cycle_time import CycleTime
from jira_analysis.analysis.stats import rolling_average_cycle_time

from .utils import sort_cycle_times, unsplit


@attr.s(frozen=True)
class AverageCycleTimePlot(Plot):

    cycle_times: List[CycleTime] = attr.ib()

    def draw(self, chart: IChart) -> None:
        sorted_cycle_times = sort_cycle_times(self.cycle_times)
        _, completed_dates, cycle_times = unsplit(sorted_cycle_times)

        chart.line(
            completed_dates,
            [mean(cycle_times) for _ in cycle_times],
            line_width=1,
            name="Average cycle time (days)",
            color="red",
            alpha=0.9,
        )


@attr.s(frozen=True)
class RollingAverageCycleTimePlot(Plot):

    cycle_times: List[CycleTime] = attr.ib()

    def draw(self, chart: IChart) -> None:
        sorted_cycle_times = sort_cycle_times(self.cycle_times)
        _, completed_dates, cycle_times = unsplit(sorted_cycle_times)

        chart.line(
            completed_dates,
            rolling_average_cycle_time(cycle_times),
            line_width=3,
            name="Rolling average cycle time (days)",
            color="green",
            alpha=0.9,
        )
