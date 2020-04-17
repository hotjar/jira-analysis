import arrow
import attr
from bs4 import BeautifulSoup

from database import get_session
from entities import (
    JiraTicket,
    JiraWorkLog,
    get_ticket_status,
    get_with_updated_work_log,
)
from managers import get_jira_ticket_from_key, persist_jira_ticket
from jira.get_issue import get_issue


def get_from_jira():
    issue = get_issue("ATV-72")
    print(issue)


def load_from_file(file_handle):
    return BeautifulSoup(file_handle, "lxml")


def persist_to_database(soup):
    session = get_session()

    for item in soup.find_all("item"):
        key = item.key.text
        status = item.status.text
        description = item.description.text
        updated = item.updated.text

        result = get_jira_ticket_from_key(key, session)

        work_log = JiraWorkLog(
            status=get_ticket_status(status),
            updated=arrow.get(updated, "ddd, D MMM YYYY H:mm:ss Z").date(),
        )
        attr.validate(work_log)

        if result is None:
            jira_ticket = JiraTicket(
                key=key,
                status=work_log.status,
                description=description,
                updated=work_log.updated,
                ticket_log=[],
            )
            attr.validate(jira_ticket)
        else:
            jira_ticket = result

        updated_ticket = get_with_updated_work_log(jira_ticket, work_log)
        persist_jira_ticket(updated_ticket, session)

    session.commit()
    session.close()
