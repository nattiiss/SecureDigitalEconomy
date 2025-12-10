from app import create_app
from database import db
from database.models import (
    Client, Event, EventType, Payment, PaymentType, Expense, ExpenseType,User
)
import random

def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        event_types = [
            EventType(title="Corporate Event"),
            EventType(title="Team Building"),
            EventType(title="Workshop")
        ]

        payment_types = [
            PaymentType(title="Bank Transfer"),
            PaymentType(title="PayPal"),
            PaymentType(title="Credit Card"),
            PaymentType(title="Cash")
        ]

        expense_types = [
            ExpenseType(title="Catering"),
            ExpenseType(title="Advertising"),
            ExpenseType(title="Equipment")
        ]

        db.session.add_all(event_types + payment_types + expense_types)
        db.session.commit()

        clients = [
            Client(name="A1 Telekom", email="contact@A1.at"),
            Client(name="OEBB Holding", email="office@oebb.at"),
            Client(name="Red Bull GmbH", email="info@redbull.com"),
            Client(name="Erste Bank", email="office@erstebank.at"),
            Client(name="Spar Oesterreich", email="office@spar.at")
        ]

        db.session.add_all(clients)
        db.session.commit()

        # Events
        titles = [
            "Annual Strategy Meeting",
            "Product Launch Event",
            "Safety Conference",
            "Leadership Retreat",
            "Marketing Workshop",
            "Innovation Summit",
            "Customer Appreciation Day"
        ]

        events = []

        for year in [2024, 2025]:
            for month in range(1, 13):  # 1–12 months
                num_events = random.randint(1, 3) 

                for i in range(num_events):
                    event = Event(
                        title=random.choice(titles),
                        date=f"{year}-{month:02d}-{random.randint(1, 28):02d}",
                        budget=random.randint(5000, 30000),
                        guests=random.randint(20, 500),
                        client_id=random.choice(clients).id,
                        event_type_id=random.choice(event_types).id
                    )
                    events.append(event)

        db.session.add_all(events)
        db.session.commit()

        # Payments
        payments = []

        for client in clients:
            for month in range(1, 13):
                amount = random.randint(2000, 15000)
                pay = Payment(
                    client_id=client.id,
                    amount=amount,
                    type_id=random.choice(payment_types).id,
                    date=f"2025-{month:02d}-{random.randint(1, 28):02d}",
                    invoice_number=f"INV-2025-{client.id}{month:02d}{random.randint(100,999)}"
                )
                payments.append(pay)

        db.session.add_all(payments)
        db.session.commit()

        #Expenses
        expenses = []

        for event in events:
            for _ in range(random.randint(1, 3)):
                exp = Expense(
                    event_id=event.id,
                    expense_type_id=random.choice(expense_types).id,
                    amount=random.randint(500, 8000),
                    date=event.date
                )
                expenses.append(exp)

        db.session.add_all(expenses)
        db.session.commit()

        users = [
        User(username="test1", password="test123"),
        User(username="test2", password="test123"),
        ]

        db.session.add_all(users)
        db.session.commit()


        print("Database is filled!")

        #Users and roles
        users = [
            User(username="boss", password="123", role="management"),
            User(username="events", password="123", role="event-management"),
            User(username="finance", password="123", role="finances"),
            User(username="admin", password="123", role="it"),
        ]

        db.session.add_all(users)
        db.session.commit()
        print("User login data is filled!")

# make only once
if __name__ == "__main__":
    seed()
