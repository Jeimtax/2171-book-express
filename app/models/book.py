from app import db

class Book (db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    

    def __init__(self, title, author, price, condition, grade=None, subject=None):
        self.title = title
        self.author = author
        self.price = price
        self.condition = condition
        self.grade = grade
        self.subject = subject

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'grade': self.grade,
            'subject': self.subject,
            'price': self.price,
            'condition': self.condtion,
            'quantity': self.quantity
        }
        
    

