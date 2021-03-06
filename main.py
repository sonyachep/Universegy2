import sys
import random

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout
import datetime
import requests

IP = 'https://phela.pythonanywhere.com/'

INTEGERS = {'целого': [10, 1],
            'десятков': [100, 2],
            'сотен': [1000, 3],
            'тысяч': [10000, 4]}
FLOAT = {'десятых': [1, 2],
         'сотых': [2, 3],
         'тысячных': [3, 4]}


def round_float(num, i):
    orig_num, str_num = str(num).split('.')
    if len(str_num) > i:
        if int(str_num[i]) >= 5:
            return float(f'{orig_num}.{int(str_num[:i]) + 1}')
        else:
            return float(f'{orig_num}.{int(str_num[:i])}')
    else:
        return num


def round_int(num, i):
    return int(round_float(num / i, 1) * i)


def make_task(block):
    text = ''

    if block == 1:
        variations = list(INTEGERS.items())
        name, rounding = random.choice(variations)
        number = round(random.random() * random.randint(10 ** rounding[1], 100_000), random.randint(1, 5))
        while '9' in str(number):
            number = round(random.random() * random.randint(10 ** rounding[1], 100_000), random.randint(1, 5))
        text += f'Округлите данное число {number} до {name}'
        answer = round_int(number, rounding[0])

    if block == 2:
        variations = list(FLOAT.items())
        name, rounding = random.choice(variations)
        number = round(random.random() * random.randint(1, 10_000), random.randint(rounding[1], 5))
        while '9' in str(number):
            number = round(random.random() * random.randint(1, 10_000), random.randint(rounding[1], 5))
        text += f'Округлите данное число {number} до {name}'
        answer = round_float(number, rounding[0])

    if block == 3:
        i = random.randint(1, 2)
        if i == 1:
            variations = list(INTEGERS.items())
            name, rounding = random.choice(variations)
            number = round(random.random() * random.randint(10 ** rounding[1], 100_000), random.randint(1, 5))
            while '9' in str(number):
                number = round(random.random() * random.randint(10 ** rounding[1], 100_000), random.randint(1, 5))
            text += f'Округлите данное число {number} до {name}'
            answer = round_int(number, rounding[0])

        elif i == 2:
            variations = list(FLOAT.items())
            name, rounding = random.choice(variations)
            number = round(random.random() * random.randint(1, 10_000), random.randint(rounding[1], 5))
            while '9' in str(number):
                number = round(random.random() * random.randint(1, 10_000), random.randint(rounding[1], 5))
            text += f'Округлите данное число {number} до {name}'
            answer = round_float(number, rounding[0])
    return text, answer


