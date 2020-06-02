from typing import Iterator

from jira_analysis.cycle_time.config import Config


def integers(start=1, end=3, num_values=10) -> Iterator[int]:
    integer_range = list(range(start, end + 1))
    i = 0
    for _ in range(num_values):
        if i >= len(integer_range):
            i = 0
        yield integer_range[i]
        i += 1


def get_config(**overrides):
    config_args = {
        "project": "PROJ-123",
        "in_progress": {"In Progress"},
        "completed": {"Done"},
        "analyse_issue_types": None,
        "jira_url": "jira.atlassian.net",
    }
    config_args.update(overrides)
    return Config(**config_args)
