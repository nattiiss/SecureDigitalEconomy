from database import db
from database.models import Event

class EventService:

    @staticmethod
    def get_all():
        return Event.query.all()

    @staticmethod
    def get_by_id(event_id):
        return Event.query.get_or_404(event_id)

    @staticmethod
    def create(data):
        event = Event(
            title=data["title"],
            date=data["date"],
            budget=data["budget"],
            client_id=data["client_id"],
            event_type_id=data["event_type_id"],
            guests=data.get("guests", 0)
        )
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def update(event_id, data):
        event = Event.query.get_or_404(event_id)

        event.title = data.get("title", event.title)
        event.date = data.get("date", event.date)
        event.budget = data.get("budget", event.budget)
        event.client_id = data.get("client_id", event.client_id)
        event.event_type_id = data.get("event_type_id", event.event_type_id)
        event.guests = data.get("guests", event.guests)


        db.session.commit()
        return event

    @staticmethod
    def delete(event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return True
