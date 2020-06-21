import attr

from abc import ABC, abstractmethod, abstractproperty
from bokeh.plotting import figure, show
from typing import Any, Callable, List, Optional, cast

from ._type import _Figure


@attr.s(frozen=True)
class Axis:
    label: str = attr.ib()
    values: Optional[List[Any]] = attr.ib()
    size: int = attr.ib()


class IChart(ABC):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractproperty
    def scatter(self) -> Callable[..., None]:
        pass

    @abstractproperty
    def line(self) -> Callable[..., None]:
        pass

    @abstractproperty
    def glyph(self) -> Callable[..., None]:
        pass

    @abstractproperty
    def wedge(self) -> Callable[..., None]:
        pass


class Chart(IChart):
    def __init__(
        self,
        x: Axis,
        y: Axis,
        label: str,
        create_chart: Callable[..., Any] = figure,
        render: Callable[[Any], None] = show,
    ):
        self._x = x
        self._y = y
        self._figure = cast(
            _Figure,
            create_chart(
                plot_width=self._x.size,
                plot_height=self._y.size,
                x_range=self._x.values,
                y_range=self._y.values,
                tooltips=[
                    (label, "@label"),
                    (self._x.label, "@x"),
                    (self._y.label, "@y"),
                ],
            ),
        )
        self._figure.xaxis.axis_label = self._x.label
        self._figure.xaxis.major_label_orientation = "vertical"
        self._figure.yaxis.axis_label = self._y.label
        self._figure.y_range.start = 0
        self._render = render

    def render(self) -> None:
        self._render(self._figure)

    @property
    def scatter(self) -> Callable[..., None]:
        return self._figure.scatter

    @property
    def line(self) -> Callable[..., None]:
        return self._figure.line

    @property
    def glyph(self) -> Callable[..., None]:
        return self._figure.add_glyph

    @property
    def wedge(self) -> Callable[..., None]:
        return self._figure.annular_wedge


class Plot(ABC):
    @abstractmethod
    def draw(self, chart: IChart) -> None:
        pass
