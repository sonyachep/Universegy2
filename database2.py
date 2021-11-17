import sqlite3
from exceptions2 import *

DATABASE = 'Universegy2.db'


class Database:
    def __init__(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cur = self.connect.cursor()

    def registration(self, name, surname, student_class, login, password, is_teacher):
        try:
            logins = self.cur.execute('''SELECT login FROM users_data''').fetchall()[0][0]
            if login in logins:
                raise LoginAlreadyExists
            if name == '' or surname == '' or student_class == '' or login == '' or password == '':
                raise NotEnoughData
            self.add_user(name, surname, student_class)
            self.connect.commit()
            user_id = self.cur.execute('''SELECT id FROM users WHERE name = ?''', (name,)).fetchall()[0][0]

            self.add_user_data(user_id, login, password, is_teacher)
            self.connect.commit()
        except LoginAlreadyExists:
            return 'Логин занят'
        except NotEnoughData:
            return 'Недостаточно данных'
        else:
            return ''

    def log_in(self, login, password):
        try:
            all_users = self.cur.execute('''SELECT user_id, login, password FROM users_data''').fetchall()
            log_pass = [(str(elem[1]), str(elem[2])) for elem in all_users]
            ids = [elem[0] for elem in all_users]
            if (login, password) in log_pass:
                return ids[log_pass.index((login, password))], True, ''
            else:
                raise UserNotFoundError
        except UserNotFoundError:
            return 0, False, 'Неверный логин или пароль'

    def add_user(self, name, surname, student_class):
        self.cur.execute('''INSERT INTO users (name, surname, class, blocks_done)
                        VALUES(?, ?, ?, ?)''', (name, surname, student_class, ''))

    def add_user_data(self, user_id, login, password, is_teacher):
        self.cur.execute('''INSERT INTO users_data (user_id, login, password, rights)
                                        VALUES(?, ?, ?, ?)''', (user_id, login, password, is_teacher))

    def add_relation(self, user_id, task_id):
        print(user_id, task_id)
        self.cur.execute('''INSERT INTO relations (user_id, task_id)
                                                VALUES(?, ?)''', (user_id, task_id))
        self.connect.commit()

    def add_block_to_user(self, user_id, blocks):
        self.cur.execute('''UPDATE users SET blocks_done = ? WHERE id = ?''', (blocks, user_id))
        self.connect.commit()

class Users:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        return self.db.cur.execute('''SELECT * FROM users''').fetchall()

    def get_user(self, id):
        return self.db.cur.execute('''SELECT * FROM users WHERE id = ?''', (id,)).fetchall()[0]

    def get_blocks(self, id):
        return str(self.db.cur.execute('''SELECT blocks_done FROM users WHERE id = ?''', (id,)).fetchall()[0][0])


class Users_data:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        data = self.db.cur.execute('''SELECT * FROM users_data''').fetchall()
        new_data = []
        for elem in data:
            id, login, password, rights = elem
            new_data.append((id, login, password, bool(rights)))
        return new_data

    def get_user_data(self, user_id):
        id, login, password, rights = self.db.cur.execute('''SELECT * FROM users_data 
        WHERE user_id = ?''', (user_id,)).fetchall()[0]
        return id, login, password, bool(rights)


class Tasks:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        return self.db.cur.execute('''SELECT * FROM tasks''').fetchall()

    def get_task(self, task_id):
        id, task_text, answer, block = self.db.cur.execute('''SELECT * FROM tasks 
        WHERE task_id = ?''', (task_id,)).fetchall()[0]
        return id, task_text, answer, block

    def get_block(self, block):
        data = self.db.cur.execute('''SELECT * FROM tasks WHERE block = ?''', (block,)).fetchall()
        new_data = []
        for elem in data:
            id, task_text, answer, block = elem
            new_data.append((id, task_text, answer))
        return new_data


task = Tasks()
print(task.get_all())
print(task.get_task(2))
print(task.get_block(1))

# user_data = Users_data()
# print(user_data.get_all())
#
# print(user_data.get_user_data(1))
# print(user_data.get_user_data(2))
