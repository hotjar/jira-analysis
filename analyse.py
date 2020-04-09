from database import get_session
from entities import get_cycle_time
from managers import get_all_jira_tickets

session = get_session()
tickets = get_all_jira_tickets(session)
session.close()

for ticket in tickets:
    print(len(ticket.ticket_log))
    if len(ticket.ticket_log) > 1:
        print(
            "{t.key}: {cycle_time}".format(t=ticket, cycle_time=get_cycle_time(ticket))
        )
