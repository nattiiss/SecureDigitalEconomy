from flask import session
from database.models.user import User
from database import db

class AuthService:

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return None

        # store in session
        session["user_id"] = user.id
        session["role"] = user.role

        if hasattr(user, "client_id") and user.client_id:
            session["client_id"] = user.client_id

        return user

    @staticmethod
    def get_current_user():
        user_id = session.get("user_id")
        if not user_id:
            return None
        return User.query.get(user_id)

    @staticmethod
    def logout():
        session.clear()
