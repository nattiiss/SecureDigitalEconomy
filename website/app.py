from flask import Flask, render_template, request, session
from database import db
from datetime import datetime
from routes.clients import clients_bp
from routes.events import events_bp
from routes.event_types import event_types_bp
from routes.payments import payments_bp
from routes.payment_types import payment_types_bp
from routes.expenses import expenses_bp
from routes.expense_types import expense_types_bp
from routes.auth import auth_bp
from dashboards.dashboards_routes import dashboard_bp
from routes.invoices import invoices_bp
from routes.tickets import ticket_bp
from routes.injects import injects_bp
from routes.request_log import request_logs_bp
from services.inject_service import InjectService
from database.models.request_logs import RequestLog
import os

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    app.secret_key = "super_secret_key_123"   # REQUIRED for session to work!

    db_path = os.path.join(os.path.dirname(__file__), "database", "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.register_blueprint(clients_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(event_types_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(payment_types_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(expense_types_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(injects_bp)
    app.register_blueprint(request_logs_bp)


    @app.route("/")
    def index():
        if InjectService.is_active("defaced_index.html"):
            return render_template("defaced_index.html") # here should be some defaced html
        return render_template("index.html")
    
    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/login")
    def login():
        return render_template("login.html")
    
    @app.after_request
    def global_request_logger(response):
        try:
            log = RequestLog(
                method=request.method,
                path=request.path,
                ip_address=request.remote_addr,
                payload=str(request.get_json(silent=True)),
                user_id=session.get("user_id"),
                role=session.get("role"),
                status_code=response.status_code,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                defaced_flag=0
            )

            db.session.add(log)
            db.session.commit()
        except Exception:
            pass

        return response


    @app.route("/invoices")
    def invoices():
        return render_template("invoices.html")

    @app.route("/tickets")
    def tickets():
        return render_template("tickets.html")


    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)
