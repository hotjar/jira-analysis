import attr

from datetime import date
from enum import Enum
from typing import Optional


class TicketStatus(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    RUNNING = "Running"
    REVIEW = "Review"
    DONE = "Done"


WORK_COMPLETE_STATUSES = frozenset([TicketStatus.RUNNING, TicketStatus.DONE])


@attr.s(frozen=True)
class JiraTicket:
    id = attr.ib(Optional[int])
    description = attr.ib(str)
    key = attr.ib(str)
    status = attr.ib(TicketStatus)
    first_updated = attr.ib(date)
    updated = attr.ib(date)

    @property
    def done(self) -> bool:
        return self.status in WORK_COMPLETE_STATUSES


def get_ticket_status(status: str) -> TicketStatus:
    status_map = {s.value: s for s in TicketStatus}
    return status_map[status]
