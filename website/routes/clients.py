from flask import Blueprint, request, jsonify
from services.clients_service import ClientService
from utils.role_required import role_required

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

@clients_bp.get("/")
@role_required("it","management","customer","event-management","finances")
def get_clients():
    clients = ClientService.get_all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "registered_date": c.registered_date.isoformat() if c.registered_date else None
        }
        for c in clients
    ])

@clients_bp.get("/<int:id>")
@role_required("it","management","customer","event-management","finances")
def get_client(id):
    c = ClientService.get_by_id(id)
    return {
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "registered_date": c.registered_date.isoformat() if c.registered_date else None
    }


@clients_bp.post("/")
@role_required("it","management","customer","event-management","finances")
def create_client():
    data = request.json
    c = ClientService.create(data)
    return {"message": "Client created", "id": c.id}, 201


@clients_bp.put("/<int:id>")
@role_required("it","management","customer","event-management","finances")
def update_client(id):
    data = request.json
    ClientService.update(id, data)
    return {"message": "Client updated"}


@clients_bp.delete("/<int:id>")
@role_required("it","management","customer","event-management","finances")
def delete_client(id):
    ClientService.delete(id)
    return {"message": "Client deleted"}
