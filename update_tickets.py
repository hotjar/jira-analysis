import arrow
from bs4 import BeautifulSoup

from database import get_session
from entities import JiraTicket, get_ticket_status
from managers import get_jira_ticket_from_key, persist_jira_ticket

with open('./on_jira_board.xml') as f:
    soup = BeautifulSoup(f, 'lxml')


session = get_session()

for item in soup.find_all('item'):
    key = item.key.text
    status = item.status.text
    description = item.description.text
    updated = item.updated.text

    result = get_jira_ticket_from_key(key, session)

    if result is None:
        jira_ticket = JiraTicket(
            id=None,
            key=key,
            status=get_ticket_status(status),
            description=description,
            updated=arrow.get(updated, 'ddd, D MMM YYYY H:mm:ss Z').date(),
            first_updated=arrow.get(updated, 'ddd, D MMM YYYY H:mm:ss Z').date()
        )
    else:
        jira_ticket = result
        print(jira_ticket.key)

    persist_jira_ticket(jira_ticket, session)
    session.commit()
