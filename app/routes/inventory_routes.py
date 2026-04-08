from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.book import Book
from app.models.inventory_adjustment import InventoryAdjustment

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

VALID_REASONS = [
    'Restock',
    'Damaged / Worn',
    'Lost / Missing',
    'Returned by Student',
    'Correction / Count Error',
    'Donated',
    'Other',
]


# ── UI Route ────────────────────────────────────────────────────────────────

@inventory_bp.route('/adjust', methods=['GET'])
def adjust_page():
    """Render the manual inventory adjustment page"""
    return render_template('inventory_adjust.html')


# ── API Routes ───────────────────────────────────────────────────────────────

@inventory_bp.route('/adjust/<int:book_id>', methods=['POST'])
def adjust_inventory(book_id):
    """
    Manually adjust the quantity of a book.

    Expected JSON body:
    {
        "new_quantity": 10,
        "reason": "Restock",
        "adjusted_by": "admin"   (optional)
    }
    """
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        # Validate new_quantity
        if 'new_quantity' not in data:
            return jsonify({'error': 'new_quantity is required'}), 400

        try:
            new_quantity = int(data['new_quantity'])
        except (ValueError, TypeError):
            return jsonify({'error': 'new_quantity must be an integer'}), 400

        if new_quantity < 0:
            return jsonify({'error': 'new_quantity cannot be negative'}), 400

        # Validate reason
        reason = data.get('reason', '').strip()
        if not reason:
            return jsonify({'error': 'reason is required'}), 400

        if len(reason) > 255:
            return jsonify({'error': 'reason must be 255 characters or fewer'}), 400

        adjusted_by = data.get('adjusted_by', None)

        # Record the adjustment
        adjustment = InventoryAdjustment(
            book_id=book.id,
            previous_quantity=book.quantity,
            new_quantity=new_quantity,
            reason=reason,
            adjusted_by=adjusted_by
        )

        # Update the book
        book.quantity = new_quantity

        db.session.add(adjustment)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Inventory updated for "{book.title}"',
            'book': book.to_dict(),
            'adjustment': adjustment.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to adjust inventory: {str(e)}'}), 500


@inventory_bp.route('/adjustments', methods=['GET'])
def get_all_adjustments():
    """
    Get full adjustment history with optional filters.

    Query params:
      - book_id (int)   filter by book
      - page    (int)   default 1
      - per_page (int)  default 20, max 100
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        book_id = request.args.get('book_id', None, type=int)

        query = InventoryAdjustment.query.order_by(InventoryAdjustment.created_at.desc())

        if book_id:
            query = query.filter(InventoryAdjustment.book_id == book_id)

        pagination = query.paginate(page=page, per_page=per_page)

        return jsonify({
            'data': [a.to_dict() for a in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to retrieve adjustments: {str(e)}'}), 500


@inventory_bp.route('/adjustments/<int:book_id>', methods=['GET'])
def get_book_adjustments(book_id):
    """Get adjustment history for a specific book"""
    try:
        Book.query.get_or_404(book_id)

        adjustments = (
            InventoryAdjustment.query
            .filter_by(book_id=book_id)
            .order_by(InventoryAdjustment.created_at.desc())
            .all()
        )

        return jsonify({
            'book_id': book_id,
            'count': len(adjustments),
            'data': [a.to_dict() for a in adjustments]
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to retrieve adjustments: {str(e)}'}), 500


@inventory_bp.route('/reasons', methods=['GET'])
def get_reasons():
    """Return the list of valid adjustment reasons"""
    return jsonify({'reasons': VALID_REASONS}), 200
