import attr

from math import pi
from typing import Any, Callable, Dict, List

from jira_analysis.chart.base import IChart, Plot
from jira_analysis.defect_rate.issue import Issue


@attr.s
class DefectRateDonut(Plot):
    issues: List[Issue] = attr.ib()
    data_source: Callable[[Dict], Any] = attr.ib()
    no_defects_transform: Callable[[str], Any] = attr.ib()
    defects_transform: Callable[[str], Any] = attr.ib()

    def draw(self, chart: IChart) -> None:
        chart.wedge(
            x=0,
            y=0,
            inner_radius=0.65,
            outer_radius=0.95,
            start_angle=self.no_defects_transform("angle"),
            end_angle=self.defects_transform("angle"),
            line_color="white",
            fill_color="color",
            legend_field="value",
            source=self.to_data_source(),
        )

    def to_data_source(self) -> Any:
        num_issues = len(self.issues)
        issues_with_defects = len([i for i in self.issues if i.defects])
        defect_rate = issues_with_defects / num_issues
        no_defect_rate = 1 - defect_rate
        return self.data_source(
            {
                "issues": [num_issues, issues_with_defects],
                "defect_rate": [no_defect_rate, defect_rate],
                "value": ["Issues", "Defect Rate"],
                "angle": [_get_angle(no_defect_rate), _get_angle(defect_rate)],
                "color": ["green", "red"],
            }
        )


def _get_angle(percentage: float) -> float:
    return percentage * pi
