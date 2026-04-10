from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db, bcrypt, login_manager
from app.forms import RegistrationForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

# Custom decorator for role-based access control
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role != role:
                flash(f'You do not have the required "{role}" role to access this page.', 'danger')
                abort(403) # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard.dashboard_page')) # Redirect to dashboard

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw, role=role)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard.dashboard_page')) # Redirect to dashboard

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember_me') == 'on' # Check for remember me checkbox

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            if not user.is_active:
                flash('Account is disabled.', 'danger')
                return render_template('login.html')

            login_user(user, remember=remember)
            session.permanent = True # Enables the PERMANENT_SESSION_LIFETIME timeout

            flash(f'Logged in as {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard_page')) # Redirect to next page or main index
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        
        # Logic incorporated from Auth.php
        if not bcrypt.check_password_hash(current_user.password, old_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        if len(new_password) < 8:
            flash('New password must be at least 8 characters.', 'danger')
            return redirect(url_for('auth.change_password'))
            
        current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('dashboard.dashboard_page'))
        
    return render_template('change_password.html')
