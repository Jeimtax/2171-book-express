from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config) 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import book
# Register blueprints
from app.routes import upload_bp
app.register_blueprint(upload_bp)




