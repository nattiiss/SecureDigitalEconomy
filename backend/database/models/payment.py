from database import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float)
    date = db.Column(db.String(20))
    invoice_number = db.Column(db.String(120))

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    type_id = db.Column(db.Integer, db.ForeignKey("payment_types.id"))

    client = db.relationship("Client")
    payment_type = db.relationship("PaymentType")
