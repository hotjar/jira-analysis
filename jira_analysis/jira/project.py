import attr

from typing import Dict


@attr.s(frozen=True)
class JiraProject:
    key: str = attr.ib()
    id: str = attr.ib()


def parse_jira_project(project_dict: Dict[str, str]) -> JiraProject:
    return JiraProject(id=project_dict["id"], key=project_dict["key"])
