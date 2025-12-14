from database.models import Invoice
from database import db


class InvoiceService:

    @staticmethod
    def get_open_by_client(client_id):
        return Invoice.query.filter(
            Invoice.client_id == client_id,
            Invoice.status != "paid"
        ).all()

    @staticmethod
    def get_all():
        return Invoice.query.all()


    #e.g. for the button "Confirm that I paid!"
    @staticmethod
    def mark_paid(invoice_id):
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None

        invoice.status = "paid"
        invoice.amount_paid = invoice.amount_total
        db.session.commit()
        return invoice
