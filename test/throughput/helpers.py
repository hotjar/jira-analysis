from jira_analysis.config.config import Config


def get_config(**overrides):
    config_args = {
        "project": "PROJ-123",
        "in_progress": {"In Progress"},
        "completed": {"Done"},
        "analyse_issue_types": None,
        "defect_types": {"Bug"},
        "exclude_issues": set(),
    }
    config_args.update(overrides)
    return Config(**config_args)