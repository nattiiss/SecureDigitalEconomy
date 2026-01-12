from database import db

class PaymentBackup(db.Model):
    __tablename__ = "payments_backup"

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer)
    amount = db.Column(db.Float)


class EventBackup(db.Model):
    __tablename__ = "events_backup"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    date = db.Column(db.String(20))


class ExpenseBackup(db.Model):
    __tablename__ = "expenses_backup"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
