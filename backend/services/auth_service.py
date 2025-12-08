from flask import session
from database.models import User
from database import db


class AuthService:

    @staticmethod
    def login(username, password):
        """
        Validates username and password using plaintext lookup.
        Stores user ID inside session.
        Returns user object if valid, otherwise None.
        plaintext passwords, no hashing.
        """
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return None

        # Store user in session (insecure, no flags)
        session["user_id"] = user.id
        return user


    @staticmethod
    def logout():
        """
        Clears session data to 'log out' the user.
        """
        session.pop("user_id", None)


    @staticmethod
    def get_current_user():
        """
        Returns currently logged-in user from session.
        If no user is logged in, returns None.
        """
        user_id = session.get("user_id")
        if not user_id:
            return None
        return User.query.get(user_id)
