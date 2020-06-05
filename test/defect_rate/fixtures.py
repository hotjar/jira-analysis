import pytest

from jira_analysis.config.config import Config


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In Progress"},
        analyse_issue_types={"Story", "Bug", "Spike"},
        defect_types={"Bug"},
    )
