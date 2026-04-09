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

    def search_books(self, title=None, author=None, grade=None, subject=None, max_price=None, quantity=None):
        query = Book.query

        if title:
            query = query.filter(Book.title.ilike(f"%{title.strip()}%"))

        if author:
            query = query.filter(Book.author.ilike(f"%{author.strip()}%"))

        if grade:
            query = query.filter(Book.grade.ilike(grade.strip()))

        if subject:
            query = query.filter(Book.subject.ilike(subject.strip()))

        if max_price is not None and max_price != "":
            try:
                price_value = float(max_price)
                query = query.filter(Book.price <= price_value)
            except ValueError:
                pass
        
        if quantity is not None and quantity != "":
            try:
                quantity_value = int(quantity)
                query = query.filter(Book.quantity == quantity_value)
            except ValueError:
                pass

        # Real-time inventory levels come directly from the live DB
        results = query.order_by(Book.title.asc()).all()
        return results
    
    def low_stock_alert(self, threshold=1):
        """Return all books whose quantity is at or below the alert threshold."""
        try:
            threshold_value = int(threshold)
        except (TypeError, ValueError):
            threshold_value = 1

        if threshold_value < 0:
            threshold_value = 0

        return (
            Book.query
            .filter(Book.quantity <= threshold_value)
            .order_by(Book.quantity.asc(), Book.title.asc())
            .all()
        )
    
    
