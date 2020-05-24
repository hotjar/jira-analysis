import pytest

from io import StringIO
from yaml import dump

from jira_analysis.jira.auth import JiraConfig, get_config


def _credentials():
    return {"email": "test@example.com", "token": "123"}


@pytest.fixture
def credentials_dict():
    return _credentials()


@pytest.fixture
def jira_config():
    return JiraConfig(**_credentials())


def test_jira_config_from_credentials(credentials_dict, jira_config):
    config = JiraConfig.from_credentials({"jira_credentials": credentials_dict})
    assert config == jira_config


def test_get_config(credentials_dict, jira_config):
    content = StringIO()
    dump({"jira_credentials": credentials_dict}, content)
    content.seek(0)
    assert get_config(content) == jira_config


def test_jira_config_validate():
    with pytest.raises(ValueError):
        JiraConfig(email="invalid", token="123")
