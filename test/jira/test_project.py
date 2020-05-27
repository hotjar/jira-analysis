import pytest

from jira_analysis.jira.project import JiraProject, parse_jira_project


def _project_dict():
    return {"id": 10, "key": "PROJ"}


@pytest.fixture
def jira_project():
    return JiraProject(**_project_dict())


@pytest.fixture
def jira_json():
    return _project_dict()


def test_parse_jira_project(jira_project, jira_json):
    assert parse_jira_project(jira_json) == jira_project

