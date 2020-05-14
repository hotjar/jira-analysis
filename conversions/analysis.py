from analysis.config import Config
from analysis.issue import create_issue_with_config, Issue
from jira.issue import JiraTicket


def convert_jira_to_analysis(config: Config, ticket: JiraTicket) -> Issue:
    changes = [(cl.status_to, cl.created) for cl in ticket.changelog]
    return create_issue_with_config(
        config, ticket.key, ticket.created, ticket.status, changes
    )
