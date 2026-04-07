from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Suppliers.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    supplier = db.relationship('Supplier', back_populates='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier': self.supplier.to_dict() if self.supplier else None,
            'items': self.items,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Order {self.id} supplier_id={self.supplier_id}>'
