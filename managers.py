from typing import Optional

from entities import JiraTicket, get_ticket_status
from models import Ticket, TicketUpdate


def get_jira_ticket_from_key(key: str, session) -> Optional[JiraTicket]:
    """Return a JiraTicket from a given key or None.
    """
    result = (
        session.query(Ticket, TicketUpdate)
        .filter(Ticket.key == key)
        .order_by(TicketUpdate.updated.desc())
        .first()
    )

    if result is not None:
        ticket, ticket_update = result
        return JiraTicket(
            id=ticket.id,
            key=ticket.key,
            status=get_ticket_status(ticket_update.status),
            updated=ticket_update.updated,
            description=ticket.description,
        )
    return None


def persist_jira_ticket(jira_ticket: JiraTicket, session) -> None:
    """Persist a JiraTicket to the Database if there were any changes.

    If nothing changed, this does nothing.
    """
    ticket = Ticket(key=jira_ticket.key, description=jira_ticket.description)
    ticket_update = TicketUpdate(
        ticket=ticket, status=jira_ticket.status.value, updated=jira_ticket.updated,
    )

    if jira_ticket.id is None:
        session.add_all([ticket, ticket_update])
    else:
        ticket_update = (
            session.query(TicketUpdate)
            .filter(TicketUpdate.ticket_id == jira_ticket.id)
            .order_by(TicketUpdate.updated.desc())
            .first()
        )

        if ticket_update.updated != jira_ticket.updated:
            session.add(ticket_update)
