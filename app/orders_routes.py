from flask import Blueprint, render_template, request
from app import db
from app.forms import ManageOrderForm
from app.models.order import Order
from app.models.supplier import Supplier

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/manage-orders', methods=['GET', 'POST'])
def manage_orders():
    form = ManageOrderForm()
    message = None

    if request.method == 'POST' and form.validate_on_submit():
        supplier = Supplier(
            name=form.supplier_name.data.strip(),
            phone=form.supplier_phone.data.strip(),
            address=form.supplier_address.data.strip(),
        )
        db.session.add(supplier)
        db.session.flush()

        order = Order(
            supplier_id=supplier.id,
            items=form.items.data.strip(),
        )
        db.session.add(order)
        db.session.commit()

        message = 'Order created successfully.'
        form = ManageOrderForm()

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('manage_orders.html', form=form, orders=orders, message=message)
