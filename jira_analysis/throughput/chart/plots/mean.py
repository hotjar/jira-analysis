from bokeh.models.sources import ColumnDataSource, DataSource
from dataclasses import dataclass
from datetime import date
from statistics import mean
from typing import List, Tuple, Type
from toolz.sandbox.core import unzip

from jira_analysis.chart.mean import LinePlot


@dataclass(frozen=True)
class AverageThroughputPlot(LinePlot):

    data_points: List[Tuple[date, int]]
    data_source: Type[DataSource] = ColumnDataSource

    def to_data_source(self) -> DataSource:
        """Convert the data points into a DataSource."""
        weeks, throughputs = unzip(self.data_points)
        mean_throughput = mean(throughputs)

        return self.data_source(
            {
                "x": [wc.strftime("%d/%m/%Y") for wc in sorted(weeks)],
                "y": [mean_throughput] * len(self.data_points),
                "label": [self.label] * len(self.data_points),
            }
        )

    @property
    def label(self) -> str:
        return "Average throughput (stories / week)"

    @property
    def color(self) -> str:
        return "red"

    @property
    def width(self) -> int:
        return 1