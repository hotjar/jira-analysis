from jira_analysis.cycle_time.config import Config
from jira_analysis.cycle_time.issue import create_issue_with_config, Issue
from jira_analysis.jira.issue import JiraTicket


def convert_jira_to_analysis(config: Config, ticket: JiraTicket) -> Issue:
    changes = [(cl.status_to, cl.created) for cl in ticket.changelog]
    return create_issue_with_config(
        config, ticket.key, ticket.created, ticket.status, changes
    )
