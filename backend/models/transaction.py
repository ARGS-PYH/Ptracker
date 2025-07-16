from backend.database import db
from datetime import datetime

class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime)

    #Indexes
    
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='check_positive_amount'),
        db.Index('idx_user_date', 'user_id', 'date'),
        db.Index('idx_category', 'category_id'),
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'description': self.description,
            'date': self.date.isoformat(),
            'user_id': self.user_id,
            'category_id': self.category_id,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
