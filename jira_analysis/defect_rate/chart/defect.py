from bokeh.models.sources import ColumnDataSource
from bokeh.transform import cumsum
from functools import partial
from typing import List, Type

from jira_analysis.chart.base import Axis, IChart, Chart
from jira_analysis.defect_rate.issue import Issue
from .plot.donut import DefectRateDonut


def generate_defect_chart(
    issues: List[Issue], chart_class: Type[IChart] = Chart
) -> None:
    chart = chart_class(
        label=None,
        x=Axis(label="", values=None, size=600),
        y=Axis(label="", values=None, size=300),
        tooltips="@value: @defect_rate{0.1f}%",
    )
    DefectRateDonut(
        issues=issues,
        data_source=ColumnDataSource,
        no_defects_transform=partial(cumsum, include_zero=True),
        defects_transform=cumsum,
    ).draw(chart)

    chart.render()
