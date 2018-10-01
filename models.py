#
#   Imports
#
from app import *
from flask_login import UserMixin
from flask_mongoengine import Document
from mongoengine import ReferenceField, ListField
from wtforms import StringField, BooleanField

#
#   Research model
#
class Research (db.Document):
    meta = {
        'collection' : 'Research'
    }
    title = db.StringField()
    description = db.StringField()
    open_to_subscribe = db.BooleanField()

#
#   User model
#
class User(UserMixin, db.Document):
    meta = {
        'collection': 'User',
        'allow_inheritance': True
    }
    full_name = db.StringField(max_length = MAX_FULLNAME_LENGTH, required = True)
    nickname = db.StringField(max_length = MAX_NICKNAME_LENGTH, required = True)
    password = db.StringField(required = True)
    email = db.StringField(required = True)
    lattes = db.StringField()
    researches = db.ListField(ReferenceField(Research))

#
#   Student model
#
class Student (User):
    brief_description = db.StringField()
    
#
#   Professor model
#
class Professor (User):
    laboratory = db.StringField(max_length = MAX_LABORATORY_LENGTH)