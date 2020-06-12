import attr

from abc import ABCMeta, abstractmethod, abstractproperty
from bokeh.models.sources import DataSource
from typing import List, Type

from jira_analysis.chart.base import IChart, Plot
from jira_analysis.cycle_time.cycle_time import CycleTime


@attr.s(frozen=True)
class BaseCycleTimeLinePlot(Plot, metaclass=ABCMeta):

    cycle_times: List[CycleTime] = attr.ib()
    data_source: Type[DataSource] = attr.ib()

    def draw(self, chart: IChart) -> None:
        chart.line(
            "x",
            "y",
            source=self.to_data_source(),
            line_width=self.width,
            name=self.label,
            color=self.color,
            alpha=self.alpha,
        )

    @abstractmethod
    def to_data_source(self) -> DataSource:
        pass

    @abstractproperty
    def label(self) -> str:
        pass

    @abstractproperty
    def color(self) -> str:
        pass

    @abstractproperty
    def width(self) -> int:
        pass

    @property
    def alpha(self) -> float:
        return 0.9
