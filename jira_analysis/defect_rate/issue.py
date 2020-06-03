import attr

from datetime import date
from typing import List


@attr.s(frozen=True)
class Defect:
    key: str = attr.ib()


@attr.s(frozen=True)
class Issue:
    key: str = attr.ib()
    completed: date = attr.ib()
    defects: List[Defect] = attr.ib()
