from database import db
from database.models import EventType

class EventTypeService:

    @staticmethod
    def get_all():
        return EventType.query.all()
