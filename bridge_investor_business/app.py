# Flask app entry point
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
import logging
import os

# Initialize Flask app and database
app = Flask(__name__, static_folder='static')
app.config.from_object("config.Config")

# Enable CSRF protection
csrf = CSRFProtect(app)

# Initialize database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import blueprints
from routes.auth import bp as auth_bp
from routes.business import bp as business_bp
from routes.investor import bp as investor_bp
from routes.banker import bp as banker_bp
from routes.advisor import bp as advisor_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(business_bp, url_prefix='/business')
app.register_blueprint(investor_bp, url_prefix='/investor')
app.register_blueprint(banker_bp, url_prefix='/banker')
app.register_blueprint(advisor_bp, url_prefix='/advisor')

# Add a root route
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log',
                   level=logging.INFO,
                   format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Import models (must be done before creating tables)
from models import User, BusinessIdea, InvestorProposal, LoanDetail, BusinessAdvice

# Create tables
with app.app_context():
    db.create_all()
