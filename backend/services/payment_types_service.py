from database import db
from database.models import PaymentType

class PaymentTypeService:

    @staticmethod
    def get_all():
        return PaymentType.query.all()

    @staticmethod
    def create(data):
        pt = PaymentType(title=data["title"])
        db.session.add(pt)
        db.session.commit()
        return pt
