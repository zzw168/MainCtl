# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Speed_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QHeaderView,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Dialog_Set_Speed(object):
    def setupUi(self, Dialog_Set_Speed):
        if not Dialog_Set_Speed.objectName():
            Dialog_Set_Speed.setObjectName(u"Dialog_Set_Speed")
        Dialog_Set_Speed.resize(480, 280)
        Dialog_Set_Speed.setMinimumSize(QSize(480, 280))
        Dialog_Set_Speed.setMaximumSize(QSize(480, 280))
        self.gridLayout = QGridLayout(Dialog_Set_Speed)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog_Set_Speed)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 200))
        self.frame.setMaximumSize(QSize(16777215, 210))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.tableWidget_Set_Speed = QTableWidget(self.frame)
        if (self.tableWidget_Set_Speed.columnCount() < 4):
            self.tableWidget_Set_Speed.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget_Set_Speed.rowCount() < 5):
            self.tableWidget_Set_Speed.setRowCount(5)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_Set_Speed.setVerticalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(0, 3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 2, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(1, 3, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 2, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(2, 3, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(3, 3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 1, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 2, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_Set_Speed.setItem(4, 3, __qtablewidgetitem28)
        self.tableWidget_Set_Speed.setObjectName(u"tableWidget_Set_Speed")
        self.tableWidget_Set_Speed.setMinimumSize(QSize(200, 150))
        self.tableWidget_Set_Speed.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(12)
        font.setBold(False)
        self.tableWidget_Set_Speed.setFont(font)
        self.tableWidget_Set_Speed.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Set_Speed.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Set_Speed.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.tableWidget_Set_Speed, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog_Set_Speed)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 0))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(Dialog_Set_Speed)
        self.buttonBox.accepted.connect(Dialog_Set_Speed.accept)
        self.buttonBox.rejected.connect(Dialog_Set_Speed.reject)

        QMetaObject.connectSlotsByName(Dialog_Set_Speed)
    # setupUi

    def retranslateUi(self, Dialog_Set_Speed):
        Dialog_Set_Speed.setWindowTitle(QCoreApplication.translate("Dialog_Set_Speed", u"\u901f\u5ea6\u8bbe\u7f6e", None))
        ___qtablewidgetitem = self.tableWidget_Set_Speed.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u901f\u5ea6", None));
        ___qtablewidgetitem1 = self.tableWidget_Set_Speed.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u52a0\u901f", None));
        ___qtablewidgetitem2 = self.tableWidget_Set_Speed.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u51cf\u901f", None));
        ___qtablewidgetitem3 = self.tableWidget_Set_Speed.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u5ef6\u65f6", None));
        ___qtablewidgetitem4 = self.tableWidget_Set_Speed.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f741", None));
        ___qtablewidgetitem5 = self.tableWidget_Set_Speed.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f742", None));
        ___qtablewidgetitem6 = self.tableWidget_Set_Speed.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f743", None));
        ___qtablewidgetitem7 = self.tableWidget_Set_Speed.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f744", None));
        ___qtablewidgetitem8 = self.tableWidget_Set_Speed.verticalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog_Set_Speed", u"\u8f745", None));

        __sortingEnabled = self.tableWidget_Set_Speed.isSortingEnabled()
        self.tableWidget_Set_Speed.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.tableWidget_Set_Speed.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem10 = self.tableWidget_Set_Speed.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem11 = self.tableWidget_Set_Speed.item(0, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem12 = self.tableWidget_Set_Speed.item(0, 3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem13 = self.tableWidget_Set_Speed.item(1, 0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem14 = self.tableWidget_Set_Speed.item(1, 1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem15 = self.tableWidget_Set_Speed.item(1, 2)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem16 = self.tableWidget_Set_Speed.item(1, 3)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem17 = self.tableWidget_Set_Speed.item(2, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem18 = self.tableWidget_Set_Speed.item(2, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem19 = self.tableWidget_Set_Speed.item(2, 2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem20 = self.tableWidget_Set_Speed.item(2, 3)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem21 = self.tableWidget_Set_Speed.item(3, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem22 = self.tableWidget_Set_Speed.item(3, 1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem23 = self.tableWidget_Set_Speed.item(3, 2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem24 = self.tableWidget_Set_Speed.item(3, 3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        ___qtablewidgetitem25 = self.tableWidget_Set_Speed.item(4, 0)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Dialog_Set_Speed", u"300", None));
        ___qtablewidgetitem26 = self.tableWidget_Set_Speed.item(4, 1)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.3", None));
        ___qtablewidgetitem27 = self.tableWidget_Set_Speed.item(4, 2)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0.2", None));
        ___qtablewidgetitem28 = self.tableWidget_Set_Speed.item(4, 3)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("Dialog_Set_Speed", u"0", None));
        self.tableWidget_Set_Speed.setSortingEnabled(__sortingEnabled)

    # retranslateUi

