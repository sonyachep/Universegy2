from flask import Flask, render_template, redirect, request, abort
from data import db_session, uni_api
from forms.user import LoginForm
from data.users import User
from data.tasks import Tasks
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

db_session.global_init("db/Universegy.db")

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
    return render_template('universegy.html')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        print(1)
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
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/students', methods=['GET', 'POST'])
@login_required
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
    print(people)

    return render_template('students.html', people=people, surname=current_user.surname.capitalize(), name=current_user.name.capitalize())


def main():
    db_session.global_init("db/Universegy.db")
    api.add_resource(uni_api.UniResource, '/api/uni/<int:id>')
    app.run()


if __name__ == '__main__':
    main()
