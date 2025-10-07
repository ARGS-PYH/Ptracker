from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.transaction import Transaction
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

def parse_date(s):
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        return None

@transactions_bp.route('', methods=['GET'])
@jwt_required()
def list_transactions():
    user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id', type=int)

    q = Transaction.query.filter_by(user_id=user_id, is_deleted=False)

    if start_date:
        sd = parse_date(start_date)
        if not sd:
            return jsonify({'error': 'Invalid start_date (YYYY-MM-DD)'}), 400
        q = q.filter(Transaction.date >= sd)
    if end_date:
        ed = parse_date(end_date)
        if not ed:
            return jsonify({'error': 'Invalid end_date (YYYY-MM-DD)'}), 400
        q = q.filter(Transaction.date <= ed)
    if category_id:
        q = q.filter_by(category_id=category_id)

    paginated = q.order_by(Transaction.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = [t.to_dict() for t in paginated.items]

    return jsonify({
        'items': items,
        'page': paginated.page,
        'per_page': paginated.per_page,
        'total': paginated.total,
        'pages': paginated.pages
    }), 200


@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    if 'amount' not in data:
        return jsonify({'error': 'Missing amount'}), 400
    if 'category_id' not in data:
        return jsonify({'error': 'Missing category_id'}), 400

    try:
        amount = float(data['amount'])
    except ValueError:
        return jsonify({'error': 'Invalid amount; must be a number'}), 400

    date_str = data.get('date')
    date_obj = parse_date(date_str) if date_str else datetime.utcnow().date()
    if date_str and not date_obj:
        return jsonify({'error': 'Invalid date (YYYY-MM-DD)'}), 400

    tx = Transaction(
        amount=amount,
        description=data.get('description'),
        date=date_obj,
        category_id=data['category_id'],
        user_id=user_id
    )
    db.session.add(tx)
    db.session.commit()
    return jsonify(tx.to_dict()), 201


@transactions_bp.route('/<int:tx_id>', methods=['PUT'])
@jwt_required()
def update_transaction(tx_id):
    user_id = get_jwt_identity()
    tx = Transaction.query.get(tx_id)
    if not tx or tx.is_deleted:
        return jsonify({'error': 'Transaction not found'}), 404
    if tx.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json() or {}
    if 'amount' in data:
        try:
            tx.amount = float(data['amount'])
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400
    if 'description' in data:
        tx.description = data['description']
    if 'date' in data:
        d = parse_date(data['date'])
        if not d:
            return jsonify({'error': 'Invalid date'}), 400
        tx.date = d
    if 'category_id' in data:
        tx.category_id = data['category_id']

    db.session.commit()
    return jsonify(tx.to_dict()), 200



@transactions_bp.route('/<int:tx_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(tx_id):
    user_id = get_jwt_identity()
    tx = Transaction.query.get(tx_id)
    if not tx or tx.is_deleted:
        return jsonify({'error': 'Transaction not found'}), 404
    if tx.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    tx.soft_delete()
    db.session.commit()
    return jsonify({'message': 'Transaction soft-deleted'}), 200
