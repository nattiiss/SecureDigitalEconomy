from flask import Blueprint, jsonify, session
from services.invoices_service import InvoiceService
from utils.role_required import role_required

invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@invoices_bp.get("/my")
@role_required("customer", "it","event-management")
def my_invoices():
    client_id = session.get("client_id")

    if not client_id:
        return {"error": "Client not linked to user"}, 400

    invoices = InvoiceService.get_open_by_client(client_id)

    return jsonify([
        {
            "id": i.id,
            "invoice_number": i.invoice_number,
            "amount_total": i.amount_total,
            "status": i.status,
            "due_date": i.due_date
        }
        for i in invoices
    ])


@invoices_bp.get("/")
@role_required("customer", "it","event-management")
def all_invoices():
    invoices = InvoiceService.get_all()

    return jsonify([
        {
            "id": i.id,
            "invoice_number": i.invoice_number,
            "client_id": i.client_id,
            "status": i.status,
            "amount_total": i.amount_total
        }
        for i in invoices
    ])


@invoices_bp.post("/<int:invoice_id>/pay")
@role_required("customer", "it","event-management")
def pay_invoice(invoice_id):
    invoice = InvoiceService.mark_paid(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}, 404

    return {"message": "Invoice marked as paid"}
