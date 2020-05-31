import pytest

from copy import deepcopy
from datetime import datetime
from dateutil.tz import tzutc


from jira_analysis.jira.issue import (
    JiraTicket,
    StatusChange,
    parse_jira_ticket,
    parse_json,
)


@pytest.fixture
def valid_jira_json():
    return {
        "key": "KEY-123",
        "created": "2020-01-10T09:01:10.000000",
        "updated": "2020-01-30T15:01:05.000000",
        "description": "Test description",
        "status": "Done",
        "issue_type": "Bug",
        "changelog": [
            {
                "created": "2020-01-30T15:01:05.000000",
                "status_from": "To do",
                "status_to": "Done",
            }
        ],
    }


def jira_descriptions():
    base_json = {
        "key": "KEY-123",
        "fields": {
            "created": "2020-01-10T09:01:10.000000",
            "updated": "2020-01-30T15:01:05.000000",
            "status": {"name": "Done"},
            "description": {"type": "doc"},
            "issuetype": {"name": "bug"},
        },
        "changelog": {
            "histories": [
                {
                    "created": "2020-01-30T15:01:05.000000",
                    "items": [
                        {"field": "status", "fromString": "To do", "toString": "Done",},
                        {"field": "comment"},
                    ],
                }
            ]
        },
    }
    descriptions = [
        {"type": "hardBreak"},
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "test"},
                {"type": "text", "text": "other"},
            ],
        },
        {"type": "text", "text": "some text"},
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [{"type": "text", "text": "Header"}],
        },
        {
            "type": "heading",
            "attrs": {"level": 3},
            "content": [{"type": "text", "text": "Header 3"}],
        },
        {
            "type": "link",
            "attrs": {"href": "https://example.com"},
            "content": [{"type": "text", "text": "Link text"}],
        },
        {"type": "mention", "attrs": {"text": "John Smith"}},
        {
            "type": "codeBlock",
            "attrs": {"language": "python"},
            "content": [{"type": "text", "text": "print('Hello, world')"}],
        },
        {
            "type": "orderedList",
            "content": [
                {"content": [{"type": "text", "text": "Item"},]},
                {"content": [{"type": "text", "text": "Item"},]},
            ],
        },
        {
            "type": "unorderedList",
            "content": [
                {"content": [{"type": "text", "text": "Item"},]},
                {"content": [{"type": "text", "text": "Item"},]},
            ],
        },
        {"type": "image", "content": []},
    ]
    parsed_descriptions = [
        "---",
        "test\n\nother",
        "some text",
        "# Header",
        "### Header 3",
        "[Link text](https://example.com)",
        "@John Smith",
        "```python\nprint('Hello, world')\n```",
        "1. Item\n2. Item",
        "* Item\n* Item",
        "",
    ]
    raw_descriptions = []
    for description in descriptions:
        raw = deepcopy(base_json)
        raw["fields"]["description"]["content"] = [description]
        raw_descriptions.append(raw)
    return list(zip(parsed_descriptions, raw_descriptions))


@pytest.fixture
def valid_jira_ticket():
    return JiraTicket(
        key="KEY-123",
        created=datetime(2020, 1, 10, 9, 1, 10, tzinfo=tzutc()),
        updated=datetime(2020, 1, 30, 15, 1, 5, tzinfo=tzutc()),
        description="Test description",
        status="Done",
        issue_type="Bug",
        changelog=[
            StatusChange(
                created=datetime(2020, 1, 30, 15, 1, 5, tzinfo=tzutc()),
                status_from="To do",
                status_to="Done",
            )
        ],
    )


@pytest.mark.parametrize("parsed,raw", jira_descriptions())
def test_parse_jira_ticket(parsed, raw):
    assert parse_jira_ticket(raw).description == parsed


def test_parse_json(valid_jira_json, valid_jira_ticket):
    assert parse_json(valid_jira_json) == valid_jira_ticket
