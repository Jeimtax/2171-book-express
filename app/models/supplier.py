from app import db


class Supplier(db.Model):
    __tablename__ = 'Suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Order', back_populates='supplier', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
        }

    def __repr__(self):
        return f'<Supplier {self.id} {self.name}>'
