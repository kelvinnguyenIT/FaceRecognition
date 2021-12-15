from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import camera_regconition
from datetime import datetime
import pymysql


class GUI_R(QWidget):

    def __init__(self):
        super().__init__()
        self.height = 450
        self.width = 800
        self.initUI()
        self.setObjectName("body")
        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          passwd="",
                                          database="face_recognition")
        self.thread = ''
        self.setWindowTitle('Recognition')
        self.setGeometry(0, 0, self.width, self.height)
        styleSheet ="""
                     #body{
                            background-color:white;
                            
                        }
                    #btn{
                            color:white;
                            background-color:#3498DB;
                            border-radius:10px;
                            font-size:15px;
                            height:50%;
                            width:50%;
                        }
        """
        self.setStyleSheet(styleSheet)

    def closeEvent(self, a0: QCloseEvent) -> None:
        if(self.thread!=''):
            self.thread.stop()
        print("close")

    def initUI(self):
        # V doc H ngang
        hboxtop = QHBoxLayout()

        vboxLeft = QVBoxLayout()

        self.lblCamera = QLabel()
        self.lblCamera.setFixedSize(600, 450)
        self.lblCamera.setStyleSheet("border:1px solid #3498DB;border-radius:5px;")
        self.lblCamera.setAlignment(Qt.AlignCenter)

        self.btnStart = QPushButton("Start Regconition")
        self.btnStart.setObjectName("btn")
        self.btnStart.clicked.connect(self.StartReg)

        self.listW = QListWidget()

        vboxLeft.addWidget(self.btnStart,1)
        vboxLeft.addWidget(self.listW,10)

        hboxtop.addWidget(self.lblCamera,7)
        hboxtop.addLayout(vboxLeft,3)
        self.setLayout(hboxtop)
    def StartReg(self):

        self.thread = camera_regconition.VideoThread()
        self.btnStart.setText("Loading model...")
        self.thread.set_value(self.lblCamera.width(), self.lblCamera.height())
        self.thread.start()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.change_list_signal.connect(self.regconition)

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.lblCamera.setPixmap(QPixmap.fromImage(cv_img))
    def regconition(self,iduser):
        print("name: ",iduser)
        datenow = datetime.now()
        date = datenow.date()
        p = datenow.strftime("%p")
        idrecog = str(date) + p + iduser
        InsertSQL = "INSERT INTO recognition(idrecog,iduser,date,sess) VALUES ('" + idrecog + "','" + iduser + "','" + str(datenow) + "','" + p + "')"
        checkSQL = "SELECT * FROM recognition WHERE idrecog = '"+idrecog+"';"
        try:
            cursor = self.connection.cursor()

            cursor.execute(checkSQL)
            rowcheck = cursor.fetchall()
            if(rowcheck==()):
                cursor.execute(InsertSQL)
                self.listW.addItem(iduser+" Vừa điểm danh")
            self.connection.commit()
        except:
            print("đã điểm danh")


        cursor.close()
