from flask import Blueprint, jsonify, render_template, request
from app.models.book import Book
from flask_login import login_required, current_user
from app.models.inventorymanager import InventoryManager

dashboard_bp = Blueprint('dashboard', __name__)
inventory_manager = InventoryManager()

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard_data():
    # Extract search and filter parameters from the query string
    title = request.args.get('title')
    author = request.args.get('author')
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    max_price = request.args.get('max_price')

    # Use the InventoryManager to filter the books based on the search criteria
    books = inventory_manager.search_books(
        title=title,
        author=author,
        grade=grade,
        subject=subject,
        max_price=max_price
    )

    total_books = sum(book.quantity for book in books)
    total_value = sum(book.quantity * book.price for book in books)


    return jsonify({
        "total_books": total_books,
        "total_value": total_value,
        "books": [book.to_dict() for book in books]
    })

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_page():
    title = request.args.get('title')
    author = request.args.get('author')
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    max_price = request.args.get('max_price')

    books = inventory_manager.search_books(
        title=title,
        author=author,
        grade=grade,
        subject=subject,
        max_price=max_price
    )
    return render_template('dashboard.html', books=books, user=current_user)