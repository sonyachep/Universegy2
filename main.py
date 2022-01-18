import sys
import random

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout

from data import db_session
from data.users import User
from data.tasks import Tasks

from database import *

db_session.global_init("db/Universegy.db")

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
        self.db = Database()
        self.users = Users()

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
        self.is_teacher.setCheckState(False)
        self.stackedWidget.setCurrentIndex(2)

    def run_to_page4(self):
        if self.logged:
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.run_to_page1()

    def run_to_page5(self):
        self.answer_edit.setText('')
        self.task_view.setText('')
        # self.task1_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task2_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task3_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task4_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task5_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task6_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task7_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task8_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task9_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task10_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task11_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task12_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task13_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task14_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task15_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task16_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task17_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task18_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task19_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
        # self.task20_label.setStyleSheet('background-color: rgb(217, 247, 255); border-radius: 6px')
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
            self.task_number, self.right_answer = self.db.get_task_amount_and_right(self.current_user, self.block,
                                                                                    str(datetime.datetime.now().date()))
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
        self.current_user, self.logged, error = self.db.log_in(login, password)
        if not error:
            self.run_to_page4()
        self.login_error_label.setText(error)

    def registrate(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        student_class = self.class_choice.currentText()
        login = self.login_edit.text()
        password = self.password_edit.text()
        is_teacher = int(self.is_teacher.checkState())
        error = self.db.registration(name, surname, student_class, login, password, is_teacher)
        if not error:
            self.run_to_page1()
        self.registrationerror_label.setText(error)

    def show_tasks(self):
        self.right_label.setText(str(self.right_answer))
        self.wrong_label.setText(str(self.wrong_answer))
        self.task_amount.setText(str(self.task_number))
        # if self.sender().text() == '<-':
        #     self.task_number -= 1
        if self.sender().text() == '->':
            self.task_number += 1
            self.wrong_answer += 1
        # else:
        #     self.task_number = int(self.sender().text()[8:])
        # if self.task_number > 20:
        #     self.task_number = 20
        # if self.task_number < 1:
        #     self.task_number = 1
        # if self.answers[self.block][self.task_number]:
        #     self.set_answer.hide()
        #     self.answer_edit.setText(str(self.answers[self.block][self.task_number]))
        # else:
        #     self.set_answer.show()
        # tasks = self.tasks.get_block(self.block)
        # for elem in tasks:
        #     id, text, answer = elem
        #     id = id % 20
        #     if id == 0:
        #         id = 20
        #     if id == self.task_number:
        text, self.answer = make_task(self.block)
        self.task_view.setText(text)
        # self.answer_edit.setText(self.answers[self.block][self.task_number])
        # break

    def write_current_answer(self):
        student_answer = self.answer_edit.text()
        self.answer_edit.setText('')
        self.check_answer(student_answer)
        self.task_number += 1
        if self.db.get_relation(self.current_user, self.block, date=str(datetime.datetime.now().date())):
            self.db.update_relation(self.current_user, self.block, self.task_number - 1, self.right_answer,
                                    date=str(datetime.datetime.now().date()))
        else:
            self.db.add_relation(self.current_user, self.block, self.task_number - 1, self.right_answer)
        # self.right_label.setText(str(self.right_answer))
        # self.wrong_label.setText(str(self.wrong_answer))
        # self.task_amount.setText(str(self.task_number))
        self.show_tasks()

    def check_answer(self, student_answer):
        if student_answer == str(self.answer) or student_answer == ','.join(str(self.answer).split('.')):
            self.right_answer += 1
            self.previous_answer.setText('')
        else:
            self.wrong_answer += 1
            self.previous_answer.setText(f'Предыдущий ответ был: {self.answer}, будь внимательнее!')
            # self.db.add_relation(self.current_user, id + (20 * (self.block - 1)))
            # self.answers[self.block][self.task_number] = student_answer
            # self.set_answer.hide()
        #     if id == 1:
        #         self.task1_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 2:
        #         self.task2_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 3:
        #         self.task3_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 4:
        #         self.task4_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 5:
        #         self.task5_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 6:
        #         self.task6_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 7:
        #         self.task7_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 8:
        #         self.task8_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 9:
        #         self.task9_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 10:
        #         self.task10_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 11:
        #         self.task11_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 12:
        #         self.task12_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 13:
        #         self.task13_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 14:
        #         self.task14_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 15:
        #         self.task15_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 16:
        #         self.task16_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 17:
        #         self.task17_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 18:
        #         self.task18_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 19:
        #         self.task19_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        #     if id == 20:
        #         self.task20_label.setStyleSheet('background-color: rgb(0, 255, 0); border-radius: 6px')
        # else:
        #     if id == 1:
        #         self.task1_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 2:
        #         self.task2_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 3:
        #         self.task3_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 4:
        #         self.task4_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 5:
        #         self.task5_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 6:
        #         self.task6_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 7:
        #         self.task7_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 8:
        #         self.task8_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 9:
        #         self.task9_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 10:
        #         self.task10_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 11:
        #         self.task11_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 12:
        #         self.task12_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 13:
        #         self.task13_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 14:
        #         self.task14_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 15:
        #         self.task15_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 16:
        #         self.task16_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 17:
        #         self.task17_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 18:
        #         self.task18_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 19:
        #         self.task19_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')
        #     if id == 20:
        #         self.task20_label.setStyleSheet('background-color: rgb(255, 0, 0); border-radius: 6px')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Universegy()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
