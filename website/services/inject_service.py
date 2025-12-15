import random
from database.models import SimulationState, RequestLog, Payment, Ticket, Event, Client, Expense, TicketType
from datetime import datetime, timedelta
from database import db



class InjectService:

    @staticmethod
    def is_active(name):
        state = SimulationState.query.filter_by(name=name).first()
        return state and state.state == 1

    @staticmethod
    def activate(name):
        state = SimulationState.query.filter_by(name=name).first()
        if state:
            state.state = 1
            db.session.commit()

    @staticmethod
    def deactivate(name):
        state = SimulationState.query.filter_by(name=name).first()
        if state:
            state.state = 0
            db.session.commit()

    @staticmethod
    def deactivate_all():
        SimulationState.query.update({SimulationState.state: 0})
        db.session.commit()

    @staticmethod
    def simulate_logs_xss():
        count = 10
        xss_payloads = [
           "&lt;script&gt;alert('XSS')&lt;/script&gt;",
            "&lt;img src=x onerror=alert(1)&gt;",
            "&lt;svg onload=alert('xss')&gt;",
            "\"&gt;&lt;script&gt;alert(document.cookie)&lt;/script&gt;",
            "[XSS_ATTEMPT] fetch(document.cookie)"
        ]

        paths = [
            "/ticket",
            "/dashboard",
            "/contact",
            "/dashboard/finance",
            "/about"
        ]

        methods = ["POST", "GET"]
        roles = [None, "it"]
        users = ["management_worker1","events_worker2","finance_worker2"]

        base_time = datetime.now()

        logs = []

        for i in range(count):
            log = RequestLog(
                method=random.choice(methods),
                path=random.choice(paths),
                ip_address=f"192.168.1.{random.randint(20, 200)}",
                payload=random.choice(xss_payloads),
                user_name=random.choice(users),
                role=random.choice(roles),
                status_code=200,
                created_at=(
                    base_time - timedelta(minutes=random.randint(1, 15))
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )

            logs.append(log)

        db.session.add_all(logs)
        db.session.commit()

    @staticmethod
    def simulate_logs_mitm():
        suspicious_ip = f"10.0.0.{random.randint(50, 90)}" 

        paths = [
            "/dashboard/finance/income-per-month",
            "/dashboard/events/event-details",
            "/invoices/my",
            "/payments",
        ]

        roles = ["management"]
        users = ["management_worker1","events_worker2","finance_worker2"]

        base_time = datetime.now()
        logs = []

        for i in range(10):
            log = RequestLog(
                method="GET",
                path=random.choice(paths),
                ip_address=suspicious_ip,  # SAME IP for many requests
                payload=None,
                user_name=random.choice(users),
                role=random.choice(roles),
                status_code=200,
                created_at=(
                    base_time - timedelta(minutes=i * random.randint(1, 3))
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )
            logs.append(log)

        db.session.add_all(logs)
        db.session.commit()



    @staticmethod
    def change_dashboard_values():
        payments = Payment.query.limit(5).all()
        for p in payments:
            p.amount = random.choice([
                -50000000,   
                99999999,   
                0
            ])

        events = Event.query.limit(3).all()
        for e in events:
            e.date = random.choice([
                "1770-01-01",
                "2099-12-31"
            ])

        expenses = Expense.query.limit(5).all()
        for ex in expenses:
            ex.amount = random.choice([
                0,
                10000000,
                -3000
            ])

        fake_clients = [
            Client(name="HACKED CLIENT", email=f"hacked{random.randint(1,999)}@evil.stuff"),
            Client(name="UNKNOWN ENTITY", email=f"unknown{random.randint(1,999)}@fake.stuff")
        ]

        db.session.add_all(fake_clients)
        db.session.commit()

    @staticmethod
    def make_fake_bookings():
        book_event_type = TicketType.query.filter_by(title="Book Event").first()

        clients = Client.query.limit(5).all()

        base_time = datetime.now()
        count = random.randint(20, 30)

        tickets = []

        for i in range(count):
            ticket = Ticket(
                client_id=None,
                ticket_type_id=book_event_type.id,
                title=random.choice([
                    "Event booking request",
                    "Request to book corporate event",
                    "Conference booking",
                    "Workshop booking inquiry"
                ]),
                description=random.choice([
                    "We would like to book an event as soon as possible.",
                    "Please confirm availability for an event.",
                    "Booking request for upcoming corporate event.",
                    "Automated booking request."
                ]),
                status="open",
                created_at=(
                    base_time - timedelta(minutes=random.randint(0, 60))
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
            tickets.append(ticket)

        db.session.add_all(tickets)
        db.session.commit()
