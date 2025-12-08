from flask import Blueprint, request, jsonify
from services.clients_service import ClientService

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.get("/")
def get_clients():
    clients = ClientService.get_all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email} for c in clients])


@clients_bp.get("/<int:id>")
def get_client(id):
    c = ClientService.get_by_id(id)
    return {"id": c.id, "name": c.name, "email": c.email}


@clients_bp.post("/")
def create_client():
    data = request.json
    c = ClientService.create(data)
    return {"message": "Client created", "id": c.id}, 201


@clients_bp.put("/<int:id>")
def update_client(id):
    data = request.json
    ClientService.update(id, data)
    return {"message": "Client updated"}


@clients_bp.delete("/<int:id>")
def delete_client(id):
    ClientService.delete(id)
    return {"message": "Client deleted"}
