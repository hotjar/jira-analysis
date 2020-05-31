import arrow
import attr

from typing import Any, Dict, List
from datetime import datetime


@attr.s
class StatusChange:
    created: datetime = attr.ib()
    status_from: str = attr.ib()
    status_to: str = attr.ib()


@attr.s
class JiraTicket:
    key: str = attr.ib()
    created: datetime = attr.ib()
    updated: datetime = attr.ib()

    description: str = attr.ib()
    status: str = attr.ib()
    changelog: List[StatusChange] = attr.ib()
    issue_type: str = attr.ib()


def parse_jira_ticket(ticket_dict: Dict[str, Any]) -> JiraTicket:
    changelog = []
    for item in ticket_dict["changelog"]["histories"]:
        for log in item["items"]:
            if log["field"] != "status":
                continue
            changelog.append(
                StatusChange(
                    created=arrow.get(item["created"]).datetime,
                    status_from=log["fromString"],
                    status_to=log["toString"],
                )
            )

    return JiraTicket(
        key=ticket_dict["key"],
        created=arrow.get(ticket_dict["fields"]["created"]).datetime,
        updated=arrow.get(ticket_dict["fields"]["updated"]).datetime,
        description=_parse_description(ticket_dict["fields"]["description"])
        if ticket_dict["fields"]["description"]
        else "",
        status=ticket_dict["fields"]["status"]["name"],
        issue_type=ticket_dict["fields"]["issuetype"]["name"],
        changelog=changelog,
    )


def parse_json(ticket_dict: Dict[str, Any]) -> JiraTicket:
    return JiraTicket(
        key=ticket_dict["key"],
        created=arrow.get(ticket_dict["created"]).datetime,
        updated=arrow.get(ticket_dict["updated"]).datetime,
        description=ticket_dict["description"],
        status=ticket_dict["status"],
        issue_type=ticket_dict["issue_type"],
        changelog=[
            StatusChange(
                created=arrow.get(cl["created"]).datetime,
                status_from=cl["status_from"],
                status_to=cl["status_to"],
            )
            for cl in ticket_dict["changelog"]
        ],
    )


def _parse_description(doc: Dict[str, Any]) -> str:
    if doc["type"] == "doc":
        return "\n".join(_parse_description(item) for item in doc["content"])
    if doc["type"] == "paragraph":
        return "\n\n".join(
            _parse_description(paragraph) for paragraph in doc["content"]
        )
    if doc["type"] == "text":
        return doc["text"]
    if doc["type"] == "heading":
        return "{} {}".format(
            "#" * doc["attrs"]["level"],
            "".join(_parse_description(text) for text in doc["content"]),
        )
    if doc["type"] == "link":
        return "[{}]({})".format(
            "".join(_parse_description(text) for text in doc["content"]),
            doc["attrs"]["href"],
        )
    if doc["type"] == "hardBreak":
        return "---"
    if doc["type"] == "mention":
        return "@{}".format(doc["attrs"]["text"])
    if doc["type"] == "codeBlock":
        return "```{}\n{}\n```".format(
            doc["attrs"].get("language", ""),
            "\n".join(_parse_description(text) for text in doc["content"]),
        )
    if doc["type"] == "orderedList":
        items = []
        for i, item in enumerate(doc["content"], start=1):
            items.append(
                "{}. {}".format(
                    i, "".join(_parse_description(line) for line in item["content"])
                )
            )
        return "\n".join(items)
    if doc["type"] == "unorderedList":
        items = []
        for item in doc["content"]:
            items.append(
                "* {}".format(
                    "".join(_parse_description(line) for line in item["content"])
                )
            )
        return "\n".join(items)
    return ""
