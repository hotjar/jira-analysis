import pytest

from io import StringIO

from jira_analysis.config.config import Config, get_config


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In progress", "Review"},
        analyse_issue_types=None,
        defect_types={"Bug"},
        exclude_issues=set(),
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
                defect_types={"Bug"},
                exclude_issues=set(),
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
                defect_types={"Bug"},
                exclude_issues=set(),
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
                defect_types={"Bug"},
                exclude_issues=set(),
            ),
            "Bug",
            False,
        ),
    ],
)
def test_should_be_analysed(test_config, test_input, expected_result):
    assert test_config.should_be_analysed(test_input) == expected_result


@pytest.mark.parametrize(
    "test_input,expected_output", [("Bug", True), ("Story", False)]
)
def test_is_defect_type(test_input, expected_output, config):
    assert config.is_defect_type(test_input) == expected_output


@pytest.mark.parametrize(
    "expected,test_input",
    [
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types=None,
                defect_types={"Bug"},
                exclude_issues=set(),
            ),
            """projects:
  PROJ:
    key: PROJ
    in_progress:
      - In progress
      - Review
    completed:
      - Done
    defect_types:
      - Bug
""",
        ),
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types={"Story", "Bug"},
                defect_types={"Bug"},
                exclude_issues=set(),
            ),
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
    defect_types:
        - Bug
""",
        ),
        (
            Config(
                project="PROJ",
                completed={"Done"},
                in_progress={"In progress", "Review"},
                analyse_issue_types={"Story", "Bug"},
                defect_types={"Bug"},
                exclude_issues={"PROJ-123", "PROJ-5"},
            ),
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
    defect_types:
        - Bug
    exclude_issues:
        - PROJ-5
        - PROJ-123
""",
        ),
    ],
)
def test_get_config(expected, test_input):
    assert get_config("PROJ", StringIO(test_input)) == expected
