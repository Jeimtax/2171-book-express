from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.book import Book
from app.models.inventorymanager import InventoryManager

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')


@stock_bp.route("/")
def low_stocks():
    low_stocks = InventoryManager.low_stock_alert(threshold=10)
    return render_template("low_stocks.html", books=low_stocks)