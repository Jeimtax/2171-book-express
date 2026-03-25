from app.models.book import Book
from app import db

class InventoryManager:
    
    def add_book(self, title, author, price, condition, grade, subject, quantity):
        """Adds a Book to the database"""
        book = Book( title, author, price, condition, grade, subject, quantity)
        db.session.add(book)
        db.session.commit()
        return book
    
    def manage_book_info(self, id, title=None, author=None, price=None, condition=None, grade=None, subject=None, quantity=None):
        """Allows to edit a singular or multiple attributes of a Book"""
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

        if quantity is not None:
            book.quantity = quantity
        db.session.commit()
        return book

    def search_books(self, title=None, author=None, grade=None, subject=None, max_price=None):
        query = Book.query

        if title:
            query = query.filter(Book.title == title)

        if author:
            query = query.filter(Book.author == author)

        if grade:
            query = query.filter(Book.grade == grade)

        if subject:
            query = query.filter(Book.subject == subject)

        if max_price is not None and max_price != "":
            try:
                price_value = float(max_price)
                query = query.filter(Book.price <= price_value)
            except ValueError:
                pass



        # Real-time inventory levels come directly from the live DB
        results = query.order_by(Book.title.asc()).all()
        return results
    
    
