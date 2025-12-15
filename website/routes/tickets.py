from flask import Blueprint, request, jsonify, session
from services.tickets_service import TicketService
from utils.role_required import role_required

ticket_bp = Blueprint("ticket", __name__, url_prefix="/ticket")

#left this one open for fake booking inject
@ticket_bp.post("/")
def create_ticket():
    data = request.json
    client_id = session.get("client_id")

    ticket = TicketService.create(data, client_id)

    return jsonify({
        "message": "Ticket created",
        "ticket_id": ticket.id,
        "title": ticket.title,
        "status": ticket.status
    }), 201


@ticket_bp.get("/my")
@role_required("customer", "it","event_management","management")
def my_tickets():
    client_id = session.get("client_id")
    tickets = TicketService.get_by_client(client_id)

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "ticket_type": t.ticket_type.title
        }
        for t in tickets
    ])


@ticket_bp.get("/")
@role_required("customer", "it","event_management","management")
def all_tickets():
    tickets = TicketService.get_all()

    return jsonify([
        {
            "id": t.id,
            "client_id": t.client_id,
            "title": t.title,
            "status": t.status,
            "type": t.ticket_type.title
        }
        for t in tickets
    ])


@ticket_bp.put("/<int:ticket_id>/status")
@role_required("customer", "it","event_management","management")
def update_ticket_status(ticket_id):
    data = request.json
    ticket = TicketService.update_status(ticket_id, data["status"])

    if not ticket:
        return {"error": "Ticket not found"}, 404

    return {"message": "Ticket updated"}


@ticket_bp.get("/event-management")
@role_required("customer", "it","event_management","management")
def event_management_tickets():
    tickets = TicketService.get_event_management_tickets()

    return jsonify([
        {
            "id": t.id,
            "type": t.ticket_type.title,
            "title": t.title,
            "description": t.description,
            "status": t.status
        }
        for t in tickets
    ])


@ticket_bp.get("/it")
@role_required("customer", "it","event_management","management")
def it_tickets():
    tickets = TicketService.get_it_tickets()

    return jsonify([
        {
            "id": t.id,
            "type": t.ticket_type.title,
            "title": t.title,
            "description": t.description,
            "status": t.status
        }
        for t in tickets
    ])

