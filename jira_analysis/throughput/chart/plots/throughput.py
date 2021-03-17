from bokeh.models.sources import ColumnDataSource, DataSource

from dataclasses import dataclass
from datetime import date
from typing import List

from jira_analysis.chart.base import IChart, Plot


@dataclass(frozen=True)
class ThroughputPlot(Plot):

    weeks: List[date]
    throughputs: List[int]

    def draw(self, chart: IChart) -> None:
        """Draw the throughput bar chart onto chart.

        :param chart: The chart to draw on.
        """
        chart.vertical_bar(x="weeks", top="throughputs", source=self.to_data_source())

    def to_data_source(self) -> DataSource:
        return ColumnDataSource(
            data={
                "weeks": [wc.strftime("%d/%m/%Y") for wc in self.weeks],
                "throughputs": self.throughputs,
            }
        )
