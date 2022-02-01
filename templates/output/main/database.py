import datetime
from exceptions import *
from data import db_session
from data.users import User
from data.tasks import Tasks

db_session.global_init("db/Universegy.db")


class Database:
    def registration(self, name, surname, grade, login, password, rights=0):
        try:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == login).first():
                raise LoginAlreadyExists
            if name == '' or surname == '' or grade == '' or login == '' or password == '':
                raise NotEnoughData
            user = User(
                login=login,
                name=name,
                surname=surname,
                grade=grade,
                rights=rights,
            )
            user.set_password(password)
            db_sess.add(user)
            db_sess.commit()
        except LoginAlreadyExists:
            return 'Логин занят'
        except NotEnoughData:
            return 'Недостаточно данных'
        else:
            return ''

    def log_in(self, login, password):
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.login == login).first()
            if user and user.check_password(password):
                return user.id, True, ''
            else:
                raise UserNotFoundError
        except UserNotFoundError:
            return 0, False, 'Неверный логин или пароль'

    def add_relation(self, user_id, task_block, tasks_done, right_answer):
        db_sess = db_session.create_session()
        tasks = Tasks(
            user_id=user_id,
            task_block=task_block,
            tasks_done=tasks_done,
            right_answers=right_answer,
            date=str(datetime.datetime.now().date()),
        )
        db_sess.add(tasks)
        db_sess.commit()

    def get_relation(self, user_id, task_block, date):
        db_sess = db_session.create_session()
        relation = db_sess.query(Tasks).filter(Tasks.user_id == user_id, Tasks.task_block == task_block,
                                               Tasks.date == date).first()
        return relation

    def get_task_amount_and_right(self, user_id, task_block, date):
        db_sess = db_session.create_session()
        relation = db_sess.query(Tasks).filter(Tasks.user_id == user_id, Tasks.task_block == task_block,
                                               Tasks.date == date).first()
        if relation:
            return relation.tasks_done, relation.right_answers
        return 0, 0

    def update_relation(self, user_id, task_block, tasks_done, right_answer, date):
        db_sess = db_session.create_session()
        relation = db_sess.query(Tasks).filter(Tasks.user_id == user_id, Tasks.task_block == task_block,
                                               Tasks.date == date).first()
        if relation:
            relation.tasks_done = tasks_done
            relation.right_answer = right_answer
            db_sess.commit()


class Users:
    def get_all(self):
        db_sess = db_session.create_session()
        return db_sess.query(User).all()

    def get_user(self, id):
        db_sess = db_session.create_session()
        return db_sess.query(User).filter(User.id == id).first()


class Users_data:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        db_sess = db_session.create_session()
        data = db_sess.query(User).all()
        new_data = []
        for user in data:
            id, login, password, rights = user.id, user.login, user.password, user.rights
            new_data.append((id, login, password, bool(rights)))
        return new_data

    def get_user_data(self, user_id):
        db_sess = db_session.create_session()
        id, login, password, rights = db_sess.query(User).filter(User.id == id).first()
        return id, login, password, bool(rights)

# class Tasks:
#     def __init__(self):
#         self.db = Database()
#
#     def get_all(self):
#         return self.db.cur.execute('''SELECT * FROM tasks''').fetchall()
#
#     def get_task(self, task_id):
#         id, task_text, answer, block = self.db.cur.execute('''SELECT * FROM tasks
#         WHERE task_id = ?''', (task_id,)).fetchall()[0]
#         return id, task_text, answer, block
#
#     def get_block(self, block):
#         data = self.db.cur.execute('''SELECT * FROM tasks WHERE block = ?''', (block,)).fetchall()
#         new_data = []
#         for elem in data:
#             id, task_text, answer, block = elem
#             new_data.append((id, task_text, answer))
#         return new_data
#
