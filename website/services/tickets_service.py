from database.models import Ticket
from database.models.ticket_type import TicketType
from database import db

TICKET_TYPE_MAP = {
    "book": "Book Event",
    "event": "Report Event Issue",
    "tech": "Report Technical Issue"
}

class TicketService:

    @staticmethod
    def create(data, client_id):
        category = data.get("category")

        ticket_type = TicketType.query.filter_by(
            title=TICKET_TYPE_MAP.get(category)
        ).first()

        if not ticket_type:
            raise ValueError("Invalid ticket category")

        ticket = Ticket(
            client_id=client_id,
            ticket_type_id=ticket_type.id,
            title=data["title"],
            description=data.get("message"),
            status="open"
        )

        db.session.add(ticket)
        db.session.commit()
        return ticket


    @staticmethod
    def get_by_client(client_id):
        return Ticket.query.filter_by(client_id=client_id).all()

    @staticmethod
    def get_all():
        return Ticket.query.all()

    @staticmethod
    def update_status(ticket_id, status):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None

        ticket.status = status
        db.session.commit()
        return ticket

    @staticmethod
    def get_event_management_tickets():
        return Ticket.query.join(Ticket.ticket_type).filter(
            TicketType.title.in_(["Book Event", "Report Event Issue"])
        ).all()

    @staticmethod
    def get_it_tickets():
        return Ticket.query.join(Ticket.ticket_type).filter(
            TicketType.title == "Report Technical Issue"
        ).all()

