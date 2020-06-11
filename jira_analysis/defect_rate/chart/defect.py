from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from typing import List

from jira_analysis.defect_rate.issue import Issue
from .plot.donut import DefectRateDonut


def generate_defect_chart(issues: List[Issue]):
    p = figure(plot_width=600, plot_height=600,)
    p.annular_wedge(
        x=0,
        y=0,
        inner_radius=0.15,
        outer_radius=0.25,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="value",
        source=DefectRateDonut(
            issues=issues, data_source=ColumnDataSource
        ).to_data_source(),
    )
    show(p)
