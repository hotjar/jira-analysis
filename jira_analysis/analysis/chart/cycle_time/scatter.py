import attr

from bokeh.models.sources import DataSource
from collections import Counter
from datetime import date
from operator import attrgetter
from typing import Dict, List, Optional, Tuple, Type, cast

from jira_analysis.analysis.cycle_time import CycleTime
from jira_analysis.analysis.stats import rolling_average_cycle_time, standard_deviations

from jira_analysis.analysis.chart.base import IChart, Plot


@attr.s(frozen=True)
class CycleTimeScatterPlot(Plot):

    cycle_times: List[CycleTime] = attr.ib()
    data_source: Type[DataSource] = attr.ib()

    def draw(self, chart: IChart) -> None:
        data = self.to_data_source()
        chart.scatter("x", "y", marker="circle", source=data, size="sizes")

    def to_data_source(self) -> DataSource:
        sorted_cycle_times = _sort_cycle_times(self.cycle_times)

        keys, completions, cycle_times = _unsplit(sorted_cycle_times)

        completion_cycle_times = list(zip(completions, cycle_times))
        cycle_time_heatmap = Counter(completion_cycle_times)

        return self.data_source(
            {
                "x": completions,
                "y": cycle_times,
                "sizes": [
                    cycle_time_heatmap[(c, t)] * 3 + 2
                    for c, t in completion_cycle_times
                ],
                "label": keys,
            }
        )


def _sort_cycle_times(cycle_times: List[CycleTime]) -> List[CycleTime]:
    return list(sorted(cycle_times, key=attrgetter("completed")))


def _unsplit(
    cycle_times: List[CycleTime],
) -> Tuple[Tuple[str, ...], Tuple[date, ...], Tuple[float, ...]]:
    return cast(
        Tuple[Tuple[str, ...], Tuple[date, ...], Tuple[float, ...]],
        tuple(zip(*(attr.astuple(ct) for ct in cycle_times))),
    )
