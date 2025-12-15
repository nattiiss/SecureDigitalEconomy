from flask import Blueprint, request, jsonify
from services.expenses_service import ExpenseService
from utils.role_required import role_required

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.get("/")
@role_required("it","management","customer","event-management","finances")
def get_expenses():
    expenses = ExpenseService.get_all()
    return jsonify([
        {
            "id": e.id,
            "event_id": e.event_id,
            "expense_type_id": e.expense_type_id,
            "amount": e.amount,
            "date": e.date
        }
        for e in expenses
    ])


@expenses_bp.get("/<int:expense_id>")
@role_required("it","management","customer","event-management","finances")
def get_expense(expense_id):
    e = ExpenseService.get_by_id(expense_id)
    return {
        "id": e.id,
        "event_id": e.event_id,
        "expense_type_id": e.expense_type_id,
        "amount": e.amount,
        "date": e.date
    }


@expenses_bp.post("/")
@role_required("it","management","customer","event-management","finances")
def create_expense():
    data = request.json
    e = ExpenseService.create(data)
    return {"message": "Expense created", "id": e.id}, 201


@expenses_bp.put("/<int:expense_id>")
@role_required("it","management","customer","event-management","finances")
def update_expense(expense_id):
    data = request.json
    ExpenseService.update(expense_id, data)
    return {"message": "Expense updated"}


@expenses_bp.delete("/<int:expense_id>")
@role_required("it","management","customer","event-management","finances")
def delete_expense(expense_id):
    ExpenseService.delete(expense_id)
    return {"message": "Expense deleted"}
