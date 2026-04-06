from datetime import datetime
from app import db


class InventoryAdjustment(db.Model):
    """
    Records every manual adjustment made to a Book's quantity.
    Stores the reason, who changed it, the delta, and the resulting quantity.
    """
    __tablename__ = "InventoryAdjustments"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)
    previous_quantity = db.Column(db.Integer, nullable=False)
    new_quantity = db.Column(db.Integer, nullable=False)
    adjustment = db.Column(db.Integer, nullable=False)   # positive = restock, negative = removal
    reason = db.Column(db.String(255), nullable=False)
    adjusted_by = db.Column(db.String(80), nullable=True)   # placeholder for future auth
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship back to Book
    book = db.relationship('Book', backref=db.backref('adjustments', lazy=True))

    def __init__(self, book_id, previous_quantity, new_quantity, reason, adjusted_by=None):
        self.book_id = book_id
        self.previous_quantity = previous_quantity
        self.new_quantity = new_quantity
        self.adjustment = new_quantity - previous_quantity
        self.reason = reason
        self.adjusted_by = adjusted_by

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'previous_quantity': self.previous_quantity,
            'new_quantity': self.new_quantity,
            'adjustment': self.adjustment,
            'reason': self.reason,
            'adjusted_by': self.adjusted_by,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        direction = '+' if self.adjustment >= 0 else ''
        return (
            f'<InventoryAdjustment book_id={self.book_id} '
            f'adjustment={direction}{self.adjustment} reason="{self.reason}">'
        )
