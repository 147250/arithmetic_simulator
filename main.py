# -*- coding: utf-8 -*-

import random
import sys

from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QWidget, QPushButton, QLabel, QSlider, \
    QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit


class ArithmeticWidget(QWidget):
    operator_dict = {
        '+': int.__add__,
        '-': int.__sub__,
        '*': int.__mul__,
        '//': int.__floordiv__
    }

    def __init__(self, operand_range: tuple, operators: tuple, parent=None):
        super(ArithmeticWidget, self).__init__(parent)
        self.operand_range = operand_range
        self.operators = operators
        operand_left = random.randint(*self.operand_range)
        operand_right = random.randint(*self.operand_range)
        operator = random.choice(self.operators)
        self.correct_answer = self.operator_dict[operator](operand_left, operand_right)
        print(self.correct_answer)  # TODO: del this
        self.counter = 0

        main_box = QVBoxLayout()

        # backend timer
        self.time = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.change_time)

        # counter examples and timer
        self.counter_label = QLabel(str(self.counter))
        self.counter_label.setAlignment(Qt.AlignLeft)
        self.time_label = QLabel('0:00:00')
        self.time_label.setAlignment(Qt.AlignRight)
        h_box = QHBoxLayout()
        h_box.setContentsMargins(50, 20, 50, 0)
        h_box.addWidget(self.counter_label)
        h_box.addWidget(self.time_label)
        main_box.addLayout(h_box)

        # labels of nums and sign
        self.num_1_label = QLabel(str(operand_left))
        self.num_1_label.setAlignment(Qt.AlignRight)
        self.num_2_label = QLabel(str(operand_right))
        self.num_2_label.setAlignment(Qt.AlignLeft)
        self.sign_label = QLabel(operator)
        self.sign_label.setFixedWidth(20)
        self.sign_label.setAlignment(Qt.AlignHCenter)
        h_box = QHBoxLayout()
        h_box.setContentsMargins(80, 0, 80, 0)
        h_box.addWidget(self.num_1_label)
        h_box.addWidget(self.sign_label)
        h_box.addWidget(self.num_2_label)
        main_box.addLayout(h_box)

        # answer field
        self.answer_field = QLineEdit()
        self.answer_field.setAlignment(Qt.AlignCenter)
        self.answer_field.setValidator(QIntValidator())
        h_box = QHBoxLayout()
        h_box.setContentsMargins(80, 0, 80, 0)
        h_box.addWidget(self.answer_field)
        main_box.addLayout(h_box)

        # confirm and skip buttons
        self.confirm_btn = QPushButton('Enter answer')
        self.confirm_btn.clicked.connect(self.next_round)
        self.skip_btn = QPushButton('Skip')
        self.skip_btn.clicked.connect(self.skip_round)
        v_box = QVBoxLayout()
        v_box.setContentsMargins(80, 0, 80, 0)
        v_box.addWidget(self.confirm_btn)
        v_box.addSpacing(30)
        v_box.addWidget(self.skip_btn)
        main_box.addLayout(v_box)

        self.setLayout(main_box)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def change_time(self):
        self.time = self.time.addSecs(1)
        text = self.time.toString('h:mm:ss')
        self.time_label.setText(text)

    def next_round(self):
        answer = self.answer_field.text()
        if len(answer) and int(answer) == self.correct_answer:
            operand_left = random.randint(*self.operand_range)
            operand_right = random.randint(*self.operand_range)
            operator = random.choice(self.operators)
            self.correct_answer = self.operator_dict[operator](operand_left, operand_right)
            self.num_1_label.setText(str(operand_left))
            self.num_2_label.setText(str(operand_right))
            self.sign_label.setText(operator)
            self.counter += 1
            self.counter_label.setText(str(self.counter))
            self.answer_field.clear()
            print(self.correct_answer)  # TODO: del this

    def skip_round(self):
        operand_left = random.randint(*self.operand_range)
        operand_right = random.randint(*self.operand_range)
        operator = random.choice(self.operators)
        self.correct_answer = self.operator_dict[operator](operand_left, operand_right)
        self.num_1_label.setText(str(operand_left))
        self.num_2_label.setText(str(operand_right))
        self.sign_label.setText(operator)
        self.answer_field.clear()
        print(self.correct_answer)  # TODO: del this


