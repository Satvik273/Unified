from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('business', 'Business People'),
        ('investor', 'Investor'),
        ('banker', 'Banker'),
        ('advisor', 'Business Advisor')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class IdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Idea')

class ProposalForm(FlaskForm):
    idea_id = SelectField('Business Idea', coerce=int, validators=[DataRequired()])
    details = TextAreaField('Proposal Details', validators=[DataRequired(), Length(min=50, max=1000)])
    submit = SubmitField('Submit Proposal')

class LoanApprovalForm(FlaskForm):
    interest_rate = FloatField('Interest Rate (%)', 
                             validators=[DataRequired(), NumberRange(min=0, max=100)])
    term_months = IntegerField('Term (months)', 
                             validators=[DataRequired(), NumberRange(min=1, max=360)])
    submit = SubmitField('Approve Loan')

class LoanRequestForm(FlaskForm):
    amount = FloatField('Loan Amount ($)', 
                       validators=[DataRequired(), NumberRange(min=1000, max=10000000)])
    purpose = TextAreaField('Loan Purpose', 
                          validators=[DataRequired(), Length(min=50, max=500)])
    submit = SubmitField('Submit Loan Request')

class AdviceRequestForm(FlaskForm):
    subject = StringField('Subject', 
                         validators=[DataRequired(), Length(min=5, max=100)])
    details = TextAreaField('Request Details', 
                          validators=[DataRequired(), Length(min=50, max=1000)])
    submit = SubmitField('Request Advice')

class AdviceResponseForm(FlaskForm):
    advice = TextAreaField('Your Advice', 
                         validators=[DataRequired(), Length(min=100, max=2000)])
    submit = SubmitField('Submit Advice')
