# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Result_Dlg.ui'
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
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(346, 286)
        Dialog.setMinimumSize(QSize(346, 286))
        Dialog.setMaximumSize(QSize(346, 286))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_8 = QGroupBox(Dialog)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(300, 10))
        self.groupBox_8.setMaximumSize(QSize(320, 16777215))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_8.setFont(font)
        self.gridLayout_28 = QGridLayout(self.groupBox_8)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.label_87 = QLabel(self.groupBox_8)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_87, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.groupBox_8)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(230, 42))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.frame_5.setFont(font1)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_68 = QGridLayout(self.frame_5)
        self.gridLayout_68.setObjectName(u"gridLayout_68")
        self.gridLayout_68.setContentsMargins(0, -1, 18, -1)
        self.lineEdit_result_7 = QLineEdit(self.frame_5)
        self.lineEdit_result_7.setObjectName(u"lineEdit_result_7")
        self.lineEdit_result_7.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_7.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_7.setFont(font1)
        self.lineEdit_result_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_7, 0, 7, 1, 1)

        self.lineEdit_result_5 = QLineEdit(self.frame_5)
        self.lineEdit_result_5.setObjectName(u"lineEdit_result_5")
        self.lineEdit_result_5.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_5.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_5.setFont(font1)
        self.lineEdit_result_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_5, 0, 5, 1, 1)

        self.lineEdit_result_3 = QLineEdit(self.frame_5)
        self.lineEdit_result_3.setObjectName(u"lineEdit_result_3")
        self.lineEdit_result_3.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_3.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_3.setFont(font1)
        self.lineEdit_result_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_3, 0, 3, 1, 1)

        self.lineEdit_result_1 = QLineEdit(self.frame_5)
        self.lineEdit_result_1.setObjectName(u"lineEdit_result_1")
        self.lineEdit_result_1.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_1.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_1.setFont(font1)
        self.lineEdit_result_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_1, 0, 1, 1, 1)

        self.lineEdit_result_8 = QLineEdit(self.frame_5)
        self.lineEdit_result_8.setObjectName(u"lineEdit_result_8")
        self.lineEdit_result_8.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_8.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_8.setFont(font1)
        self.lineEdit_result_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_8, 0, 8, 1, 1)

        self.lineEdit_result_6 = QLineEdit(self.frame_5)
        self.lineEdit_result_6.setObjectName(u"lineEdit_result_6")
        self.lineEdit_result_6.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_6.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_6.setFont(font1)
        self.lineEdit_result_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_6, 0, 6, 1, 1)

        self.lineEdit_result_9 = QLineEdit(self.frame_5)
        self.lineEdit_result_9.setObjectName(u"lineEdit_result_9")
        self.lineEdit_result_9.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_9.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_9.setFont(font1)
        self.lineEdit_result_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_9, 0, 9, 1, 1)

        self.lineEdit_result_2 = QLineEdit(self.frame_5)
        self.lineEdit_result_2.setObjectName(u"lineEdit_result_2")
        self.lineEdit_result_2.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_2.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_2.setFont(font1)
        self.lineEdit_result_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_2, 0, 2, 1, 1)

        self.lineEdit_result_4 = QLineEdit(self.frame_5)
        self.lineEdit_result_4.setObjectName(u"lineEdit_result_4")
        self.lineEdit_result_4.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_4.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_4.setFont(font1)
        self.lineEdit_result_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_4, 0, 4, 1, 1)

        self.lineEdit_result_0 = QLineEdit(self.frame_5)
        self.lineEdit_result_0.setObjectName(u"lineEdit_result_0")
        self.lineEdit_result_0.setMinimumSize(QSize(24, 10))
        self.lineEdit_result_0.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_0.setFont(font1)
        self.lineEdit_result_0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_68.addWidget(self.lineEdit_result_0, 0, 0, 1, 1)


        self.gridLayout_28.addWidget(self.frame_5, 3, 1, 1, 2)

        self.widget_camera_monitor = QWidget(self.groupBox_8)
        self.widget_camera_monitor.setObjectName(u"widget_camera_monitor")
        self.widget_camera_monitor.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_monitor, 1, 1, 1, 2)

        self.widget_camera_sony = QWidget(self.groupBox_8)
        self.widget_camera_sony.setObjectName(u"widget_camera_sony")
        self.widget_camera_sony.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_sony, 0, 1, 1, 2)

        self.label_89 = QLabel(self.groupBox_8)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_89, 2, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_16, 3, 0, 1, 1)

        self.pushButton_Send_Res = QPushButton(self.groupBox_8)
        self.pushButton_Send_Res.setObjectName(u"pushButton_Send_Res")
        self.pushButton_Send_Res.setMinimumSize(QSize(50, 30))
        self.pushButton_Send_Res.setStyleSheet(u"background:rgb(0,255,0)")

        self.gridLayout_28.addWidget(self.pushButton_Send_Res, 4, 0, 1, 3)

        self.widget_camera_fit = QWidget(self.groupBox_8)
        self.widget_camera_fit.setObjectName(u"widget_camera_fit")
        self.widget_camera_fit.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_fit, 2, 1, 1, 2)

        self.label_88 = QLabel(self.groupBox_8)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_88, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_8, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u7ed3\u679c\u786e\u8ba4", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"\u8bc6\u522b\u6570\u636e", None))
        self.label_87.setText(QCoreApplication.translate("Dialog", u"\u7d22\u5c3c:", None))
        self.lineEdit_result_7.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_5.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_3.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_1.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_8.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_6.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_9.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_2.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_4.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.lineEdit_result_0.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_89.setText(QCoreApplication.translate("Dialog", u"\u6838\u5bf9:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"\u53d1\u9001:", None))
        self.pushButton_Send_Res.setText(QCoreApplication.translate("Dialog", u"\u53d1\u9001\u7ed3\u679c", None))
        self.label_88.setText(QCoreApplication.translate("Dialog", u"\u76d1\u63a7:", None))
    # retranslateUi

