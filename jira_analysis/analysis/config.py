import attr

from typing import Set
from yaml import safe_load


@attr.s
class Config:
    project: str = attr.ib()
    completed: Set[str] = attr.ib()
    in_progress: Set[str] = attr.ib()

    def is_completed_status(self, status: str) -> bool:
        return status in self.completed

    def is_in_progress_status(self, status: str) -> bool:
        return status in self.in_progress


def get_config(project_key: str, config_file) -> Config:
    config = safe_load(config_file)

    project = config["projects"][project_key]
    return Config(
        project=project["key"],
        completed=set(project["completed"]),
        in_progress=set(project["in_progress"]),
    )
