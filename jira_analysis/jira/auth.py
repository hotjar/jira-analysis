import attr
import validators

from typing import Dict, IO
from yaml import safe_load


@attr.s
class _Attribute:
    name: str = attr.ib()


@attr.s(frozen=True)
class JiraConfig:
    email: str = attr.ib()
    token: str = attr.ib()
    jira_url: str = attr.ib()

    @email.validator
    def valid_email_address(self, attribute: _Attribute, value: str) -> None:
        if not validators.email(value):
            _invalid_format(attribute, value)

    @jira_url.validator
    def valid_hostname(self, attribute: _Attribute, value: str) -> None:
        to_check = value
        if not value.startswith("http"):
            to_check = f"https://{value}"
        if not validators.url(to_check):
            _invalid_format(attribute, value)


def _from_credentials(credentials: Dict[str, Dict[str, str]]) -> JiraConfig:
    return JiraConfig(**credentials["jira_credentials"])


def get_config(credentials_file: IO[str]) -> JiraConfig:
    credentials = safe_load(credentials_file)
    return _from_credentials(credentials)


def _invalid_format(attribute: _Attribute, value: str) -> None:
    raise ValueError(f"Invalid {attribute.name} format: '{value}'.")
