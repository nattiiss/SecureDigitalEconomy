from flask import Blueprint, jsonify
from dashboards.dashboard_services import DashboardService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/management/events-per-month")
def events_per_month():
    return jsonify(DashboardService.events_per_month())


@dashboard_bp.get("/management/profit-per-month")
def profit_per_month():
    return jsonify(DashboardService.profit_per_month())


@dashboard_bp.get("/management/customers-per-month")
def customers_per_month():
    return jsonify(DashboardService.customers_per_month())


@dashboard_bp.get("/management/avg-profit-per-customer")
def avg_profit_per_customer():
    return jsonify(DashboardService.avg_profit_per_customer())


@dashboard_bp.get("/management/top-payment-systems")
def top_payment_systems():
    return jsonify(DashboardService.top_payment_systems())


# EVENT MANAGEMENT
@dashboard_bp.get("/events/events-per-month-type")
def events_per_month_type():
    return jsonify(DashboardService.events_per_month_by_type())


@dashboard_bp.get("/events/event-details")
def event_details():
    return jsonify(DashboardService.event_details())


@dashboard_bp.get("/events/top-budgets")
def top_budgets():
    return jsonify(DashboardService.top_budgets())


# FINANCE
@dashboard_bp.get("/finance/income-per-month")
def income_per_month():
    return jsonify(DashboardService.income_per_month())


@dashboard_bp.get("/finance/expenses-per-month")
def expenses_per_month():
    return jsonify(DashboardService.expenses_per_month())
