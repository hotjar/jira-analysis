import pytest

from io import StringIO

from jira_analysis.jira.auth import JiraConfig, get_config


def _credentials():
    return {"email": "test@example.com", "token": "123"}


@pytest.fixture
def credentials_dict():
    return _credentials()


@pytest.fixture
def jira_config():
    return JiraConfig(**_credentials())


@pytest.fixture
def config_file():
    return StringIO(
        """jira_credentials:
    email: test@example.com
    token: '123'
"""
    )


def test_jira_config_from_credentials(credentials_dict, jira_config):
    config = JiraConfig.from_credentials({"jira_credentials": credentials_dict})
    assert config == jira_config


def test_get_config(config_file, jira_config):
    assert get_config(config_file) == jira_config


def test_jira_config_validate():
    with pytest.raises(ValueError):
        JiraConfig(email="invalid", token="123")