class Universegy(QMainWindow):
    def __init__(self):

        super().__init__()
        uic.loadUi('universegy.ui', self)
        self.setWindowTitle('Universegy')
        self.logged = False
        self.current_user = 0
        self.block = 0
        self.task_number = 1
        self.right_answer = 0
        self.wrong_answer = 0
        self.answer = ''

        self.run_to_page1()

        self.back_to_main_from_login.clicked.connect(self.run_to_page1)
        self.back_to_main_from_registration.clicked.connect(self.run_to_page1)

        self.login.clicked.connect(self.run_to_page2)
        self.registration.clicked.connect(self.run_to_page3)
        self.logout.clicked.connect(self.run_to_page1)
        self.integer_round.clicked.connect(self.run_to_page5)
        self.float_round.clicked.connect(self.run_to_page5)
        self.random_round.clicked.connect(self.run_to_page5)
        self.back_to_theme.clicked.connect(self.run_to_page5)
        self.go_main.clicked.connect(self.run_to_page4)

        self.task1.clicked.connect(self.show_tasks)
        self.task2.clicked.connect(self.show_tasks)
        self.task3.clicked.connect(self.show_tasks)
        self.task4.clicked.connect(self.show_tasks)
        self.task5.clicked.connect(self.show_tasks)
        self.task6.clicked.connect(self.show_tasks)
        self.task7.clicked.connect(self.show_tasks)
        self.task8.clicked.connect(self.show_tasks)
        self.task9.clicked.connect(self.show_tasks)
        self.task10.clicked.connect(self.show_tasks)
        self.task11.clicked.connect(self.show_tasks)
        self.task12.clicked.connect(self.show_tasks)
        self.task13.clicked.connect(self.show_tasks)
        self.task14.clicked.connect(self.show_tasks)
        self.task15.clicked.connect(self.show_tasks)
        self.task16.clicked.connect(self.show_tasks)
        self.task17.clicked.connect(self.show_tasks)
        self.task18.clicked.connect(self.show_tasks)
        self.task19.clicked.connect(self.show_tasks)
        self.task20.clicked.connect(self.show_tasks)
        self.next_task.clicked.connect(self.show_tasks)

        self.set_answer.clicked.connect(self.write_current_answer)

        self.enterance.clicked.connect(self.log_in)

        self.set_user.clicked.connect(self.registrate)
        self.show_password_reg.stateChanged.connect(self.show_pass_reg)
        self.show_password_login.stateChanged.connect(self.show_pass_login)

    def run_to_page1(self):
        self.current_user = 0
        self.logged = False
        self.stackedWidget.setCurrentIndex(0)

    def run_to_page2(self):
        self.login_in_edit.setText('')
        self.password_in_edit.setText('')
        self.login_error_label.setText('')
        self.stackedWidget.setCurrentIndex(1)

    def run_to_page3(self):
        self.name_edit.setText('')
        self.surname_edit.setText('')
        self.class_choice.setCurrentIndex(0)
        self.login_edit.setText('')
        self.password_edit.setText('')
        self.registrationerror_label.setText('')
        self.server_error.setText('')
        self.stackedWidget.setCurrentIndex(2)

    def run_to_page4(self):
        if self.logged:
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.run_to_page1()

    def run_to_page5(self):
        self.answer_edit.setText('')
        self.task_view.setText('')
        block = self.sender().text()
        if block == 'Округление целых чисел':
            self.block = 1
            self.task_number = 1
            self.right_answer = 0
            self.wrong_answer = 0
            self.stackedWidget.setCurrentIndex(4)
        if block == 'Округление десятичных дробей':
            self.block = 2
            self.task_number = 1
            self.right_answer = 0
            self.wrong_answer = 0
            self.stackedWidget.setCurrentIndex(4)
        if block == 'Случайные задания':
            self.block = 3
            self.task_number = 1
            self.right_answer = 0
            self.wrong_answer = 0
        self.stackedWidget.setCurrentIndex(4)
        try:
            response = requests.get(f'{IP}/db/get_task_amount_and_right',
                                    json={'user_id': self.current_user,
                                          'task_block': self.block,
                                          'date': str(datetime.datetime.now().date())}).json()
            self.task_number, self.right_answer = response['task_number'], response['right_answer']
            self.wrong_answer = self.task_number - self.right_answer
            self.task_number += 1
        except IndexError:
            pass
        self.previous_answer.setText('')
        self.show_tasks()

    def run_to_page6(self):
        self.stackedWidget.setCurrentIndex(5)

    def show_pass_reg(self):
        if self.show_password_reg.checkState():
            self.password_edit.setEchoMode(0)
        else:
            self.password_edit.setEchoMode(2)

    def show_pass_login(self):
        if self.show_password_login.checkState():
            self.password_in_edit.setEchoMode(0)
        else:
            self.password_in_edit.setEchoMode(2)

    def log_in(self):
        login = self.login_in_edit.text()
        password = self.password_in_edit.text()
        try:
            response = requests.get(f'{IP}/db/log_in',
                                    json={'login': login, 'password': password}).json()
            self.current_user, self.logged, error = response['user'], response['logged'], response['error']
            if not error:
                self.run_to_page4()
            self.login_error_label.setText(error)
        except:
            self.login_error_label.setText('Отсутствует подключение к сервису Universegy')

    def registrate(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        student_class = self.class_choice.currentText()
        login = self.login_edit.text()
        password = self.password_edit.text()
        try:
            error = requests.post(f'{IP}/db/registration',
                                  json={'name': name, 'surname': surname, 'student_class': student_class,
                                        'login': login,
                                        'password': password}).json()['error']
            if not error:
                self.run_to_page1()
            self.registrationerror_label.setText(error)
        except:
            self.server_error.setText('Отсутствует подключение к сервису Universegy')

    def show_tasks(self):
        self.right_label.setText(str(self.right_answer))
        self.wrong_label.setText(str(self.wrong_answer))
        self.task_amount.setText(str(self.task_number))
        if self.sender().text() == '->':
            self.task_number += 1
            self.wrong_answer += 1
        text, self.answer = make_task(self.block)
        self.task_view.setText(text)

    def write_current_answer(self):
        student_answer = self.answer_edit.text()
        self.answer_edit.setText('')
        self.check_answer(student_answer)
        self.task_number += 1
        if requests.get(f'{IP}/db/get_relation',
                        json={'current_user': self.current_user, 'task_block': self.block,
                              'date': str(datetime.datetime.now().date())}).json()['response']:
            requests.post(f'{IP}/db/update_relation',
                          json={'current_user': self.current_user, 'task_block': self.block,
                                'task_number': self.task_number - 1, 'right_answer': self.right_answer,
                                'date': str(datetime.datetime.now().date())})
        else:
            requests.post(f'{IP}/db/add_relation',
                          json={'current_user': self.current_user, 'task_block': self.block,
                                'task_number': self.task_number - 1, 'right_answer': self.right_answer})
        self.show_tasks()

    def check_answer(self, student_answer):
        if student_answer == str(self.answer) or student_answer == ','.join(str(self.answer).split('.')):
            self.right_answer += 1
            self.previous_answer.setText('')
        else:
            self.wrong_answer += 1
            self.previous_answer.setText(f'Предыдущий ответ был: {self.answer}, будь внимательнее!')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Universegy()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
