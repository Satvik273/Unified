from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db
from models import BusinessIdea, InvestorProposal
from forms import ProposalForm
import logging

bp = Blueprint('investor', __name__)

@bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'investor':
        return redirect(url_for('auth.login'))
    
    ideas = BusinessIdea.query.all()
    proposals = InvestorProposal.query.filter_by(investor_id=session['user_id']).all()
    return render_template('investor_dashboard.html', 
                         ideas=ideas, 
                         proposals=proposals)

@bp.route('/post_proposal/<int:idea_id>', methods=['GET', 'POST'])
def post_proposal(idea_id):
    if session.get('role') != 'investor':
        return redirect(url_for('auth.login'))
    
    idea = BusinessIdea.query.get_or_404(idea_id)
    form = ProposalForm()
    
    if form.validate_on_submit():
        proposal = InvestorProposal(
            investor_id=session['user_id'],
            idea_id=idea_id,
            details=form.details.data
        )
        db.session.add(proposal)
        try:
            db.session.commit()
            flash('Your proposal has been submitted successfully!', 'success')
            return redirect(url_for('investor.dashboard'))
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error submitting proposal: {str(e)}')
            flash('An error occurred while submitting your proposal.', 'danger')
    
    return render_template('post_proposal.html', form=form, idea=idea)
