import random
from datetime import datetime, timedelta
from database import db
from database.models import RequestLog


class RequestLogSeedService:

    @staticmethod
    def _get_real_routes(app):
        """
        Extracts real routes from Flask app.url_map.
        Excludes static, inject-control, and dynamic routes.
        """
        routes = []

        EXCLUDED_PREFIXES = (
            "/injects"
        )

        for rule in app.url_map.iter_rules():
            if rule.endpoint == "static":
                continue
            if "<" in rule.rule:
                continue
            if rule.rule.startswith(EXCLUDED_PREFIXES):
                continue

            methods = [m for m in rule.methods if m not in ("HEAD", "OPTIONS")]
            if not methods:
                continue

            routes.append({
                "path": rule.rule,
                "methods": methods
            })

        return routes


    @staticmethod
    def seed_logs(app, count=2500):
        """
        Generates realistic request logs based on real Flask routes.
        """

        routes = RequestLogSeedService._get_real_routes(app)
        if not routes:
            return {"error": "No routes found. Ensure app is created before seeding."}

        # realistic user/role pool (adjust to your project)
        users = [
            {"user_name": None, "role": None},                
            {"user_name": "A1_manager", "role": "user"},
            {"user_name": "OEBB_manager", "role": "user"},
            {"user_name": "management_worker1", "role": "management"},
            {"user_name": "admin1", "role": "it"},
        ]

        # some fake payloads (keep them NON-executable)
        payload_pool = [
            None,
            '{"q":"news"}',
            '{"category":"event","title":"Request for an event","message":"Hello, please ..."}',
            '{"search":"invoice"}'
        ]

        # IP pool
        def random_ip():
            if random.random() < 0.7:
                return f"192.168.1.{random.randint(2, 250)}"
            return f"84.112.{random.randint(0, 255)}.{random.randint(0, 255)}" 

        def random_status(user):
            r = random.random()
            if user["role"] is None and r < 0.15:
                return 401
            if user["role"] not in (None, "it") and r < 0.05:
                return 403
            if r < 0.02:
                return 500
            return 200

        now = datetime.now()
        logs = []

        for i in range(count):
            route = random.choice(routes)

            # prefer GET traffic heavily (normal browsing)
            if "GET" in route["methods"] and random.random() < 0.8:
                method = "GET"
            else:
                method = random.choice(route["methods"])

            user = random.choice(users)
            status = random_status(user)

            # payload: mostly None for GET
            payload = None
            if method in ("POST", "PUT", "PATCH") and random.random() < 0.7:
                payload = random.choice(payload_pool)
            elif random.random() < 0.05:
                payload = random.choice(payload_pool)

            # distribute timestamps across last 7 days
            ts = now - timedelta(
                days=random.randint(0, 6),
                minutes=random.randint(0, 24 * 60)
            )

            logs.append(RequestLog(
                method=method,
                path=route["path"],
                ip_address=random_ip(),
                payload=payload,
                user_name=user["user_name"],
                role=user["role"],
                status_code=status,
                created_at=ts.strftime("%Y-%m-%d %H:%M:%S")
            ))

        db.session.add_all(logs)
        db.session.commit()

        return {
            "message": "Request logs seeded",
            "logs_created": len(logs),
            "routes_used": len(routes)
        }
