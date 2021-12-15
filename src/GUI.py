from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore
import sys
import GUI_Check, GUI_Train, GUI_Recognition

class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.height = 550
        self.width = 700

        self.setObjectName("body")
        self.setGeometry(0, 0, self.width, self.height)
        styleSheet="""
            #body{
                background-color:white;
            }
            #btn{
                background-color: white;
                border: 2px solid #3498DB;
                color:blue;
                height:40px;
                width:50px;
                border-radius: 10px;
            }
            """
        self.setStyleSheet(styleSheet)
        self.initUI()
        self.setWindowTitle('QCheckBox')
        self.show()
    def initUI(self):
        #V doc H ngang
        vboxtop = QVBoxLayout()
        hbox_option = QHBoxLayout()
        
        btn_reg = QPushButton()
        btn_reg.setIcon(QtGui.QIcon('icon/face-regc.png'))

        btn_reg.setIconSize(QtCore.QSize(36, 36))
        btn_reg.setObjectName("btn")
        btn_reg.clicked.connect(self.eventBtnReg)

        btn_train = QPushButton()
        btn_train.setIcon(QtGui.QIcon("icon/train-face.png"))
        btn_train.setIconSize(QtCore.QSize(36,36))
        btn_train.setObjectName("btn")
        btn_train.clicked.connect(self.eventBtnTrain)

        btn_check = QPushButton()
        btn_check.setIcon(QtGui.QIcon('icon/icon-check.png'))
        btn_check.setIconSize(QtCore.QSize(36, 36))
        btn_check.setObjectName("btn")
        btn_check.clicked.connect(self.eventBtnCheck)


        hbox_option.addWidget(btn_reg,1)
        hbox_option.addWidget(btn_train,1)
        hbox_option.addWidget(btn_check, 1)
        vboxtop.addLayout(hbox_option)
        self.setLayout(vboxtop)
    def eventBtnCheck(self):
        pass
    def eventBtnReg(self):
        self.uiReg = GUI_Recognition.GUI_R()
        self.uiReg.show()
    def eventBtnTrain(self):

        self.uiTrain = GUI_Train.GUI_T()
        self.uiTrain.show()


def main():
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()