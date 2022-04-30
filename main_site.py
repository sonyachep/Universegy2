from flask import Flask, render_template, redirect, request, abort
from data import db_session, uni_api
from forms.user import LoginForm
from data.users import User
from data.tasks import Tasks
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from database import Database

db_session.global_init("db/Universegy.db")
db = Database()

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def start():
    try:
        return render_template('universegy.html',
                               greeting=f'Добро пожаловать, {current_user.name.capitalize()} {current_user.surname.capitalize()}!')
    except AttributeError:
        return render_template('universegy.html', greeting='Зарегиструруйтесь, чтобы продолжить')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            if user.rights == 0:
                return render_template('log_in.html',
                                       message="Вы не учитель",
                                       form=form)
            login_user(user, remember=form.remember_me.data)
            return redirect('/students')
        return render_template('log_in.html',
                               message="Неверный логин или пароль",
                               form=form)
    return render_template('log_in.html', title='Авторизация', form=form)


@app.route('/log_out')
def logout():
    try:
        name = current_user.name
        logout_user()
        return redirect("/")
    except AttributeError:
        return redirect("/")


@app.route('/students', methods=['GET', 'POST'])
def students():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    people = {}
    for user in users:
        if user.rights == 1:
            continue
        sorted_tasks = {}
        sum_first = 0
        sum_second = 0
        sum_third = 0
        tasks = db_sess.query(Tasks).filter(Tasks.user_id == user.id).all()
        for task in tasks:
            if task.date in sorted_tasks:
                pass
            else:
                sorted_tasks[task.date] = {1: 0,
                                           2: 0,
                                           3: 0}
            sorted_tasks[task.date][task.task_block] += task.right_answers
            if task.task_block == 1:
                sum_first += task.right_answers
            if task.task_block == 2:
                sum_second += task.right_answers
            if task.task_block == 3:
                sum_third += task.right_answers
        people[f'{user.name} {user.surname}'] = {'grade': user.grade,
                                                 'total': {1: sum_first,
                                                           2: sum_second,
                                                           3: sum_third},
                                                 'date': sorted_tasks}
    max_data = len(sorted(people.items(), key=lambda x: -len(x[1]['date']))[0][1]['date'])
    try:
        return render_template('students.html', people=people, max_data=max_data,
                               greeting=f'Добро пожаловать {current_user.name.capitalize()} {current_user.surname.capitalize()}!')
    except AttributeError:
        return render_template('students.html', people={}, max_data=0, greeting='Зарегиструруйтесь чтобы продолжить')


@app.route('/db/get_task_amount_and_right', methods=['GET'])
def get_task_amount_and_right():
    if request.method == 'GET':
        user_id = request.json['user_id']
        task_block = request.json['task_block']
        date = request.json['date']
        task_number, right_answer = db.get_task_amount_and_right(user_id, task_block, date=date)
        return {'task_number': task_number, 'right_answer': right_answer}


@app.route('/db/log_in', methods=['GET'])
def db_log_in():
    if request.method == 'GET':
        login = request.json['login']
        password = request.json['password']
        user, logged, error = db.log_in(login, password)
        return {'user': user, 'logged': logged, 'error': error}


@app.route('/db/registration', methods=['POST'])
def db_registration():
    if request.method == 'POST':
        name = request.json['name']
        surname = request.json['surname']
        student_class = request.json['student_class']
        login = request.json['login']
        password = request.json['password']
        error = db.registration(name, surname, student_class, login, password)
        return {'error': error}
    return


@app.route('/db/get_relation', methods=['GET'])
def get_relation():
    if request.method == 'GET':
        user = request.json['current_user']
        task_block = request.json['task_block']
        date = request.json['date']
        response = db.get_relation(user, task_block, date=date)
        if response:
            return {'response': response.id}
        return {'response': False}
    return


@app.route('/db/update_relation', methods=['POST'])
def update_relation():
    if request.method == 'POST':
        user = request.json['current_user']
        task_block = request.json['task_block']
        task_number = request.json['task_number']
        right_answer = request.json['right_answer']
        date = request.json['date']
        response = db.update_relation(user, task_block, task_number, right_answer,
                                      date=date)
        return
    return


@app.route('/db/add_relation', methods=['POST'])
def add_relation():
    if request.method == 'POST':
        user = request.json['current_user']
        task_block = request.json['task_block']
        task_number = request.json['task_number']
        right_answer = request.json['right_answer']
        response = db.add_relation(user, task_block, task_number, right_answer)
        return
    return


def main():
    db_session.global_init("db/Universegy.db")
    api.add_resource(uni_api.UniResource, '/api/uni/<int:id>')
    app.run()


if __name__ == '__main__':
    main()
