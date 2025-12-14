from database import db

class PaymentType(db.Model):
    __tablename__ = "payment_types"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
