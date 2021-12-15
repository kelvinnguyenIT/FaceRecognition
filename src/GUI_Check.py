from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,QtCore
import sys



class GUI_C(QWidget):

    def __init__(self):
        super().__init__()
        self.height = 500
        self.width = 700
        self.initUI()
        self.setStyleSheet("background-color:white")
        self.setWindowTitle('al')
        self.setGeometry(0, 0, self.width, self.height)


    def initUI(self):
        # V doc H ngang
        vboxtop = QVBoxLayout()
        hbox_option = QHBoxLayout()

        self.btn_reg = QPushButton()
        self.btn_reg.setIcon(QtGui.QIcon('icon/face-regc.png'))

        self.btn_reg.setIconSize(QtCore.QSize(36, 36))
        self.btn_reg.setStyleSheet("background-color: white;"
                                   "border: 2px solid #3498DB;"
                                   "color:blue;"
                                   "height:40px;width:50px;"
                                   "border-radius: 10px;")

        self.btn_train = QPushButton()
        self.btn_train.setIcon(QtGui.QIcon("icon/train-face.png"))
        self.btn_train.setIconSize(QtCore.QSize(36, 36))
        self.btn_train.setStyleSheet("background-color: white;"
                                     "border: 2px solid #3498DB;"
                                     "color:blue;"
                                     "height:40px;width:50px;"
                                     "border-radius: 10px;")

        self.btn_check = QPushButton()
        self.btn_check.setIcon(QtGui.QIcon('icon/icon-check.png'))
        self.btn_check.setIconSize(QtCore.QSize(36, 36))
        self.btn_check.setStyleSheet("background-color: white;"
                                     "border: 2px solid #3498DB;"
                                     "color:blue;"
                                     "height:40px;width:50px;"
                                     "border-radius: 10px;")
        self.btn_reg.installEventFilter(self)
        hbox_option.addWidget(self.btn_reg, 1)

        hbox_option.addWidget(self.btn_check, 1)
        vboxtop.addLayout(hbox_option)
        self.setLayout(vboxtop)