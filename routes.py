#
#   TODO:
#   - Fazer o método de registrar usuário em uma única URL para o POST;
#   - Mexer no form HTML de registro
#

#
#   Imports
#
from forms import *
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

#
#   Login manager
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = LOGIN_VIEW

@login_manager.user_loader
def load_professor(user_id):
    return Professor.objects(pk=user_id).first()

@login_manager.user_loader
def load_student(user_id):
    return Student.objects(pk=user_id).first()

#
#   Routes
#

# Route to homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Route to the main register page
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            if form.student.data == True:
                existing_user = Student.objects(nickname=form.nickname.data).first()
            else:
                existing_user = Professor.objects(nickname=form.nickname.data).first()
            if existing_user is None:
                if (form.password.data == form.password_confirmation.data):
                    hashpass = generate_password_hash(form.password.data, method='sha256')
                    if form.student.data == True:
                        new_user = Student(nickname = form.nickname.data, password = hashpass, full_name = form.full_name.data, email = form.email.data).save()
                    else:
                        new_user = Professor(nickname = form.nickname.data, password = hashpass, full_name = form.full_name.data, email = form.email.data).save()
                    login_user(new_user)
                    return redirect(url_for('dashboard'))
                else:
                    error = "Passwords not matching"
            else:
                error = "User already exists"
        else:
            error = "Form not validated!"
    return render_template('register.html', form = form)

# Route to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = Student.objects(nickname=form.nickname.data).first()
            if not check_user:
                check_user = Professor.objects(nickname=form.nickname.data).first()
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

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)