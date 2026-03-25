from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.extensions import db
from app.models.inventorymanager import InventoryManager
from app.models.book import Book

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

inventory_manager = InventoryManager()


@app.route('/')
def home():
    return redirect(url_for('inventory_search'))


@app.route('/inventory-search', methods=['GET', 'POST'])
def inventory_search():
    grade = request.values.get('grade', '').strip() or None
    subject = request.values.get('subject', '').strip() or None
    max_price = request.values.get('max_price', '').strip() or None
    q = request.values.get('q', '').strip() or None

    books = []
    if request.method == 'POST' or any([grade, subject, max_price, q]):
        books = inventory_manager.search_books(grade=grade, subject=subject, max_price=max_price, q=q)

    grades = [g[0] for g in db.session.query(Book.grade).distinct().filter(Book.grade.isnot(None)).order_by(Book.grade)]
    subjects = [s[0] for s in db.session.query(Book.subject).distinct().filter(Book.subject.isnot(None)).order_by(Book.subject)]

    return render_template('dashboard.html', books=books, grades=grades, subjects=subjects, selected_grade=grade, selected_subject=subject, max_price=max_price, q=q)

# app/__init__.py
if __name__ == "__main__":
    app.run(debug=True)

