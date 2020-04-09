from operator import attrgetter
from typing import Any, Dict, List, Optional, Tuple

from entities import (
    JiraTicket,
    JiraWorkLog,
    get_ticket_status,
    get_with_updated_work_log,
)
from models import Ticket, TicketUpdate


def get_all_jira_tickets(session) -> List[JiraTicket]:
    result = (
        session.query(Ticket, TicketUpdate)
        .filter(Ticket.id == TicketUpdate.ticket_id)
        .order_by(Ticket.key, TicketUpdate.updated)
    )

    tickets: Dict[Any, JiraTicket] = {}
    for ticket, ticket_update in result:
        jira_ticket = tickets.get(
            ticket.id,
            JiraTicket(
                id=ticket.id,
                key=ticket.key,
                status=get_ticket_status(ticket_update.status),
                updated=ticket_update.updated,
                description=ticket.description,
                ticket_log=[],
            ),
        )
        work_log = JiraWorkLog(
            id=ticket_update.id,
            updated=ticket_update.updated,
            status=get_ticket_status(ticket_update.status),
        )

        tickets[jira_ticket.id] = get_with_updated_work_log(jira_ticket, work_log)
    return list(sorted(tickets.values(), key=attrgetter("key")))


def get_jira_ticket_from_key(key: str, session) -> Optional[JiraTicket]:
    """Return a JiraTicket from a given key or None.
    """
    result = (
        session.query(Ticket, TicketUpdate)
        .filter(Ticket.key == key, Ticket.id == TicketUpdate.ticket_id)
        .order_by(TicketUpdate.updated)
    )

    base_ticket = None
    work_tickets = []
    for ticket, ticket_update in result:
        if base_ticket is None:
            base_ticket = ticket

        work_tickets.append(
            JiraWorkLog(
                id=ticket_update.id,
                status=get_ticket_status(ticket_update.status),
                updated=ticket_update.updated,
            )
        )
    if base_ticket is not None:
        last_ticket = work_tickets[-1]
        return JiraTicket(
            id=base_ticket.id,
            key=base_ticket.key,
            status=last_ticket.status,
            updated=last_ticket.updated,
            description=base_ticket.description,
            ticket_log=work_tickets,
        )
    return None


def persist_jira_ticket(jira_ticket: JiraTicket, session) -> None:
    """Persist a JiraTicket to the Database if there were any changes.

    If nothing changed, this does nothing.
    """
    if jira_ticket.id is None:
        ticket = Ticket(key=jira_ticket.key, description=jira_ticket.description)
        session.add(ticket)
    else:
        ticket = session.query(Ticket).filter(Ticket.id == jira_ticket.id).one()

    for work_log in jira_ticket.ticket_log:
        if work_log.id is None:
            ticket_update = TicketUpdate(
                ticket=ticket, updated=work_log.updated, status=work_log.status.value
            )
            session.add(ticket_update)
