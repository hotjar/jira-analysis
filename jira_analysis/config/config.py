import attr

from typing import IO, Optional, Set
from yaml import safe_load


@attr.s
class Config:
    project: str = attr.ib()
    completed: Set[str] = attr.ib()
    in_progress: Set[str] = attr.ib()
    analyse_issue_types: Optional[Set[str]] = attr.ib()
    defect_types: Set[str] = attr.ib()
    exclude_issues: Set[str] = attr.ib()

    def is_completed_status(self, status: str) -> bool:
        return status in self.completed

    def is_in_progress_status(self, status: str) -> bool:
        return status in self.in_progress

    def should_be_analysed(self, issue_type: str) -> bool:
        """Return whether issue_type should be analysed.

        If the analyse_issue_types attribute is not set (or empty), then this always
        returns True.

        :param issue_type: Issue type to be analysed.
        :return: Whether the issue type should be analysed.
        """
        return (
            issue_type in self.analyse_issue_types if self.analyse_issue_types else True
        )

    def is_defect_type(self, issue_type: str) -> bool:
        """Return whether the given issue type is a defined defect type.

        :param issue_type: The issue type to check.
    :return: Whether the given issue type is a defined defect type.
        """
        return issue_type in self.defect_types


def get_config(project_key: str, config_file: IO[str]) -> Config:
    config = safe_load(config_file)

    project = config["projects"][project_key]
    analyse_issue_types = project.get("analyse_issue_types")
    return Config(
        project=project["key"],
        completed=set(project["completed"]),
        in_progress=set(project["in_progress"]),
        analyse_issue_types=set(analyse_issue_types) if analyse_issue_types else None,
        defect_types=set(project.get("defect_types", [])),
        exclude_issues=set(project.get("exclude_issues", [])),
    )
