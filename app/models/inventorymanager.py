from app.models.book import Book
from app import db

class InventoryManager:
    
    def add_book(self, title, author, price, grade, subject, quantity):
        """Adds a Book to the database"""
        book = Book(title=title, author=author, price=price, grade=grade, subject=subject, quantity=quantity)
        db.session.add(book)
        db.session.commit()
        return book
    
    @staticmethod
    def delete_book(book_id):
        """Removes a book from the database"""
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return True
    
    def manage_book_info(self, id, title=None, author=None, price=None, grade=None, subject=None, quantity=None):
        """Allows to edit a singular or multiple attributes of a Book"""
        book = Book.query.get_or_404(id)

        if title is not None: book.title = title
        if author is not None: book.author = author
        if price is not None: book.price = price
        if grade is not None: book.grade = grade
        if subject is not None: book.subject = subject
        if quantity is not None: book.quantity = quantity
        
        db.session.commit()
        return book

    def search_books(self, title=None, author=None, grade=None, subject=None, max_price=None):
        query = Book.query

        if title and title.strip():
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author and author.strip():
            query = query.filter(Book.author.ilike(f"%{author}%"))

        if grade and grade.strip():
            query = query.filter(Book.grade == grade)

        if subject and subject.strip():
            query = query.filter(Book.subject == subject)

        if max_price:
            try:
                price_value = float(max_price)
                query = query.filter(Book.price <= price_value)
            except ValueError:
                pass



        # Real-time inventory levels come directly from the live DB
        results = query.order_by(Book.title.asc()).all()
        return results
    
    @staticmethod
    def low_stock_alert(threshold=10):
        return Book.query.filter(Book.quantity < threshold).all()
        
    
    
