from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app import db
from models import LoanRequest, Loan
from forms import LoanApprovalForm
import logging

bp = Blueprint('banker', __name__, url_prefix='/banker')

@bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'banker':
        return redirect(url_for('auth.login'))
    
    loan_requests = LoanRequest.query.filter_by(status='pending').all()
    approved_loans = Loan.query.filter_by(banker_id=session['user_id']).all()
    return render_template('banker_dashboard.html', 
                         loan_requests=loan_requests, 
                         approved_loans=approved_loans)

@bp.route('/approve_loan/<int:request_id>', methods=['GET', 'POST'])
def approve_loan(request_id):
    if session.get('role') != 'banker':
        return redirect(url_for('auth.login'))
    
    loan_request = LoanRequest.query.get_or_404(request_id)
    form = LoanApprovalForm()
    
    if form.validate_on_submit():
        loan = Loan(
            request_id=request_id,
            banker_id=session['user_id'],
            amount=loan_request.amount,
            interest_rate=form.interest_rate.data,
            term_months=form.term_months.data
        )
        loan_request.status = 'approved'
        db.session.add(loan)
        try:
            db.session.commit()
            flash('Loan has been approved successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error approving loan.', 'danger')
            logging.error(f'Error approving loan: {str(e)}')
        return redirect(url_for('banker.dashboard'))
    
    return render_template('approve_loan.html', form=form, request=loan_request)

@bp.route('/reject_loan/<int:request_id>')
def reject_loan(request_id):
    if session.get('role') != 'banker':
        return redirect(url_for('auth.login'))
    
    loan_request = LoanRequest.query.get_or_404(request_id)
    loan_request.status = 'rejected'
    try:
        db.session.commit()
        flash('Loan request has been rejected.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error rejecting loan request.', 'danger')
        logging.error(f'Error rejecting loan: {str(e)}')
    return redirect(url_for('banker.dashboard'))
