from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from models import BusinessAdvice, AdviceRequest
import logging

bp = Blueprint('advisor', __name__, url_prefix='/advisor')

@bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'advisor':
        return redirect(url_for('auth.login'))
    
    advice_requests = AdviceRequest.query.filter_by(status='pending').all()
    given_advice = BusinessAdvice.query.filter_by(advisor_id=session['user_id']).all()
    return render_template('advisor_dashboard.html', 
                         advice_requests=advice_requests, 
                         given_advice=given_advice)

@bp.route('/post_advice/<int:request_id>', methods=['GET', 'POST'])
def post_advice(request_id):
    if session.get('role') != 'advisor':
        return redirect(url_for('auth.login'))
        
    advice_request = AdviceRequest.query.get_or_404(request_id)
    if request.method == 'POST':
        advice = BusinessAdvice(
            advisor_id=session['user_id'],
            request_id=request_id,
            information=request.form['information']
        )
        advice_request.status = 'answered'
        db.session.add(advice)
        try:
            db.session.commit()
            flash('Advice posted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error posting advice.', 'danger')
        return redirect(url_for('advisor.dashboard'))
    return render_template('post_solution.html', request=advice_request)
