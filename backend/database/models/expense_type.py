from database import db

class ExpenseType(db.Model):
    __tablename__ = "expense_types"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
