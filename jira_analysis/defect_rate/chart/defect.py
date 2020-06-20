from bokeh.models.sources import ColumnDataSource
from typing import List

from jira_analysis.chart.base import Axis, IChart, Chart
from jira_analysis.defect_rate.issue import Issue
from .plot.donut import DefectRateDonut


def generate_defect_chart(issues: List[Issue], chart_class: IChart = Chart) -> None:
    chart = chart_class(
        x=Axis(label="", values=None, size=600),
        y=Axis(label="", values=None, size=300),
        label="Defects",
    )
    DefectRateDonut(issues=issues, data_source=ColumnDataSource).draw(chart)

    chart.render()
