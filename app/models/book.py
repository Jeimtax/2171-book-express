from . import db

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    grade = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, title: str, author: str, isbn: int, grade: str, subject: str, price: float, stock: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.grade = grade
        self.subject = subject
        self.price = price
        self.stock = stock
        
    

