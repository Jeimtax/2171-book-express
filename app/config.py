import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base Config Object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-fallback-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Security Configuration (Incorporate SessionManager.php)
    SESSION_COOKIE_NAME = os.environ.get('SESSION_NAME', 'BOOK_EXPRESS_SESSION')
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_TIMEOUT', 3600))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv'}

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
