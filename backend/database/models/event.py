from database import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date = db.Column(db.String(20))
    budget = db.Column(db.Integer)
    guests = db.Column(db.Integer)

    event_type_id = db.Column(db.Integer, db.ForeignKey("event_types.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    event_type = db.relationship("EventType")
    client = db.relationship("Client")
