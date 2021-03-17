import attr

from typing import Any, Callable


@attr.s
class _Figure:
    add_glyph: Callable[..., None] = attr.ib()
    line: Callable[..., None] = attr.ib()
    scatter: Callable[..., None] = attr.ib()
    annular_wedge: Callable[..., None] = attr.ib()
    vbar: Callable[..., None] = attr.ib()
    xaxis: Any = attr.ib()
    x_range: Any = attr.ib()
    yaxis: Any = attr.ib()
    y_range: Any = attr.ib()
