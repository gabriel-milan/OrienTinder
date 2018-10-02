#
#   Imports
#
from settings import *
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from wtforms import StringField, PasswordField, BooleanField

#
#   Student registration form
#
class RegistrationForm (FlaskForm):
    full_name = StringField('full_name', validators=[InputRequired(), Length(max = MAX_FULLNAME_LENGTH)])
    nickname = StringField('nickname', validators=[InputRequired(), Length(max = MAX_NICKNAME_LENGTH)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])
    password_confirmation = PasswordField(validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])
    email = StringField('email', validators=[InputRequired(), Email()])
    student = BooleanField(validators=[InputRequired()])

#
#   Login form
#
class LoginForm (FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(), Length(max = MAX_NICKNAME_LENGTH)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])