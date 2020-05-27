import pytest

from io import StringIO

from jira_analysis.analysis.config import Config, get_config


@pytest.fixture
def config():
    return Config(
        project="PROJ", completed={"Done"}, in_progress={"In progress", "Review"}
    )


@pytest.fixture
def config_file():
    return StringIO(
        """projects:
  PROJ:
    key: PROJ
    in_progress:
      - In progress
      - Review
    completed:
      - Done
"""
    )


def test_config_is_completed_status(config):
    assert config.is_completed_status("Done")


def test_config_is_completed_status_false(config):
    assert not config.is_completed_status("In progress")


def test_config_is_in_progress_status(config):
    assert config.is_in_progress_status("In progress")


def test_config_is_in_progress_status_false(config):
    assert not config.is_in_progress_status("Backlog")


def test_get_config(config, config_file):
    assert get_config("PROJ", config_file) == config
