from flask import Blueprint, request, jsonify
from services.payment_types_service import PaymentTypeService
from utils.role_required import role_required

payment_types_bp = Blueprint("payment_types", __name__, url_prefix="/payment-types")


@payment_types_bp.get("/")
@role_required("it","management","customer","event-management","finances")
def get_payments_types():
    types = PaymentTypeService.get_all()
    return jsonify([
        {"id": t.id, "title": t.title}
        for t in types
    ])


@payment_types_bp.post("/")
@role_required("it","management","customer","event-management","finances")
def create_payment_type():
    data = request.json
    pt = PaymentTypeService.create(data)
    return {"message": "Payment type created", "id": pt.id}, 201
