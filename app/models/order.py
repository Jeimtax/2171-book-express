from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Suppliers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=True)
    items = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    supplier = db.relationship('Supplier', back_populates='orders')
    book = db.relationship('Book', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier': self.supplier.to_dict() if self.supplier else None,
            'book': self.book.to_dict() if self.book else None,
            'book_id': self.book_id,
            'items': self.items,
            'title': self.title,
            'author': self.author,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return (
            f'<Order {self.id} supplier_id={self.supplier_id} '
            f'book_id={self.book_id} title={self.title!r} quantity={self.quantity}>'
        )
