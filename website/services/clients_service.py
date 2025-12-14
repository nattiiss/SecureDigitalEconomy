from database import db
from database.models import Client

class ClientService:

    @staticmethod
    def get_all():
        return Client.query.all()

    @staticmethod
    def get_by_id(client_id):
        return Client.query.get_or_404(client_id)

    @staticmethod
    def create(data):
        client = Client(
            name=data["name"],
            email=data["email"],
            registered_date=data.get("registered_date")
        )

        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def update(client_id, data):
        client = Client.query.get_or_404(client_id)

        client.name = data.get("name", client.name)
        client.email = data.get("email", client.email)

        # DO NOT overwrite registered_date unless user explicitly sends a value
        if "registered_date" in data:
            client.registered_date = data["registered_date"]

        db.session.commit()
        return client

    @staticmethod
    def delete(client_id):
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return True
