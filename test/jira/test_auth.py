import pytest

from io import StringIO

from jira_analysis.jira.auth import JiraConfig, get_config

from .fixtures import jira_config


@pytest.fixture
def config_file():
    return StringIO(
        """jira_credentials:
    email: test@example.com
    token: abc123
    jira_url: jira.example.com
"""
    )


def test_get_config(config_file, jira_config):
    assert get_config(config_file) == jira_config


@pytest.mark.parametrize(
    "test_input,exception,message",
    [
        (
            {"email": "invalid", "token": "123", "jira_url": "jira.example.com"},
            ValueError,
            "Invalid email format: 'invalid'.",
        ),
        (
            {"email": "test@example.com", "token": "123", "jira_url": "invalid"},
            ValueError,
            "Invalid jira_url format: 'invalid'.",
        ),
        (
            {
                "email": "test@example.com",
                "token": "123",
                "jira_url": "https://invalid",
            },
            ValueError,
            "Invalid jira_url format: 'https://invalid'.",
        ),
    ],
)
def test_jira_config_validate(test_input, exception, message):
    with pytest.raises(exception) as exc:
        JiraConfig(**test_input)
    assert str(exc.value) == message
