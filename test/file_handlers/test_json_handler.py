import pytest

from datetime import datetime
from enum import Enum
from io import StringIO

from jira_analysis.file_handlers.json_handler import dump


class _CustomEnum(Enum):
    SOME_VALUE = "some_value"


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        (datetime(2020, 7, 10, 14, 1, 3), '"2020-07-10T14:01:03"'),
        (1, "1"),
        (_CustomEnum.SOME_VALUE, '"some_value"'),
    ],
)
def test_dump(test_input, expected_output):
    assert _run_dump(test_input) == expected_output


def _run_dump(value) -> str:
    output = StringIO()
    dump(value, to=output)
    output.seek(0)
    return output.read()
