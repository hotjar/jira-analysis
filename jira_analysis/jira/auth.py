import attr
from typing import Dict, IO, TypeVar, Type
from validate_email import validate_email
from yaml import safe_load

T = TypeVar("T", bound="Parent")


@attr.s(frozen=True)
class JiraConfig:
    email: str = attr.ib()
    token: str = attr.ib()

    @email.validator
    def valid_email_address(self, attribute: str, value: str) -> None:
        if not validate_email(value):
            raise ValueError(f"Invalid {attribute} format: {value}")

    @classmethod
    def from_credentials(cls: Type[T], credentials: Dict[str, Dict[str, str]]) -> T:
        return cls(**credentials["jira_credentials"])


def get_config(credentials_file: IO) -> JiraConfig:
    credentials = safe_load(credentials_file)
    return JiraConfig.from_credentials(credentials)
