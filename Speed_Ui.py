# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Speed_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Dialog_Set_Speed(object):
    def setupUi(self, Dialog_Set_Speed):
        if not Dialog_Set_Speed.objectName():
            Dialog_Set_Speed.setObjectName(u"Dialog_Set_Speed")
        Dialog_Set_Speed.resize(560, 280)
        Dialog_Set_Speed.setMinimumSize(QSize(560, 280))
        Dialog_Set_Speed.setMaximumSize(QSize(560, 280))
        self.gridLayout = QGridLayout(Dialog_Set_Speed)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.label_3 = QLabel(Dialog_Set_Speed)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        font.setPointSize(10)
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.lineEdit_time_set = QLineEdit(Dialog_Set_Speed)
        self.lineEdit_time_set.setObjectName(u"lineEdit_time_set")
        self.lineEdit_time_set.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_time_set.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_time_set, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog_Set_Speed)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 0))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout.addWidget(self.buttonBox, 1, 3, 1, 1)

        self.label_4 = QLabel(Dialog_Set_Speed)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.frame = QFrame(Dialog_Set_Speed)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 200))
        self.frame.setMaximumSize(QSize(16777215, 210))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.checkBox_auto_line = QCheckBox(self.frame)
        self.checkBox_auto_line.setObjectName(u"checkBox_auto_line")
        self.checkBox_auto_line.setFont(font)

        self.gridLayout_2.addWidget(self.checkBox_auto_line, 0, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)

        self.lineEdit_time = QLineEdit(self.frame)
        self.lineEdit_time.setObjectName(u"lineEdit_time")
        self.lineEdit_time.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_time.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEdit_time, 0, 3, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(245, 0))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.frame_2, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 0, 4, 1, 1)

        self.tableWidget_Set_Speed = QTableWidget(self.frame)
        if (self.tableWidget_Set_Speed.columnCount() < 6):
            self.tableWidget_Set_Speed.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget_Set_Speed.rowCount() < 5):
            self.tableWidget_Set_Speed.setRowCount(5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(4, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 3, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 4, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 5, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 2, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 3, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 4, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 5, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 1, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 2, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 3, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 4, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 5, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 4, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 5, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        __qtablewidgetitem35.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 0, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        __qtablewidgetitem36.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 1, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 2, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        __qtablewidgetitem38.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 3, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        __qtablewidgetitem39.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 4, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 5, __qtablewidgetitem40)
        self.tableWidget_Set_Speed.setObjectName(u"tableWidget_Set_Speed")
        self.tableWidget_Set_Speed.setMinimumSize(QSize(280, 150))
        self.tableWidget_Set_Speed.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.tableWidget_Set_Speed.setFont(font1)
        self.tableWidget_Set_Speed.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Set_Speed.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Set_Speed.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.tableWidget_Set_Speed, 1, 0, 1, 5)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 4)


        self.retranslateUi(Dialog_Set_Speed)
        self.buttonBox.accepted.connect(Dialog_Set_Speed.accept)
        self.buttonBox.rejected.connect(Dialog_Set_Speed.reject)

        QMetaObject.connectSlotsByName(Dialog_Set_Speed)
    # setupUi

    def retranslateUi(self, Dialog_Set_Speed):
        Dialog_Set_Speed.setWindowTitle(QCoreApplication.translate("Dialog_Set_Speed", u"\u901f\u5ea6\u8bbe\u7f6e", None))
        self.label_3.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u79d2", None))
        self.lineEdit_time_set.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None))
        self.label_4.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8bbe\u7f6e\u5b8c\u6210\u65f6\u95f4\uff1a", None))
        self.checkBox_auto_line.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u81ea\u52a8\u8c03\u6574\u5bf9\u89d2\u76f4\u7ebf", None))
        self.label.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u9884\u8ba1\u5b8c\u6210\u65f6\u95f4\uff1a", None))
        self.lineEdit_time.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u79d2", None))
        ___qtablewidgetitem = self.tableWidget_Set_Speed.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u901f\u5ea6", None));
        ___qtablewidgetitem1 = self.tableWidget_Set_Speed.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u52a0\u901f", None));
        ___qtablewidgetitem2 = self.tableWidget_Set_Speed.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u51cf\u901f", None));
        ___qtablewidgetitem3 = self.tableWidget_Set_Speed.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u5ef6\u65f6(\u79d2)", None));
        ___qtablewidgetitem4 = self.tableWidget_Set_Speed.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8d77\u901f", None));
        ___qtablewidgetitem5 = self.tableWidget_Set_Speed.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u5e73\u6ed1(\u6beb\u79d2)", None));
        ___qtablewidgetitem6 = self.tableWidget_Set_Speed.verticalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f741", None));
        ___qtablewidgetitem7 = self.tableWidget_Set_Speed.verticalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f742", None));
        ___qtablewidgetitem8 = self.tableWidget_Set_Speed.verticalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f743", None));
        ___qtablewidgetitem9 = self.tableWidget_Set_Speed.verticalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f744", None));
        ___qtablewidgetitem10 = self.tableWidget_Set_Speed.verticalHeaderItem(4)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f745", None));

        __sortingEnabled = self.tableWidget_Set_Speed.isSortingEnabled()
        self.tableWidget_Set_Speed.setSortingEnabled(False)
        ___qtablewidgetitem11 = self.tableWidget_Set_Speed.item(0, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem12 = self.tableWidget_Set_Speed.item(0, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem13 = self.tableWidget_Set_Speed.item(0, 2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem14 = self.tableWidget_Set_Speed.item(0, 3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem15 = self.tableWidget_Set_Speed.item(0, 4)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog_Set_Speed", u"1", None));
        ___qtablewidgetitem16 = self.tableWidget_Set_Speed.item(0, 5)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog_Set_Speed", u"3", None));
        ___qtablewidgetitem17 = self.tableWidget_Set_Speed.item(1, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem18 = self.tableWidget_Set_Speed.item(1, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem19 = self.tableWidget_Set_Speed.item(1, 2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem20 = self.tableWidget_Set_Speed.item(1, 3)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem21 = self.tableWidget_Set_Speed.item(1, 4)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Dialog_Set_Speed", u"1", None));
        ___qtablewidgetitem22 = self.tableWidget_Set_Speed.item(1, 5)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Dialog_Set_Speed", u"3", None));
        ___qtablewidgetitem23 = self.tableWidget_Set_Speed.item(2, 0)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem24 = self.tableWidget_Set_Speed.item(2, 1)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem25 = self.tableWidget_Set_Speed.item(2, 2)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem26 = self.tableWidget_Set_Speed.item(2, 3)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem27 = self.tableWidget_Set_Speed.item(2, 4)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Dialog_Set_Speed", u"1", None));
        ___qtablewidgetitem28 = self.tableWidget_Set_Speed.item(2, 5)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("Dialog_Set_Speed", u"3", None));
        ___qtablewidgetitem29 = self.tableWidget_Set_Speed.item(3, 0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem30 = self.tableWidget_Set_Speed.item(3, 1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem31 = self.tableWidget_Set_Speed.item(3, 2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem32 = self.tableWidget_Set_Speed.item(3, 3)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem33 = self.tableWidget_Set_Speed.item(3, 4)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("Dialog_Set_Speed", u"1", None));
        ___qtablewidgetitem34 = self.tableWidget_Set_Speed.item(3, 5)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("Dialog_Set_Speed", u"3", None));
        ___qtablewidgetitem35 = self.tableWidget_Set_Speed.item(4, 0)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem36 = self.tableWidget_Set_Speed.item(4, 1)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem37 = self.tableWidget_Set_Speed.item(4, 2)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem38 = self.tableWidget_Set_Speed.item(4, 3)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem39 = self.tableWidget_Set_Speed.item(4, 4)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("Dialog_Set_Speed", u"1", None));
        ___qtablewidgetitem40 = self.tableWidget_Set_Speed.item(4, 5)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("Dialog_Set_Speed", u"3", None));
        self.tableWidget_Set_Speed.setSortingEnabled(__sortingEnabled)

    # retranslateUi

