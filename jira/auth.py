import attr
from typing import Dict, TypeVar, Type
from yaml import safe_load

T = TypeVar("T", bound="Parent")


@attr.s(frozen=True)
class JiraConfig:
    email: str = attr.ib()
    token: str = attr.ib()

    @classmethod
    def from_credentials(cls: Type[T], credentials: Dict[str, Dict[str, str]]) -> T:
        return cls(**credentials["jira_credentials"])


def get_config(credentials_file: str) -> JiraConfig:
    with open(credentials_file) as f:
        credentials = safe_load(f)
    return JiraConfig.from_credentials(credentials)
