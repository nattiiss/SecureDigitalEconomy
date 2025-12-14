from database.models import Ticket
from database import db


class TicketService:

    @staticmethod
    def create(data, client_id):
        ticket = Ticket(
            client_id=client_id,
            ticket_type_id=data["ticket_type_id"],
            title=data["title"],
            description=data["description"],
            status="open",
            created_at=data.get("created_at")
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
