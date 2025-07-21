from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from backend.database import db
from backend.models.budget import Budget
from backend.models.transaction import Transaction
from backend.services.budget_service import calculate_spending


budget_bp = Blueprint("budget_bp", __name__)


@budget_bp.route("/ping", methods=["GET"])
def ping():
    return {"message": "Budget service is up"}, 200


@budget_bp.route("/api/budgets", methods=["POST"])
@jwt_required()
def create_budget():
    user_id = get_jwt_identity()
    data = request.json

    # Validate input...
    budget = Budget(
        category_id=data["category_id"],
        user_id=user_id,
        amount=data["amount"],
        period=data["period"],
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({"message": "Budget created", "budget": budget.id}), 201


@budget_bp.route("/api/budgets", methods=["GET"])
@jwt_required()
def list_budgets():
    user_id = get_jwt_identity()
    budgets = Budget.query.filter_by(user_id=user_id).all()
    return jsonify(
        [
            {
                "id": b.id,
                "category_id": b.category_id,
                "amount": b.amount,
                "period": b.period,
            }
            for b in budgets
        ]
    )


@budget_bp.route("/api/budgets/<int:budget_id>", methods=["PUT"])
@jwt_required()
def update_budget(budget_id):
    user_id = get_jwt_identity()
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first_or_404()
    data = request.json
    budget.amount = data.get("amount", budget.amount)
    budget.period = data.get("period", budget.period)
    db.session.commit()
    return jsonify({"message": "Budget updated"})


@budget_bp.route("/api/budgets/<int:budget_id>", methods=["DELETE"])
@jwt_required()
def delete_budget(budget_id):
    user_id = get_jwt_identity()
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first_or_404()
    db.session.delete(budget)
    db.session.commit()
    return jsonify({"message": "Budget deleted"})


@budget_bp.route("/api/budgets/status", methods=["GET"])
@jwt_required()
def budget_status():
    user_id = get_jwt_identity()
    budgets = Budget.query.filter_by(user_id=user_id).all()
    status_list = []

    for b in budgets:
        spent = calculate_spending(user_id, b.category_id, b.period)
        status_list.append(
            {
                "budget_id": b.id,
                "category_id": b.category_id,
                "amount_budgeted": b.amount,
                "amount_spent": spent,
                "status": "over" if spent > b.amount else "under",
                "difference": round(spent - b.amount, 2),
            }
        )

    return jsonify(status_list)


def check_alerts(user_id):
    alerts = []
    budgets = Budget.query.filter_by(user_id=user_id).all()
    for b in budgets:
        spent = calculate_spending(user_id, b.category_id, b.period)
        if spent > b.amount:
            alerts.append(f"You've exceeded your budget for category {b.category_id}.")
    return alerts
