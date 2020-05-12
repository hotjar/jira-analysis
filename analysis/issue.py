import attr

from datetime import datetime
from enum import Enum


class TicketStatus(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    RUNNING = "Running"
    REVIEW = "Review"
    DONE = "Done"


_WORK_COMPLETE_STATUSES = frozenset([TicketStatus.RUNNING, TicketStatus.DONE])
_WORK_IN_PROGRESS_STATUSES = frozenset([TicketStatus.IN_PROGRESS, TicketStatus.REVIEW])


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    created: datetime = attr.ib()
    completed: datetime = attr.ib()

    status: TicketStatus = attr.ib()
    done: bool = attr.ib()
