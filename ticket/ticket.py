import attr

from datetime import date
from enum import Enum
from operator import attrgetter
from typing import List, Optional

from numpy import busday_count


class TicketStatus(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    RUNNING = "Running"
    REVIEW = "Review"
    DONE = "Done"


_WORK_COMPLETE_STATUSES = frozenset([TicketStatus.RUNNING, TicketStatus.DONE])
_WORK_IN_PROGRESS_STATUSES = frozenset([TicketStatus.IN_PROGRESS, TicketStatus.REVIEW])


@attr.s(frozen=True)
class JiraWorkLog:
    status: TicketStatus = attr.ib()
    updated: date = attr.ib()
    id: Optional[int] = attr.ib(
        None, validator=attr.validators.optional(attr.validators.instance_of(int))
    )

    @property
    def done(self) -> bool:
        return self.status in _WORK_COMPLETE_STATUSES

    @property
    def in_progress(self) -> bool:
        return self.status in _WORK_IN_PROGRESS_STATUSES


@attr.s(frozen=True)
class JiraTicket:
    description: str = attr.ib()
    key: str = attr.ib()
    status: TicketStatus = attr.ib()
    updated: date = attr.ib()
    ticket_log: List[JiraWorkLog] = attr.ib()
    id: Optional[int] = attr.ib(
        None, validator=attr.validators.optional(attr.validators.instance_of(int))
    )

    @property
    def done(self) -> bool:
        return self.status in _WORK_COMPLETE_STATUSES


def get_ticket_status(status: str) -> TicketStatus:
    status_map = {s.value: s for s in TicketStatus}
    return status_map[status]


def get_with_updated_work_log(
    jira_ticket: JiraTicket, new_item: JiraWorkLog
) -> JiraTicket:
    """Return the updated Jira Ticket Log
    """
    new_items = []
    should_add_new_item = True
    for item in jira_ticket.ticket_log:
        new_items.append(item)
        if new_item.status is item.status:
            should_add_new_item = False

    if should_add_new_item:
        new_items.append(new_item)
    new_items = list(sorted(new_items, key=attrgetter("updated")))
    return JiraTicket(
        id=jira_ticket.id,
        key=jira_ticket.key,
        description=jira_ticket.description,
        status=new_items[-1].status,
        updated=new_items[-1].updated,
        ticket_log=new_items,
    )


def get_cycle_time(jira_ticket: JiraTicket) -> Optional[int]:
    if jira_ticket.done:
        in_progress = done = None
        for item in sorted(jira_ticket.ticket_log, key=attrgetter("updated")):
            if item.status == TicketStatus.TO_DO and in_progress is None:
                created = item
            if item.in_progress and in_progress is None:
                in_progress = item
            if item.done and done is None:
                done = item
        if done is None or in_progress is None:
            return None
        return int(busday_count(in_progress.updated, done.updated))

    return None
