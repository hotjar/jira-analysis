import attr

from datetime import datetime
from enum import Enum
from typing import Optional


class TicketStatus(Enum):
    BACKLOG = "Backlog"
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    RUNNING = "Running"
    BLOCKED = "Blocked"
    READY_FOR_REVIEW = "Ready for Review"
    REVIEW = "Review"
    IN_REVIEW = "In Review"
    DONE = "Done"


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    created: datetime = attr.ib()
    completed: Optional[datetime] = attr.ib()
    started: Optional[datetime] = attr.ib()

    status: TicketStatus = attr.ib()
