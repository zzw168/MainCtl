# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UdpData_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_Dialog_UdpData(object):
    def setupUi(self, Dialog_UdpData):
        if not Dialog_UdpData.objectName():
            Dialog_UdpData.setObjectName(u"Dialog_UdpData")
        Dialog_UdpData.resize(660, 441)
        Dialog_UdpData.setMinimumSize(QSize(370, 400))
        Dialog_UdpData.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(Dialog_UdpData)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_14 = QGroupBox(Dialog_UdpData)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(350, 380))
        self.groupBox_14.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_14.setFont(font)
        self.gridLayout_37 = QGridLayout(self.groupBox_14)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.gridLayout_37.setContentsMargins(0, -1, 0, -1)
        self.textBrowser = QTextBrowser(self.groupBox_14)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_37.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_14, 0, 0, 1, 1)


        self.retranslateUi(Dialog_UdpData)

        QMetaObject.connectSlotsByName(Dialog_UdpData)
    # setupUi

    def retranslateUi(self, Dialog_UdpData):
        Dialog_UdpData.setWindowTitle(QCoreApplication.translate("Dialog_UdpData", u"\u8bc6\u522b\u6570\u636e", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("Dialog_UdpData", u"\u8bc6\u522b\u6570\u636e", None))
    # retranslateUi

