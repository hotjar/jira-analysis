import pytest

from datetime import datetime
from io import StringIO

from jira_analysis.file_handlers.json_handler import dump


@pytest.fixture
def current_date():
    return datetime(2020, 7, 10, 14, 1, 3)


@pytest.fixture
def current_date_isoformat():
    return '"2020-07-10T14:01:03"'  # Time represented as JSON string


@pytest.fixture
def an_integer():
    return 1


def test_dump(current_date, current_date_isoformat):
    assert _run_dump(current_date) == current_date_isoformat


def test_dump_default(an_integer):
    assert _run_dump(an_integer) == str(an_integer)


def _run_dump(value) -> str:
    output = StringIO()
    dump(value, to=output)
    output.seek(0)
    return output.read()
