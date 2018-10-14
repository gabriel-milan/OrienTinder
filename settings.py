###
# File that configures everything. Set macros here
###

# Database
DATABASE_NAME = 'OrienTinder'
DATABASE_URI = 'mongodb://127.0.0.1:27017/' + DATABASE_NAME

# Flask app
CSRF_SECRET_KEY = 'IUUIH@*HA#()RU)(A9102u'

# Views
LOGIN_VIEW = 'login'

# Models settings
MAX_NICKNAME_LENGTH = 20
MAX_FULLNAME_LENGTH = 50
MAX_LABORATORY_LENGTH = 100
MIN_PASSWORD_LENGTH = 8

# Types of users
STUDENT_USER = 11
PROFESSOR_USER = 12

# Error messages
HTTP_401_DEFAULT_MESSAGE = 'Você não está autorizado a realizar essa ação!'