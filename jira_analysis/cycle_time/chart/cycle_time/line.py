from dataclasses import dataclass

from bokeh.models.sources import DataSource
from numpy import mean
from typing import List, Type

from jira_analysis.chart.mean import LinePlot
from jira_analysis.cycle_time.cycle_time import CycleTime
from jira_analysis.cycle_time.stats import rolling_average_cycle_time

from .utils import sort_cycle_times, unsplit


@dataclass(frozen=True)
class AverageCycleTimePlot(LinePlot):

    data_points: List[CycleTime]
    data_source: Type[DataSource]

    def to_data_source(self) -> DataSource:
        sorted_cycle_times = sort_cycle_times(self.data_points)
        _, completions, cycle_times = unsplit(sorted_cycle_times)
        mean_cycle_time = mean(cycle_times)

        return self.data_source(
            {
                "x": completions,
                "y": [mean_cycle_time for _ in cycle_times],
                "label": [self.label for _ in completions],
            }
        )

    @property
    def label(self) -> str:
        return "Average cycle time (days)"

    @property
    def color(self) -> str:
        return "red"

    @property
    def width(self) -> int:
        return 1


@dataclass(frozen=True)
class RollingAverageCycleTimePlot(LinePlot):

    data_points: List[CycleTime]
    data_source: Type[DataSource]

    def to_data_source(self) -> DataSource:
        sorted_cycle_times = sort_cycle_times(self.data_points)
        _, completions, cycle_times = unsplit(sorted_cycle_times)

        return self.data_source(
            {
                "x": completions,
                "y": rolling_average_cycle_time(cycle_times),
                "label": [self.label for _ in completions],
            }
        )

    @property
    def label(self) -> str:
        return "Rolling average cycle time (days)"

    @property
    def color(self) -> str:
        return "green"

    @property
    def width(self) -> int:
        return 3
