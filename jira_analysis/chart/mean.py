from abc import ABCMeta, abstractmethod, abstractproperty
from bokeh.models.sources import DataSource
from typing import Any, List, Type

from .base import IChart, Plot


class LinePlot(Plot, metaclass=ABCMeta):

    data_points: List[Any]
    data_source: Type[DataSource]

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
