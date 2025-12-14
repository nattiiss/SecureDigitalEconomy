from database import db
from sqlalchemy.sql import func

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    registered_date = db.Column(db.Date, server_default=func.current_date())



