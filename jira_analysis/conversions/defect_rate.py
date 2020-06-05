from jira_analysis.jira.issue import JiraTicket, LinkDirection

from jira_analysis.config.config import Config
from jira_analysis.defect_rate.issue import Issue, create_issue_with_config


def convert_jira_to_defect(jira_ticket: JiraTicket, config: Config) -> Issue:
    return create_issue_with_config(
        config,
        jira_ticket.key,
        [(cl.status_to, cl.created.date()) for cl in jira_ticket.changelog],
        [
            (lt.key, lt.issue_type)
            for lt in jira_ticket.related_issues
            if lt.link_direction is LinkDirection.OUTBOUND
        ],
    )
