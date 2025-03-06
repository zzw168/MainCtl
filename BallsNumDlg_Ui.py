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
        Dialog_BallsNum.resize(500, 230)
        Dialog_BallsNum.setMinimumSize(QSize(500, 230))
        Dialog_BallsNum.setMaximumSize(QSize(500, 230))
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

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 3)

        self.label = QLabel(Dialog_BallsNum)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(36)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)

        self.frame = QFrame(Dialog_BallsNum)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame, 4, 0, 1, 1)

        self.label_3 = QLabel(Dialog_BallsNum)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 3)

        self.frame_2 = QFrame(Dialog_BallsNum)
        self.frame_2.setObjectName(u"frame_2")
        font2 = QFont()
        font2.setPointSize(20)
        self.frame_2.setFont(font2)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_2, 4, 2, 1, 1)

        self.pushButton_ok = QPushButton(Dialog_BallsNum)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(0, 38))
        self.pushButton_ok.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.pushButton_ok, 4, 1, 1, 1)

        self.label_4 = QLabel(Dialog_BallsNum)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 30))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"color: rgb(0, 200, 0);")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 3)


        self.retranslateUi(Dialog_BallsNum)

        QMetaObject.connectSlotsByName(Dialog_BallsNum)
    # setupUi

    def retranslateUi(self, Dialog_BallsNum):
        Dialog_BallsNum.setWindowTitle(QCoreApplication.translate("Dialog_BallsNum", u"\u7ed3\u679c\u786e\u8ba4", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_BallsNum", u"Please confirm that there are 8 balls at the starting point", None))
        self.label.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u8bf7\u786e\u8ba4\u8d77\u70b9\u67098\u9897\u7403", None))
        self.label_3.setText("")
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u786e\u8ba4(confirm)", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_BallsNum", u"\u81ea\u52a8\u5c01\u76d8\uff0c\u5f00\u8d5b\u8bf7\u91cd\u65b0\u5f00\u76d8", None))
    # retranslateUi

