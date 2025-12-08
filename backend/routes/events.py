from flask import Blueprint, request, jsonify
from services.events_service import EventService

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.get("/")
def get_events():
    events = EventService.get_all()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "date": e.date,
            "budget": e.budget,
            "client_id": e.client_id,
            "event_type_id": e.event_type_id
        }
        for e in events
    ])


@events_bp.get("/<int:event_id>")
def get_event(event_id):
    e = EventService.get_by_id(event_id)
    return {
        "id": e.id,
        "title": e.title,
        "date": e.date,
        "budget": e.budget,
        "client_id": e.client_id,
        "event_type_id": e.event_type_id
    }


@events_bp.post("/")
def create_event():
    data = request.json
    e = EventService.create(data)
    return {"message": "Event created", "id": e.id}, 201


@events_bp.put("/<int:event_id>")
def update_event(event_id):
    data = request.json
    EventService.update(event_id, data)
    return {"message": "Event updated"}


@events_bp.delete("/<int:event_id>")
def delete_event(event_id):
    EventService.delete(event_id)
    return {"message": "Event deleted"}
