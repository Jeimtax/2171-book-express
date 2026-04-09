from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.models.book import Book
from app.models.inventorymanager import InventoryManager
from app.forms import AddBook


books_bp = Blueprint('books', __name__, url_prefix= '/books')

    
@books_bp.route('/view', methods=['GET', 'POST'])
def create():
    form = AddBook()
    inventory_manager = InventoryManager()

    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book(
                title = form.title.data,
                author = form.author.data,
                price =form.price.data,
                condition = form.condition.data,
                grade = form.grade.data,
                subject = form.subject.data,
                quantity = form.quantity.data
            )
        
            db.session.add(book)
            db.session.commit()  
            flash('New Book was added!', 'success')
            return redirect(url_for('books.create'))
    all_books = Book.query.all()
    low_stock_books = inventory_manager.low_stock_alert()
    return render_template(
        'books.html',
        all_books=all_books,
        form=form,
        low_stock_books=low_stock_books
    )  
   
