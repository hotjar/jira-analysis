import attr

from bokeh.models.sources import DataSource
from collections import Counter
from datetime import date
from operator import attrgetter
from typing import Dict, List, Tuple, Type, TypeVar

from jira_analysis.analysis.cycle_time import CycleTime

from .base import BaseDataConverter
from jira_analysis.analysis.stats import rolling_average_cycle_time, standard_deviations


@attr.s
class CycleTimeDataSource(BaseDataConverter):

    cycle_times: List[CycleTime] = attr.ib()

    def to_data_source(
        self, data_source: Type[DataSource], x="x", y="y", sizes="sizes", label="label"
    ) -> DataSource:
        sorted_cycle_times = _sort_cycle_times(self.cycle_times)

        keys, completions, cycle_times = _unsplit(sorted_cycle_times)

        completion_cycle_times = list(zip(completions, cycle_times))
        cycle_time_heatmap = Counter(completion_cycle_times)

        return data_source(
            {
                x: completions,
                y: cycle_times,
                sizes: [
                    cycle_time_heatmap[(c, t)] * 3 + 2
                    for c, t in completion_cycle_times
                ],
                label: keys,
            }
        )


@attr.s
class CycleTimeDeviationDataSource(BaseDataConverter):

    cycle_times: List[CycleTime] = attr.ib()

    def to_data_source(
        self, data_source: Type[DataSource], x="x", y1="y1", y2="y2", sizes="sizes"
    ) -> DataSource:
        sorted_cycle_times = _sort_cycle_times(self.cycle_times)
        _, completions, cycle_times = _unsplit(sorted_cycle_times)

        rolling_cycle_times = rolling_average_cycle_time(
            c.cycle_time for c in sorted_cycle_times
        )

        zipped_deviations = zip(
            rolling_cycle_times,
            standard_deviations(c.cycle_time for c in sorted_cycle_times),
        )
        upper_deviation, lower_deviation = list(
            zip(*((ct + sd, ct - sd) for ct, sd in zipped_deviations))
        )

        return data_source({x: completions, y1: upper_deviation, y2: lower_deviation,})


def _sort_cycle_times(cycle_times: List[CycleTime]) -> List[CycleTime]:
    return list(sorted(cycle_times, key=attrgetter("completed")))


def _unsplit(cycle_times: List[CycleTime]) -> List[Tuple[str, date, float]]:
    return list(zip(*(attr.astuple(ct) for ct in cycle_times)))
