from database import db

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    expense_type_id = db.Column(db.Integer, db.ForeignKey("expense_types.id"))

    event = db.relationship("Event")
    expense_type = db.relationship("ExpenseType")
