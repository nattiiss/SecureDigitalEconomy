import random
from database.models import SimulationState, RequestLog, Payment, Ticket, Event, Client, Expense, TicketType,EventBackup,ExpenseBackup,PaymentBackup
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
        count = 30
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

        for i in range(40):
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
        # --- BACKUP FIRST ---
        for p in Payment.query.limit(5).all():
            db.session.add(PaymentBackup(
                payment_id=p.id,
                amount=p.amount
            ))
            p.amount = random.choice([-50000000, 99999999, 0])

        for e in Event.query.limit(3).all():
            db.session.add(EventBackup(
                event_id=e.id,
                date=e.date
            ))
            e.date = random.choice(["1770-01-01", "2099-12-31"])

        for ex in Expense.query.limit(5).all():
            db.session.add(ExpenseBackup(
                expense_id=ex.id,
                amount=ex.amount
            ))
            ex.amount = random.choice([0, 10000000, -3000])

        fake_clients = [
            Client(name="HACKED CLIENT", email=f"hacked{random.randint(1,999)}@evil.stuff"),
            Client(name="UNKNOWN ENTITY", email=f"unknown{random.randint(1,999)}@fake.stuff")
        ]

        db.session.add_all(fake_clients)
        db.session.commit()

    @staticmethod
    def restore_dashboard_values():
        # Restore payments
        for b in PaymentBackup.query.all():
            p = Payment.query.get(b.payment_id)
            if p:
                p.amount = b.amount

        # Restore events
        for b in EventBackup.query.all():
            e = Event.query.get(b.event_id)
            if e:
                e.date = b.date

        # Restore expenses
        for b in ExpenseBackup.query.all():
            ex = Expense.query.get(b.expense_id)
            if ex:
                ex.amount = b.amount

        # Remove fake clients
        Client.query.filter(
            Client.email.like("%@evil.stuff") |
            Client.email.like("%@fake.stuff")
        ).delete(synchronize_session=False)

        # Clear backups
        PaymentBackup.query.delete()
        EventBackup.query.delete()
        ExpenseBackup.query.delete()

        db.session.commit()

        return {"message": "Dashboard values restored"}


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
                    "Hello, we’re interested in booking an event with Next Gen. Please reach out to us at office@erstee.com to discuss availability and details.",
                    "We would like to inquire about hosting an upcoming event. Kindly contact us at pr@aone.com.",
                    "Our team is planning an event and would love to get more information about booking with you. Please email front_desk@eobb.at.",
                    "We’re looking to reserve a date for a corporate event. Please contact management@raiff.com with next steps.",
                    "Could you please confirm availability for an upcoming event? You can reach us at office@reddbull.com.",
                    "We are interested in organizing an event with Next Gen. Please get in touch via office@sparta.com.",
                    "We’d like to request details for booking an event. Please contact us at asist@erste.com.",
                    "Our office is currently planning an event and would appreciate further information. Email us at assistance@rebull.com.",
                    "We are exploring event options and would like to discuss availability. Please reach out to hr@erstebank.at",
                    "Please let us know how to proceed with an event booking. You can contact us at office@erste.at."
                ]),
                status="open",
                created_at=(
                    base_time - timedelta(minutes=random.randint(0, 60))
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
            tickets.append(ticket)

        db.session.add_all(tickets)
        db.session.commit()
