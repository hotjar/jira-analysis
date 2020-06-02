import attr

from datetime import date


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    completed: date = attr.ib()


@attr.s(frozen=True)
class Defect:
    key: str = attr.ib()
    created: date = attr.ib()
    issue: Issue = attr.ib()
