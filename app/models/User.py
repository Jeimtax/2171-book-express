from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'Users' # Consistent with other models

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff') # 'staff' or 'manager'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }