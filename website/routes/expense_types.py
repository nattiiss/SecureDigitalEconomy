from flask import Blueprint, request, jsonify
from services.expense_types_service import ExpenseTypeService
from utils.role_required import role_required

expense_types_bp = Blueprint("expense_types", __name__, url_prefix="/expense-types")


@expense_types_bp.get("/")
@role_required("it","management","customer","event-management","finances")
def get_expense_types():
    types = ExpenseTypeService.get_all()
    return jsonify([
        {"id": t.id, "title": t.title}
        for t in types
    ])


@expense_types_bp.post("/")
@role_required("it","management","customer","event-management","finances")
def create_expense_type():
    data = request.json
    et = ExpenseTypeService.create(data)
    return {"message": "Expense type created", "id": et.id}, 201
