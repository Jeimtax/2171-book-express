from app.extensions import db

class Book (db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_quantity = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, title, author, price, condition, grade=None, subject=None, quantity=0, min_quantity=0):
        self.title = title
        self.author = author
        self.price = price
        self.condition = condition
        self.grade = grade
        self.subject = subject
        self.quantity = quantity
        self.min_quantity = min_quantity

    @property
    def is_low_stock(self):
        try:
            return self.quantity <= self.min_quantity
        except Exception:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'grade': self.grade,
            'subject': self.subject,
            'price': self.price,
            'condition': self.condition,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'is_low_stock': self.is_low_stock
        }
        
    

