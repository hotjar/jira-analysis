import pytest

from jira_analysis.config.config import Config


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In progress"},
        analyse_issue_types=None,
        defect_types={"Bug"},
    )
