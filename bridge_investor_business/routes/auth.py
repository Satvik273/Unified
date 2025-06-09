from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User
from forms import RegistrationForm, LoginForm
import logging

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for(f"{session['role']}.dashboard"))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            password=hashed_password,
            role=form.role.data
        )
        
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f'Registration error: {str(e)}')
            flash('An error occurred during registration. Please try again.', 'danger')
            
    return render_template('register.html', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for(f"{session['role']}.dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            # Redirect based on user role
            if user.role in ['business', 'investor', 'banker', 'advisor']:
                flash(f'Welcome {user.username}!', 'success')
                return redirect(url_for(f'{user.role}.dashboard'))
            else:
                flash('Invalid role assigned to your account.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
