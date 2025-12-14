from database import db


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(db.String(50))

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))

    amount_total = db.Column(db.Float)

    status = db.Column(
        db.String(20), 
        default="open"
    )  # open | paid | overdue

    issue_date = db.Column(db.String(20))
    due_date = db.Column(db.String(20))

    client = db.relationship("Client", backref="invoices")
    event = db.relationship("Event", backref="invoices")
