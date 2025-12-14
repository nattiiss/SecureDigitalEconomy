from flask import Blueprint
from services.inject_service import InjectService
from utils.role_required import role_required

injects_bp = Blueprint("injects", __name__, url_prefix="/injects")


@injects_bp.post("/activate/i1")
def start_i1():
    InjectService.activate("defaced_index.html")
    return {"message": "Inject defaced_index.html activated"}

@injects_bp.post("/deactivate/i1")
@role_required("it")
def stop_i1():
    InjectService.deactivate("defaced_index.html")
    return {"message": "Inject defaced_index.html deactivated"}


@injects_bp.post("/activate/i2")
@role_required("it") # replace with admin 
def start_i2():
    InjectService.activate("inject2")
    return {"message": "Inject i2 activated"}

@injects_bp.post("/deactivate/i2")
@role_required("it")
def stop_i2():
    InjectService.deactivate("inject2")
    return {"message": "Inject i2 deactivated"}