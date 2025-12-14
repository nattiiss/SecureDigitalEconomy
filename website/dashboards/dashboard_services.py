from database import db
from database.models import Event, Payment, Expense, Client, EventType, PaymentType
from sqlalchemy import func
from sqlalchemy.sql import extract


class DashboardService:

    # MANAGEMENT

    @staticmethod
    def events_per_month():
        """
        Returns number of events per month for 2024 and 2025.
        Output format:
        {
            "2024": {"1": count, "2": count, ...},
            "2025": {"1": count, "2": count, ...}
        }
        """
        result = {"2024": {}, "2025": {}}

        monthly = (
            db.session.query(
                extract("year", Event.date).label("year"),
                extract("month", Event.date).label("month"),
                func.count(Event.id)
            )
            .group_by("year", "month")
            .all()
        )

        for year, month, count in monthly:
            year = int(year)
            month = int(month)

            if year in [2024, 2025]:
                result[str(year)][str(month)] = count

        return result

    @staticmethod
    def profit_per_month():
        """
        Calculates monthly profit for each month in 2024 and 2025.

        Profit = sum(payments.amount) - sum(expenses.amount)

        Output format:
        {
            "2024": { "1": profit, "2": profit, ... },
            "2025": { "1": profit, "2": profit, ... }
        }
        """
        income = (
            db.session.query(
                extract("year", Payment.date).label("year"),
                extract("month", Payment.date).label("month"),
                func.sum(Payment.amount)
            )
            .group_by("year", "month")
            .all()
        )

        expenses = (
            db.session.query(
                extract("year", Expense.date).label("year"),
                extract("month", Expense.date).label("month"),
                func.sum(Expense.amount)
            )
            .group_by("year", "month")
            .all()
        )

        data = {"2024": {}, "2025": {}}

        for y, m, val in income:
            if int(y) in [2024, 2025]:
                data[str(int(y))][str(int(m))] = val

        for y, m, val in expenses:
            if int(y) in [2024, 2025]:
                current = data[str(int(y))].get(str(int(m)), 0)
                data[str(int(y))][str(int(m))] = current - val

        return data

    @staticmethod
    def customers_per_month():
        """
        Counts the number of distinct customers per month based on their events.

        Output format:
        {
            "2024": { "1": number_of_customers, ... },
            "2025": { "1": number_of_customers, ... }
        }

        """
        data = {"2024": {}, "2025": {}}

        rows = (
            db.session.query(
                extract("year", Event.date).label("year"),
                extract("month", Event.date).label("month"),
                Event.client_id
            )
            .group_by("year", "month", Event.client_id)
            .all()
        )

        temp = {}
        for year, month, client in rows:
            year, month = str(int(year)), str(int(month))
            if year not in ["2024", "2025"]:
                continue

            if (year, month) not in temp:
                temp[(year, month)] = set()
            temp[(year, month)].add(client)

        for (year, month), clients in temp.items():
            data[year][month] = len(clients)

        return data

    @staticmethod
    def avg_profit_per_customer():
        """
        Computes the average profit per customer for the year 2025 only.

        Profit per customer = total income from customer - total expenses of customers events

        Output format:
        [
            { "client": "A1 Telekom", "avg_profit": value },
            { "client": "ÖBB", "avg_profit": value },
            ...
        ]
        """
        income = dict(
            db.session.query(
                Payment.client_id,
                func.sum(Payment.amount)
            ).group_by(Payment.client_id).all()
        )

        expenses_rows = (
            db.session.query(
                Event.client_id,
                func.sum(Expense.amount)
            )
            .join(Expense, Expense.event_id == Event.id)
            .group_by(Event.client_id)
            .all()
        )
        expenses = dict(expenses_rows)

        results = []
        for client_id, inc in income.items():
            prof = inc - expenses.get(client_id, 0)
            results.append({
                "client": Client.query.get(client_id).name,
                "avg_profit": prof
            })

        return results

    @staticmethod
    def top_payment_systems():
        """
        Returns the top 3 most frequently used payment methods.

        Output format:
        [
            { "payment_type": "Bank Transfer", "count": number },
            { "payment_type": "Credit Card", "count": number },
            ...
        ]

        """
        rows = (
            db.session.query(
                PaymentType.title,
                func.count(Payment.id).label("count")
            )
            .join(Payment, Payment.type_id == PaymentType.id)
            .group_by(PaymentType.title)
            .order_by(func.count(Payment.id).desc())
            .limit(3)
            .all()
        )

        return [{"payment_type": t, "count": c} for t, c in rows]


    # EVENT MANAGEMENT

    @staticmethod
    def events_per_month_by_type():
        """
        Returns the number of events per month, grouped by event type.

        Output format:
        {
            "Conference": { "1": count, "2": count, ... },
            "Workshop":   { "1": count, "2": count, ... },
            ...
        }

        """
        rows = (
            db.session.query(
                EventType.title,
                extract("month", Event.date).label("month"),
                func.count(Event.id)
            )
            .join(EventType, EventType.id == Event.event_type_id)
            .group_by(EventType.title, "month")
            .all()
        )

        result = {}
        for type_name, month, count in rows:
            month = str(int(month))
            if type_name not in result:
                result[type_name] = {}
            result[type_name][month] = count

        return result

    @staticmethod
    def event_details():
        """
        Returns the detailed event table.

        Output format:
        [
            {
                "title": "Event X",
                "type": "Conference",
                "date": "2025-05-12",
                "budget": 18000,
                "guests": 120
            },
            ...
        ]
        """
        rows = (
            db.session.query(
                Event.title,
                EventType.title,
                Event.date,
                Event.budget,
                Event.guests
            )
            .join(EventType, EventType.id == Event.event_type_id)
            .all()
        )

        return [
            {
                "title": title,
                "type": type,
                "date": date,
                "budget": budget,
                "guests": guests
            }
            for title, type, date, budget, guests in rows
        ]


    @staticmethod
    def top_budgets():
        """
        Returns the top 5 events with the highest budgets.

        Output format:
        [
            { "title": "Innovation Summit", "budget": 30000 },
            ...
        ]
        """
        rows = (
            db.session.query(
                Event.title,
                Event.budget
            )
            .order_by(Event.budget.desc())
            .limit(5)
            .all()
        )

        return [{"title": title, "budget": budget} for title, budget in rows]

    # FINANCE 

    @staticmethod
    def income_per_month():
        """
        Returns total income per month.

        Output format:
        {
            "1": total_income_in_january,
            "2": total_income_in_february,
            ...
        }

        """
        rows = (
            db.session.query(
                extract("month", Payment.date).label("month"),
                func.sum(Payment.amount)
            )
            .group_by("month")
            .all()
        )

        return {str(int(month)): total for month, total in rows}

    @staticmethod
    def expenses_per_month():
        """
        Returns total expenses per month.

        Output format:
        {
            "1": total_expenses_in_january,
            "2": total_expenses_in_february,
            ...
        }
        """
        rows = (
            db.session.query(
                extract("month", Expense.date).label("month"),
                func.sum(Expense.amount)
            )
            .group_by("month")
            .all()
        )

        return {str(int(month)): total for month, total in rows}