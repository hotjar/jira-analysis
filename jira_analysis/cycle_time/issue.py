import attr

from datetime import datetime
from toolz import itertoolz as it
from typing import Iterable, Optional, Tuple

from jira_analysis.config.config import Config


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    created: datetime = attr.ib()
    completed: Optional[datetime] = attr.ib()
    started: Optional[datetime] = attr.ib()
    status: str = attr.ib()


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
        key=key, created=created, completed=completed, started=started, status=status,
    )
