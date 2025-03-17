# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Map_Ui.ui'
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
    QSizePolicy, QWidget)

class Ui_Dialog_Map(object):
    def setupUi(self, Dialog_Map):
        if not Dialog_Map.objectName():
            Dialog_Map.setObjectName(u"Dialog_Map")
        Dialog_Map.resize(370, 400)
        Dialog_Map.setMinimumSize(QSize(370, 400))
        Dialog_Map.setMaximumSize(QSize(370, 400))
        self.gridLayout = QGridLayout(Dialog_Map)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_14 = QGroupBox(Dialog_Map)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(350, 380))
        self.groupBox_14.setMaximumSize(QSize(350, 380))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_14.setFont(font)
        self.gridLayout_37 = QGridLayout(self.groupBox_14)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.gridLayout_37.setContentsMargins(0, -1, 0, -1)
        self.widget_map = QWidget(self.groupBox_14)
        self.widget_map.setObjectName(u"widget_map")
        self.widget_map.setMinimumSize(QSize(350, 350))
        self.widget_map.setMaximumSize(QSize(350, 350))

        self.gridLayout_37.addWidget(self.widget_map, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_14, 0, 0, 1, 1)


        self.retranslateUi(Dialog_Map)

        QMetaObject.connectSlotsByName(Dialog_Map)
    # setupUi

    def retranslateUi(self, Dialog_Map):
        Dialog_Map.setWindowTitle(QCoreApplication.translate("Dialog_Map", u"\u536b\u661f\u56fe", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("Dialog_Map", u"\u536b\u661f\u56fe", None))
    # retranslateUi

