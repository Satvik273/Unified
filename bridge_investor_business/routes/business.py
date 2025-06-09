from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db
from models import BusinessIdea, InvestorProposal, LoanRequest, AdviceRequest
from forms import IdeaForm, LoanRequestForm, AdviceRequestForm
import logging

bp = Blueprint('business', __name__)

@bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'business':
        return redirect(url_for('auth.login'))
    
    my_ideas = BusinessIdea.query.filter_by(business_id=session['user_id']).all()
    received_proposals = InvestorProposal.query\
        .join(BusinessIdea, BusinessIdea.id == InvestorProposal.idea_id)\
        .filter(BusinessIdea.business_id == session['user_id'])\
        .all()
    
    return render_template('business_dashboard.html', 
                         my_ideas=my_ideas, 
                         proposals=received_proposals)

@bp.route('/post_idea', methods=['GET', 'POST'])
def post_idea():
    if session.get('role') != 'business':
        return redirect(url_for('auth.login'))
    
    form = IdeaForm()
    if form.validate_on_submit():
        idea = BusinessIdea(
            business_id=session['user_id'],
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(idea)
        try:
            db.session.commit()
            flash('Your business idea has been posted!', 'success')
            return redirect(url_for('business.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while posting your idea. Please try again.', 'danger')
            logging.error(f'Error posting business idea: {str(e)}')
    
    return render_template('post_idea.html', form=form)

@bp.route('/request_loan', methods=['GET', 'POST'])
def request_loan():
    if session.get('role') != 'business':
        return redirect(url_for('auth.login'))
    
    form = LoanRequestForm()
    if form.validate_on_submit():
        loan_request = LoanRequest(
            business_id=session['user_id'],
            amount=form.amount.data,
            purpose=form.purpose.data,
            status='pending'
        )
        db.session.add(loan_request)
        try:
            db.session.commit()
            flash('Loan request submitted successfully!', 'success')
            return redirect(url_for('business.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting loan request.', 'danger')
            logging.error(f'Error submitting loan request: {str(e)}')
    
    return render_template('request_loan.html', form=form)

@bp.route('/request_advice', methods=['GET', 'POST'])
def request_advice():
    if session.get('role') != 'business':
        return redirect(url_for('auth.login'))
    
    form = AdviceRequestForm()
    if form.validate_on_submit():
        advice_request = AdviceRequest(
            business_id=session['user_id'],
            subject=form.subject.data,
            details=form.details.data,
            status='pending'
        )
        db.session.add(advice_request)
        try:
            db.session.commit()
            flash('Advice request submitted successfully!', 'success')
            return redirect(url_for('business.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting advice request.', 'danger')
            logging.error(f'Error submitting advice request: {str(e)}')
    
    return render_template('request_advice.html', form=form)
