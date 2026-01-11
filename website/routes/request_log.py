from flask import Blueprint, jsonify
from services.request_log_service import RequestLogService
from utils.role_required import role_required

request_logs_bp = Blueprint(
    "request_logs",
    __name__,
    url_prefix="/request-logs"
)


@request_logs_bp.get("/")
@role_required("management", "it","event-management")
def get_logs():
    """
    Returns all request logs for SOC / management dashboard.
    """
    logs = RequestLogService.get_all()

    return jsonify([
        {
            "id": l.id,
            "method": l.method,
            "path": l.path,
            "ip_address": l.ip_address,
            "payload": l.payload,
            "user_name": l.user_name,
            "role": l.role,
            "status_code": l.status_code,
            "created_at": l.created_at,
        }
        for l in logs
    ])
