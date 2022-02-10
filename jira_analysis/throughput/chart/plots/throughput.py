from bokeh.models.sources import ColumnDataSource, DataSource

from dataclasses import dataclass
from datetime import date
from typing import List, Type

from jira_analysis.chart.base import IChart, Plot


@dataclass(frozen=True)
class ThroughputPlot(Plot):
    """Throughputs as a vertical bar chart."""

    weeks: List[date]
    throughputs: List[int]
    data_source: Type[DataSource] = ColumnDataSource

    def draw(self, chart: IChart) -> None:
        """Draw the throughput bar plot onto chart.

        :param chart: The chart to draw on.
        """
        chart.vertical_bar(
            x="weeks", top="throughputs", source=self.to_data_source(), width=0.9
        )

    def to_data_source(self) -> DataSource:
        """Output the data for the bar plot.

        :return: The data source with weeks and throughput data.
        """
        return self.data_source(
            data={
                "weeks": [wc.strftime("%d/%m/%Y") for wc in self.weeks],
                "throughputs": self.throughputs,
            }
        )
