import attr

from bokeh.models import VArea
from bokeh.models.sources import DataSource
from typing import List, Tuple, Type, cast

from jira_analysis.analysis.cycle_time import CycleTime
from jira_analysis.analysis.stats import rolling_average_cycle_time, standard_deviations
from jira_analysis.analysis.chart.base import IChart, Plot

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
        deviation_glyph = VArea(
            x="x", y1="y1", y2="y2", fill_color="green", fill_alpha=0.3
        )

        chart.glyph(data, deviation_glyph)
        chart.line(
            completions,
            upper_deviation,
            line_width=1,
            name="Upper bound",
            color="green",
            alpha=0.3,
        )

        chart.line(
            completions,
            lower_deviation,
            line_width=1,
            name="Lower bound",
            color="green",
            alpha=0.3,
        )

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
    rolling_cycle_times = rolling_average_cycle_time(c.cycle_time for c in cycle_times)

    zipped_deviations = zip(
        rolling_cycle_times, standard_deviations(c.cycle_time for c in cycle_times),
    )
    return cast(
        Tuple[Tuple[float, ...], Tuple[float, ...]],
        tuple(zip(*((ct + sd, ct - sd) for ct, sd in zipped_deviations))),
    )
