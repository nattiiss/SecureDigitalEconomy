from database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))   # plain text is OK for this assignment
    role = db.Column(db.String(50))        # management, event-management, finances, it
