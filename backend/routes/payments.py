from flask import Blueprint, request, jsonify
from services.payments_service import PaymentService

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.get("/")
def get_payments():
    payments = PaymentService.get_all()
    return jsonify([
        {
            "id": p.id,
            "client_id": p.client_id,
            "amount": p.amount,
            "type_id": p.type_id,
            "date": p.date,
            "invoice_number": p.invoice_number
        }
        for p in payments
    ])


@payments_bp.get("/<int:payment_id>")
def get_payment(payment_id):
    p = PaymentService.get_by_id(payment_id)
    return {
        "id": p.id,
        "client_id": p.client_id,
        "amount": p.amount,
        "type_id": p.type_id,
        "date": p.date,
        "invoice_number": p.invoice_number
    }


@payments_bp.post("/")
def create_payment():
    data = request.json
    p = PaymentService.create(data)
    return {"message": "Payment created", "id": p.id}, 201


@payments_bp.put("/<int:payment_id>")
def update_payment(payment_id):
    data = request.json
    PaymentService.update(payment_id, data)
    return {"message": "Payment updated"}


@payments_bp.delete("/<int:payment_id>")
def delete_payment(payment_id):
    PaymentService.delete(payment_id)
    return {"message": "Payment deleted"}
