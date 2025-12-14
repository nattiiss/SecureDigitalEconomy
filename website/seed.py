from app import create_app
from database import db
from database.models import (
    Client, Event, EventType, Payment, PaymentType, Expense, ExpenseType,User, Invoice, Ticket, TicketType, SimulationState
)
import random
from datetime import datetime, timedelta

def random_date(start_year=2024, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

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
            Client(name="A1 Telekom", email="contact@A1.at", registered_date=random_date().date()),
            Client(name="OEBB Holding", email="office@oebb.at", registered_date=random_date().date()),
            Client(name="Red Bull GmbH", email="info@redbull.com", registered_date=random_date().date()),
            Client(name="Erste Bank", email="office@erstebank.at", registered_date=random_date().date()),
            Client(name="Spar Oesterreich", email="office@spar.at", registered_date=random_date().date())
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
            User(username="customer", password="123", role="customer")
           
        ]

        db.session.add_all(users)
        db.session.commit()
        print("User login data is filled!")

        ticket_types = [
        TicketType(title="Book Event"),
        TicketType(title="Report Issue")
        ]

        db.session.add_all(ticket_types)
        db.session.commit()

        invoices = [
            Invoice(
                invoice_number="INV-2025-001",
                client_id=clients[0].id,
                event_id=events[0].id,
                amount_total=12000,
                status="open",
                issue_date="2025-03-01",
                due_date="2025-03-31"
            ),
            Invoice(
                invoice_number="INV-2025-002",
                client_id=clients[1].id,
                event_id=events[1].id,
                amount_total=18000,
                status="paid",
                issue_date="2025-02-01",
                due_date="2025-02-28"
            ),
            Invoice(
                invoice_number="INV-2025-003",
                client_id=clients[2].id,
                event_id=None,
                amount_total=7500,
                status="open",
                issue_date="2025-04-10",
                due_date="2025-04-30"
            )
        ]

        db.session.add_all(invoices)
        db.session.commit()

        tickets = [
            Ticket(
                client_id=clients[0].id,
                ticket_type_id=ticket_types[0].id,
                title="Request new strategy workshop",
                description="We would like to organize a workshop in June for our management team.",
                status="open",
                created_at="2025-04-12"
            ),
            Ticket(
                client_id=clients[1].id,
                ticket_type_id=ticket_types[1].id,
                title="Incorrect budget shown in dashboard",
                description="The dashboard shows a wrong budget for our last event. Please investigate.",
                status="open",
                created_at="2025-04-14"
            ),
            Ticket(
                client_id=clients[2].id,
                ticket_type_id=ticket_types[1].id,
                title="Invoice amount seems incorrect",
                description="The invoice amount does not match our agreement.",
                status="in_progress",
                created_at="2025-04-15"
            )
        ]

        db.session.add_all(tickets)
        db.session.commit()

        sim_states = [
            SimulationState(name="defaced_index.html")
            ]
        
        db.session.add_all(sim_states)
        db.session.commit()
        print("Simulation State data is filled!")


# make only once
if __name__ == "__main__":
    seed()
