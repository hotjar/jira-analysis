import attr

from bokeh.models import VArea
from bokeh.models.sources import DataSource
from typing import List, Tuple, Type, cast

from jira_analysis.cycle_time.cycle_time import CycleTime
from jira_analysis.cycle_time.stats import (
    rolling_average_cycle_time,
    standard_deviations,
)
from jira_analysis.cycle_time.chart.base import IChart, Plot

from .base import BaseCycleTimeLinePlot
from .utils import sort_cycle_times, unsplit


@attr.s(frozen=True)
class CycleTimeDeviationPlot(Plot):

    cycle_times: List[CycleTime] = attr.ib()
    data_source: Type[DataSource] = attr.ib()

    def draw(self, chart: IChart) -> None:
        sorted_cycle_times = sort_cycle_times(self.cycle_times)
        _, completions, cycle_times = unsplit(sorted_cycle_times)
        upper_deviation, lower_deviation = _get_standard_deviations(sorted_cycle_times)

        data = self.to_data_source()
        upper_plot = _DeviationLinePlot(
            cycle_times=sorted_cycle_times,
            data_source=self.data_source,
            deviation_bound="Upper",
            deviations=upper_deviation,
        )
        lower_plot = _DeviationLinePlot(
            cycle_times=sorted_cycle_times,
            data_source=self.data_source,
            deviation_bound="Lower",
            deviations=lower_deviation,
        )

        deviation_glyph = VArea(
            x="x", y1="y1", y2="y2", fill_color="green", fill_alpha=0.3
        )

        chart.glyph(data, deviation_glyph)
        upper_plot.draw(chart)
        lower_plot.draw(chart)

    def to_data_source(self) -> DataSource:
        sorted_cycle_times = sort_cycle_times(self.cycle_times)
        _, completions, cycle_times = unsplit(sorted_cycle_times)

        upper_deviation, lower_deviation = _get_standard_deviations(sorted_cycle_times)

        return self.data_source(
            {"x": completions, "y1": upper_deviation, "y2": lower_deviation}
        )


def _get_standard_deviations(
    cycle_times: List[CycleTime],
) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
    cycle_time_values = [c.cycle_time for c in cycle_times]
    rolling_cycle_times = rolling_average_cycle_time(cycle_time_values)

    zipped_deviations = zip(
        rolling_cycle_times, standard_deviations(cycle_time_values),
    )
    return cast(
        Tuple[Tuple[float, ...], Tuple[float, ...]],
        tuple(zip(*((ct + sd, ct - sd) for ct, sd in zipped_deviations))),
    )


@attr.s(frozen=True)
class _DeviationLinePlot(BaseCycleTimeLinePlot):
    cycle_times: List[CycleTime] = attr.ib()
    data_source: Type[DataSource] = attr.ib()
    deviation_bound: str = attr.ib()
    deviations: Tuple[float, ...] = attr.ib()

    @property
    def alpha(self) -> float:
        return 0.3

    @property
    def color(self) -> str:
        return "green"

    @property
    def label(self) -> str:
        return f"{self.deviation_bound} bound"

    @property
    def width(self) -> int:
        return 1

    def to_data_source(self) -> DataSource:
        sorted_cycle_times = sort_cycle_times(self.cycle_times)
        _, completions, cycle_times = unsplit(sorted_cycle_times)

        return self.data_source(
            {
                "x": completions,
                "y": self.deviations,
                "label": [self.label for _ in completions],
            }
        )
