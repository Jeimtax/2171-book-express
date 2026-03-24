from app.models.book import Book
from app import db

class InventoryManager:
    
    def add_book(self, title, author, price, condition, grade, subject):
        book = Book( title, author, price, condition, grade, subject)
        db.session.add(book)
        db.session.commit()
        return book
    
    def manage_book_info(self, id, title=None, author=None, price=None, condition=None, grade=None, subject=None):
        book = Book.query.get_or_404(id)

        if title is not None:
            book.title = title

        if author is not None:
            book.author = author

        if price is not None:
            book.price = price

        if condition is not None:
            book.condition = condition

        if grade is not None:
            book.grade = grade

        if subject is not None:
            book.subject = subject
        db.session.commit()

    
    
