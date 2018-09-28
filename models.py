#
#   Imports
#
from settings import *
from server import db
from flask_login import UserMixin
from flask_mongoengine import Document
from wtforms import StringField, BooleanField

#
#   User class
#
class User(UserMixin, db.Document):
    # Database stuff
    meta = {'collection': 'User'}
    nickname = db.StringField(max_length = MAX_NICKNAME_LENGTH)
    password = db.StringField()
    full_name = db.StringField(max_length = MAX_FULLNAME_LENGTH)

#
#   Research class
#
class Research (db.Document):
    meta = {
        'collection' : 'Research'
    }
    title = db.StringField()
    description = db.StringField()
    laboratory = db.StringField(max_length = MAX_LABORATORY_LENGTH)
    open_to_subscribe = db.BooleanField()