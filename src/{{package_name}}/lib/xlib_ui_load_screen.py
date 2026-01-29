"""load screen"""

import os
from PyQt5 import QtWidgets, QtCore, uic


class WindowLoadScreen(QtWidgets.QWidget):
    """window loadscreen class"""
    ui_path = f"{os.path.split(os.path.dirname(__file__))[0]}/res/window_load_screen.ui"

    def __init__(self):
        super(WindowLoadScreen, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        uic.loadUi(self.ui_path, self)
        self.show()
