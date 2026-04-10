from app.models.book import Book
from app import db

class InventoryManager:
    
    def add_book(self, title, author, price, grade, subject, quantity):
        """Adds a Book to the database"""
        book = Book( title, author, price, grade, subject, quantity)
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
    
    
    @staticmethod
    def manage_book_info(id, data):
        """Allows to edit a singular or multiple attributes of a Book"""
        book = Book.query.get_or_404(id)

        book.title = data.get('title')
        book.author = data.get('author')
        book.price = data.get('price')
        book.condition = data.get('condition')
        book.grade = data.get('grade')
        book.subject = data.get('subject')
        book.quantity = data.get('quantity')
        
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
    
    @staticmethod
    def low_stock_alert(threshold=10):
        return Book.query.filter(Book.quantity < threshold).all()
        
    
    
