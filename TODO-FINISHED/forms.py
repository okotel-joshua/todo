from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class RegistrationForm(FlaskForm):
	email = EmailField('email',
		validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('password',
		validators=[validators.DataRequired(), validators.Length(min=8, message="Choose a password of at least 8 characters")])
	password2 = PasswordField('password2',
		validators=[validators.DataRequired(),
		validators.EqualTo('password', message='Passwords must match')])
	submit = SubmitField('submit', [validators.DataRequired()])

class LoginForm(FlaskForm):
	email = EmailField('email',
		validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('password',
		validators=[validators.DataRequired()])
	submit = SubmitField('submit', [validators.DataRequired()])
