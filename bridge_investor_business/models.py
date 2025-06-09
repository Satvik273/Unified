# SQLAlchemy models
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Increased length for hash
    role = db.Column(db.String(20), nullable=False)  # user, business, investor, banker, advisor

class BusinessIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Changed from user_id
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add relationship
    business = db.relationship('User', foreign_keys=[business_id])

class InvestorProposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('business_idea.id'), nullable=False)
    details = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected

    # Add relationships
    investor = db.relationship('User', foreign_keys=[investor_id])
    idea = db.relationship('BusinessIdea', foreign_keys=[idea_id])

class LoanRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    # Relationships
    business = db.relationship('User', foreign_keys=[business_id])
    loan = db.relationship('Loan', backref='request', uselist=False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('loan_request.id'), nullable=False)
    banker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    date_approved = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    banker = db.relationship('User', foreign_keys=[banker_id])

class LoanDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    
    # Relationship
    loan = db.relationship('Loan', backref='payments')

class AdviceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, answered
    
    # Relationships
    business = db.relationship('User', foreign_keys=[business_id])
    advice = db.relationship('BusinessAdvice', backref='request', uselist=False)

class BusinessAdvice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('advice_request.id'), nullable=False)
    information = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    advisor = db.relationship('User', foreign_keys=[advisor_id])
