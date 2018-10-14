#
#   Imports
#
from forms import *
from models import *
from flask_table import Table, Col, LinkCol
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

#
#   Login manager
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = LOGIN_VIEW

@login_manager.user_loader
def load_user(user_id):
    user = Student.objects(pk=user_id).first()
    if (user):
        return user
    else:
        return Professor.objects(pk=user_id).first()

#
#   Auxiliar function to check user type
#
def get_user_type ():
    try:
        laboratory = current_user.laboratory
        return PROFESSOR_USER
    except:
        return STUDENT_USER

#
#   Edit Research table class
#
class EditResearchTable (Table):
    classes = ['table']
    id = Col('Id', show = False)
    title = Col('Título')
    professor = Col('Professor', show = False)
    description = Col('Descrição')
    open_to_subscribe = Col('Aberta')
    edit = LinkCol('Editar', 'edit', url_kwargs=dict(id = 'id'))

#
#   Apply Research table class
#
class ApplyResearchTable (Table):
    classes = ['table']
    id = Col('Id', show = False)
    title = Col('Título')
    professor = Col('Professor')
    description = Col('Descrição')
    apply = LinkCol('Candidatar!', 'apply', url_kwargs=dict(id = 'id'))

#
#   Requests table class
#
class RequestsTable (Table):
    classes = ['table']
    title = Col('Pesquisa')
    full_name = Col('Nome do aluno')
    lattes = Col('Link Lattes')
    email = Col('E-mail')

#
#   Exception class (from flask Docs, minor changes)
#
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error_message'] = self.message
        rv['error_code'] = self.status_code
        return rv

#
#   Error pages
#
@app.errorhandler(InvalidUsage)
def unauthorized (error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return render_template('error_page.html', error_code = error.status_code, error_message = error.message)

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
                        new_user = Student(nickname = form.nickname.data, password = hashpass, full_name = form.full_name.data, email = form.email.data, lattes = form.lattes.data).save()
                    else:
                        new_user = Professor(nickname = form.nickname.data, password = hashpass, full_name = form.full_name.data, email = form.email.data, lattes = form.lattes.data).save()
                    login_user(new_user)
                    return redirect(url_for('dashboard'))
                else:
                    flash('As senhas não conferem!')
                    # raise InvalidUsage('As senhas não conferem!', status_code = 400)
            else:
                flash('Usuário já cadastrado!')
                # raise InvalidUsage('O usuário já existe!', status_code = 400)
        else:
            flash('Formulário não foi validado com sucesso :(')
            # raise InvalidUsage('Formulário não validado, preencha novamente!', status_code = 400)
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
    if (get_user_type() == STUDENT_USER):
        user_type = 'student'
    else:
        user_type = 'professor'
    if (current_user.lattes):
        print ("Lattes OK")
        lattes = False
    else:
        lattes = True
    return render_template('dashboard.html', name=current_user.full_name, user_type=user_type, missing_lattes = lattes)

# Route to the new research page
@app.route('/new-research', methods = ['GET', 'POST'])
@login_required
def new_research():
    form = ResearchForm()
    if (get_user_type() == PROFESSOR_USER):
        if (request.method == 'POST'):
            if True: #form.validate():
                existing_research = Research.objects(title=form.title.data).first()
                if existing_research is None:
                    research = Research(title = form.title.data, description = form.description.data, open_to_subscribe = form.open_to_subscribe.data, professor = current_user.full_name).save()
                    return redirect(url_for('dashboard'))
                else:
                    flash ('Uma pesquisa com esse título já está cadastrada')
                    # raise InvalidUsage('A pesquisa já existe!', status_code = 400)
            else:
                flash ('O formulário não foi validado com sucesso :(')
                # raise InvalidUsage('Formulário não validado, preencha novamente!', status_code = 400)
        else:
            return render_template('new_research.html', form = ResearchForm(), title = "Cadastrar nova pesquisa", user_type = 'professor', button_message = "Cadastrar", action = 'register')
    else:
        raise InvalidUsage(HTTP_401_DEFAULT_MESSAGE, status_code = 401)

# Route to list all available researches
@app.route('/researches', methods = ['GET', 'POST'])
@login_required
def researches():
    user_type = get_user_type()
    if (user_type == PROFESSOR_USER):
        research_list = Research.objects(professor = current_user.full_name)
        table = EditResearchTable(research_list)
        return render_template('researches.html', table = table, user_type = 'professor')
    else:
        research_list = Research.objects(open_to_subscribe = True)
        table = ApplyResearchTable(research_list)
        return render_template('researches.html', table = table, user_type = 'student')

# Route to edit a single research
@app.route('/edit-research/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user_type = get_user_type()
    if (user_type == PROFESSOR_USER):
        research = Research.objects(id = id).first() 
        if research:
            form = ResearchForm(formdata=request.form, obj=research)
            if request.method == 'POST': #and form.validate():
                research.title = form.title.data
                research.description = form.description.data
                research.open_to_subscribe = form.open_to_subscribe.data
                research.save()
                return redirect('/researches')
            return render_template('new_research.html', form = form, title = "Editar pesquisa", user_type = 'professor', id = id, button_message = "Alterar")
        else:
            raise InvalidUsage('Erro ao tentar carregar o ID #{id}'.format(id = id), status_code = 500)
    else:
        raise InvalidUsage(HTTP_401_DEFAULT_MESSAGE, status_code = 401)

# Route to apply to a single research
@app.route('/apply-research/<id>')
@login_required
def apply(id):
    user_type = get_user_type()
    if (user_type == STUDENT_USER):
        research = Research.objects(id = id).first() 
        if research:
            flash('Você enviou uma solicitação para o professor {} sobre a pesquisa {}'.format(research.professor, research.title))
            if (current_user not in research.requests):
                research.requests.append(current_user)
                research.save()
            return redirect('/researches')
        else:
            raise InvalidUsage('Erro ao tentar carregar o ID #{id}'.format(id = id), status_code = 500)
    else:
        raise InvalidUsage(HTTP_401_DEFAULT_MESSAGE, status_code = 401)

# Route to all requests
@app.route('/requests')
@login_required
def requests():
    user_type = get_user_type()
    if (user_type == PROFESSOR_USER):
        researches_list = Research.objects(professor = current_user.full_name)
        requests_list = []
        for research in researches_list:
            if research.requests != []:
                for req in research.requests:
                    requests_list.append({
                        'title' : research.title,
                        'full_name' : req.full_name,
                        'lattes' : req.lattes,
                        'email' : req.email
                    })
        requests_list.reverse()
        table = RequestsTable(requests_list)
        return render_template('researches.html', table = table, user_type = 'professor')
    else:
        raise InvalidUsage(HTTP_401_DEFAULT_MESSAGE, status_code = 401)

# class RequestsTable (Table):
#     title = Col('Pesquisa')
#     full_name = Col('Nome do aluno')
#     lattes = Col('Link Lattes')
#     email = Col('E-mail')

# Route to logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)