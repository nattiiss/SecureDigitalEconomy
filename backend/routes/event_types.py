from flask import Blueprint, jsonify
from services.event_types_service import EventTypeService

event_types_bp = Blueprint("event_types", __name__, url_prefix="/event-types")


@event_types_bp.get("/")
def get_event_types():
    types = EventTypeService.get_all()
    return jsonify([
        {"id": t.id, "title": t.title}
        for t in types
    ])

