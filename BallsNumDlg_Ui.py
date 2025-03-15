# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BallsNumDlg_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QGroupBox, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog_BallsNum(object):
    def setupUi(self, Dialog_BallsNum):
        if not Dialog_BallsNum.objectName():
            Dialog_BallsNum.setObjectName(u"Dialog_BallsNum")
        Dialog_BallsNum.resize(700, 630)
        Dialog_BallsNum.setMinimumSize(QSize(700, 630))
        Dialog_BallsNum.setMaximumSize(QSize(700, 630))
        self.gridLayout = QGridLayout(Dialog_BallsNum)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(Dialog_BallsNum)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(50, 0))
        font = QFont()
        font.setPointSize(20)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_2, 4, 7, 1, 1)

        self.checkBox_stop = QCheckBox(Dialog_BallsNum)
        self.checkBox_stop.setObjectName(u"checkBox_stop")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.checkBox_stop.setFont(font1)

        self.gridLayout.addWidget(self.checkBox_stop, 4, 8, 1, 1)

        self.label_4 = QLabel(Dialog_BallsNum)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"color: rgb(0, 200, 0);")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 9)

        self.label = QLabel(Dialog_BallsNum)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setPointSize(36)
        font3.setBold(False)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 9)

        self.groupBox_14 = QGroupBox(Dialog_BallsNum)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(450, 420))
        self.groupBox_14.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font4.setPointSize(10)
        font4.setBold(True)
        self.groupBox_14.setFont(font4)
        self.gridLayout_37 = QGridLayout(self.groupBox_14)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.gridLayout_37.setContentsMargins(0, -1, 0, -1)
        self.widget_map = QWidget(self.groupBox_14)
        self.widget_map.setObjectName(u"widget_map")
        self.widget_map.setMinimumSize(QSize(350, 350))

        self.gridLayout_37.addWidget(self.widget_map, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_14, 5, 0, 1, 9)

        self.label_3 = QLabel(Dialog_BallsNum)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(False)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_2 = QLabel(Dialog_BallsNum)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 30))
        self.label_2.setFont(font5)
        self.label_2.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 9)

        self.frame = QFrame(Dialog_BallsNum)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame, 4, 0, 1, 3)

        self.pushButton_close = QPushButton(Dialog_BallsNum)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setMinimumSize(QSize(150, 38))
        self.pushButton_close.setMaximumSize(QSize(200, 16777215))
        self.pushButton_close.setStyleSheet(u"background:rgb(0,240,0)")

        self.gridLayout.addWidget(self.pushButton_close, 4, 6, 1, 1)

        self.frame_3 = QFrame(Dialog_BallsNum)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_3, 4, 5, 1, 1)

        self.pushButton_continue = QPushButton(Dialog_BallsNum)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.pushButton_continue.setMinimumSize(QSize(150, 38))
        self.pushButton_continue.setMaximumSize(QSize(150, 16777215))
        self.pushButton_continue.setStyleSheet(u"background:rgb(240,0,0)")

        self.gridLayout.addWidget(self.pushButton_continue, 4, 4, 1, 1)


        self.retranslateUi(Dialog_BallsNum)

        QMetaObject.connectSlotsByName(Dialog_BallsNum)
    # setupUi

    def retranslateUi(self, Dialog_BallsNum):
        Dialog_BallsNum.setWindowTitle(QCoreApplication.translate("Dialog_BallsNum", u"\u8d77\u70b9\u786e\u8ba4", None))
        self.checkBox_stop.setText(QCoreApplication.translate("Dialog_BallsNum", u"STOP Alarm", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u8bf7\u9009\u62e9\u662f\u5426\u5c01\u76d8", None))
        self.label.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u8bf7\u786e\u8ba4\u8d77\u70b9\u67098\u9897\u7403", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("Dialog_BallsNum", u"\u536b\u661f\u56fe", None))
        self.label_3.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog_BallsNum", u"Please confirm that there are 8 balls at the starting point", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u5c01\u76d8(Closing)", None))
        self.pushButton_continue.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u7ee7\u7eed\u5f00\u8d5b(Continue)", None))
    # retranslateUi

