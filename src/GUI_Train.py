from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui,QtCore
import os,re,pymysql
import get_dataset
import cv2 as cv
import camera_train




class GUI_T(QWidget):
    def __init__(self, parent=None):


        # V doc. H ngang
        QWidget.__init__(self, parent=parent)
        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          passwd="",
                                          database="face_recognition")

        self.height = 500
        self.width = 800
        self.setWindowTitle('Train Data')
        self.setGeometry(0, 0, self.width, self.height)
        self.setObjectName("body")
        styleSheet = """
                        #body{
                            background-color:white;
                            
                        }
                        #lbltitle{
                            color:#3498DB;
                            font-size:30px;
                            font-family: 'Source Sans Pro', sans-serif;
                        }
                        #lblInput{
                            color:#3498DB;
                            font-size:12px;
                        }
                        #edtInput{
                            color:#3498DB;
                            border: 1px solid #3498DB;
                            height:30px;
                            border-radius:10px;

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
        self.initUI()
        self.id = self.edtid.text()
        self.clss = self.edtclass.text()
        self.name = self.edtname.text()
        self.birthday = self.edtbirthday.text()
        self.check_dataset = False
    def initUI(self):
        # V doc H ngang


        lbltitle = QLabel("TẠO ĐỐI TƯỢNG MỚI")
        lbltitle.setObjectName("lbltitle")
        # MaSV
        lblid = QLabel("Nhập mã sinh viên")
        lblid.setObjectName("lblInput")

        self.edtid = QLineEdit()
        self.edtid.setObjectName("edtInput")
        # Lop
        lblclass = QLabel("Nhập lớp")
        lblclass.setObjectName("lblInput")

        self.edtclass = QLineEdit()
        self.edtclass.setObjectName("edtInput")
        # Ten
        lblname = QLabel("Nhập tên")
        lblname.setObjectName("lblInput")

        self.edtname = QLineEdit()
        self.edtname.setObjectName("edtInput")
        # Ngay Sinh
        lblbirthday = QLabel("Nhập ngày sinh")
        lblbirthday.setObjectName("lblInput")

        self.edtbirthday = QDateEdit()
        self.edtbirthday.setObjectName("edtInput")
        # BTN submit
        btnGetDataset = QPushButton("Get Dataset")
        btnGetDataset.setObjectName("btn")
        btnGetDataset.clicked.connect(self.get_dataset)


        # Camera
        self.lblCam = QLabel()
        self.lblCam.setFixedSize(400, 300)
        self.lblCam.setStyleSheet("border:1px solid #3498DB;border-radius:5px;")

        self.lblCam.setAlignment(Qt.AlignCenter)


        btnNext = QPushButton("Train")
        btnNext.setObjectName('btn')
        btnNext.clicked.connect(self.eventBtnNext)

        hbox_top = QHBoxLayout()
        vboxleft = QVBoxLayout()
        vboxright = QVBoxLayout()
        vboxall = QVBoxLayout()
        hbox_option = QHBoxLayout()
        Hbox_btn = QHBoxLayout()

        vboxleft.addWidget(lblid, 1)
        vboxleft.addWidget(self.edtid, 2)
        vboxleft.addWidget(lblclass, 1)
        vboxleft.addWidget(self.edtclass, 2)
        vboxleft.addWidget(lblname, 1)
        vboxleft.addWidget(self.edtname, 2)
        vboxleft.addWidget(lblbirthday, 1)
        vboxleft.addWidget(self.edtbirthday, 2)
        vboxleft.addStretch(1)


        vboxright.addWidget(self.lblCam,10)
        vboxright.addWidget(btnGetDataset,1)

        Hbox_btn.addStretch(9)
        Hbox_btn.addWidget(btnNext, 3)


        hbox_top.addLayout(vboxleft,1)
        hbox_top.addLayout(vboxright, 1)

        hbox_option.addWidget(btnNext,1)
        hbox_option.addStretch(5)

        vboxall.addWidget(lbltitle, 1)
        vboxall.addLayout(hbox_top,8)
        vboxall.addLayout(hbox_option,1)
        self.setLayout(vboxall)

    def no_accent_vietnamese(self,s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s.replace(" ","")
    def get_dataset(self):
        if (self.edtid.text().strip() == '' or self.edtclass.text().strip() == '' or self.edtname.text().strip() == '' or self.edtbirthday.text().strip() == ''):
            QMessageBox.about(self, "Error", "Vui lòng nhập đầy đủ thông tin")
        else:
            QMessageBox.about(self,"Loading", "Vui lòng quay đủ góc mặt")
            name = self.no_accent_vietnamese(self.edtname.text().strip().replace(" ","")+self.edtid.text().strip())
            try:
                self.thread = camera_train.VideoThread()
                # connect its signal to the update_image slot
                self.thread.set_value(name,self.lblCam.width(), self.lblCam.height())
                self.thread.change_pixmap_signal.connect(self.update_image)

                # start the thread
                self.thread.start()
                self.check_dataset = True

            except:
                QMessageBox.about(self, "Error", "Lấy dữ liệu khuôn mặt thất bại")
    def eventBtnNext(self):
        id = self.edtid.text().strip()
        clss = self.edtclass.text().strip()
        name = self.edtname.text().strip()
        getbday = self.edtbirthday.text().strip().replace("/"," ").split()
        day = getbday[1]
        month = getbday[0]
        year = getbday[2]
        if(day.__len__()==1):
            day = "0"+day
        if (month.__len__() == 1):
            month = "0" + month
        bday = year+"-"+month+"-"+day

        id_insert = self.no_accent_vietnamese(name)+id
        if (id != '' and clss != '' and name != '' and bday != '' and self.check_dataset==True):
            if(os.system(
                'python classifier.py TRAIN ../Dataset/ ../Models/20180402-114759.pb ../Models/facemodel.pkl --batch_size 1000')==0):
                    insert = "INSERT INTO `user_infor`(`id`, `name`, `class`, `bday`) VALUES ('" + id_insert + "', '" + name + "', '" + clss + "', '" + bday + "');"
                    print(insert)
                    cursor = self.connection.cursor()
                    cursor.execute(insert)

                    self.connection.commit()
                    cursor.close()
                    print("ok")
            else:
                QMessageBox.about(self, "Error", "Train thất bại")
        else:
            QMessageBox.about(self, "Error", "Vui lòng lấy đầy đủ thông tin")


    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.lblCam.setPixmap(QPixmap.fromImage(cv_img))





