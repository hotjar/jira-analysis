from datetime import datetime
from operator import attrgetter
from typing import Optional

from analysis.issue import Issue, TicketStatus
from jira.issue import JiraTicket


def convert_jira_to_analysis(ticket: JiraTicket) -> Issue:
    return Issue(
        key=ticket.key,
        created=ticket.created,
        completed=get_completed(ticket),
        started=get_started(ticket),
        status=TicketStatus(ticket.status),
    )


def get_completed(ticket: JiraTicket) -> Optional[datetime]:
    if status_is_done(TicketStatus(ticket.status)):
        for changes in sorted(ticket.changelog, key=attrgetter("created")):
            status_to = TicketStatus(changes.status_to)
            if status_is_done(status_to):
                return changes.created
        else:
            raise ValueError("Invalid Completed status")
    return None


def get_started(ticket: JiraTicket) -> Optional[datetime]:
    if status_is_started(TicketStatus(ticket.status)) or status_is_done(
        TicketStatus(ticket.status)
    ):
        for changes in sorted(ticket.changelog, key=attrgetter("created")):
            status_to = TicketStatus(changes.status_to)
            if status_is_started(status_to):
                return changes.created
            if status_is_done(status_to):
                return None
        else:
            raise ValueError("Invalid Started status")
    return None


def status_is_done(status: TicketStatus) -> bool:
    return status in _WORK_COMPLETE_STATUSES


def status_is_started(status: TicketStatus) -> bool:
    return status in _WORK_IN_PROGRESS_STATUSES


_WORK_COMPLETE_STATUSES = frozenset([TicketStatus.RUNNING, TicketStatus.DONE])
_WORK_IN_PROGRESS_STATUSES = frozenset(
    [
        TicketStatus.IN_PROGRESS,
        TicketStatus.REVIEW,
        TicketStatus.IN_REVIEW,
        TicketStatus.BLOCKED,
    ]
)
