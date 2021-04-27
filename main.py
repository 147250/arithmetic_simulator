# -*- coding: utf-8 -*-

import random
import sys

from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QTime, QRect
from PyQt5.QtGui import QIntValidator, QMouseEvent, QPainter, QPaintEvent, QColor, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QWidget, QPushButton, QLabel, QSlider, \
    QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit, QMessageBox


class MyButton(QPushButton):

    def __init__(self, btn_text: str, bg_color: str = 'green', progress_color: str = 'yellow',
                 text_color: str = 'white', delay: bool = True, parent=None):
        super(MyButton, self).__init__(btn_text, parent)
        # custom properties
        self._delay = delay
        self.width = 75
        self.height = 75
        self.progress_width = 10
        self.value = 0
        self.MAX_VALUE = 100
        self.progress_color = progress_color
        self.text_color = text_color
        self.progress_rounded_cap = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_value)

        self.setFixedSize(self.width, self.height)

        self.setStyleSheet(f'background-color: {bg_color};'
                           f' border-radius: {self.width // 2}px;'
                           f' font-size: {self.width // 4}px;'
                           f' color: {self.text_color};')

    def set_delay(self, value: bool):
        self._delay = value

    def paintEvent(self, event: QPaintEvent):
        QPushButton.paintEvent(self, event)
        if not self._delay:
            return
        # set progress parameter
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width // 2
        value = self.value * 360 // self.MAX_VALUE

        # painter
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.HighQualityAntialiasing)

        # draw rectangle
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # pen
        pen = QPen()
        color = QColor(self.progress_color)
        pen.setColor(color)
        pen.setWidth(11)

        # set round cap
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # create arc / circular progress
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        paint.end()

    def _reset_activation(self):
        self.timer.stop()
        self.value = 0
        self.update()

    def _point_in_circle(self, x, y) -> bool:
        radius = self.width // 2
        x -= radius
        y -= radius
        if (x ** 2 + y ** 2) ** 0.5 <= radius:
            return True
        return False

    def change_value(self):
        if self.value >= self.MAX_VALUE:
            self._reset_activation()
            self.clicked.emit()
            return
        self.value += 4
        self.update()

    def mousePressEvent(self, evnt: QMouseEvent):
        if self._delay and evnt.button() == Qt.LeftButton and self._point_in_circle(evnt.x(), evnt.y()):
            self.timer.start(20)

    def mouseReleaseEvent(self, evnt: QMouseEvent):
        if not self._delay and evnt.button() == Qt.LeftButton and self._point_in_circle(evnt.x(), evnt.y()):
            self.clicked.emit()
            return
        if self.timer.isActive():
            self._reset_activation()

    def mouseMoveEvent(self, evnt: QMouseEvent):
        if not self._point_in_circle(evnt.x(), evnt.y()):
            self._reset_activation()


class ArithmeticWidget(QWidget):
    operator_dict = {
        '+': int.__add__,
        '-': int.__sub__,
        '*': int.__mul__,
        '//': int.__floordiv__
    }

    stop_signal = pyqtSignal()

    def __init__(self, operand_range: tuple, operators: tuple, parent=None):
        super(ArithmeticWidget, self).__init__(parent)
        self.operand_range = operand_range
        self.operators = operators
        self.correct_answer = None
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
        self.num_1_label = QLabel()
        self.num_1_label.setAlignment(Qt.AlignRight)
        self.num_2_label = QLabel()
        self.num_2_label.setAlignment(Qt.AlignLeft)
        self.sign_label = QLabel()
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
        self.answer_field.returnPressed.connect(self.check_answer)
        self.answer_field.setAlignment(Qt.AlignCenter)
        self.answer_field.setValidator(QIntValidator())
        h_box = QHBoxLayout()
        h_box.setContentsMargins(80, 0, 80, 0)
        h_box.addWidget(self.answer_field)
        main_box.addLayout(h_box)

        # buttons
        self.confirm_btn = MyButton(btn_text='Enter', bg_color='rgb(138, 226, 52)', text_color='black', delay=False)
        self.confirm_btn.clicked.connect(self.check_answer)
        h_box = QHBoxLayout()
        h_box.addWidget(self.confirm_btn)
        main_box.addLayout(h_box)

        self.skip_btn = MyButton(btn_text='Skip', bg_color='rgb(252, 233, 79)', text_color='black', delay=False)
        self.skip_btn.clicked.connect(self.show_next_example)

        self.stop_btn = MyButton(btn_text='Stop', bg_color='red', text_color='white')
        self.stop_btn.clicked.connect(self.stop_session)
        h_box = QHBoxLayout()
        h_box.addWidget(self.skip_btn)
        h_box.addWidget(self.stop_btn)
        main_box.addLayout(h_box)

        self.setLayout(main_box)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show_next_example()

    def change_time(self):
        self.time = self.time.addSecs(1)
        text = self.time.toString('h:mm:ss')
        self.time_label.setText(text)

    def show_next_example(self):
        operand_left = random.randint(*self.operand_range)
        operand_right = random.randint(*self.operand_range)
        operator = random.choice(self.operators)
        if operator == '//':
            operand_left *= operand_right
        self.correct_answer = self.operator_dict[operator](operand_left, operand_right)
        self.num_1_label.setText(str(operand_left))
        self.num_2_label.setText(str(operand_right))
        self.sign_label.setText(operator)
        self.answer_field.clear()
        print(self.correct_answer)  # TODO: del this

    def check_answer(self):
        answer = self.answer_field.text()
        if len(answer) and int(answer) == self.correct_answer:
            self.show_next_example()
            self.counter += 1
            self.counter_label.setText(str(self.counter))

    def stop_session(self):
        """Show results of session and emmit stop signal"""
        self.timer.stop()
        result_window = QMessageBox(self)
        time = self.time.second()
        counter = self.counter
        average_time = '--undefined--'
        if counter and time:
            average_time = f'{time / counter:.2}'

        result_window.setText(f'time: {self.time.toString()}\n\n'
                              f'total examples: {counter}\n\n'
                              f'Average time for arithmetic operation {average_time} second(s)'
                              )
        result_window.exec()
        self.stop_signal.emit()


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
        arithmetic_widget.stop_signal.connect(self.reshow_start_widget)
        self.arithmetic_widget = self.mdi_area.addSubWindow(arithmetic_widget)
        self.arithmetic_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.start_window.hide()
        self.arithmetic_widget.showMaximized()

    def move_to_center(self):
        """Move window to center desktop"""
        point = QPoint(self.width() // 2, self.height() // 2 + 100)
        pos = QApplication.desktop().availableGeometry().center()
        self.move(pos - point)

    def reshow_start_widget(self):
        self.mdi_area.activeSubWindow().close()
        self.start_window.showMaximized()


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
