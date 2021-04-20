# -*- coding: utf-8 -*-

import sys

# from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QWidget, QPushButton, QLabel, QSlider, \
    QVBoxLayout, QHBoxLayout, QCheckBox


class ArithmeticWidget(QWidget):

    def __init__(self, counter: int, parent=None):
        super(ArithmeticWidget, self).__init__(parent)

        self.count = 0

        main_box = QVBoxLayout()

        h_box = QHBoxLayout()
        self.counter = QLabel(f'Examples 0/{counter}')
        self.counter.setAlignment(Qt.AlignLeft)
        h_box.addWidget(self.counter)

        self.timer = QLabel('Timer')
        self.timer.setAlignment(Qt.AlignRight)
        h_box.addWidget(self.timer)
        main_box.addLayout(h_box)

        self.setLayout(main_box)


class StartWidget(QWidget):
    start_signal = pyqtSignal()

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

        self.add_check = QCheckBox('+')
        self.add_check.setCheckState(Qt.Checked)
        self.sub_check = QCheckBox('-')
        self.sub_check.setCheckState(Qt.Checked)
        self.mul_check = QCheckBox('*')
        self.mul_check.setCheckState(Qt.Checked)
        self.floordiv_check = QCheckBox('//')
        self.floordiv_check.setCheckState(Qt.Checked)
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

    def start_arithmetic(self):
        self.start_signal.emit()

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
        start_widget.start_signal.connect(self.switching_widget)
        self.start_window = self.mdi_area.addSubWindow(start_widget)
        self.start_window.setWindowFlags(Qt.FramelessWindowHint)
        self.start_window.showMaximized()

        arithmetic_widget = ArithmeticWidget(2)
        self.arithmetic_widget = self.mdi_area.addSubWindow(arithmetic_widget)
        self.arithmetic_widget.setWindowFlags(Qt.FramelessWindowHint)
        self.arithmetic_widget.hide()

        self.setCentralWidget(self.mdi_area)

    def switching_widget(self):
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

    #
    # Листинг
    # 20.4
    # .2.ExpandingFieldsGrow.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("ExpandingFieldsGrow")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .3.FieldsStayAtSizeHint.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("FieldsStayAtSizeHint")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .4.QFormLayout.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("QFormLayout")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .5.WrapAllRows.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("WrapAllRows")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .6.WrapLongRows.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("WrapLongRows")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
    # form.addRow("&Название литературного или другого произведения:",
    #             lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .7.addRow.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("addRow")
    # window.resize(300, 150)
    #
    # label1 = QtWidgets.QLabel("&Название:")
    # label2 = QtWidgets.QLabel("&Описание:")
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    #
    # label1.setBuddy(lineEdit)
    # label2.setBuddy(textEdit)
    #
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.addRow(label1, lineEdit)
    # form.addRow(label2, textEdit)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .8.insertRow.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("insertRow")
    # window.resize(300, 150)
    #
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    #
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    #
    # form.insertRow(0, "&Описание:", textEdit)
    # form.insertRow(0, "&Название:", lineEdit)
    # form.insertRow(-1, hbox)
    #
    # window.setLayout(form)
    #
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .9.setFormAlignment.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtCore, QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("setFormAlignment")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setFormAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .10.setHorizontalSpacing.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("setHorizontalSpacing")
    # window.resize(350, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setHorizontalSpacing(30)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .11.setLabelAlignment.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtCore, QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("setLabelAlignment")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setLabelAlignment(QtCore.Qt.AlignRight)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.4
    # .12.setContentsMargins.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("setContentsMargins")
    # window.resize(300, 150)
    # lineEdit = QtWidgets.QLineEdit()
    # textEdit = QtWidgets.QTextEdit()
    # spinBox = QtWidgets.QSpinBox()
    # button1 = QtWidgets.QPushButton("О&тправить")
    # button2 = QtWidgets.QPushButton("О&чистить")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(button1)
    # hbox.addWidget(button2)
    # form = QtWidgets.QFormLayout()
    # form.setContentsMargins(0, 0, 0, 0)
    # form.addRow("&Название:", lineEdit)
    # form.addRow("&Описание:", textEdit)
    # form.addRow("&Количество:", spinBox)
    # form.addRow(hbox)
    # window.setLayout(form)
    # window.show()
    # sys.exit(app.exec_())
    # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QGroupBox")
    # window.resize(300, 80)
    # radio1 = QtWidgets.QRadioButton("&Да")
    # radio2 = QtWidgets.QRadioButton("&Нет")
    # mainbox = QtWidgets.QVBoxLayout()
    # box = QtWidgets.QGroupBox("&Вы знаете язык Python?")
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(radio1)
    # hbox.addWidget(radio2)
    # box.setLayout(hbox)
    # mainbox.addWidget(box)
    # window.setLayout(mainbox)
    # radio1.setChecked(True)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.7
    # .2.setAlignment.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtCore, QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QGroupBox")
    # window.resize(300, 80)
    # radio1 = QtWidgets.QRadioButton("&Да")
    # radio2 = QtWidgets.QRadioButton("&Нет")
    # mainbox = QtWidgets.QVBoxLayout()
    # box = QtWidgets.QGroupBox()
    # box.setTitle("&Вы знаете язык Python?")
    # # box.setAlignment(QtCore.Qt.AlignRight)
    # # box.setAlignment(QtCore.Qt.AlignLeft)
    # box.setAlignment(QtCore.Qt.AlignHCenter)
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(radio1)
    # hbox.addWidget(radio2)
    # box.setLayout(hbox)
    # mainbox.addWidget(box)
    # window.setLayout(mainbox)
    # radio1.setChecked(True)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.7
    # .3.setCheckable.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QGroupBox")
    # window.resize(300, 80)
    # radio1 = QtWidgets.QRadioButton("&Да")
    # radio2 = QtWidgets.QRadioButton("&Нет")
    # mainbox = QtWidgets.QVBoxLayout()
    # box = QtWidgets.QGroupBox()
    # box.setTitle("&Вы знаете язык Python?")
    # box.setCheckable(True)
    # box.setChecked(False)
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(radio1)
    # hbox.addWidget(radio2)
    # box.setLayout(hbox)
    # mainbox.addWidget(box)
    # window.setLayout(mainbox)
    # radio1.setChecked(True)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.7
    # .4.setFlat.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtCore, QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QGroupBox")
    # window.resize(300, 80)
    # radio1 = QtWidgets.QRadioButton("&Да")
    # radio2 = QtWidgets.QRadioButton("&Нет")
    # mainbox = QtWidgets.QVBoxLayout()
    # box = QtWidgets.QGroupBox()
    # box.setTitle("&Вы знаете язык Python?")
    # box.setAlignment(QtCore.Qt.AlignHCenter)
    # box.setFlat(True)
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(radio1)
    # hbox.addWidget(radio2)
    # box.setLayout(hbox)
    # mainbox.addWidget(box)
    # window.setLayout(mainbox)
    # radio1.setChecked(True)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.7
    # .5.toggled.py
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    #
    # def on_clicked_button():
    #     box.setChecked(False if box.isChecked() else True)
    #
    #
    # def on_clicked(flag):
    #     print("on_clicked", flag)
    #
    #
    # def on_toggled(flag):
    #     print("on_toggled", flag)
    #
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QGroupBox")
    # window.resize(300, 80)
    # radio1 = QtWidgets.QRadioButton("&Да")
    # radio2 = QtWidgets.QRadioButton("&Нет")
    # button = QtWidgets.QPushButton("&Переключить флажок")
    # mainbox = QtWidgets.QVBoxLayout()
    # box = QtWidgets.QGroupBox()
    # box.setTitle("&Вы знаете язык Python?")
    # box.setCheckable(True)
    # hbox = QtWidgets.QHBoxLayout()
    # hbox.addWidget(radio1)
    # hbox.addWidget(radio2)
    # box.setLayout(hbox)
    # mainbox.addWidget(box)
    # mainbox.addWidget(button)
    # window.setLayout(mainbox)
    # radio1.setChecked(True)
    # box.clicked["bool"].connect(on_clicked)
    # box.toggled["bool"].connect(on_toggled)
    # button.clicked.connect(on_clicked_button)
    # window.show()
    # sys.exit(app.exec_())
    # 20.8.Панель
    # с
    # рамкой
    # Листинг
    # 20.8
    # .1.Box.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. Box")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .2.HLine.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. HLine")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .3.Panel.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. Panel")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .4.StyledPanel.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. StyledPanel")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.StyledPanel |
    #                      QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.StyledPanel |
    #                      QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.StyledPanel |
    #                      QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .5.VLine.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. VLine")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .6.WinPanel.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. WinPanel")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.WinPanel | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.WinPanel | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.WinPanel | QtWidgets.QFrame.Sunken)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .7.setLineWidth.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. setLineWidth")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
    # frame1.setLineWidth(5)
    # frame2.setLineWidth(5)
    # frame3.setLineWidth(5)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
    #
    # Листинг
    # 20.8
    # .8.setMidLineWidth.pyw
    # # -*- coding: utf-8 -*-
    # from PyQt5 import QtWidgets
    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QWidget()
    # window.setWindowTitle("Класс QFrame. setMidLineWidth")
    # window.resize(300, 250)
    # frame1 = QtWidgets.QFrame()
    # frame2 = QtWidgets.QFrame()
    # frame3 = QtWidgets.QFrame()
    # frame1.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
    # frame2.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
    # frame3.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken)
    # frame1.setLineWidth(5)
    # frame2.setLineWidth(5)
    # frame3.setLineWidth(5)
    # frame1.setMidLineWidth(10)
    # frame2.setMidLineWidth(10)
    # frame3.setMidLineWidth(10)
    # vbox = QtWidgets.QVBoxLayout()
    # vbox.addWidget(frame1)
    # vbox.addWidget(frame2)
    # vbox.addWidget(frame3)
    # window.setLayout(vbox)
    # window.show()
    # sys.exit(app.exec_())
