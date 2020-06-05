from jira_analysis.jira.issue import JiraTicket

from jira_analysis.config.config import Config
from jira_analysis.defect_rate.issue import Defect, Issue


def convert_jira_to_defect(jira_ticket: JiraTicket, config: Config) -> Issue:
    completed = min(
        cl.created
        for cl in jira_ticket.changelog
        if config.is_completed_status(cl.status_to)
    )
    return Issue(
        key=jira_ticket.key,
        completed=completed,
        defects=[Defect(key=ri.key) for ri in jira_ticket.related_issues],
    )
