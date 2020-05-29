import pytest

from io import StringIO

from jira_analysis.analysis.config import Config, get_config


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In progress", "Review"},
        analyse_issue_types=None,
    )


def config_files():
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


@pytest.mark.parametrize(
    "expected,test_input",
    [
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types=None,
            ),
            StringIO(
                """projects:
  PROJ:
    key: PROJ
    in_progress:
      - In progress
      - Review
    completed:
      - Done
"""
            ),
        ),
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types={"Story", "Bug"},
            ),
            StringIO(
                """projects:
  PROJ:
    key: PROJ
    in_progress:
      - In progress
      - Review
    completed:
      - Done
    analyse_issue_types:
        - Story
        - Bug
"""
            ),
        ),
    ],
)
def test_get_config(expected, test_input):
    assert get_config("PROJ", test_input) == expected
