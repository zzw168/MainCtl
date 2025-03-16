# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrapBallDlg_Ui.ui'
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

class Ui_Dialog_TrapBall(object):
    def setupUi(self, Dialog_TrapBall):
        if not Dialog_TrapBall.objectName():
            Dialog_TrapBall.setObjectName(u"Dialog_TrapBall")
        Dialog_TrapBall.resize(518, 248)
        Dialog_TrapBall.setMinimumSize(QSize(0, 0))
        Dialog_TrapBall.setMaximumSize(QSize(864, 600))
        Dialog_TrapBall.setSizeGripEnabled(True)
        self.gridLayout = QGridLayout(Dialog_TrapBall)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_trap = QGroupBox(Dialog_TrapBall)
        self.groupBox_trap.setObjectName(u"groupBox_trap")
        self.groupBox_trap.setMinimumSize(QSize(500, 200))
        self.groupBox_trap.setMaximumSize(QSize(500, 200))
        self.gridLayout_4 = QGridLayout(self.groupBox_trap)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame = QFrame(self.groupBox_trap)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_state = QLabel(self.frame)
        self.label_state.setObjectName(u"label_state")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_state.setFont(font)
        self.label_state.setStyleSheet(u"color: rgb(255, 0, 0)")

        self.gridLayout_3.addWidget(self.label_state, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 1, 0, 1, 1)

        self.pushButton_cancel = QPushButton(self.groupBox_trap)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(150, 38))
        self.pushButton_cancel.setMaximumSize(QSize(150, 16777215))
        self.pushButton_cancel.setStyleSheet(u"background:rgb(230,0,0)")

        self.gridLayout_4.addWidget(self.pushButton_cancel, 1, 1, 1, 1)

        self.groupBox_7 = QGroupBox(self.groupBox_trap)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(350, 0))
        self.groupBox_7.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox_7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_TRAP = QPushButton(self.groupBox_7)
        self.pushButton_TRAP.setObjectName(u"pushButton_TRAP")
        self.pushButton_TRAP.setMinimumSize(QSize(0, 32))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.pushButton_TRAP.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButton_TRAP, 0, 0, 1, 1)

        self.pushButton_TRAP_7 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_7.setObjectName(u"pushButton_TRAP_7")
        self.pushButton_TRAP_7.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_7.setMaximumSize(QSize(32, 32))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton_TRAP_7.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_7, 0, 7, 1, 1)

        self.pushButton_TRAP_8 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_8.setObjectName(u"pushButton_TRAP_8")
        self.pushButton_TRAP_8.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_8.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_8.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_8, 0, 8, 1, 1)

        self.pushButton_TRAP_6 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_6.setObjectName(u"pushButton_TRAP_6")
        self.pushButton_TRAP_6.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_6.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_6.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_6, 0, 6, 1, 1)

        self.pushButton_OUT_2 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_2.setObjectName(u"pushButton_OUT_2")
        self.pushButton_OUT_2.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_2.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_2, 1, 2, 1, 1)

        self.pushButton_OUT_6 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_6.setObjectName(u"pushButton_OUT_6")
        self.pushButton_OUT_6.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_6.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_6.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_6, 1, 6, 1, 1)

        self.pushButton_OUT_4 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_4.setObjectName(u"pushButton_OUT_4")
        self.pushButton_OUT_4.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_4.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_4.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_4, 1, 4, 1, 1)

        self.pushButton_OUT_10 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_10.setObjectName(u"pushButton_OUT_10")
        self.pushButton_OUT_10.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_10.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_10.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_10, 1, 10, 1, 1)

        self.pushButton_TRAP_4 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_4.setObjectName(u"pushButton_TRAP_4")
        self.pushButton_TRAP_4.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_4.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_4.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_4, 0, 4, 1, 1)

        self.pushButton_TRAP_5 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_5.setObjectName(u"pushButton_TRAP_5")
        self.pushButton_TRAP_5.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_5.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_5.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_5, 0, 5, 1, 1)

        self.pushButton_TRAP_3 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_3.setObjectName(u"pushButton_TRAP_3")
        self.pushButton_TRAP_3.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_3.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_3.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_3, 0, 3, 1, 1)

        self.pushButton_OUT_5 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_5.setObjectName(u"pushButton_OUT_5")
        self.pushButton_OUT_5.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_5.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_5.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_5, 1, 5, 1, 1)

        self.pushButton_OUT_3 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_3.setObjectName(u"pushButton_OUT_3")
        self.pushButton_OUT_3.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_3.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_3.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_3, 1, 3, 1, 1)

        self.pushButton_OUT_8 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_8.setObjectName(u"pushButton_OUT_8")
        self.pushButton_OUT_8.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_8.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_8.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_8, 1, 8, 1, 1)

        self.pushButton_OUT_1 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_1.setObjectName(u"pushButton_OUT_1")
        self.pushButton_OUT_1.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_1.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_1.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_1, 1, 1, 1, 1)

        self.pushButton_TRAP_9 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_9.setObjectName(u"pushButton_TRAP_9")
        self.pushButton_TRAP_9.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_9.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_9.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_9, 0, 9, 1, 1)

        self.pushButton_TRAP_10 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_10.setObjectName(u"pushButton_TRAP_10")
        self.pushButton_TRAP_10.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_10.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_10.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_10, 0, 10, 1, 1)

        self.pushButton_OUT = QPushButton(self.groupBox_7)
        self.pushButton_OUT.setObjectName(u"pushButton_OUT")
        self.pushButton_OUT.setMinimumSize(QSize(0, 32))
        self.pushButton_OUT.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButton_OUT, 1, 0, 1, 1)

        self.pushButton_TRAP_1 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_1.setObjectName(u"pushButton_TRAP_1")
        self.pushButton_TRAP_1.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_1.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_1.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_1, 0, 1, 1, 1)

        self.pushButton_OUT_9 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_9.setObjectName(u"pushButton_OUT_9")
        self.pushButton_OUT_9.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_9.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_9.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_9, 1, 9, 1, 1)

        self.pushButton_OUT_7 = QPushButton(self.groupBox_7)
        self.pushButton_OUT_7.setObjectName(u"pushButton_OUT_7")
        self.pushButton_OUT_7.setMinimumSize(QSize(32, 32))
        self.pushButton_OUT_7.setMaximumSize(QSize(32, 32))
        self.pushButton_OUT_7.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_OUT_7, 1, 7, 1, 1)

        self.pushButton_TRAP_2 = QPushButton(self.groupBox_7)
        self.pushButton_TRAP_2.setObjectName(u"pushButton_TRAP_2")
        self.pushButton_TRAP_2.setMinimumSize(QSize(32, 32))
        self.pushButton_TRAP_2.setMaximumSize(QSize(32, 32))
        self.pushButton_TRAP_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_TRAP_2, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_7, 0, 0, 1, 4)

        self.frame_2 = QFrame(self.groupBox_trap)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(10, 0))
        self.frame_2.setMaximumSize(QSize(10, 16777215))
        font3 = QFont()
        font3.setPointSize(20)
        self.frame_2.setFont(font3)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_2, 1, 2, 1, 1)

        self.pushButton_ok = QPushButton(self.groupBox_trap)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(150, 38))
        self.pushButton_ok.setMaximumSize(QSize(150, 16777215))
        self.pushButton_ok.setStyleSheet(u"background:rgb(0,245,0)")

        self.gridLayout_4.addWidget(self.pushButton_ok, 1, 3, 1, 1)


        self.gridLayout.addWidget(self.groupBox_trap, 1, 0, 1, 1)

        self.checkBox_stop = QCheckBox(Dialog_TrapBall)
        self.checkBox_stop.setObjectName(u"checkBox_stop")
        self.checkBox_stop.setFont(font)

        self.gridLayout.addWidget(self.checkBox_stop, 0, 0, 1, 1)


        self.retranslateUi(Dialog_TrapBall)

        QMetaObject.connectSlotsByName(Dialog_TrapBall)
    # setupUi

    def retranslateUi(self, Dialog_TrapBall):
        Dialog_TrapBall.setWindowTitle(QCoreApplication.translate("Dialog_TrapBall", u"\u7ed3\u679c\u786e\u8ba4", None))
        self.label_state.setText(QCoreApplication.translate("Dialog_TrapBall", u"\u8bf7\u786e\u8ba4\u5361\u73e0\u60c5\u51b5", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog_TrapBall", u"\u53d6\u6d88(Cancel)", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog_TrapBall", u"\u9009\u62e9\u4f4d\u7f6e", None))
        self.pushButton_TRAP.setText(QCoreApplication.translate("Dialog_TrapBall", u"\u5361\u73e0(TRAP)", None))
        self.pushButton_TRAP_7.setText(QCoreApplication.translate("Dialog_TrapBall", u"7", None))
        self.pushButton_TRAP_8.setText(QCoreApplication.translate("Dialog_TrapBall", u"8", None))
        self.pushButton_TRAP_6.setText(QCoreApplication.translate("Dialog_TrapBall", u"6", None))
        self.pushButton_OUT_2.setText(QCoreApplication.translate("Dialog_TrapBall", u"2", None))
        self.pushButton_OUT_6.setText(QCoreApplication.translate("Dialog_TrapBall", u"6", None))
        self.pushButton_OUT_4.setText(QCoreApplication.translate("Dialog_TrapBall", u"4", None))
        self.pushButton_OUT_10.setText(QCoreApplication.translate("Dialog_TrapBall", u"10", None))
        self.pushButton_TRAP_4.setText(QCoreApplication.translate("Dialog_TrapBall", u"4", None))
        self.pushButton_TRAP_5.setText(QCoreApplication.translate("Dialog_TrapBall", u"5", None))
        self.pushButton_TRAP_3.setText(QCoreApplication.translate("Dialog_TrapBall", u"3", None))
        self.pushButton_OUT_5.setText(QCoreApplication.translate("Dialog_TrapBall", u"5", None))
        self.pushButton_OUT_3.setText(QCoreApplication.translate("Dialog_TrapBall", u"3", None))
        self.pushButton_OUT_8.setText(QCoreApplication.translate("Dialog_TrapBall", u"8", None))
        self.pushButton_OUT_1.setText(QCoreApplication.translate("Dialog_TrapBall", u"1", None))
        self.pushButton_TRAP_9.setText(QCoreApplication.translate("Dialog_TrapBall", u"9", None))
        self.pushButton_TRAP_10.setText(QCoreApplication.translate("Dialog_TrapBall", u"10", None))
        self.pushButton_OUT.setText(QCoreApplication.translate("Dialog_TrapBall", u"\u98de\u73e0(OUT)", None))
        self.pushButton_TRAP_1.setText(QCoreApplication.translate("Dialog_TrapBall", u"1", None))
        self.pushButton_OUT_9.setText(QCoreApplication.translate("Dialog_TrapBall", u"9", None))
        self.pushButton_OUT_7.setText(QCoreApplication.translate("Dialog_TrapBall", u"7", None))
        self.pushButton_TRAP_2.setText(QCoreApplication.translate("Dialog_TrapBall", u"2", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog_TrapBall", u"\u786e\u8ba4(confirm)", None))
        self.checkBox_stop.setText(QCoreApplication.translate("Dialog_TrapBall", u"STOP Alarm", None))
    # retranslateUi

