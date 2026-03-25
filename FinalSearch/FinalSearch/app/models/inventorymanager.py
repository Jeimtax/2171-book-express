from app.models.book import Book
from app.extensions import db

class InventoryManager:
    
    def add_book(self, title, author, price, condition, grade=None, subject=None, quantity=0, min_quantity=0):
        book = Book(title, author, price, condition, grade, subject, quantity=quantity, min_quantity=min_quantity)
        db.session.add(book)
        db.session.commit()
        return book
    
    def manage_book_info(self, id, title=None, author=None, price=None, condition=None, grade=None, subject=None, quantity=None, min_quantity=None):
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

        if min_quantity is not None:
            book.min_quantity = min_quantity

        db.session.commit()
        return book

    def search_books(self, grade=None, subject=None, max_price=None, q=None):
        query = Book.query

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

        if q:
            search_term = f"%{q.strip()}%"
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term)
                )
            )

        # Real-time inventory levels come directly from the live DB
        results = query.order_by(Book.title.asc()).all()
        return results

    def low_stock_books(self):
        return Book.query.filter(Book.quantity <= Book.min_quantity).all()

    
    
