from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import all models so Alembic can detect them
from app.models.book import Book
from app.models.Importsalesdata import Sales
from app.models.inventory_adjustment import InventoryAdjustment

# Register blueprints
from app.csv_routes import upload_bp
from app.inventory_routes import inventory_bp

app.register_blueprint(upload_bp)
app.register_blueprint(inventory_bp)
