# Create your forms here.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from social_ceo_app.models import Business_Name, State, User
from social_ceo_app import bcrypt
from wtforms.fields.html5 import DateField


class FormSignUp(FlaskForm):
    full_name = StringField(label='Full Name',  validators=[DataRequired(), Length(min=3, max=50)])
    birthdate = DateField('Birthday', format='%Y-%m-%d')
    business_name = QuerySelectField(label='Business Name', query_factory=lambda: Business_Name.query, allow_blank=False, get_label='name')
    state = QuerySelectField(label='State You Live In', query_factory=lambda: State.query, allow_blank=False, get_label='name')
    position = StringField(label='Position', validators=[DataRequired(), Length(min=3, max=5)])
    email = StringField(label='Email', validators=[DataRequired(), Length(min=3, max=80), Email(message='Invalid email format')], )
    password = PasswordField(label='Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Sign Up')

    def validate_email(self, email):
      #Not duplicating accounts
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('It appears you already have an account. Please select login to continue.')
    
    def validate_state(self, state):
        # State and Business_Name is a double bind, in order to mitigate, a custom validator is created for state
      
        if state.data.business_name != self.business_name.data:
          raise ValidationError(f'{state.data.name} is not part of {self.business_name.data.name}')


class FormLogin(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
      # ensuring user exists in the database
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('It appears you do not have an account. Please select signup to continue.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('OH NO! It appears your password does not match. Please re-enter.')