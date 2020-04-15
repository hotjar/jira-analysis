from database import get_session
from entities import get_cycle_time
from managers import get_all_jira_tickets


def analyse():
    session = get_session()
    tickets = get_all_jira_tickets(session)
    session.close()

    for ticket in tickets:
        if len(ticket.ticket_log) > 1:
            if ticket.done:
                cycle_time = get_cycle_time(ticket)
                if cycle_time is not None:
                    print(
                        "{t.key}: {cycle_time}".format(
                            t=ticket, cycle_time=get_cycle_time(ticket)
                        )
                    )
                else:
                    print(
                        "{t.key}: {start.status} -> {t.status}".format(
                            t=ticket, start=ticket.ticket_log[0]
                        )
                    )
            else:
                print("{t.key}: {t.status}".format(t=ticket))
