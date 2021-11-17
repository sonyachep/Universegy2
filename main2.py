import sys

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

from database2 import *


class Universegy2(QMainWindow):
    def __init__(self):
        self.db = Database()
        self.tasks = Tasks()
        self.users = Users()

        super().__init__()
        uic.loadUi('universegy2.ui', self)
        self.logged = False
        self.current_user = 0
        self.block = 0

        self.answers = {1: {1: '',
                            2: '',
                            3: '',
                            4: '',
                            5: '',
                            6: '',
                            7: '',
                            8: '',
                            9: '',
                            10: '',
                            11: '',
                            12: '',
                            13: '',
                            14: '',
                            15: '',
                            16: '',
                            17: '',
                            18: '',
                            19: '',
                            20: ''
                            },
                        2: {1: '',
                            2: '',
                            3: '',
                            4: '',
                            5: '',
                            6: '',
                            7: '',
                            8: '',
                            9: '',
                            10: '',
                            11: '',
                            12: '',
                            13: '',
                            14: '',
                            15: '',
                            16: '',
                            17: '',
                            18: '',
                            19: '',
                            20: ''},
                        3: {1: '',
                            2: '',
                            3: '',
                            4: '',
                            5: '',
                            6: '',
                            7: '',
                            8: '',
                            9: '',
                            10: '',
                            11: '',
                            12: '',
                            13: '',
                            14: '',
                            15: '',
                            16: '',
                            17: '',
                            18: '',
                            19: '',
                            20: ''}
                        }
        self.task_number = 0

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
        self.task1.clicked.connect(self.run_to_page6)
        self.task2.clicked.connect(self.run_to_page6)
        self.task3.clicked.connect(self.run_to_page6)
        self.task4.clicked.connect(self.run_to_page6)
        self.task5.clicked.connect(self.run_to_page6)
        self.task6.clicked.connect(self.run_to_page6)
        self.task7.clicked.connect(self.run_to_page6)
        self.task8.clicked.connect(self.run_to_page6)
        self.task9.clicked.connect(self.run_to_page6)
        self.task10.clicked.connect(self.run_to_page6)
        self.set_answer.clicked.connect(self.get_color)



        self.enterance.clicked.connect(self.log_in)

        self.set_user.clicked.connect(self.registrate)



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
            blocks_done = str(self.users.get_blocks(self.current_user))
            self.done_1.setText('Не выполнено')
            self.done_2.setText('Не выполнено')
            self.done_3.setText('Не выполнено')
            if '1' in blocks_done:
                self.done_1.setText('Выполнено')
            if '2' in blocks_done:
                self.done_2.setText('Выполнено')
            if '3' in blocks_done:
                self.done_3.setText('Выполнено')

            self.stackedWidget.setCurrentIndex(3)
        else:
            self.run_to_page1()

    def run_to_page5(self):
        '''self.task_view.setText('')
        self.block_task_choices.setCurrentIndex(0)
        block = self.sender().text()
        blocks_done = str(self.users.get_blocks(self.current_user))
        if block == 'Округление целых чисел':
            self.block = 1
            if str(self.block) in blocks_done:
                return
            self.stackedWidget.setCurrentIndex(4)
        if block == 'Округление десятичных дробей':
            self.block = 2
            if str(self.block) in blocks_done:
                return
            self.stackedWidget.setCurrentIndex(4)
        if block == 'Случайные задания':
            self.block = 3
            if str(self.block) in blocks_done:
                return'''
        self.stackedWidget.setCurrentIndex(4)

    def run_to_page6(self):
        self.stackedWidget.setCurrentIndex(5)

    def get_color(self):
        self.answer_edit.setStyleSheet("QLineEdit {border: 2px solid  rgb(255, 0, 0);}")
        print(222)

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
        try:
            self.task_number = int(self.sender().currentText())
        except ValueError:
            return
        tasks = self.tasks.get_block(self.block)
        for elem in tasks:
            id, text, answer = elem
            id = id % 20
            if id == 0:
                id = 20
            if id == self.task_number:
                self.task_view.setText(text)
                break

    def write_current_answer(self):
        answer = self.answer_edit.text()
        self.answers[self.block][self.task_number] = answer
        self.answer_edit.setText('')

    def check_answer(self):
        score = ''
        total = 0
        answers = self.answers[self.block]
        print(answers)
        for id, student_answer in answers.items():
            id = id % 20
            if id == 0:
                id = 20
            id_wrong, task_text, right_answer, block = self.tasks.get_task(id + (20 * (self.block - 1)))


            if student_answer == str(right_answer):
                if len(f'{id}: +') < 5:
                    score += f'{id}:  +\n'
                else:
                    score += f'{id}: +\n'
                total += 1
                self.db.add_relation(self.current_user, id + (20 * (self.block - 1)))
            else:
                if len(f'{id}: -') < 5:
                    score += f'{id}:   -\n'
                else:
                    score += f'{id}: -\n'

        result = f'Результат: {total}/{len(answers.keys())}'
        self.result_view.setText(result)
        self.answer_view.setText(score)
        blocks_done = self.users.get_blocks(self.current_user)
        print(blocks_done)
        blocks_done += str(self.block)
        self.db.add_block_to_user(self.current_user, blocks_done)



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Universegy2()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
