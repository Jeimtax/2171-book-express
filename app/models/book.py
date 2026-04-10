from app import db

class Book (db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    

    def __init__(self, title, author, price, grade, subject, quantity=1):
        self.title = title
        self.author = author
        self.price = price
        self.grade = grade
        self.subject = subject
        self.quantity = quantity

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'condition': self.condition,
            'grade': self.grade,
            'subject': self.subject,
            'quantity': self.quantity
        }


    def __repr__(self):
        return f' Title:{self.title}\n Author:{self.author}\n Grade: {self.grade}\n Subject: {self.subject}\n ${self.price}\n Condition:{self.condition}\n Quantity: {self.quantity}\n'  
    

