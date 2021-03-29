# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint


class StartWidget(QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # buttons
        self.start_btn = QPushButton('Start')
        self.menu_btn = QPushButton('Menu')
        self.exit_btn = QPushButton('Exit')

        v_box = QVBoxLayout()
        v_box.addWidget(self.start_btn)
        v_box.addWidget(self.menu_btn)
        v_box.addWidget(self.exit_btn)

        self.setLayout(v_box)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mdi_area = QMdiArea()
        start_widget = StartWidget()
        self.start_window = self.mdi_area.addSubWindow(start_widget)
        self.start_window.setWindowFlags(Qt.FramelessWindowHint)
        self.start_window.showMaximized()

        self.setCentralWidget(self.mdi_area)

    def move_to_center(self):
        """Move window to center desktop"""
        point = QPoint(self.width() // 2, self.height() // 2 + 100)
        pos = QApplication.desktop().availableGeometry().center()
        self.move(pos - point)


class ArithmeticApplication(QApplication):
    """The Application object"""

    def __init__(self, argv):
        super(ArithmeticApplication, self).__init__(argv)

        # create main window
        self.main_window = MainWindow()
        self.main_window.resize(400, 400)
        self.main_window.move_to_center()
        self.main_window.show()


if __name__ == '__main__':
    arithmetic_app = ArithmeticApplication(sys.argv)
    sys.exit(arithmetic_app.exec())
