# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Camera_Ui.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QLabel, QSizePolicy, QWidget)

class Ui_Camera_Dialog(object):
    def setupUi(self, Camera_Dialog):
        if not Camera_Dialog.objectName():
            Camera_Dialog.setObjectName(u"Camera_Dialog")
        Camera_Dialog.resize(605, 390)
        self.gridLayout = QGridLayout(Camera_Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_main_camera = QGroupBox(Camera_Dialog)
        self.groupBox_main_camera.setObjectName(u"groupBox_main_camera")
        self.groupBox_main_camera.setMinimumSize(QSize(0, 300))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_main_camera.setFont(font)
        self.groupBox_main_camera.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_15 = QGridLayout(self.groupBox_main_camera)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_picture = QLabel(self.groupBox_main_camera)
        self.label_picture.setObjectName(u"label_picture")
        self.label_picture.setMinimumSize(QSize(300, 10))

        self.gridLayout_15.addWidget(self.label_picture, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_main_camera, 0, 0, 1, 1)


        self.retranslateUi(Camera_Dialog)

        QMetaObject.connectSlotsByName(Camera_Dialog)
    # setupUi

    def retranslateUi(self, Camera_Dialog):
        Camera_Dialog.setWindowTitle(QCoreApplication.translate("Camera_Dialog", u"\u6444\u50cf\u673a\u8bc6\u522b\u7ed3\u679c", None))
        self.groupBox_main_camera.setTitle(QCoreApplication.translate("Camera_Dialog", u"\u6444\u50cf\u673a\u8bc6\u522b\u7ed3\u679c", None))
        self.label_picture.setText("")
    # retranslateUi

