import attr

from abc import ABC, abstractmethod, abstractproperty
from bokeh.plotting import figure, show
from typing import Callable, List, Optional


@attr.s(frozen=True)
class Axis:
    label: str = attr.ib()
    values: Optional[List] = attr.ib()
    size: int = attr.ib()


class IChart(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

    @abstractproperty
    def scatter(self) -> Callable:
        pass

    @abstractproperty
    def line(self) -> Callable:
        pass

    @abstractproperty
    def glyph(self) -> Callable:
        pass

    @abstractproperty
    def wedge(self) -> Callable:
        pass


class Chart(IChart):
    def __init__(
        self,
        x: Axis,
        y: Axis,
        label: str,
        create_chart: Callable = figure,
        render: Callable = show,
    ):
        self._x = x
        self._y = y
        self._figure = create_chart(
            plot_width=self._x.size,
            plot_height=self._y.size,
            x_range=self._x.values,
            y_range=self._y.values,
            tooltips=[(label, "@label"), (self._x.label, "@x"), (self._y.label, "@y")],
        )
        self._figure.xaxis.axis_label = self._x.label
        self._figure.xaxis.major_label_orientation = "vertical"
        self._figure.yaxis.axis_label = self._y.label
        self._figure.y_range.start = 0
        self._render = render

    def render(self):
        self._render(self._figure)

    @property
    def scatter(self) -> Callable:
        return self._figure.scatter

    @property
    def line(self) -> Callable:
        return self._figure.line

    @property
    def glyph(self) -> Callable:
        return self._figure.add_glyph

    @property
    def wedge(self) -> Callable:
        return self._figure.annular_wedge


class Plot(ABC):
    @abstractmethod
    def draw(self, chart: IChart) -> None:
        pass
