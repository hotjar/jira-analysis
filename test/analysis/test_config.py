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


@pytest.mark.parametrize(
    "test_input,expected_result", [("Done", True), ("In progress", False)]
)
def test_config_is_completed_status(test_input, expected_result, config):
    assert config.is_completed_status(test_input) == expected_result


@pytest.mark.parametrize(
    "test_input,expected_result", [("Done", False), ("In progress", True)]
)
def test_config_is_in_progress_status(test_input, expected_result, config):
    assert config.is_in_progress_status(test_input) == expected_result


@pytest.mark.parametrize(
    "test_config,test_input,expected_result",
    [
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types=None,
            ),
            "Bug",
            True,
        ),
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types={"Story", "Task"},
            ),
            "Story",
            True,
        ),
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types={"Story", "Task"},
            ),
            "Bug",
            False,
        ),
    ],
)
def test_should_be_analysed(
    test_config: Config, test_input: str, expected_result: bool
):
    assert test_config.should_be_analysed(test_input) == expected_result


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
