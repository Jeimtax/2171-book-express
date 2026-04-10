from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app import db
from app.models.book import Book
from app.models.inventorymanager import InventoryManager
from app.forms import AddBook

books_bp = Blueprint('books', __name__, url_prefix='/books')
inventory_manager = InventoryManager()

@books_bp.route('/view', methods=['GET', 'POST'])
def create():
    form = AddBook()

    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book(
                title=form.title.data,
                author=form.author.data,
                price=form.price.data,
                grade=form.grade.data,
                subject=form.subject.data,
                quantity=form.quantity.data
            )
            db.session.add(book)
            db.session.commit()
            flash('New Book was added!', 'success')
            return redirect(url_for('books.create'))

    all_books = Book.query.all()
    return render_template('books.html', all_books=all_books, form=form)

@books_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book = Book.query.get_or_404(id)
    form = AddBook(obj=book) # This pre-fills the form with current book info
    
    if form.validate_on_submit():
        inventory_manager.manage_book_info(
            id=id,
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            grade=form.grade.data,
            subject=form.subject.data,
            quantity=form.quantity.data
        )
        flash(f'Updated "{book.title}" successfully.', 'success')
        return redirect(url_for('books.create'))
    
    return render_template('update_book.html', form=form, book=book)

@books_bp.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    InventoryManager.delete_book(id)
    flash('Book removed from inventory.', 'success')
    return redirect(url_for('books.create'))


@books_bp.route('/search', methods=['GET'])
def search():
    """Live book search used by the inventory adjust page."""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    books = Book.query.filter(
        db.or_(
            Book.title.ilike(f'%{q}%'),
            Book.author.ilike(f'%{q}%')
        )
    ).order_by(Book.title.asc()).limit(10).all()

    return jsonify([b.to_dict() for b in books])
