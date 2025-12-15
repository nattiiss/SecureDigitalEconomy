from flask import Blueprint, jsonify
from services.event_types_service import EventTypeService
from utils.role_required import role_required

event_types_bp = Blueprint("event_types", __name__, url_prefix="/event-types")


@event_types_bp.get("/")
@role_required("it","management","customer","event-management","finances")
def get_event_types():
    types = EventTypeService.get_all()
    return jsonify([
        {"id": t.id, "title": t.title}
        for t in types
    ])