class StartWidget(QWidget):
    start_signal = pyqtSignal(tuple, tuple)

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        self.difficulty = {0: (1, 10),
                           1: (5, 30),
                           2: (10, 100),
                           3: (20, 200),
                           4: (100, 1000),
                           5: (1000, 10000)}

        main_box = QVBoxLayout()

        label = QLabel('Difficulty')
        label.setAlignment(Qt.AlignCenter)
        main_box.addWidget(label)

        self.difficulty_label = QLabel('numbers from 10 to 100')
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        main_box.addWidget(self.difficulty_label)

        self.slider = QSlider()
        self.slider.setRange(0, 5)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setPageStep(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.change_difficulty_label)
        self.slider.setValue(2)
        main_box.addWidget(self.slider)

        label = QLabel('Operators')
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        main_box.addWidget(label)

        self.operator_list = []

        self.add_check = QCheckBox('+')
        self.add_check.setCheckState(Qt.Checked)
        self.add_check.toggled.connect(self.add_status_check)
        self.operator_list.append(self.add_check)
        self.sub_check = QCheckBox('-')
        self.sub_check.setCheckState(Qt.Checked)
        self.sub_check.toggled.connect(self.sub_status_check)
        self.operator_list.append(self.sub_check)
        self.mul_check = QCheckBox('*')
        self.mul_check.setCheckState(Qt.Checked)
        self.mul_check.toggled.connect(self.mul_status_check)
        self.operator_list.append(self.mul_check)
        self.floordiv_check = QCheckBox('//')
        self.floordiv_check.setCheckState(Qt.Checked)
        self.floordiv_check.toggled.connect(self.floordiv_status_check)
        self.operator_list.append(self.floordiv_check)
        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignHCenter)
        h_box.addWidget(self.add_check)
        h_box.addWidget(self.sub_check)
        h_box.addWidget(self.mul_check)
        h_box.addWidget(self.floordiv_check)
        main_box.addLayout(h_box)
        main_box.addSpacing(25)

        # button
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.start_arithmetic)
        h_box = QHBoxLayout()
        h_box.setContentsMargins(50, 0, 50, 0)
        h_box.addWidget(self.start_btn)
        main_box.addLayout(h_box)
        main_box.addSpacing(50)

        self.setLayout(main_box)

    def add_status_check(self):
        if any(map(QCheckBox.isChecked, self.operator_list)):
            return
        self.add_check.setChecked(True)

    def sub_status_check(self):
        if any(map(QCheckBox.isChecked, self.operator_list)):
            return
        self.sub_check.setChecked(True)

    def mul_status_check(self):
        if any(map(QCheckBox.isChecked, self.operator_list)):
            return
        self.mul_check.setChecked(True)

    def floordiv_status_check(self):
        if any(map(QCheckBox.isChecked, self.operator_list)):
            return
        self.floordiv_check.setChecked(True)

    def start_arithmetic(self):
        operand_range = self.difficulty[self.slider.value()]
        operators = tuple(elem.text() for elem in self.operator_list if elem.isChecked())
        self.start_signal.emit(operand_range, operators)

    def change_difficulty_label(self, value: int):
        num_1, num_2 = self.difficulty.get(value, (10, 100))
        text = f'numbers from {num_1} to {num_2}'
        self.difficulty_label.setText(text)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # create sub windows
        self.mdi_area = QMdiArea()

        start_widget = StartWidget()
        start_widget.start_signal.connect(self.create_arithmetic_widget)
        self.start_window = self.mdi_area.addSubWindow(start_widget)
        self.start_window.setWindowFlags(Qt.FramelessWindowHint)
        self.start_window.showMaximized()

        self.arithmetic_widget = None

        self.setCentralWidget(self.mdi_area)

    def create_arithmetic_widget(self, operand_range: tuple, operators: tuple):
        arithmetic_widget = ArithmeticWidget(operand_range, operators)
        self.arithmetic_widget = self.mdi_area.addSubWindow(arithmetic_widget)
        self.arithmetic_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.start_window.hide()
        self.arithmetic_widget.showMaximized()

    def move_to_center(self):
        """Move window to center desktop"""
        point = QPoint(self.width() // 2, self.height() // 2 + 100)
        pos = QApplication.desktop().availableGeometry().center()
        self.move(pos - point)


class ArithmeticApplication(QApplication):
    """The Application object"""

    def __init__(self, argv):
        super(ArithmeticApplication, self).__init__(argv)
        # with open('style.qss', 'r') as file:
        #     style = file.read()
        #     self.setStyleSheet(style)

        # create main window
        self.main_window = MainWindow()
        self.main_window.resize(400, 400)
        self.main_window.move_to_center()
        self.main_window.show()


if __name__ == '__main__':
    arithmetic_app = ArithmeticApplication(sys.argv)
    sys.exit(arithmetic_app.exec())
