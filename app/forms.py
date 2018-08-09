from app.models import User
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, URL, ValidationError

class AddTackForm(FlaskForm):
	link = StringField('link', validators=[URL(), DataRequired()])
	submit = SubmitField('tack')

class UserForm(FlaskForm):
	email = EmailField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])

class LoginForm(UserForm):
	submit = SubmitField('login')

	def validate_email(self, email):
		user = get_user(email.data)
		if user is None:
			raise ValidationError('Please use a different email address.')

class RegistrationForm(FlaskForm):
	email = EmailField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	confirm = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField('register')

	def validate_email(self, email):
		user = get_user(email.data)
		if user is not None:
			raise ValidationError('Please use a different email address.')

def get_user(email):
	return User.query.filter_by(email=email).first()
