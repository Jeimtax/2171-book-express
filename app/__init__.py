from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login' # Specify the login view blueprint.route
login_manager.login_message_category = 'info' # Category for flashed messages


from app.models.book import Book
from app.models.Importsalesdata import Sales
from app.models.inventory_adjustment import InventoryAdjustment
from app.models.supplier import Supplier
from app.models.order import Order
from app.models.user import User # Import the new User model

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.routes.books_routes import books_bp
from app.routes.csv_routes import upload_bp
from app.routes.inventory_routes import inventory_bp
from app.routes.orders_routes import orders_bp

app.register_blueprint(books_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(orders_bp)
