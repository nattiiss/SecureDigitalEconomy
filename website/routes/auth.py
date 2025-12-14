from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    """
    POST /auth/login
    Expected JSON:
    { "username": "...", "password": "..." }
    200- success, 401- fail
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = AuthService.login(username, password)

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    })


@auth_bp.post("/logout")
def logout():
    """
    POST /auth/logout
    Clears session info.
    """
    AuthService.logout()
    return {"message": "Logged out"}


@auth_bp.get("/me")
def me():
    """
    GET /auth/me
    Returns info about currently logged-in user.
    """
    user = AuthService.get_current_user()
    if not user:
        return jsonify({"logged_in": False})

    return jsonify({
        "logged_in": True,
        "id": user.id,
        "username": user.username,
    })

