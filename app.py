#
#   Imports
#
from settings import *
from forms import *
from server import *
from models import *
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

#
#   Login manager
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = LOGIN_VIEW
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

#
#   Routes
#

# Route to the main register page
@app.route('/register')
def register():
    return render_template('register.html')

# Route to the student register page
@app.route('/register/student', methods = ['GET', 'POST'])
def register_student():
    form = StudentRegForm()
    flag_student = True
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(nickname=form.nickname.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                new_user = User(form.nickname.data, hashpass, form.full_name.data).save()
                login_user(new_user)
                return redirect(url_for('dashboard'))
            else:
                error = "User already exists"
        else:
            error = "Form not validated!"
    return render_template('register-form.html', form = form, form_type = 'student')

# Route to the professor register page
@app.route('/register/professor', methods=['GET', 'POST'])
def register_professor():
    form = ProfessorRegForm()
    flag_student = False
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(nickname=form.nickname.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                new_user = User(form.nickname.data, hashpass, form.full_name.data).save()
                login_user(new_user)
                return redirect(url_for('dashboard'))
            else:
                error = "User already exists"
        else:
            error = "Form not validated!"
    return render_template('register-form.html', form = form, form_type = 'professor')

# Route to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(nickname=form.nickname.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# Route to the dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.full_name)

# Route to logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))