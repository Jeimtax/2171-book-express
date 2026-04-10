from flask import Blueprint, render_template, request, jsonify
from app import db
from app.forms import ManageOrderForm
from app.models.order import Order
from app.models.supplier import Supplier
from app.models.book import Book

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/manage-orders', methods=['GET', 'POST'])
def manage_orders():
    form = ManageOrderForm()
    message = None
    book_id_error = None

    if request.method == 'POST' and form.validate_on_submit():
        selected_book_id = form.book_id.data
        linked_book = None

        if selected_book_id and selected_book_id != 0:
            linked_book = Book.query.get(selected_book_id)
            if not linked_book:
                book_id_error = 'Linked book not found'

        supplier = Supplier(
            name=form.supplier_name.data.strip(),
            phone=form.supplier_phone.data.strip(),
            address=form.supplier_address.data.strip(),
        )
        db.session.add(supplier)
        db.session.flush()

        order = Order(
            supplier_id=supplier.id,
            book_id=linked_book.id if linked_book else None,
            items=(
                f"Title: {form.title.data.strip()}\n"
                f"Author: {form.author.data.strip()}\n"
                f"Quantity: {form.quantity.data}"
            ),
            title=form.title.data.strip(),
            author=form.author.data.strip(),
            quantity=form.quantity.data,
        )
        db.session.add(order)
        db.session.commit()
        
        message = 'Order created successfully.'
        form = ManageOrderForm()

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template(
        'manage_orders.html',
        form=form,
        orders=orders,
        message=message,
        book_id_error=book_id_error,
    )


@orders_bp.route('/orders/<int:order_id>/confirm-delivery', methods=['POST'])
def confirm_delivery(order_id):
    """
    Confirm delivery of an order.
    Adds the order quantity to the matched book's inventory.

    Matching priority:
      1. book_id if set on the order (exact match)
      2. title + author match (case-insensitive) as fallback
    """
    try:
        order = Order.query.get_or_404(order_id)

        # Prevent double-confirming
        if order.status == 'delivered':
            return jsonify({
                'success': False,
                'error': f'Order #{order_id} has already been delivered.'
            }), 400

        # Find the book — prefer FK match, fall back to title+author
        book = None

        if order.book_id:
            book = Book.query.get(order.book_id)

        if not book:
            book = Book.query.filter(
                db.func.lower(Book.title) == order.title.strip().lower(),
                db.func.lower(Book.author) == order.author.strip().lower()
            ).first()

        if not book:
            return jsonify({
                'success': False,
                'error': (
                    f'No matching book found for "{order.title}" by {order.author}. '
                    f'Please link the order to a book or add the book to inventory first.'
                )
            }), 404

        previous_quantity = book.quantity
        book.quantity += order.quantity
        order.status = 'delivered'

        db.session.commit()

        return jsonify({
            'success': True,
            'message': (
                f'Delivery confirmed. "{book.title}" inventory updated '
                f'from {previous_quantity} to {book.quantity}.'
            ),
            'book': book.to_dict(),
            'order_id': order.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to confirm delivery: {str(e)}'}), 500
