import pytest
from datetime import date

from jira_analysis.config.config import Config
from jira_analysis.defect_rate.issue import Defect, Issue


@pytest.fixture
def issue():
    return Issue(
        key="PROJ-123", completed=date(2020, 5, 1), defects=[Defect(key="PROJ-444")]
    )


@pytest.fixture
def config():
    return Config(
        project="PROJ",
        completed={"Done"},
        in_progress={"In Progress"},
        analyse_issue_types={"Story", "Bug", "Spike"},
        defect_types={"Bug"},
        exclude_issues=set(),
    )
