import attr

from datetime import datetime
from enum import Enum
from toolz import itertoolz as it
from typing import Iterable, Optional, Tuple

from .config import Config


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


def create_issue_with_config(
    config: Config,
    key: str,
    created: datetime,
    status: str,
    changelog: Iterable[Tuple[str, datetime]],
) -> Issue:
    completed = started = None

    for change, updated in sorted(changelog, key=it.last):
        if config.is_completed_status(change) and completed is None:
            completed = updated
        if config.is_in_progress_status(change) and started is None:
            started = updated

    return Issue(
        key=key,
        created=created,
        completed=completed,
        started=started,
        status=TicketStatus(status),
    )
