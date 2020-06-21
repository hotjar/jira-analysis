import pytest

from datetime import date
from jira_analysis.defect_rate.issue import (
    Defect,
    Issue,
    IssueNotComplete,
    create_issue_with_config,
)

from .fixtures import config


@pytest.mark.parametrize(
    "test_related_issues,expected_output",
    [
        (
            [("PROJ-888", "Bug"), ("PROJ-777", "Story")],
            Issue(
                key="PROJ-123",
                completed=date(2020, 5, 1),
                defects=[Defect(key="PROJ-888")],
            ),
        ),
        (
            [("PROJ-712", "Spike")],
            Issue(key="PROJ-123", completed=date(2020, 5, 1), defects=[]),
        ),
        ([], Issue(key="PROJ-123", completed=date(2020, 5, 1), defects=[])),
    ],
)
def test_create_issue_with_config(test_related_issues, expected_output, config):
    assert (
        create_issue_with_config(
            config, "PROJ-123", [("Done", date(2020, 5, 1))], test_related_issues,
        )
        == expected_output
    )


def test_create_issue_with_config_raises_exception(config):
    with pytest.raises(IssueNotComplete) as exc:
        create_issue_with_config(
            config, "PROJ-123", [("In Progress", date(2020, 5, 1))], []
        )
    assert exc.value.issue_key == "PROJ-123"
