from flask import Blueprint
from services.inject_service import InjectService

injects_bp = Blueprint("injects", __name__, url_prefix="/injects")

@injects_bp.post("/activate/xss")
def start_i1():
    InjectService.simulate_logs_xss()
    return {"message": "Inject xss activated"}

@injects_bp.post("/activate/mitm")
def start_i2():
    InjectService.simulate_logs_mitm()
    return {"message": "Inject mitm activated"}

@injects_bp.post("/activate/defaced_about")
def start_i3():
    InjectService.activate("defaced_about.html")
    return {"message": "Inject defaced_about.html activated"}

@injects_bp.post("/deactivate/defaced_about")
def stop_i3():
    InjectService.deactivate("defaced_about.html")
    return {"message": "Inject defaced_about.html deactivated"}

@injects_bp.post("/activate/defaced_home")
def start_i4():
    InjectService.activate("defaced_index.html")
    return {"message": "Inject defaced_index.html activated"}

@injects_bp.post("/deactivate/defaced_home")
def stop_i4():
    InjectService.deactivate("defaced_index.html")
    return {"message": "Inject defaced_index.html deactivated"}

@injects_bp.post("/activate/defaced_invoices")
def start_i5():
    InjectService.activate("defaced_invoices.html")
    return {"message": "Inject defaced_invoices.html activated"}

@injects_bp.post("/deactivate/defaced_invoices")
def stop_i5():
    InjectService.deactivate("defaced_invoices.html")
    return {"message": "Inject defaced_invoices.html deactivated"}

@injects_bp.post("/activate/defaced_dashboard")
def start_i6():
    InjectService.change_dashboard_values()
    return {"message": "Inject defaced_dashboard activated"}

@injects_bp.post("/activate/multiple_bookings")
def start_i7():
    InjectService.make_fake_bookings()
    return {"message": "Inject multiple_bookings activated"}

@injects_bp.post("/activate/defaced_tickets")
def start_i8():
    InjectService.activate("defaced_tickets.html")
    return {"message": "Inject defaced_tickets.html activated"}

@injects_bp.post("/deactivate/defaced_tickets")
def stop_i8():
    InjectService.deactivate("defaced_tickets.html")
    return {"message": "Inject defaced_tickets.html deactivated"}