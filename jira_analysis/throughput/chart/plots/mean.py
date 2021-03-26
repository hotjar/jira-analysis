from bokeh.models.sources import ColumnDataSource, DataSource

from dataclasses import dataclass
from datetime import date
from typing import List, Type

from jira_analysis.chart.base import IChart, Plot


@dataclass(frozen=True)
class AverageThroughputPlot(Plot):

    weeks: List[date]
    throughputs: List[int]
    data_source: Type[DataSource] = ColumnDataSource

    def draw(self, chart: IChart) -> None:
        """Draw the average throughput line onto the plot.

        :param chart: The chart to draw on.
        """
        chart.vertical_bar(
            x="weeks", top="throughputs", source=self.to_data_source(), width=0.9
        )

    def to_data_source(self) -> DataSource:
        return self.data_source(
            data={
                "weeks": [wc.strftime("%d/%m/%Y") for wc in self.weeks],
                "throughputs": self.throughputs,
            }
        )
