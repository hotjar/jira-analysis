"""Convert Jira tickets into Throughput Issues.
"""
from jira_analysis.jira.issue import JiraTicket

from jira_analysis.config.config import Config
from jira_analysis.throughput.issue import Issue, create_issue_with_config


def convert_jira_to_throughput(jira_ticket: JiraTicket, config: Config) -> Issue:
    """Take a given Jira Ticket and convert it into a Throughput ticket.

    :param jira_ticket: The Jira Ticket to convert.
    :param config: The Configuration.
    :return: A Throughput ticket.
    :raises IssueNotComplete: If the given ticket isn't marked as complete.
    """
    for change in jira_ticket.changelog:
        if config.is_completed_status(change.status_to):
            completed = change.created
            break

    return create_issue_with_config(
        key=jira_ticket.key,
        completed=completed.date(),
        status=jira_ticket.status,
        config=config,
    )
