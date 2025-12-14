from database import db
from database.models import ExpenseType

class ExpenseTypeService:

    @staticmethod
    def get_all():
        return ExpenseType.query.all()

    @staticmethod
    def create(data):
        et = ExpenseType(title=data["title"])
        db.session.add(et)
        db.session.commit()
        return et
