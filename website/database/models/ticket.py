from database import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    ticket_type_id = db.Column(db.Integer, db.ForeignKey("ticket_types.id"))

    title = db.Column(db.String(200))
    description = db.Column(db.Text)

    status = db.Column(
        db.String(20), 
        default="open"
    )  # open | closed 

    created_at = db.Column(db.String(20))

    # Relationships
    client = db.relationship("Client", backref="tickets")
    ticket_type = db.relationship("TicketType")
