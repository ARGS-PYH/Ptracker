# services/budget_service.py
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.database import db
from backend.models.transaction import Transaction


def calculate_spending(user_id, category_id, period):
    now = datetime.utcnow()

    if period == "monthly":
        start = datetime(now.year, now.month, 1)
    elif period == "weekly":
        start = now - timedelta(days=now.weekday())  # Monday start
    else:
        return 0

    total = (
        db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.category_id == category_id,
            Transaction.created_at >= start,
        )
        .scalar()
    )

    return total
