#
#   Imports
#
from settings import *
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from wtforms import StringField, PasswordField

#
#   Student registration form
#
class StudentRegForm (FlaskForm):
    full_name = StringField('full_name', validators=[InputRequired(), Length(max = MAX_FULLNAME_LENGTH)])
    nickname = StringField('nickname', validators=[InputRequired(), Length(max = MAX_NICKNAME_LENGTH)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])
    brief_resume = StringField('brief_resume', validators=[InputRequired()])

#
#   Professor registration form
#
class ProfessorRegForm (FlaskForm):
    full_name = StringField('full_name', validators=[InputRequired(), Length(max = MAX_FULLNAME_LENGTH)])
    nickname = StringField('nickname', validators=[InputRequired(), Length(max = MAX_NICKNAME_LENGTH)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])
    laboratory = StringField('laboratory', validators=[InputRequired(), Length(max = MAX_LABORATORY_LENGTH)])

#
#   Login form
#
class LoginForm (FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(), Length(max = MAX_NICKNAME_LENGTH)])
    password = PasswordField('password', validators=[InputRequired(), Length(min = MIN_PASSWORD_LENGTH)])