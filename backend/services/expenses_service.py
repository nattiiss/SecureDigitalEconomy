from database import db
from database.models import Expense

class ExpenseService:

    @staticmethod
    def get_all():
        return Expense.query.all()

    @staticmethod
    def get_by_id(expense_id):
        return Expense.query.get_or_404(expense_id)

    @staticmethod
    def create(data):
        expense = Expense(
            event_id=data["event_id"],
            expense_type_id=data["expense_type_id"],
            amount=data["amount"],
            date=data["date"]
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def update(expense_id, data):
        expense = Expense.query.get_or_404(expense_id)

        expense.event_id = data.get("event_id", expense.event_id)
        expense.expense_type_id = data.get("expense_type_id", expense.expense_type_id)
        expense.amount = data.get("amount", expense.amount)
        expense.date = data.get("date", expense.date)

        db.session.commit()
        return expense

    @staticmethod
    def delete(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return True
