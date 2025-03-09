# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kaj789_Ui.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QGroupBox, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Dialog_Kaj789_Ui(object):
    def setupUi(self, Dialog_Kaj789_Ui):
        if not Dialog_Kaj789_Ui.objectName():
            Dialog_Kaj789_Ui.setObjectName(u"Dialog_Kaj789_Ui")
        Dialog_Kaj789_Ui.resize(1189, 651)
        Dialog_Kaj789_Ui.setMinimumSize(QSize(560, 280))
        Dialog_Kaj789_Ui.setMaximumSize(QSize(5000, 5000))
        self.gridLayout = QGridLayout(Dialog_Kaj789_Ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.buttonBox = QDialogButtonBox(Dialog_Kaj789_Ui)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 0))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.frame = QFrame(Dialog_Kaj789_Ui)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 200))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBox_kaj789 = QComboBox(self.groupBox)
        self.comboBox_kaj789.setObjectName(u"comboBox_kaj789")

        self.gridLayout_3.addWidget(self.comboBox_kaj789, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(500, 0))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_3.addWidget(self.frame_2, 0, 1, 1, 1)

        self.tableWidget_Results = QTableWidget(self.groupBox)
        if (self.tableWidget_Results.columnCount() < 15):
            self.tableWidget_Results.setColumnCount(15)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_Results.setHorizontalHeaderItem(14, __qtablewidgetitem14)
        self.tableWidget_Results.setObjectName(u"tableWidget_Results")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.tableWidget_Results.setFont(font1)
        self.tableWidget_Results.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Results.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.tableWidget_Results.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Results.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_3.addWidget(self.tableWidget_Results, 1, 0, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 3)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)


        self.retranslateUi(Dialog_Kaj789_Ui)
        self.buttonBox.accepted.connect(Dialog_Kaj789_Ui.accept)
        self.buttonBox.rejected.connect(Dialog_Kaj789_Ui.reject)

        QMetaObject.connectSlotsByName(Dialog_Kaj789_Ui)
    # setupUi

    def retranslateUi(self, Dialog_Kaj789_Ui):
        Dialog_Kaj789_Ui.setWindowTitle(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u5f00\u5956\u7ed3\u679c", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u9009\u62e9\u65e5\u671f", None))
        ___qtablewidgetitem = self.tableWidget_Results.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u671f\u53f7", None));
        ___qtablewidgetitem1 = self.tableWidget_Results.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u5f00\u8dd1\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget_Results.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u5012\u6570", None));
        ___qtablewidgetitem3 = self.tableWidget_Results.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u72b6\u6001", None));
        ___qtablewidgetitem4 = self.tableWidget_Results.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u81ea\u52a8\u8d5b\u679c", None));
        ___qtablewidgetitem5 = self.tableWidget_Results.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u624b\u52a8\u8d5b\u679c", None));
        ___qtablewidgetitem6 = self.tableWidget_Results.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u53d1\u9001\u72b6\u6001", None));
        ___qtablewidgetitem7 = self.tableWidget_Results.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u56fe\u7247\u4e0a\u4f20", None));
        ___qtablewidgetitem8 = self.tableWidget_Results.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u5907\u6ce8", None));
        ___qtablewidgetitem9 = self.tableWidget_Results.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u56fe\u7247", None));
        ___qtablewidgetitem10 = self.tableWidget_Results.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u5f55\u50cf", None));
        ___qtablewidgetitem11 = self.tableWidget_Results.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u7ed3\u675f\u65f6\u95f4\u6233", None));
        ___qtablewidgetitem12 = self.tableWidget_Results.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u6570\u636e\u5305", None));
        ___qtablewidgetitem13 = self.tableWidget_Results.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u8865\u53d1\u72b6\u6001", None));
        ___qtablewidgetitem14 = self.tableWidget_Results.horizontalHeaderItem(14)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog_Kaj789_Ui", u"\u8865\u4f20\u72b6\u6001", None));
    # retranslateUi

