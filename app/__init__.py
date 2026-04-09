from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.models.book import Book
from app.models.Importsalesdata import Sales
from app.models.inventory_adjustment import InventoryAdjustment
from app.models.supplier import Supplier
from app.models.order import Order

from app.routes.books_routes import books_bp
from app.routes.csv_routes import upload_bp
from app.routes.inventory_routes import inventory_bp
from app.routes.orders_routes import orders_bp
from app.routes.dashboard_routes import dashboard_bp

app.register_blueprint(books_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(dashboard_bp)
