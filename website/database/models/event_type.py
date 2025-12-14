from database import db

class EventType(db.Model):
    __tablename__ = "event_types"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
