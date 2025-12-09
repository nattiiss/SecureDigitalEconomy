from flask import Flask, render_template
from database import db
from routes.clients import clients_bp
from routes.events import events_bp
from routes.event_types import event_types_bp
from routes.payments import payments_bp
from routes.payment_types import payment_types_bp
from routes.expenses import expenses_bp
from routes.expense_types import expense_types_bp
from routes.auth import auth_bp
import os

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

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


    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/dashboard/")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/login")
    def login():
        return render_template("login.html")



    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)
