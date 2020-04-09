from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    description = Column(String)

    def __repr__(self):
        return "<Ticket(key={s.key})>".format(s=self)


class TicketUpdate(Base):
    __tablename__ = "ticket_update"
    __table_args__ = (UniqueConstraint("ticket_id", "status"),)

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id", name="fk_ticket"))
    status = Column(String)
    updated = Column(Date)

    ticket = relationship(Ticket, primaryjoin=ticket_id == Ticket.id, post_update=True)

    def __repr__(self):
        return "<TicketUpdate(ticket_id={s.ticket_id}, status={s.status}>".format(
            s=self
        )
