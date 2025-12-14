from flask import Blueprint, request, jsonify, session
from services.tickets_service import Ticket
from utils.role_required import role_required
ticket_bp = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket_bp.post("/ticket")
@role_required("user")
def create_ticket():
    data = request.json
    client_id = session.get("client_id")

    ticket = Ticket.create(data, client_id)

    return jsonify({
        "message": "Ticket created",
        "ticket_id": ticket.id
    })


@ticket_bp.get("/my")
@role_required("user")
def my_tickets():
    client_id = session.get("client_id")
    tickets = Ticket.get_by_client(client_id)

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "ticket_type_id": t.ticket_type_id
        }
        for t in tickets
    ])


@ticket_bp.get("/")
@role_required("management")
def all_tickets():
    tickets = Ticket.get_all()

    return jsonify([
        {
            "id": t.id,
            "client_id": t.client_id,
            "title": t.title,
            "status": t.status
        }
        for t in tickets
    ])


@ticket_bp.put("/<int:ticket_id>/status")
@role_required("management")
def update_ticket_status(ticket_id):
    data = request.json
    ticket = Ticket.update_status(ticket_id, data["status"])

    if not ticket:
        return {"error": "Ticket not found"}, 404

    return {"message": "Ticket updated"}
