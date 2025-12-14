from flask import Blueprint, jsonify
from dashboards.dashboard_services import DashboardService
from utils.role_required import role_required


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/management/events-per-month")
@role_required("management")
def events_per_month():
    return jsonify(DashboardService.events_per_month())


@dashboard_bp.get("/management/profit-per-month")
#@role_required("management")
def profit_per_month():
    return jsonify(DashboardService.profit_per_month())


@dashboard_bp.get("/management/customers-per-month")
@role_required("management")
def customers_per_month():
    return jsonify(DashboardService.customers_per_month())


@dashboard_bp.get("/management/avg-profit-per-customer")
@role_required("management")
def avg_profit_per_customer():
    return jsonify(DashboardService.avg_profit_per_customer())


@dashboard_bp.get("/management/top-payment-systems")
@role_required("management")
def top_payment_systems():
    return jsonify(DashboardService.top_payment_systems())


# EVENT MANAGEMENT
@dashboard_bp.get("/events/events-per-month-type")
@role_required("event-management")
def events_per_month_type():
    return jsonify(DashboardService.events_per_month_by_type())


@dashboard_bp.get("/events/event-details")
@role_required("event-management")
def event_details():
    return jsonify(DashboardService.event_details())


@dashboard_bp.get("/events/top-budgets")
@role_required("event-management")
def top_budgets():
    return jsonify(DashboardService.top_budgets())


# FINANCE
@dashboard_bp.get("/finance/income-per-month")
def income_per_month():
    return jsonify(DashboardService.income_per_month())


@dashboard_bp.get("/finance/expenses-per-month")
@role_required("finances")
def expenses_per_month():
    return jsonify(DashboardService.expenses_per_month())
