from flask import Blueprint, jsonify, render_template
from app.models.book import Book

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard_data():
    books = Book.query.all()

    total_books = sum(book.quantity for book in books)
    total_value = sum(book.quantity * book.price for book in books)


    return jsonify({
        "total_books": total_books,
        "total_value": total_value,
    })


@dashboard_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')