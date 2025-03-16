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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog_BallsNum(object):
    def setupUi(self, Dialog_BallsNum):
        if not Dialog_BallsNum.objectName():
            Dialog_BallsNum.setObjectName(u"Dialog_BallsNum")
        Dialog_BallsNum.resize(526, 238)
        Dialog_BallsNum.setMinimumSize(QSize(500, 0))
        Dialog_BallsNum.setMaximumSize(QSize(526, 630))
        self.gridLayout = QGridLayout(Dialog_BallsNum)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Dialog_BallsNum)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 7)

        self.label_3 = QLabel(Dialog_BallsNum)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.pushButton_continue = QPushButton(Dialog_BallsNum)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.pushButton_continue.setMinimumSize(QSize(150, 38))
        self.pushButton_continue.setMaximumSize(QSize(150, 16777215))
        self.pushButton_continue.setStyleSheet(u"background:rgb(240,0,0)")

        self.gridLayout.addWidget(self.pushButton_continue, 4, 2, 1, 1)

        self.frame = QFrame(Dialog_BallsNum)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame, 4, 0, 1, 2)

        self.label = QLabel(Dialog_BallsNum)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(36)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 7)

        self.label_4 = QLabel(Dialog_BallsNum)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"color: rgb(0, 200, 0);")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 7)

        self.frame_3 = QFrame(Dialog_BallsNum)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_3, 4, 3, 1, 1)

        self.pushButton_close = QPushButton(Dialog_BallsNum)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setMinimumSize(QSize(150, 38))
        self.pushButton_close.setMaximumSize(QSize(200, 16777215))
        self.pushButton_close.setStyleSheet(u"background:rgb(0,240,0)")

        self.gridLayout.addWidget(self.pushButton_close, 4, 4, 1, 1)

        self.frame_2 = QFrame(Dialog_BallsNum)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(50, 0))
        font3 = QFont()
        font3.setPointSize(20)
        self.frame_2.setFont(font3)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_2, 4, 5, 1, 2)


        self.retranslateUi(Dialog_BallsNum)

        QMetaObject.connectSlotsByName(Dialog_BallsNum)
    # setupUi

    def retranslateUi(self, Dialog_BallsNum):
        Dialog_BallsNum.setWindowTitle(QCoreApplication.translate("Dialog_BallsNum", u"\u8d77\u70b9\u786e\u8ba4", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_BallsNum", u"Please confirm that there are 8 balls at the starting point", None))
        self.label_3.setText("")
        self.pushButton_continue.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u7ee7\u7eed\u5f00\u8d5b(Continue)", None))
        self.label.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u8bf7\u786e\u8ba4\u8d77\u70b9\u67098\u9897\u7403", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u8bf7\u9009\u62e9\u662f\u5426\u5c01\u76d8", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u5c01\u76d8(Closing)", None))
    # retranslateUi

