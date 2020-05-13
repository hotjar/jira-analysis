import arrow
import attr

from typing import Any, Dict, List, Optional, TypeVar, Type
from datetime import datetime

T = TypeVar("T", bound="Parent")


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

    @classmethod
    def from_jira_ticket(cls: Type[T], ticket_dict: Dict[str, Dict[str, Any]]) -> T:
        changelog = []
        for item in ticket_dict["changelog"]["histories"]:
            log = item["items"][0]
            if log["field"] != "status":
                continue
            changelog.append(
                StatusChange(
                    created=arrow.get(item["created"]).datetime,
                    status_from=log["fromString"],
                    status_to=log["toString"],
                )
            )

        return cls(
            key=ticket_dict["key"],
            created=arrow.get(ticket_dict["fields"]["created"]).datetime,
            updated=arrow.get(ticket_dict["fields"]["updated"]).datetime,
            description=_parse_description(ticket_dict["fields"]["description"])
            if ticket_dict["fields"]["description"]
            else "",
            status=ticket_dict["fields"]["status"]["name"],
            changelog=changelog,
        )

    @classmethod
    def from_json(cls: Type[T], ticket_dict: Dict[str, Any]) -> T:
        return cls(
            key=ticket_dict["key"],
            created=arrow.get(ticket_dict["created"]).datetime,
            updated=arrow.get(ticket_dict["updated"]).datetime,
            description=ticket_dict["description"],
            status=ticket_dict["status"],
            changelog=[
                StatusChange(
                    created=arrow.get(cl["created"]).datetime,
                    status_from=cl["status_from"],
                    status_to=cl["status_to"],
                )
                for cl in ticket_dict["changelog"]
            ],
        )


def _parse_description(doc: Dict[str, str]) -> str:
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
        return "\n".join(
            "* {}".format(
                "".join(_parse_description(line) for line in item["content"])
                for item in doc["content"]
            )
        )
    return ""
