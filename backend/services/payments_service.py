from database import db
from database.models import Payment

class PaymentService:

    @staticmethod
    def get_all():
        return Payment.query.all()

    @staticmethod
    def get_by_id(payment_id):
        return Payment.query.get_or_404(payment_id)

    @staticmethod
    def create(data):
        payment = Payment(
            client_id=data["client_id"],
            amount=data["amount"],
            type_id=data["type_id"],
            date=data["date"],
            invoice_number=data["invoice_number"]
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def update(payment_id, data):
        payment = Payment.query.get_or_404(payment_id)

        payment.client_id = data.get("client_id", payment.client_id)
        payment.amount = data.get("amount", payment.amount)
        payment.type_id = data.get("type_id", payment.type_id)
        payment.date = data.get("date", payment.date)
        payment.invoice_number = data.get("invoice_number", payment.invoice_number)

        db.session.commit()
        return payment

    @staticmethod
    def delete(payment_id):
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return True
