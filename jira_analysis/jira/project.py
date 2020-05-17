import attr

from typing import Dict, TypeVar, Type

T = TypeVar("T", bound="Parent")


@attr.s
class JiraProject:
    key: str = attr.ib()
    id: str = attr.ib()

    @classmethod
    def from_jira_project(cls: Type[T], project_dict: Dict[str, str]) -> T:
        return cls(id=project_dict["id"], key=project_dict["key"])
