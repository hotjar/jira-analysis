import arrow

from collections import OrderedDict
from datetime import date
from operator import attrgetter
from typing import Iterable, List

from .issue import Issue


def group_issues_by_week_commence(
    issues: Iterable[Issue],
) -> OrderedDict[date, List[Issue]]:
    """Generate a mapping of week commence date -> issue list for the given issues.

    This will return _all_ weeks between the first and last issue, ordered by date.
    Some weeks may have no issues resolved.

    :param issues: The issues to group.
    :return: The mapped week commencements to issues.
    """
    sorted_issues = list(sorted(issues, key=attrgetter("completed")))

    first_monday = _week_commence(sorted_issues[0].completed)
    last_monday = arrow.get(sorted_issues[-1].completed).ceil("week")
    grouped_issues: OrderedDict[date, List[Issue]] = OrderedDict(
        (wc.date(), []) for wc in arrow.Arrow.range("week", first_monday, last_monday)
    )
    for issue in sorted_issues:
        grouped_issues[_week_commence(issue.completed).date()].append(issue)

    return grouped_issues


def _week_commence(dt: date) -> arrow.Arrow:
    """Return the week commencing date.

    :param dt: Date to convert.
    :return: The week commence date.
    """
    return arrow.get(dt).floor("week")
