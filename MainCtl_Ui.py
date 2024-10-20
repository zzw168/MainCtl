# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainCtl_Ui.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextBrowser, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1363, 975)
        MainWindow.setMinimumSize(QSize(100, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget_Ranking = QTabWidget(self.centralwidget)
        self.tabWidget_Ranking.setObjectName(u"tabWidget_Ranking")
        self.tabWidget_Ranking.setMinimumSize(QSize(10, 10))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(10)
        self.tabWidget_Ranking.setFont(font)
        self.tab_0 = QWidget()
        self.tab_0.setObjectName(u"tab_0")
        self.gridLayout_11 = QGridLayout(self.tab_0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_Results = QTableWidget(self.tab_0)
        if (self.tableWidget_Results.columnCount() < 10):
            self.tableWidget_Results.setColumnCount(10)
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
        self.tableWidget_Results.setObjectName(u"tableWidget_Results")
        self.tableWidget_Results.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Results.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Results.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_11.addWidget(self.tableWidget_Results, 2, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_0)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_3)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.groupBox = QGroupBox(self.frame_3)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.groupBox.setFont(font1)
        self.groupBox.setStyleSheet(u"")
        self.gridLayout_9 = QGridLayout(self.groupBox)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_9.addWidget(self.radioButton, 0, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_9.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.radioButton_3 = QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_9.addWidget(self.radioButton_3, 2, 0, 1, 1)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_9.addWidget(self.checkBox, 3, 0, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox, 0, 0, 3, 1)

        self.groupBox_status = QGroupBox(self.frame_3)
        self.groupBox_status.setObjectName(u"groupBox_status")
        self.groupBox_status.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.groupBox_status)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.status_live = QToolButton(self.groupBox_status)
        self.status_live.setObjectName(u"status_live")
        self.status_live.setFont(font1)
        self.status_live.setAutoFillBackground(False)
        self.status_live.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_live.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_live.setAutoRaise(True)

        self.verticalLayout.addWidget(self.status_live)

        self.status_road = QToolButton(self.groupBox_status)
        self.status_road.setObjectName(u"status_road")
        self.status_road.setFont(font1)
        self.status_road.setAutoFillBackground(False)
        self.status_road.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_road.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_road.setAutoRaise(True)
        self.status_road.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout.addWidget(self.status_road)

        self.status_lenses = QToolButton(self.groupBox_status)
        self.status_lenses.setObjectName(u"status_lenses")
        self.status_lenses.setFont(font1)
        self.status_lenses.setAutoFillBackground(False)
        self.status_lenses.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_lenses.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_lenses.setAutoRaise(True)

        self.verticalLayout.addWidget(self.status_lenses)

        self.status_track = QToolButton(self.groupBox_status)
        self.status_track.setObjectName(u"status_track")
        self.status_track.setFont(font1)
        self.status_track.setAutoFillBackground(False)
        self.status_track.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_track.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_track.setAutoRaise(True)

        self.verticalLayout.addWidget(self.status_track)


        self.gridLayout_12.addWidget(self.groupBox_status, 0, 1, 3, 1)

        self.groupBox_status_2 = QGroupBox(self.frame_3)
        self.groupBox_status_2.setObjectName(u"groupBox_status_2")
        self.groupBox_status_2.setMaximumSize(QSize(375, 16777215))
        self.groupBox_status_2.setFont(font1)
        self.gridLayout_3 = QGridLayout(self.groupBox_status_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.status_server1 = QToolButton(self.groupBox_status_2)
        self.status_server1.setObjectName(u"status_server1")
        self.status_server1.setFont(font1)
        self.status_server1.setAutoFillBackground(False)
        self.status_server1.setStyleSheet(u"background:rgb(255, 0, 0)")
        self.status_server1.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_server1.setAutoRaise(True)
        self.status_server1.setArrowType(Qt.ArrowType.NoArrow)

        self.gridLayout_3.addWidget(self.status_server1, 0, 0, 1, 2)

        self.status_server2 = QToolButton(self.groupBox_status_2)
        self.status_server2.setObjectName(u"status_server2")
        self.status_server2.setFont(font1)
        self.status_server2.setAutoFillBackground(False)
        self.status_server2.setStyleSheet(u"background:rgb(255, 0, 0)")
        self.status_server2.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_server2.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_server2, 0, 2, 1, 2)

        self.status_sportsCards = QToolButton(self.groupBox_status_2)
        self.status_sportsCards.setObjectName(u"status_sportsCards")
        self.status_sportsCards.setFont(font1)
        self.status_sportsCards.setAutoFillBackground(False)
        self.status_sportsCards.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_sportsCards.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_sportsCards.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_sportsCards, 0, 4, 1, 2)

        self.frame_4 = QFrame(self.groupBox_status_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(70, 0))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_3.addWidget(self.frame_4, 0, 6, 2, 1)

        self.status_obs = QToolButton(self.groupBox_status_2)
        self.status_obs.setObjectName(u"status_obs")
        self.status_obs.setFont(font1)
        self.status_obs.setAutoFillBackground(False)
        self.status_obs.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_obs.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_obs.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_obs, 1, 0, 1, 1)

        self.status_mainlenses = QToolButton(self.groupBox_status_2)
        self.status_mainlenses.setObjectName(u"status_mainlenses")
        self.status_mainlenses.setFont(font1)
        self.status_mainlenses.setAutoFillBackground(False)
        self.status_mainlenses.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_mainlenses.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_mainlenses.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_mainlenses, 1, 1, 1, 2)

        self.status_Recognition = QToolButton(self.groupBox_status_2)
        self.status_Recognition.setObjectName(u"status_Recognition")
        self.status_Recognition.setFont(font1)
        self.status_Recognition.setAutoFillBackground(False)
        self.status_Recognition.setStyleSheet(u"background:rgb(255, 0, 0)")
        self.status_Recognition.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_Recognition.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_Recognition, 1, 3, 1, 2)

        self.status_Extension = QToolButton(self.groupBox_status_2)
        self.status_Extension.setObjectName(u"status_Extension")
        self.status_Extension.setFont(font1)
        self.status_Extension.setAutoFillBackground(False)
        self.status_Extension.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_Extension.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_Extension.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_Extension, 1, 5, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_status_2, 0, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_16 = QGridLayout(self.groupBox_3)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.checkBox_2 = QCheckBox(self.groupBox_3)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_2, 0, 0, 1, 1)

        self.checkBox_7 = QCheckBox(self.groupBox_3)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_7, 0, 1, 1, 1)

        self.checkBox_3 = QCheckBox(self.groupBox_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_3, 1, 0, 1, 1)

        self.checkBox_4 = QCheckBox(self.groupBox_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_4, 1, 1, 1, 1)

        self.checkBox_6 = QCheckBox(self.groupBox_3)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_6, 2, 0, 1, 1)

        self.checkBox_5 = QCheckBox(self.groupBox_3)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_5, 2, 1, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_3, 0, 3, 2, 2)

        self.groupBox_2 = QGroupBox(self.frame_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(375, 16777215))
        self.groupBox_2.setFont(font1)
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_8.addWidget(self.lineEdit_4, 0, 2, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_8.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_8.addWidget(self.lineEdit_3, 0, 3, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_8.addWidget(self.lineEdit_2, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.groupBox_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(50, 0))
        self.frame_5.setMaximumSize(QSize(100, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_8.addWidget(self.frame_5, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_2, 1, 2, 2, 1)

        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 50))
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton.setFont(font2)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton, 2, 3, 1, 1)

        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_17.addWidget(self.label_2, 0, 3, 1, 1)

        self.lineEdit_5 = QLineEdit(self.frame)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_5.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineEdit_5, 0, 2, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(85, 16777215))
        self.label.setFont(font1)
        self.label.setAutoFillBackground(False)

        self.gridLayout_17.addWidget(self.label, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame, 2, 4, 1, 1)


        self.gridLayout_11.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_0)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(300, 0))
        self.frame_2.setMaximumSize(QSize(380, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMaximumSize(QSize(16777215, 16777215))
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_add_3 = QPushButton(self.frame_8)
        self.pushButton_add_3.setObjectName(u"pushButton_add_3")
        self.pushButton_add_3.setMaximumSize(QSize(200, 16777215))
        self.pushButton_add_3.setFont(font1)
        self.pushButton_add_3.setStyleSheet(u"background:rgb(255, 0, 0)")

        self.horizontalLayout_2.addWidget(self.pushButton_add_3)

        self.pushButton_start_2 = QPushButton(self.frame_8)
        self.pushButton_start_2.setObjectName(u"pushButton_start_2")
        self.pushButton_start_2.setMaximumSize(QSize(200, 16777215))
        self.pushButton_start_2.setFont(font1)
        self.pushButton_start_2.setStyleSheet(u"background:rgb(255, 255, 0)")

        self.horizontalLayout_2.addWidget(self.pushButton_start_2)


        self.gridLayout_10.addWidget(self.frame_8, 0, 0, 1, 1)

        self.textBrowser_msg = QTextBrowser(self.frame_2)
        self.textBrowser_msg.setObjectName(u"textBrowser_msg")

        self.gridLayout_10.addWidget(self.textBrowser_msg, 4, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.pushButton_add_2 = QPushButton(self.frame_7)
        self.pushButton_add_2.setObjectName(u"pushButton_add_2")

        self.gridLayout_7.addWidget(self.pushButton_add_2, 0, 0, 1, 1)

        self.pushButton_save_2 = QPushButton(self.frame_7)
        self.pushButton_save_2.setObjectName(u"pushButton_save_2")
        self.pushButton_save_2.setMinimumSize(QSize(20, 0))
        self.pushButton_save_2.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_2, 0, 1, 1, 1)

        self.pushButton_update_2 = QPushButton(self.frame_7)
        self.pushButton_update_2.setObjectName(u"pushButton_update_2")
        self.pushButton_update_2.setMinimumSize(QSize(20, 0))
        self.pushButton_update_2.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_2, 0, 2, 1, 1)

        self.pushButton_save_3 = QPushButton(self.frame_7)
        self.pushButton_save_3.setObjectName(u"pushButton_save_3")
        self.pushButton_save_3.setMinimumSize(QSize(20, 0))
        self.pushButton_save_3.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_3, 0, 3, 1, 1)

        self.pushButton_update_3 = QPushButton(self.frame_7)
        self.pushButton_update_3.setObjectName(u"pushButton_update_3")
        self.pushButton_update_3.setMinimumSize(QSize(20, 0))
        self.pushButton_update_3.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_3, 0, 4, 1, 1)

        self.pushButton_save_4 = QPushButton(self.frame_7)
        self.pushButton_save_4.setObjectName(u"pushButton_save_4")
        self.pushButton_save_4.setMinimumSize(QSize(20, 0))
        self.pushButton_save_4.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_4, 0, 5, 1, 1)

        self.pushButton_update_5 = QPushButton(self.frame_7)
        self.pushButton_update_5.setObjectName(u"pushButton_update_5")
        self.pushButton_update_5.setMinimumSize(QSize(20, 0))
        self.pushButton_update_5.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_5, 0, 6, 1, 1)

        self.pushButton_save_5 = QPushButton(self.frame_7)
        self.pushButton_save_5.setObjectName(u"pushButton_save_5")
        self.pushButton_save_5.setMinimumSize(QSize(20, 0))
        self.pushButton_save_5.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_5, 0, 7, 1, 1)

        self.pushButton_update_4 = QPushButton(self.frame_7)
        self.pushButton_update_4.setObjectName(u"pushButton_update_4")
        self.pushButton_update_4.setMinimumSize(QSize(20, 0))
        self.pushButton_update_4.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_4, 0, 8, 1, 1)

        self.pushButton_save_6 = QPushButton(self.frame_7)
        self.pushButton_save_6.setObjectName(u"pushButton_save_6")
        self.pushButton_save_6.setMinimumSize(QSize(20, 0))
        self.pushButton_save_6.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_6, 0, 9, 1, 1)

        self.pushButton_update_6 = QPushButton(self.frame_7)
        self.pushButton_update_6.setObjectName(u"pushButton_update_6")
        self.pushButton_update_6.setMinimumSize(QSize(30, 0))
        self.pushButton_update_6.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_6, 0, 10, 1, 1)

        self.pushButton_once_2 = QPushButton(self.frame_7)
        self.pushButton_once_2.setObjectName(u"pushButton_once_2")

        self.gridLayout_7.addWidget(self.pushButton_once_2, 1, 0, 1, 1)

        self.pushButton_save_7 = QPushButton(self.frame_7)
        self.pushButton_save_7.setObjectName(u"pushButton_save_7")
        self.pushButton_save_7.setMinimumSize(QSize(20, 0))
        self.pushButton_save_7.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_7, 1, 1, 1, 1)

        self.pushButton_update_10 = QPushButton(self.frame_7)
        self.pushButton_update_10.setObjectName(u"pushButton_update_10")
        self.pushButton_update_10.setMinimumSize(QSize(20, 0))
        self.pushButton_update_10.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_10, 1, 2, 1, 1)

        self.pushButton_save_11 = QPushButton(self.frame_7)
        self.pushButton_save_11.setObjectName(u"pushButton_save_11")
        self.pushButton_save_11.setMinimumSize(QSize(20, 0))
        self.pushButton_save_11.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_11, 1, 3, 1, 1)

        self.pushButton_update_9 = QPushButton(self.frame_7)
        self.pushButton_update_9.setObjectName(u"pushButton_update_9")
        self.pushButton_update_9.setMinimumSize(QSize(20, 0))
        self.pushButton_update_9.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_9, 1, 4, 1, 1)

        self.pushButton_save_8 = QPushButton(self.frame_7)
        self.pushButton_save_8.setObjectName(u"pushButton_save_8")
        self.pushButton_save_8.setMinimumSize(QSize(20, 0))
        self.pushButton_save_8.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_8, 1, 5, 1, 1)

        self.pushButton_update_11 = QPushButton(self.frame_7)
        self.pushButton_update_11.setObjectName(u"pushButton_update_11")
        self.pushButton_update_11.setMinimumSize(QSize(20, 0))
        self.pushButton_update_11.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_11, 1, 6, 1, 1)

        self.pushButton_save_9 = QPushButton(self.frame_7)
        self.pushButton_save_9.setObjectName(u"pushButton_save_9")
        self.pushButton_save_9.setMinimumSize(QSize(20, 0))
        self.pushButton_save_9.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_9, 1, 7, 1, 1)

        self.pushButton_update_8 = QPushButton(self.frame_7)
        self.pushButton_update_8.setObjectName(u"pushButton_update_8")
        self.pushButton_update_8.setMinimumSize(QSize(20, 0))
        self.pushButton_update_8.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_8, 1, 8, 1, 1)

        self.pushButton_save_10 = QPushButton(self.frame_7)
        self.pushButton_save_10.setObjectName(u"pushButton_save_10")
        self.pushButton_save_10.setMinimumSize(QSize(20, 0))
        self.pushButton_save_10.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_save_10, 1, 9, 1, 1)

        self.pushButton_update_7 = QPushButton(self.frame_7)
        self.pushButton_update_7.setObjectName(u"pushButton_update_7")
        self.pushButton_update_7.setMinimumSize(QSize(30, 0))
        self.pushButton_update_7.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_update_7, 1, 10, 1, 1)


        self.gridLayout_10.addWidget(self.frame_7, 3, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 16777215))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_add = QPushButton(self.frame_6)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_save = QPushButton(self.frame_6)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_update = QPushButton(self.frame_6)
        self.pushButton_update.setObjectName(u"pushButton_update")
        self.pushButton_update.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_update)

        self.pushButton_once = QPushButton(self.frame_6)
        self.pushButton_once.setObjectName(u"pushButton_once")
        self.pushButton_once.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_once)

        self.pushButton_start = QPushButton(self.frame_6)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_start)


        self.gridLayout_10.addWidget(self.frame_6, 1, 0, 1, 1)

        self.widget_9 = QWidget(self.frame_2)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setMinimumSize(QSize(0, 200))
        self.gridLayout_5 = QGridLayout(self.widget_9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_3 = QLabel(self.widget_9)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"color:rgb(255, 0, 0)")

        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 2)

        self.label_4 = QLabel(self.widget_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.widget_9)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setFont(font1)

        self.gridLayout_5.addWidget(self.lineEdit_6, 1, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.widget_9)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_2, 1, 2, 1, 1)

        self.label_5 = QLabel(self.widget_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.gridLayout_5.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_7 = QLineEdit(self.widget_9)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setFont(font1)

        self.gridLayout_5.addWidget(self.lineEdit_7, 2, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.widget_9)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_3, 2, 2, 1, 1)

        self.lineEdit_8 = QLineEdit(self.widget_9)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setFont(font1)

        self.gridLayout_5.addWidget(self.lineEdit_8, 3, 0, 1, 2)

        self.checkBox_8 = QCheckBox(self.widget_9)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setFont(font1)

        self.gridLayout_5.addWidget(self.checkBox_8, 3, 2, 1, 1)

        self.frame_9 = QFrame(self.widget_9)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_add_4 = QPushButton(self.frame_9)
        self.pushButton_add_4.setObjectName(u"pushButton_add_4")
        self.pushButton_add_4.setMaximumSize(QSize(100, 16777215))
        self.pushButton_add_4.setAutoDefault(False)
        self.pushButton_add_4.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_add_4)

        self.pushButton_save_12 = QPushButton(self.frame_9)
        self.pushButton_save_12.setObjectName(u"pushButton_save_12")
        self.pushButton_save_12.setMaximumSize(QSize(100, 16777215))
        self.pushButton_save_12.setAutoDefault(False)
        self.pushButton_save_12.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_save_12)

        self.pushButton_update_12 = QPushButton(self.frame_9)
        self.pushButton_update_12.setObjectName(u"pushButton_update_12")
        self.pushButton_update_12.setMaximumSize(QSize(100, 16777215))
        self.pushButton_update_12.setAutoDefault(False)
        self.pushButton_update_12.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_update_12)


        self.gridLayout_5.addWidget(self.frame_9, 4, 0, 1, 3)


        self.gridLayout_10.addWidget(self.widget_9, 2, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame_2, 1, 1, 2, 1)

        self.tabWidget_Ranking.addTab(self.tab_0, "")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.gridLayout_20 = QGridLayout(self.tab_1)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.tab_1)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_13)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.lineEdit_rename = QLineEdit(self.frame_13)
        self.lineEdit_rename.setObjectName(u"lineEdit_rename")

        self.gridLayout_13.addWidget(self.lineEdit_rename, 0, 10, 1, 1)

        self.comboBox_plan = QComboBox(self.frame_13)
        self.comboBox_plan.setObjectName(u"comboBox_plan")
        self.comboBox_plan.setMinimumSize(QSize(200, 0))
        self.comboBox_plan.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_plan, 0, 2, 1, 1)

        self.checkBox_test = QCheckBox(self.frame_13)
        self.checkBox_test.setObjectName(u"checkBox_test")
        self.checkBox_test.setFont(font1)

        self.gridLayout_13.addWidget(self.checkBox_test, 0, 7, 1, 1)

        self.frame_14 = QFrame(self.frame_13)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(50, 0))
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_14, 0, 4, 1, 1)

        self.label_22 = QLabel(self.frame_13)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.gridLayout_13.addWidget(self.label_22, 0, 1, 1, 1)

        self.frame_19 = QFrame(self.frame_13)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(50, 0))
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_19, 0, 8, 1, 1)

        self.pushButton_rename = QPushButton(self.frame_13)
        self.pushButton_rename.setObjectName(u"pushButton_rename")
        self.pushButton_rename.setFont(font1)

        self.gridLayout_13.addWidget(self.pushButton_rename, 0, 11, 1, 1)

        self.label_23 = QLabel(self.frame_13)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)

        self.gridLayout_13.addWidget(self.label_23, 0, 9, 1, 1)

        self.pushButton_fsave = QPushButton(self.frame_13)
        self.pushButton_fsave.setObjectName(u"pushButton_fsave")
        self.pushButton_fsave.setMinimumSize(QSize(100, 0))
        self.pushButton_fsave.setFont(font1)

        self.gridLayout_13.addWidget(self.pushButton_fsave, 0, 3, 1, 1)

        self.checkBox_selectall = QCheckBox(self.frame_13)
        self.checkBox_selectall.setObjectName(u"checkBox_selectall")
        self.checkBox_selectall.setFont(font1)

        self.gridLayout_13.addWidget(self.checkBox_selectall, 0, 0, 1, 1)

        self.checkBox_follow = QCheckBox(self.frame_13)
        self.checkBox_follow.setObjectName(u"checkBox_follow")
        self.checkBox_follow.setFont(font1)

        self.gridLayout_13.addWidget(self.checkBox_follow, 0, 5, 1, 1)

        self.frame_29 = QFrame(self.frame_13)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(50, 0))
        self.frame_29.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_29, 0, 6, 1, 1)


        self.gridLayout_20.addWidget(self.frame_13, 0, 0, 1, 1)

        self.tableWidget_Step = QTableWidget(self.tab_1)
        if (self.tableWidget_Step.columnCount() < 18):
            self.tableWidget_Step.setColumnCount(18)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(11, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(12, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(13, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(14, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(15, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(16, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(17, __qtablewidgetitem27)
        self.tableWidget_Step.setObjectName(u"tableWidget_Step")
        self.tableWidget_Step.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Step.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Step.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_20.addWidget(self.tableWidget_Step, 1, 0, 1, 1)

        self.frame_23 = QFrame(self.tab_1)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(0, 0))
        self.frame_23.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_23)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(-1, 0, -1, 0)

        self.gridLayout_20.addWidget(self.frame_23, 2, 0, 1, 1)

        self.frame_10 = QFrame(self.tab_1)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(300, 0))
        self.frame_10.setMaximumSize(QSize(300, 16777215))
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_34 = QGridLayout(self.frame_10)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setContentsMargins(-1, 0, -1, 0)
        self.groupBox_6 = QGroupBox(self.frame_10)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFont(font1)
        self.gridLayout_22 = QGridLayout(self.groupBox_6)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(-1, 0, -1, 0)
        self.frame_17 = QFrame(self.groupBox_6)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_17)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(-1, 0, -1, 0)
        self.label_20 = QLabel(self.frame_17)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.gridLayout_23.addWidget(self.label_20, 0, 0, 1, 1)

        self.lineEdit_axis0 = QLineEdit(self.frame_17)
        self.lineEdit_axis0.setObjectName(u"lineEdit_axis0")
        font4 = QFont()
        font4.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.lineEdit_axis0.setFont(font4)
        self.lineEdit_axis0.setStyleSheet(u"background:rgb(240,240,240)")
        self.lineEdit_axis0.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_axis0.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_axis0, 0, 1, 1, 1)

        self.label_21 = QLabel(self.frame_17)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)

        self.gridLayout_23.addWidget(self.label_21, 1, 0, 1, 1)

        self.lineEdit_axis1 = QLineEdit(self.frame_17)
        self.lineEdit_axis1.setObjectName(u"lineEdit_axis1")
        self.lineEdit_axis1.setFont(font4)
        self.lineEdit_axis1.setStyleSheet(u"background:rgb(240,240,240)")
        self.lineEdit_axis1.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_axis1.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_axis1, 1, 1, 1, 1)

        self.label_25 = QLabel(self.frame_17)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font1)

        self.gridLayout_23.addWidget(self.label_25, 2, 0, 1, 1)

        self.lineEdit_axis2 = QLineEdit(self.frame_17)
        self.lineEdit_axis2.setObjectName(u"lineEdit_axis2")
        self.lineEdit_axis2.setFont(font4)
        self.lineEdit_axis2.setStyleSheet(u"background:rgb(240,240,240)")
        self.lineEdit_axis2.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_axis2.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_axis2, 2, 1, 1, 1)

        self.label_26 = QLabel(self.frame_17)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.gridLayout_23.addWidget(self.label_26, 3, 0, 1, 1)

        self.lineEdit_axis3 = QLineEdit(self.frame_17)
        self.lineEdit_axis3.setObjectName(u"lineEdit_axis3")
        self.lineEdit_axis3.setFont(font4)
        self.lineEdit_axis3.setStyleSheet(u"background:rgb(240,240,240)")
        self.lineEdit_axis3.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_axis3.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_axis3, 3, 1, 1, 1)

        self.label_24 = QLabel(self.frame_17)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font1)

        self.gridLayout_23.addWidget(self.label_24, 4, 0, 1, 1)

        self.lineEdit_axis4 = QLineEdit(self.frame_17)
        self.lineEdit_axis4.setObjectName(u"lineEdit_axis4")
        self.lineEdit_axis4.setFont(font4)
        self.lineEdit_axis4.setStyleSheet(u"background:rgb(240,240,240)")
        self.lineEdit_axis4.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_axis4.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_axis4, 4, 1, 1, 1)


        self.gridLayout_22.addWidget(self.frame_17, 1, 0, 1, 1)

        self.frame_16 = QFrame(self.groupBox_6)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 0))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_16)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(-1, 0, -1, 0)
        self.checkBox_key = QCheckBox(self.frame_16)
        self.checkBox_key.setObjectName(u"checkBox_key")
        self.checkBox_key.setFont(font1)

        self.gridLayout_19.addWidget(self.checkBox_key, 0, 0, 1, 1)

        self.pushButton_ToTable = QPushButton(self.frame_16)
        self.pushButton_ToTable.setObjectName(u"pushButton_ToTable")
        self.pushButton_ToTable.setMinimumSize(QSize(0, 30))
        self.pushButton_ToTable.setFont(font1)

        self.gridLayout_19.addWidget(self.pushButton_ToTable, 0, 1, 1, 1)


        self.gridLayout_22.addWidget(self.frame_16, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.groupBox_6)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 100))
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_15)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.pushButton_CardRun = QPushButton(self.frame_15)
        self.pushButton_CardRun.setObjectName(u"pushButton_CardRun")
        self.pushButton_CardRun.setMinimumSize(QSize(0, 30))
        self.pushButton_CardRun.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardRun, 1, 0, 1, 1)

        self.frame_18 = QFrame(self.frame_15)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMaximumSize(QSize(135, 16777215))
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_18)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.label_18 = QLabel(self.frame_18)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font1)

        self.gridLayout_21.addWidget(self.label_18, 0, 0, 1, 1)

        self.lineEdit_CardNo = QLineEdit(self.frame_18)
        self.lineEdit_CardNo.setObjectName(u"lineEdit_CardNo")
        self.lineEdit_CardNo.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_CardNo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_21.addWidget(self.lineEdit_CardNo, 0, 1, 1, 1)


        self.gridLayout_24.addWidget(self.frame_18, 0, 0, 1, 1)

        self.pushButton_CardStop = QPushButton(self.frame_15)
        self.pushButton_CardStop.setObjectName(u"pushButton_CardStop")
        self.pushButton_CardStop.setMinimumSize(QSize(0, 30))
        self.pushButton_CardStop.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardStop, 2, 0, 1, 1)

        self.pushButton_CardStart = QPushButton(self.frame_15)
        self.pushButton_CardStart.setObjectName(u"pushButton_CardStart")
        self.pushButton_CardStart.setMinimumSize(QSize(0, 30))
        self.pushButton_CardStart.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardStart, 0, 1, 1, 1)

        self.pushButton_CardReset = QPushButton(self.frame_15)
        self.pushButton_CardReset.setObjectName(u"pushButton_CardReset")
        self.pushButton_CardReset.setMinimumSize(QSize(0, 30))
        self.pushButton_CardReset.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardReset, 1, 1, 1, 1)

        self.pushButton_CardNext = QPushButton(self.frame_15)
        self.pushButton_CardNext.setObjectName(u"pushButton_CardNext")
        self.pushButton_CardNext.setMinimumSize(QSize(0, 30))
        self.pushButton_CardNext.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardNext, 2, 1, 1, 1)

        self.pushButton_CardCloseAll = QPushButton(self.frame_15)
        self.pushButton_CardCloseAll.setObjectName(u"pushButton_CardCloseAll")
        self.pushButton_CardCloseAll.setMinimumSize(QSize(0, 30))
        self.pushButton_CardCloseAll.setFont(font1)

        self.gridLayout_24.addWidget(self.pushButton_CardCloseAll, 3, 0, 1, 2)


        self.gridLayout_22.addWidget(self.frame_15, 2, 0, 1, 1)


        self.gridLayout_34.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.frame_10)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 230))
        self.groupBox_4.setFont(font1)
        self.gridLayout_14 = QGridLayout(self.groupBox_4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, 0, -1, 6)
        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_14.addWidget(self.label_6, 1, 0, 1, 1)

        self.tableWidget_Sources = QTableWidget(self.groupBox_4)
        if (self.tableWidget_Sources.columnCount() < 3):
            self.tableWidget_Sources.setColumnCount(3)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(0, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(1, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(2, __qtablewidgetitem30)
        self.tableWidget_Sources.setObjectName(u"tableWidget_Sources")
        self.tableWidget_Sources.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Sources.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Sources.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_14.addWidget(self.tableWidget_Sources, 2, 0, 1, 2)

        self.comboBox_Scenes = QComboBox(self.groupBox_4)
        self.comboBox_Scenes.setObjectName(u"comboBox_Scenes")

        self.gridLayout_14.addWidget(self.comboBox_Scenes, 1, 1, 1, 1)

        self.frame_22 = QFrame(self.groupBox_4)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_22)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.pushButton_ObsConnect = QPushButton(self.frame_22)
        self.pushButton_ObsConnect.setObjectName(u"pushButton_ObsConnect")
        self.pushButton_ObsConnect.setMinimumSize(QSize(0, 30))
        self.pushButton_ObsConnect.setFont(font1)

        self.gridLayout_6.addWidget(self.pushButton_ObsConnect, 0, 0, 1, 1)

        self.pushButton_Obs_delete = QPushButton(self.frame_22)
        self.pushButton_Obs_delete.setObjectName(u"pushButton_Obs_delete")
        self.pushButton_Obs_delete.setMinimumSize(QSize(0, 30))
        self.pushButton_Obs_delete.setFont(font1)

        self.gridLayout_6.addWidget(self.pushButton_Obs_delete, 0, 1, 1, 1)

        self.pushButton_Obs2Table = QPushButton(self.frame_22)
        self.pushButton_Obs2Table.setObjectName(u"pushButton_Obs2Table")
        self.pushButton_Obs2Table.setMinimumSize(QSize(0, 30))
        self.pushButton_Obs2Table.setFont(font1)

        self.gridLayout_6.addWidget(self.pushButton_Obs2Table, 1, 0, 1, 1)

        self.pushButton_Source2Table = QPushButton(self.frame_22)
        self.pushButton_Source2Table.setObjectName(u"pushButton_Source2Table")
        self.pushButton_Source2Table.setMinimumSize(QSize(0, 30))
        self.pushButton_Source2Table.setFont(font1)

        self.gridLayout_6.addWidget(self.pushButton_Source2Table, 1, 1, 1, 1)


        self.gridLayout_14.addWidget(self.frame_22, 0, 0, 1, 2)


        self.gridLayout_34.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.textBrowser = QTextBrowser(self.frame_10)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setReadOnly(False)

        self.gridLayout_34.addWidget(self.textBrowser, 2, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.frame_10)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setFont(font1)
        self.gridLayout_18 = QGridLayout(self.groupBox_10)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.radioButton_noball = QRadioButton(self.groupBox_10)
        self.radioButton_noball.setObjectName(u"radioButton_noball")

        self.gridLayout_18.addWidget(self.radioButton_noball, 0, 0, 1, 1)

        self.radioButton_ball = QRadioButton(self.groupBox_10)
        self.radioButton_ball.setObjectName(u"radioButton_ball")
        self.radioButton_ball.setChecked(True)

        self.gridLayout_18.addWidget(self.radioButton_ball, 0, 1, 1, 1)

        self.checkBox_saveImgs = QCheckBox(self.groupBox_10)
        self.checkBox_saveImgs.setObjectName(u"checkBox_saveImgs")
        self.checkBox_saveImgs.setFont(font1)

        self.gridLayout_18.addWidget(self.checkBox_saveImgs, 0, 2, 1, 1)


        self.gridLayout_34.addWidget(self.groupBox_10, 3, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_10, 0, 1, 3, 1)

        self.tabWidget_Ranking.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_39 = QGridLayout(self.tab_2)
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.gridLayout_39.setContentsMargins(0, 0, 0, 0)
        self.widget_map_big = QWidget(self.tab_2)
        self.widget_map_big.setObjectName(u"widget_map_big")
        self.widget_map_big.setMinimumSize(QSize(860, 860))

        self.gridLayout_39.addWidget(self.widget_map_big, 0, 0, 1, 1)

        self.frame_21 = QFrame(self.tab_2)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMaximumSize(QSize(420, 16777215))
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_42 = QGridLayout(self.frame_21)
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.gridLayout_42.setContentsMargins(0, 0, 0, 0)
        self.groupBox_21 = QGroupBox(self.frame_21)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setMaximumSize(QSize(16777215, 150))
        self.groupBox_21.setFont(font1)
        self.gridLayout_45 = QGridLayout(self.groupBox_21)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.pushButton_del_camera = QPushButton(self.groupBox_21)
        self.pushButton_del_camera.setObjectName(u"pushButton_del_camera")

        self.gridLayout_45.addWidget(self.pushButton_del_camera, 0, 2, 1, 1)

        self.pushButton_add_camera = QPushButton(self.groupBox_21)
        self.pushButton_add_camera.setObjectName(u"pushButton_add_camera")

        self.gridLayout_45.addWidget(self.pushButton_add_camera, 0, 0, 1, 1)

        self.pushButton_save_camera = QPushButton(self.groupBox_21)
        self.pushButton_save_camera.setObjectName(u"pushButton_save_camera")

        self.gridLayout_45.addWidget(self.pushButton_save_camera, 0, 3, 1, 1)


        self.gridLayout_42.addWidget(self.groupBox_21, 1, 0, 1, 1)

        self.groupBox_22 = QGroupBox(self.frame_21)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setMinimumSize(QSize(0, 0))
        self.groupBox_22.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_22.setFont(font1)
        self.gridLayout_46 = QGridLayout(self.groupBox_22)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.gridLayout_46.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_add_Audio = QPushButton(self.groupBox_22)
        self.pushButton_add_Audio.setObjectName(u"pushButton_add_Audio")

        self.gridLayout_46.addWidget(self.pushButton_add_Audio, 2, 0, 1, 1)

        self.pushButton_del_Audio = QPushButton(self.groupBox_22)
        self.pushButton_del_Audio.setObjectName(u"pushButton_del_Audio")

        self.gridLayout_46.addWidget(self.pushButton_del_Audio, 2, 1, 1, 1)

        self.pushButton_save_Audio = QPushButton(self.groupBox_22)
        self.pushButton_save_Audio.setObjectName(u"pushButton_save_Audio")

        self.gridLayout_46.addWidget(self.pushButton_save_Audio, 2, 2, 1, 1)

        self.tableWidget_Audio = QTableWidget(self.groupBox_22)
        if (self.tableWidget_Audio.columnCount() < 4):
            self.tableWidget_Audio.setColumnCount(4)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(0, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(1, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(2, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(3, __qtablewidgetitem34)
        self.tableWidget_Audio.setObjectName(u"tableWidget_Audio")
        self.tableWidget_Audio.setMinimumSize(QSize(0, 0))
        self.tableWidget_Audio.setMaximumSize(QSize(500, 16777215))
        font5 = QFont()
        font5.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font5.setPointSize(12)
        font5.setBold(False)
        self.tableWidget_Audio.setFont(font5)
        self.tableWidget_Audio.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Audio.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Audio.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_46.addWidget(self.tableWidget_Audio, 3, 0, 1, 3)

        self.checkBox_main_music = QCheckBox(self.groupBox_22)
        self.checkBox_main_music.setObjectName(u"checkBox_main_music")
        self.checkBox_main_music.setFont(font1)

        self.gridLayout_46.addWidget(self.checkBox_main_music, 1, 0, 1, 1)

        self.frame_162 = QFrame(self.groupBox_22)
        self.frame_162.setObjectName(u"frame_162")
        self.gridLayout_50 = QGridLayout(self.frame_162)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.gridLayout_50.setContentsMargins(-1, 0, -1, 3)
        self.radioButton_music_1 = QRadioButton(self.frame_162)
        self.radioButton_music_1.setObjectName(u"radioButton_music_1")
        self.radioButton_music_1.setChecked(False)

        self.gridLayout_50.addWidget(self.radioButton_music_1, 0, 0, 1, 1)

        self.radioButton_music_2 = QRadioButton(self.frame_162)
        self.radioButton_music_2.setObjectName(u"radioButton_music_2")
        self.radioButton_music_2.setChecked(True)

        self.gridLayout_50.addWidget(self.radioButton_music_2, 0, 1, 1, 1)

        self.radioButton_music_3 = QRadioButton(self.frame_162)
        self.radioButton_music_3.setObjectName(u"radioButton_music_3")

        self.gridLayout_50.addWidget(self.radioButton_music_3, 0, 2, 1, 1)


        self.gridLayout_46.addWidget(self.frame_162, 1, 1, 1, 2)


        self.gridLayout_42.addWidget(self.groupBox_22, 2, 0, 1, 1)

        self.groupBox_19 = QGroupBox(self.frame_21)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setFont(font1)
        self.gridLayout_44 = QGridLayout(self.groupBox_19)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.pushButton_add_Ai = QPushButton(self.groupBox_19)
        self.pushButton_add_Ai.setObjectName(u"pushButton_add_Ai")

        self.gridLayout_44.addWidget(self.pushButton_add_Ai, 0, 0, 1, 1)

        self.pushButton_del_Ai = QPushButton(self.groupBox_19)
        self.pushButton_del_Ai.setObjectName(u"pushButton_del_Ai")

        self.gridLayout_44.addWidget(self.pushButton_del_Ai, 0, 1, 1, 1)

        self.pushButton_save_Ai = QPushButton(self.groupBox_19)
        self.pushButton_save_Ai.setObjectName(u"pushButton_save_Ai")

        self.gridLayout_44.addWidget(self.pushButton_save_Ai, 0, 2, 1, 1)

        self.tableWidget_Ai = QTableWidget(self.groupBox_19)
        if (self.tableWidget_Ai.columnCount() < 4):
            self.tableWidget_Ai.setColumnCount(4)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(0, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(1, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(2, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(3, __qtablewidgetitem38)
        self.tableWidget_Ai.setObjectName(u"tableWidget_Ai")
        self.tableWidget_Ai.setMinimumSize(QSize(0, 0))
        self.tableWidget_Ai.setMaximumSize(QSize(500, 380))
        self.tableWidget_Ai.setFont(font5)
        self.tableWidget_Ai.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Ai.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Ai.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_44.addWidget(self.tableWidget_Ai, 1, 0, 1, 3)


        self.gridLayout_42.addWidget(self.groupBox_19, 3, 0, 1, 1)

        self.groupBox_23 = QGroupBox(self.frame_21)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.groupBox_23.setMaximumSize(QSize(16777215, 150))
        self.groupBox_23.setFont(font1)
        self.gridLayout_49 = QGridLayout(self.groupBox_23)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.checkBox_show_ai = QCheckBox(self.groupBox_23)
        self.checkBox_show_ai.setObjectName(u"checkBox_show_ai")
        self.checkBox_show_ai.setFont(font1)
        self.checkBox_show_ai.setChecked(True)

        self.gridLayout_49.addWidget(self.checkBox_show_ai, 1, 3, 1, 1)

        self.checkBox_show_audio = QCheckBox(self.groupBox_23)
        self.checkBox_show_audio.setObjectName(u"checkBox_show_audio")
        self.checkBox_show_audio.setFont(font1)
        self.checkBox_show_audio.setChecked(True)

        self.gridLayout_49.addWidget(self.checkBox_show_audio, 1, 2, 1, 1)

        self.checkBox_show_orbit = QCheckBox(self.groupBox_23)
        self.checkBox_show_orbit.setObjectName(u"checkBox_show_orbit")
        self.checkBox_show_orbit.setFont(font1)

        self.gridLayout_49.addWidget(self.checkBox_show_orbit, 1, 0, 1, 1)

        self.checkBox_show_camera = QCheckBox(self.groupBox_23)
        self.checkBox_show_camera.setObjectName(u"checkBox_show_camera")
        self.checkBox_show_camera.setFont(font1)
        self.checkBox_show_camera.setChecked(True)

        self.gridLayout_49.addWidget(self.checkBox_show_camera, 1, 1, 1, 1)


        self.gridLayout_42.addWidget(self.groupBox_23, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.frame_21, 0, 1, 1, 1)

        self.tabWidget_Ranking.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_26 = QGridLayout(self.tab_3)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.tab_3)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 10))
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_40 = QGridLayout(self.frame_12)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.gridLayout_40.setContentsMargins(-1, 0, -1, 0)
        self.groupBox_5 = QGroupBox(self.frame_12)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 10))
        self.groupBox_5.setFont(font1)
        self.groupBox_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_15 = QGridLayout(self.groupBox_5)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_main_picture = QLabel(self.groupBox_5)
        self.label_main_picture.setObjectName(u"label_main_picture")
        self.label_main_picture.setMinimumSize(QSize(300, 10))

        self.gridLayout_15.addWidget(self.label_main_picture, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_5, 0, 0, 2, 1)

        self.groupBox_9 = QGroupBox(self.frame_12)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 10))
        self.groupBox_9.setFont(font1)
        self.groupBox_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_33 = QGridLayout(self.groupBox_9)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.label_monitor_picture = QLabel(self.groupBox_9)
        self.label_monitor_picture.setObjectName(u"label_monitor_picture")
        self.label_monitor_picture.setMinimumSize(QSize(300, 10))

        self.gridLayout_33.addWidget(self.label_monitor_picture, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_9, 0, 1, 2, 1)

        self.groupBox_8 = QGroupBox(self.frame_12)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(300, 10))
        self.groupBox_8.setMaximumSize(QSize(300, 16777215))
        self.groupBox_8.setFont(font1)
        self.gridLayout_28 = QGridLayout(self.groupBox_8)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.textBrowser_background_data = QTextBrowser(self.groupBox_8)
        self.textBrowser_background_data.setObjectName(u"textBrowser_background_data")
        self.textBrowser_background_data.setMinimumSize(QSize(0, 10))
        self.textBrowser_background_data.setFont(font4)
        self.textBrowser_background_data.setReadOnly(False)

        self.gridLayout_28.addWidget(self.textBrowser_background_data, 8, 0, 1, 2)

        self.widget_camera_sony = QWidget(self.groupBox_8)
        self.widget_camera_sony.setObjectName(u"widget_camera_sony")
        self.widget_camera_sony.setMinimumSize(QSize(200, 38))

        self.gridLayout_28.addWidget(self.widget_camera_sony, 0, 1, 1, 1)

        self.lineEdit_result_send = QLineEdit(self.groupBox_8)
        self.lineEdit_result_send.setObjectName(u"lineEdit_result_send")
        self.lineEdit_result_send.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.lineEdit_result_send, 3, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.label_9, 0, 0, 1, 1)

        self.widget_camera_monitor = QWidget(self.groupBox_8)
        self.widget_camera_monitor.setObjectName(u"widget_camera_monitor")
        self.widget_camera_monitor.setMinimumSize(QSize(200, 38))

        self.gridLayout_28.addWidget(self.widget_camera_monitor, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.label_10, 1, 0, 1, 1)

        self.widget_camera_fit = QWidget(self.groupBox_8)
        self.widget_camera_fit.setObjectName(u"widget_camera_fit")
        self.widget_camera_fit.setMinimumSize(QSize(200, 38))

        self.gridLayout_28.addWidget(self.widget_camera_fit, 2, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox_8)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.label_11, 2, 0, 1, 1)

        self.pushButton_test_2 = QPushButton(self.groupBox_8)
        self.pushButton_test_2.setObjectName(u"pushButton_test_2")
        self.pushButton_test_2.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.pushButton_test_2, 6, 0, 1, 2)

        self.checkBox_ShowUdp = QCheckBox(self.groupBox_8)
        self.checkBox_ShowUdp.setObjectName(u"checkBox_ShowUdp")
        self.checkBox_ShowUdp.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.checkBox_ShowUdp, 7, 0, 1, 2)

        self.label_16 = QLabel(self.groupBox_8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 10))

        self.gridLayout_28.addWidget(self.label_16, 3, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_8, 0, 2, 1, 1)

        self.groupBox_12 = QGroupBox(self.frame_12)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(0, 10))
        self.groupBox_12.setFont(font1)
        self.gridLayout_31 = QGridLayout(self.groupBox_12)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_Draw = QPushButton(self.groupBox_12)
        self.pushButton_Draw.setObjectName(u"pushButton_Draw")
        self.pushButton_Draw.setMinimumSize(QSize(0, 25))

        self.gridLayout_31.addWidget(self.pushButton_Draw, 0, 0, 1, 1)

        self.pushButton_to_TXT = QPushButton(self.groupBox_12)
        self.pushButton_to_TXT.setObjectName(u"pushButton_to_TXT")
        self.pushButton_to_TXT.setMinimumSize(QSize(0, 25))

        self.gridLayout_31.addWidget(self.pushButton_to_TXT, 0, 1, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_12, 1, 2, 1, 1)


        self.gridLayout_26.addWidget(self.frame_12, 1, 0, 1, 1)

        self.frame_11 = QFrame(self.tab_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 10))
        self.frame_11.setMaximumSize(QSize(16777215, 420))
        self.gridLayout_27 = QGridLayout(self.frame_11)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(-1, 0, -1, 0)
        self.groupBox_14 = QGroupBox(self.frame_11)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(0, 10))
        self.groupBox_14.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_14.setFont(font1)
        self.gridLayout_37 = QGridLayout(self.groupBox_14)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.gridLayout_37.setContentsMargins(0, -1, 0, -1)
        self.widget_map = QWidget(self.groupBox_14)
        self.widget_map.setObjectName(u"widget_map")
        self.widget_map.setMinimumSize(QSize(350, 350))

        self.gridLayout_37.addWidget(self.widget_map, 0, 0, 1, 1)


        self.gridLayout_27.addWidget(self.groupBox_14, 0, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.frame_11)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(0, 10))
        self.groupBox_7.setMaximumSize(QSize(500, 16777215))
        self.groupBox_7.setFont(font1)
        self.gridLayout_4 = QGridLayout(self.groupBox_7)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tableWidget_Ranking = QTableWidget(self.groupBox_7)
        if (self.tableWidget_Ranking.columnCount() < 5):
            self.tableWidget_Ranking.setColumnCount(5)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(0, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(1, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(2, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(3, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(4, __qtablewidgetitem43)
        self.tableWidget_Ranking.setObjectName(u"tableWidget_Ranking")
        self.tableWidget_Ranking.setMinimumSize(QSize(330, 10))
        self.tableWidget_Ranking.setMaximumSize(QSize(500, 16777215))
        self.tableWidget_Ranking.setFont(font5)
        self.tableWidget_Ranking.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Ranking.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Ranking.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_4.addWidget(self.tableWidget_Ranking, 0, 0, 1, 1)


        self.gridLayout_27.addWidget(self.groupBox_7, 0, 1, 1, 1)

        self.groupBox_20 = QGroupBox(self.frame_11)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setMinimumSize(QSize(300, 10))
        self.groupBox_20.setMaximumSize(QSize(200, 16777215))
        self.groupBox_20.setFont(font1)
        self.gridLayout_29 = QGridLayout(self.groupBox_20)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.groupBox_11 = QGroupBox(self.groupBox_20)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setMinimumSize(QSize(0, 10))
        self.groupBox_11.setMaximumSize(QSize(16777215, 180))
        self.gridLayout_30 = QGridLayout(self.groupBox_11)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(-1, 0, -1, 0)
        self.label_15 = QLabel(self.groupBox_11)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_15, 2, 0, 1, 1)

        self.pushButton_save_Ranking = QPushButton(self.groupBox_11)
        self.pushButton_save_Ranking.setObjectName(u"pushButton_save_Ranking")
        self.pushButton_save_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.pushButton_save_Ranking, 4, 0, 1, 4)

        self.lineEdit_area_Ranking = QLineEdit(self.groupBox_11)
        self.lineEdit_area_Ranking.setObjectName(u"lineEdit_area_Ranking")
        self.lineEdit_area_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_area_Ranking, 1, 2, 1, 2)

        self.lineEdit_lap_Ranking = QLineEdit(self.groupBox_11)
        self.lineEdit_lap_Ranking.setObjectName(u"lineEdit_lap_Ranking")
        self.lineEdit_lap_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_lap_Ranking, 3, 2, 1, 2)

        self.lineEdit_Time_Restart_Ranking = QLineEdit(self.groupBox_11)
        self.lineEdit_Time_Restart_Ranking.setObjectName(u"lineEdit_Time_Restart_Ranking")
        self.lineEdit_Time_Restart_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_Time_Restart_Ranking, 2, 2, 1, 2)

        self.label_13 = QLabel(self.groupBox_11)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_11)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_14, 3, 0, 1, 1)

        self.pushButton_reset_Ranking = QPushButton(self.groupBox_11)
        self.pushButton_reset_Ranking.setObjectName(u"pushButton_reset_Ranking")
        self.pushButton_reset_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.pushButton_reset_Ranking, 0, 0, 1, 4)


        self.gridLayout_29.addWidget(self.groupBox_11, 0, 0, 1, 1)

        self.groupBox_18 = QGroupBox(self.groupBox_20)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setMinimumSize(QSize(0, 10))
        self.groupBox_18.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_18.setFont(font1)
        self.gridLayout_48 = QGridLayout(self.groupBox_18)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.groupBox_25 = QGroupBox(self.groupBox_18)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setMinimumSize(QSize(0, 10))
        self.gridLayout_41 = QGridLayout(self.groupBox_25)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.gridLayout_41.setContentsMargins(-1, 0, -1, 0)
        self.label_42 = QLabel(self.groupBox_25)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(0, 10))
        self.label_42.setFont(font1)

        self.gridLayout_41.addWidget(self.label_42, 0, 5, 1, 1)

        self.label_27 = QLabel(self.groupBox_25)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(0, 10))
        self.label_27.setMaximumSize(QSize(120, 16777215))
        self.label_27.setFont(font1)

        self.gridLayout_41.addWidget(self.label_27, 0, 2, 1, 1)

        self.checkBox_restart = QCheckBox(self.groupBox_25)
        self.checkBox_restart.setObjectName(u"checkBox_restart")
        self.checkBox_restart.setMinimumSize(QSize(80, 10))
        self.checkBox_restart.setFont(font1)

        self.gridLayout_41.addWidget(self.checkBox_restart, 0, 0, 1, 1)

        self.lineEdit_time = QLineEdit(self.groupBox_25)
        self.lineEdit_time.setObjectName(u"lineEdit_time")
        self.lineEdit_time.setMinimumSize(QSize(0, 10))
        self.lineEdit_time.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_time.setFont(font1)
        self.lineEdit_time.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.lineEdit_time.setReadOnly(True)

        self.gridLayout_41.addWidget(self.lineEdit_time, 0, 3, 1, 1)

        self.frame_30 = QFrame(self.groupBox_25)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setMinimumSize(QSize(20, 10))
        self.frame_30.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_41.addWidget(self.frame_30, 0, 1, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_25, 0, 0, 1, 1)

        self.groupBox_27 = QGroupBox(self.groupBox_18)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setMinimumSize(QSize(0, 10))
        self.gridLayout_47 = QGridLayout(self.groupBox_27)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.label_28 = QLabel(self.groupBox_27)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 10))
        self.label_28.setFont(font1)

        self.gridLayout_47.addWidget(self.label_28, 0, 0, 1, 1)

        self.lineEdit_time_send_result = QLineEdit(self.groupBox_27)
        self.lineEdit_time_send_result.setObjectName(u"lineEdit_time_send_result")
        self.lineEdit_time_send_result.setMinimumSize(QSize(0, 10))
        self.lineEdit_time_send_result.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_47.addWidget(self.lineEdit_time_send_result, 0, 1, 1, 1)

        self.label_29 = QLabel(self.groupBox_27)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(0, 10))
        self.label_29.setFont(font1)

        self.gridLayout_47.addWidget(self.label_29, 0, 2, 1, 1)

        self.pushButton_CardRun_2 = QPushButton(self.groupBox_27)
        self.pushButton_CardRun_2.setObjectName(u"pushButton_CardRun_2")
        self.pushButton_CardRun_2.setMinimumSize(QSize(0, 10))
        self.pushButton_CardRun_2.setFont(font1)

        self.gridLayout_47.addWidget(self.pushButton_CardRun_2, 0, 3, 2, 1)

        self.label_41 = QLabel(self.groupBox_27)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(0, 10))
        self.label_41.setFont(font1)

        self.gridLayout_47.addWidget(self.label_41, 1, 0, 1, 1)

        self.lineEdit_time_count_ball = QLineEdit(self.groupBox_27)
        self.lineEdit_time_count_ball.setObjectName(u"lineEdit_time_count_ball")
        self.lineEdit_time_count_ball.setMinimumSize(QSize(0, 10))
        self.lineEdit_time_count_ball.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_47.addWidget(self.lineEdit_time_count_ball, 1, 1, 1, 1)

        self.label_40 = QLabel(self.groupBox_27)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(0, 10))
        self.label_40.setFont(font1)

        self.gridLayout_47.addWidget(self.label_40, 1, 2, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_27, 1, 0, 1, 1)

        self.groupBox_24 = QGroupBox(self.groupBox_18)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMinimumSize(QSize(0, 10))
        self.gridLayout_43 = QGridLayout(self.groupBox_24)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.lineEdit_ball_num = QLineEdit(self.groupBox_24)
        self.lineEdit_ball_num.setObjectName(u"lineEdit_ball_num")
        self.lineEdit_ball_num.setMinimumSize(QSize(50, 10))
        self.lineEdit_ball_num.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_ball_num.setFont(font1)
        self.lineEdit_ball_num.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.lineEdit_ball_num.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_ball_num, 0, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_24)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 10))
        self.label_7.setMaximumSize(QSize(150, 16777215))
        self.label_7.setFont(font1)

        self.gridLayout_43.addWidget(self.label_7, 0, 0, 1, 1)

        self.frame_28 = QFrame(self.groupBox_24)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMinimumSize(QSize(100, 10))
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_43.addWidget(self.frame_28, 0, 2, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_24, 2, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_18, 1, 0, 1, 1)


        self.gridLayout_27.addWidget(self.groupBox_20, 0, 3, 1, 1)


        self.gridLayout_26.addWidget(self.frame_11, 0, 0, 1, 1)

        self.tabWidget_Ranking.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_36 = QGridLayout(self.tab_4)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.gridLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_24 = QFrame(self.tab_4)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMaximumSize(QSize(500, 16777215))
        self.frame_24.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_54 = QGridLayout(self.frame_24)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.gridLayout_54.setContentsMargins(0, 0, -1, -1)
        self.groupBox_26 = QGroupBox(self.frame_24)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.groupBox_26.setMinimumSize(QSize(0, 0))
        self.groupBox_26.setMaximumSize(QSize(600, 150))
        self.groupBox_26.setFont(font1)
        self.gridLayout_53 = QGridLayout(self.groupBox_26)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.lineEdit_music_3 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_3.setObjectName(u"lineEdit_music_3")
        self.lineEdit_music_3.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_3.setFont(font4)

        self.gridLayout_53.addWidget(self.lineEdit_music_3, 4, 1, 1, 2)

        self.radioButton_music_background_2 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_2.setObjectName(u"radioButton_music_background_2")
        self.radioButton_music_background_2.setFont(font5)
        self.radioButton_music_background_2.setChecked(True)

        self.gridLayout_53.addWidget(self.radioButton_music_background_2, 3, 0, 1, 1)

        self.lineEdit_music_2 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_2.setObjectName(u"lineEdit_music_2")
        self.lineEdit_music_2.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_2.setFont(font4)
        self.lineEdit_music_2.setReadOnly(True)

        self.gridLayout_53.addWidget(self.lineEdit_music_2, 3, 1, 1, 2)

        self.radioButton_music_background_1 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_1.setObjectName(u"radioButton_music_background_1")
        self.radioButton_music_background_1.setFont(font5)

        self.gridLayout_53.addWidget(self.radioButton_music_background_1, 2, 0, 1, 1)

        self.lineEdit_music_1 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_1.setObjectName(u"lineEdit_music_1")
        self.lineEdit_music_1.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_1.setFont(font4)
        self.lineEdit_music_1.setReadOnly(True)

        self.gridLayout_53.addWidget(self.lineEdit_music_1, 2, 1, 1, 2)

        self.radioButton_music_background_3 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_3.setObjectName(u"radioButton_music_background_3")
        self.radioButton_music_background_3.setFont(font5)

        self.gridLayout_53.addWidget(self.radioButton_music_background_3, 4, 0, 1, 1)


        self.gridLayout_54.addWidget(self.groupBox_26, 0, 0, 1, 1)

        self.groupBox_28 = QGroupBox(self.frame_24)
        self.groupBox_28.setObjectName(u"groupBox_28")

        self.gridLayout_54.addWidget(self.groupBox_28, 1, 0, 1, 1)


        self.gridLayout_36.addWidget(self.frame_24, 0, 1, 2, 1)

        self.frame_20 = QFrame(self.tab_4)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMaximumSize(QSize(600, 16777215))
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_51 = QGridLayout(self.frame_20)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.gridLayout_51.setContentsMargins(-1, 0, -1, -1)
        self.groupBox_17 = QGroupBox(self.frame_20)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setMinimumSize(QSize(0, 0))
        self.groupBox_17.setMaximumSize(QSize(600, 150))
        self.groupBox_17.setFont(font1)
        self.gridLayout_35 = QGridLayout(self.groupBox_17)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.lineEdit_cardNo = QLineEdit(self.groupBox_17)
        self.lineEdit_cardNo.setObjectName(u"lineEdit_cardNo")
        self.lineEdit_cardNo.setFont(font4)
        self.lineEdit_cardNo.setReadOnly(True)

        self.gridLayout_35.addWidget(self.lineEdit_cardNo, 0, 2, 1, 1)

        self.label_33 = QLabel(self.groupBox_17)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font5)

        self.gridLayout_35.addWidget(self.label_33, 0, 0, 1, 2)

        self.lineEdit_s485_Axis_No = QLineEdit(self.groupBox_17)
        self.lineEdit_s485_Axis_No.setObjectName(u"lineEdit_s485_Axis_No")
        self.lineEdit_s485_Axis_No.setFont(font4)
        self.lineEdit_s485_Axis_No.setReadOnly(True)

        self.gridLayout_35.addWidget(self.lineEdit_s485_Axis_No, 1, 2, 1, 1)

        self.label_36 = QLabel(self.groupBox_17)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font5)

        self.gridLayout_35.addWidget(self.label_36, 1, 0, 1, 2)

        self.label_38 = QLabel(self.groupBox_17)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font5)

        self.gridLayout_35.addWidget(self.label_38, 2, 0, 1, 2)

        self.lineEdit_s485_Cam_No = QLineEdit(self.groupBox_17)
        self.lineEdit_s485_Cam_No.setObjectName(u"lineEdit_s485_Cam_No")
        self.lineEdit_s485_Cam_No.setFont(font4)

        self.gridLayout_35.addWidget(self.lineEdit_s485_Cam_No, 2, 2, 1, 2)


        self.gridLayout_51.addWidget(self.groupBox_17, 2, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.frame_20)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMinimumSize(QSize(0, 0))
        self.groupBox_13.setMaximumSize(QSize(600, 200))
        self.groupBox_13.setFont(font1)
        self.gridLayout_32 = QGridLayout(self.groupBox_13)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.label_17 = QLabel(self.groupBox_13)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font5)

        self.gridLayout_32.addWidget(self.label_17, 0, 0, 1, 2)

        self.lineEdit_UdpServer_ip = QLineEdit(self.groupBox_13)
        self.lineEdit_UdpServer_ip.setObjectName(u"lineEdit_UdpServer_ip")
        self.lineEdit_UdpServer_ip.setFont(font4)
        self.lineEdit_UdpServer_ip.setReadOnly(True)

        self.gridLayout_32.addWidget(self.lineEdit_UdpServer_ip, 0, 2, 1, 1)

        self.label_19 = QLabel(self.groupBox_13)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font5)

        self.gridLayout_32.addWidget(self.label_19, 0, 3, 1, 1)

        self.lineEdit_UdpServer_Port = QLineEdit(self.groupBox_13)
        self.lineEdit_UdpServer_Port.setObjectName(u"lineEdit_UdpServer_Port")
        self.lineEdit_UdpServer_Port.setFont(font4)

        self.gridLayout_32.addWidget(self.lineEdit_UdpServer_Port, 0, 4, 1, 1)

        self.label_31 = QLabel(self.groupBox_13)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font5)

        self.gridLayout_32.addWidget(self.label_31, 1, 0, 1, 2)

        self.lineEdit_TcpServer_ip = QLineEdit(self.groupBox_13)
        self.lineEdit_TcpServer_ip.setObjectName(u"lineEdit_TcpServer_ip")
        self.lineEdit_TcpServer_ip.setFont(font4)
        self.lineEdit_TcpServer_ip.setReadOnly(True)

        self.gridLayout_32.addWidget(self.lineEdit_TcpServer_ip, 1, 2, 1, 1)

        self.label_30 = QLabel(self.groupBox_13)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font5)

        self.gridLayout_32.addWidget(self.label_30, 1, 3, 1, 1)

        self.lineEdit_TcpServer_Port = QLineEdit(self.groupBox_13)
        self.lineEdit_TcpServer_Port.setObjectName(u"lineEdit_TcpServer_Port")
        self.lineEdit_TcpServer_Port.setFont(font4)

        self.gridLayout_32.addWidget(self.lineEdit_TcpServer_Port, 1, 4, 1, 1)

        self.label_34 = QLabel(self.groupBox_13)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font5)

        self.gridLayout_32.addWidget(self.label_34, 2, 0, 1, 2)

        self.lineEdit_wakeup_addr = QLineEdit(self.groupBox_13)
        self.lineEdit_wakeup_addr.setObjectName(u"lineEdit_wakeup_addr")
        self.lineEdit_wakeup_addr.setFont(font4)

        self.gridLayout_32.addWidget(self.lineEdit_wakeup_addr, 2, 2, 1, 3)

        self.label_32 = QLabel(self.groupBox_13)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font5)

        self.gridLayout_32.addWidget(self.label_32, 3, 0, 1, 1)

        self.lineEdit_rtsp_url = QLineEdit(self.groupBox_13)
        self.lineEdit_rtsp_url.setObjectName(u"lineEdit_rtsp_url")
        self.lineEdit_rtsp_url.setFont(font4)

        self.gridLayout_32.addWidget(self.lineEdit_rtsp_url, 3, 1, 1, 4)


        self.gridLayout_51.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.groupBox_16 = QGroupBox(self.frame_20)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setFont(font1)
        self.gridLayout_38 = QGridLayout(self.groupBox_16)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.lineEdit_balls_count = QLineEdit(self.groupBox_16)
        self.lineEdit_balls_count.setObjectName(u"lineEdit_balls_count")
        self.lineEdit_balls_count.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_balls_count.setFont(font4)
        self.lineEdit_balls_count.setReadOnly(True)

        self.gridLayout_38.addWidget(self.lineEdit_balls_count, 0, 1, 1, 1)

        self.label_35 = QLabel(self.groupBox_16)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font5)

        self.gridLayout_38.addWidget(self.label_35, 0, 0, 1, 1)

        self.frame_25 = QFrame(self.groupBox_16)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(300, 0))
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_38.addWidget(self.frame_25, 0, 2, 1, 1)

        self.groupBox_15 = QGroupBox(self.groupBox_16)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMaximumSize(QSize(600, 600))
        self.groupBox_15.setFont(font1)
        self.gridLayout_52 = QGridLayout(self.groupBox_15)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.label_62 = QLabel(self.groupBox_15)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font5)

        self.gridLayout_52.addWidget(self.label_62, 9, 5, 1, 1)

        self.lineEdit_Color_Eng_5 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_5.setObjectName(u"lineEdit_Color_Eng_5")
        self.lineEdit_Color_Eng_5.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_5.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_5.setFont(font4)
        self.lineEdit_Color_Eng_5.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_5, 5, 2, 1, 1)

        self.lineEdit_Color_Ch_3 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_3.setObjectName(u"lineEdit_Color_Ch_3")
        self.lineEdit_Color_Ch_3.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_3.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_3, 3, 7, 1, 2)

        self.lineEdit_Color_Eng_4 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_4.setObjectName(u"lineEdit_Color_Eng_4")
        self.lineEdit_Color_Eng_4.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_4.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_4.setFont(font4)
        self.lineEdit_Color_Eng_4.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_4, 4, 2, 1, 2)

        self.label_63 = QLabel(self.groupBox_15)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font5)

        self.gridLayout_52.addWidget(self.label_63, 9, 0, 1, 1)

        self.lineEdit_Color_Eng_3 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_3.setObjectName(u"lineEdit_Color_Eng_3")
        self.lineEdit_Color_Eng_3.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_3.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_3.setFont(font4)
        self.lineEdit_Color_Eng_3.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_3, 3, 2, 1, 1)

        self.label_64 = QLabel(self.groupBox_15)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFont(font5)

        self.gridLayout_52.addWidget(self.label_64, 10, 5, 1, 1)

        self.label_59 = QLabel(self.groupBox_15)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font5)

        self.gridLayout_52.addWidget(self.label_59, 6, 0, 1, 1)

        self.lineEdit_Color_Eng_10 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_10.setObjectName(u"lineEdit_Color_Eng_10")
        self.lineEdit_Color_Eng_10.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_10.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_10.setFont(font4)
        self.lineEdit_Color_Eng_10.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_10, 10, 2, 1, 1)

        self.lineEdit_Color_Eng_8 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_8.setObjectName(u"lineEdit_Color_Eng_8")
        self.lineEdit_Color_Eng_8.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_8.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_8.setFont(font4)
        self.lineEdit_Color_Eng_8.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_8, 8, 2, 1, 1)

        self.lineEdit_Color_Ch_2 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_2.setObjectName(u"lineEdit_Color_Ch_2")
        self.lineEdit_Color_Ch_2.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_2.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_2, 2, 7, 1, 2)

        self.label_56 = QLabel(self.groupBox_15)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFont(font5)

        self.gridLayout_52.addWidget(self.label_56, 8, 0, 1, 2)

        self.label_39 = QLabel(self.groupBox_15)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font5)

        self.gridLayout_52.addWidget(self.label_39, 3, 5, 1, 1)

        self.label_37 = QLabel(self.groupBox_15)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font5)

        self.gridLayout_52.addWidget(self.label_37, 3, 0, 1, 1)

        self.label_55 = QLabel(self.groupBox_15)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font5)

        self.gridLayout_52.addWidget(self.label_55, 8, 5, 1, 1)

        self.label_50 = QLabel(self.groupBox_15)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font5)

        self.gridLayout_52.addWidget(self.label_50, 0, 0, 1, 1)

        self.lineEdit_Color_Eng_1 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_1.setObjectName(u"lineEdit_Color_Eng_1")
        self.lineEdit_Color_Eng_1.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_1.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_1.setFont(font4)
        self.lineEdit_Color_Eng_1.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_1, 0, 2, 1, 2)

        self.label_44 = QLabel(self.groupBox_15)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font5)

        self.gridLayout_52.addWidget(self.label_44, 4, 0, 1, 1)

        self.lineEdit_Color_Eng_2 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_2.setObjectName(u"lineEdit_Color_Eng_2")
        self.lineEdit_Color_Eng_2.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_2.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_2.setFont(font4)
        self.lineEdit_Color_Eng_2.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_2, 2, 2, 1, 1)

        self.label_57 = QLabel(self.groupBox_15)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font5)

        self.gridLayout_52.addWidget(self.label_57, 6, 5, 1, 1)

        self.lineEdit_Color_Eng_7 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_7.setObjectName(u"lineEdit_Color_Eng_7")
        self.lineEdit_Color_Eng_7.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_7.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_7.setFont(font4)
        self.lineEdit_Color_Eng_7.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_7, 7, 2, 1, 1)

        self.label_52 = QLabel(self.groupBox_15)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font5)

        self.gridLayout_52.addWidget(self.label_52, 2, 0, 1, 1)

        self.lineEdit_Color_Ch_1 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_1.setObjectName(u"lineEdit_Color_Ch_1")
        self.lineEdit_Color_Ch_1.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_1.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_1, 0, 7, 1, 2)

        self.label_61 = QLabel(self.groupBox_15)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFont(font5)

        self.gridLayout_52.addWidget(self.label_61, 10, 0, 1, 1)

        self.label_54 = QLabel(self.groupBox_15)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font5)

        self.gridLayout_52.addWidget(self.label_54, 7, 0, 1, 2)

        self.label_53 = QLabel(self.groupBox_15)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font5)

        self.gridLayout_52.addWidget(self.label_53, 7, 5, 1, 1)

        self.lineEdit_Color_Eng_6 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_6.setObjectName(u"lineEdit_Color_Eng_6")
        self.lineEdit_Color_Eng_6.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_6.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_6.setFont(font4)
        self.lineEdit_Color_Eng_6.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_6, 6, 2, 1, 1)

        self.label_51 = QLabel(self.groupBox_15)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font5)

        self.gridLayout_52.addWidget(self.label_51, 2, 5, 1, 1)

        self.lineEdit_Color_Eng_9 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_9.setObjectName(u"lineEdit_Color_Eng_9")
        self.lineEdit_Color_Eng_9.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_9.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_9.setFont(font4)
        self.lineEdit_Color_Eng_9.setReadOnly(True)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_9, 9, 2, 1, 1)

        self.label_49 = QLabel(self.groupBox_15)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font5)

        self.gridLayout_52.addWidget(self.label_49, 0, 5, 1, 1)

        self.label_60 = QLabel(self.groupBox_15)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font5)

        self.gridLayout_52.addWidget(self.label_60, 5, 0, 1, 2)

        self.label_58 = QLabel(self.groupBox_15)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setFont(font5)

        self.gridLayout_52.addWidget(self.label_58, 5, 5, 1, 1)

        self.label_43 = QLabel(self.groupBox_15)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font5)

        self.gridLayout_52.addWidget(self.label_43, 4, 5, 1, 2)

        self.lineEdit_Color_Ch_4 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_4.setObjectName(u"lineEdit_Color_Ch_4")
        self.lineEdit_Color_Ch_4.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_4.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_4, 4, 7, 1, 2)

        self.lineEdit_Color_Ch_5 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_5.setObjectName(u"lineEdit_Color_Ch_5")
        self.lineEdit_Color_Ch_5.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_5.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_5, 5, 7, 1, 2)

        self.lineEdit_Color_Ch_6 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_6.setObjectName(u"lineEdit_Color_Ch_6")
        self.lineEdit_Color_Ch_6.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_6.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_6, 6, 7, 1, 2)

        self.lineEdit_Color_Ch_7 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_7.setObjectName(u"lineEdit_Color_Ch_7")
        self.lineEdit_Color_Ch_7.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_7.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_7, 7, 7, 1, 2)

        self.lineEdit_Color_Ch_8 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_8.setObjectName(u"lineEdit_Color_Ch_8")
        self.lineEdit_Color_Ch_8.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_8.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_8, 8, 7, 1, 2)

        self.lineEdit_Color_Ch_9 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_9.setObjectName(u"lineEdit_Color_Ch_9")
        self.lineEdit_Color_Ch_9.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_9.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_9, 9, 7, 1, 2)

        self.lineEdit_Color_Ch_10 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_10.setObjectName(u"lineEdit_Color_Ch_10")
        self.lineEdit_Color_Ch_10.setMinimumSize(QSize(350, 0))
        self.lineEdit_Color_Ch_10.setFont(font4)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_10, 10, 7, 1, 2)


        self.gridLayout_38.addWidget(self.groupBox_15, 1, 0, 1, 4)

        self.pushButton_Save_Ball = QPushButton(self.groupBox_16)
        self.pushButton_Save_Ball.setObjectName(u"pushButton_Save_Ball")

        self.gridLayout_38.addWidget(self.pushButton_Save_Ball, 0, 3, 1, 1)


        self.gridLayout_51.addWidget(self.groupBox_16, 3, 0, 1, 1)


        self.gridLayout_36.addWidget(self.frame_20, 0, 0, 2, 1)

        self.frame_27 = QFrame(self.tab_4)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_36.addWidget(self.frame_27, 0, 2, 2, 1)

        self.tabWidget_Ranking.addTab(self.tab_4, "")

        self.gridLayout.addWidget(self.tabWidget_Ranking, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget_Ranking.setCurrentIndex(4)
        self.pushButton.setDefault(True)
        self.pushButton_add.setDefault(True)
        self.pushButton_save.setDefault(True)
        self.pushButton_update.setDefault(True)
        self.pushButton_once.setDefault(True)
        self.pushButton_start.setDefault(True)
        self.pushButton_2.setDefault(True)
        self.pushButton_3.setDefault(True)
        self.pushButton_add_4.setDefault(True)
        self.pushButton_save_12.setDefault(True)
        self.pushButton_update_12.setDefault(True)
        self.pushButton_rename.setDefault(True)
        self.pushButton_fsave.setDefault(True)
        self.pushButton_ToTable.setDefault(True)
        self.pushButton_CardRun.setDefault(True)
        self.pushButton_CardStop.setDefault(True)
        self.pushButton_CardStart.setDefault(True)
        self.pushButton_CardReset.setDefault(True)
        self.pushButton_CardNext.setDefault(True)
        self.pushButton_CardCloseAll.setDefault(True)
        self.pushButton_ObsConnect.setDefault(True)
        self.pushButton_Obs_delete.setDefault(True)
        self.pushButton_Obs2Table.setDefault(True)
        self.pushButton_Source2Table.setDefault(True)
        self.pushButton_CardRun_2.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e2d\u63a7", None))
        ___qtablewidgetitem = self.tableWidget_Results.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u671f\u53f7", None));
        ___qtablewidgetitem1 = self.tableWidget_Results.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u8dd1\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget_Results.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u5012\u6570", None));
        ___qtablewidgetitem3 = self.tableWidget_Results.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtablewidgetitem4 = self.tableWidget_Results.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u8d5b\u679c", None));
        ___qtablewidgetitem5 = self.tableWidget_Results.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4\u8d5b\u679c", None));
        ___qtablewidgetitem6 = self.tableWidget_Results.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None));
        ___qtablewidgetitem7 = self.tableWidget_Results.horizontalHeaderItem(8)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u5f55\u50cf", None));
        ___qtablewidgetitem8 = self.tableWidget_Results.horizontalHeaderItem(9)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u590d\u76d8", None));
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u76d8\u53e3\u72b6\u6001", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u76d8", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"\u5c01\u76d8", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u62df", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u9ed1\u5c4f", None))
        self.groupBox_status.setTitle(QCoreApplication.translate("MainWindow", u"\u72b6\u60011", None))
        self.status_live.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u64ad\u72b6\u6001", None))
        self.status_road.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u9053\u72b6\u6001", None))
        self.status_lenses.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934\u72b6\u6001", None))
        self.status_track.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u9053\u72b6\u6001", None))
        self.groupBox_status_2.setTitle(QCoreApplication.translate("MainWindow", u"\u72b6\u60012", None))
        self.status_server1.setText(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u670d\u52a1\u5668", None))
        self.status_server2.setText(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u670d\u52a1\u56682", None))
        self.status_sportsCards.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361", None))
        self.status_obs.setText(QCoreApplication.translate("MainWindow", u"OBS\u72b6\u6001", None))
        self.status_mainlenses.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u955c\u5934", None))
        self.status_Recognition.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8bc6\u522b1", None))
        self.status_Extension.setText(QCoreApplication.translate("MainWindow", u"\u5206\u673a1", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u8d77\u70b9\u8bc6\u522b", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5c40\u7ed3\u675f\u540e\u81ea\u52a8\u9ed1\u5c4f", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u8d77\u4e8c\u6b21\u6392\u540d", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5c40\u7ed3\u675f\u540e\u81ea\u52a8\u5c01\u76d8", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\u4e00\u5f39\u5c04", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\u5173\u8b66\u62a5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u9501\u5b9a\u671f\u53f7", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7c92", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\u73e0\u5b50\u6570\u91cf\uff1a", None))
        self.pushButton_add_3.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u9053\u505c\u6b62", None))
        self.pushButton_start_2.setText(QCoreApplication.translate("MainWindow", u"\u6536\u5de5", None))
        self.pushButton_add_2.setText(QCoreApplication.translate("MainWindow", u"\u5361\u73e0", None))
        self.pushButton_save_2.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_update_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_save_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_update_3.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_save_4.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_update_5.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_save_5.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_update_4.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_save_6.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_update_6.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pushButton_once_2.setText(QCoreApplication.translate("MainWindow", u"\u98de\u73e0", None))
        self.pushButton_save_7.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_update_10.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_save_11.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_update_9.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_save_8.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_update_11.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_save_9.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_update_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_save_10.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_update_7.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pushButton_add.setText(QCoreApplication.translate("MainWindow", u"\u51c6\u5907", None))
        self.pushButton_save.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.pushButton_update.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u5173", None))
        self.pushButton_once.setText(QCoreApplication.translate("MainWindow", u"\u6536\u73e0", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u679c\u786e\u8ba4 \u8bc6\u522b\u72b6\u6001", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u6444\u50cf\u673a\uff1a  ", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u9009", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u540e\u5907\u6444\u50cf\u673a\uff1a", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u9009", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8", None))
        self.pushButton_add_4.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u8d5b\u679c", None))
        self.pushButton_save_12.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88\u5f53\u5c40", None))
        self.pushButton_update_12.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u8bc6\u522b", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_0), QCoreApplication.translate("MainWindow", u"\u76f4\u64ad\u5927\u5385", None))
        self.checkBox_test.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u6a21\u5f0f", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u65b9\u6848\uff1a", None))
        self.pushButton_rename.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u547d\u540d\u65b9\u6848", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u6848\u540d\u79f0\uff1a", None))
        self.pushButton_fsave.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u65b9\u6848", None))
        self.checkBox_selectall.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
        self.checkBox_follow.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u8ddf\u8e2a", None))
        ___qtablewidgetitem9 = self.tableWidget_Step.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u5708\u6570", None));
        ___qtablewidgetitem10 = self.tableWidget_Step.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u53f3", None));
        ___qtablewidgetitem11 = self.tableWidget_Step.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u524d\u540e", None));
        ___qtablewidgetitem12 = self.tableWidget_Step.horizontalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e0b", None));
        ___qtablewidgetitem13 = self.tableWidget_Step.horizontalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u5934\u65cb\u8f6c", None));
        ___qtablewidgetitem14 = self.tableWidget_Step.horizontalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"\u5934\u4e0a\u4e0b", None));
        ___qtablewidgetitem15 = self.tableWidget_Step.horizontalHeaderItem(7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6", None));
        ___qtablewidgetitem16 = self.tableWidget_Step.horizontalHeaderItem(8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u901f", None));
        ___qtablewidgetitem17 = self.tableWidget_Step.horizontalHeaderItem(9)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u901f", None));
        ___qtablewidgetitem18 = self.tableWidget_Step.horizontalHeaderItem(10)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934\u7f29\u653e", None));
        ___qtablewidgetitem19 = self.tableWidget_Step.horizontalHeaderItem(11)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6", None));
        ___qtablewidgetitem20 = self.tableWidget_Step.horizontalHeaderItem(12)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"\u673a\u5173", None));
        ___qtablewidgetitem21 = self.tableWidget_Step.horizontalHeaderItem(13)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u4f4d\u7f6e", None));
        ___qtablewidgetitem22 = self.tableWidget_Step.horizontalHeaderItem(14)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None));
        ___qtablewidgetitem23 = self.tableWidget_Step.horizontalHeaderItem(15)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem24 = self.tableWidget_Step.horizontalHeaderItem(16)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"OBS\u753b\u9762", None));
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u8f741\uff1a", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u8f742\uff1a", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\u8f743\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u8f744\uff1a", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u8f745\uff1a", None))
        self.checkBox_key.setText(QCoreApplication.translate("MainWindow", u"\u952e\u76d8\u5b9a\u4f4d", None))
        self.pushButton_ToTable.setText(QCoreApplication.translate("MainWindow", u"\u5750\u6807\u5165\u8868", None))
        self.pushButton_CardRun.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5f00\u542f", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361\u53f7\uff1a", None))
        self.pushButton_CardStop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.pushButton_CardStart.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u8fd0\u52a8\u5361", None))
        self.pushButton_CardReset.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
        self.pushButton_CardNext.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u52a8\u4f5c", None))
        self.pushButton_CardCloseAll.setText(QCoreApplication.translate("MainWindow", u"\u7d27\u6025\u5173\u95ed\u6240\u6709\u673a\u5173", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"OBS\u7ba1\u7406", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe\uff1a", None))
        ___qtablewidgetitem25 = self.tableWidget_Sources.horizontalHeaderItem(1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"\u6765\u6e90", None));
        ___qtablewidgetitem26 = self.tableWidget_Sources.horizontalHeaderItem(2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"id", None));
        self.pushButton_ObsConnect.setText(QCoreApplication.translate("MainWindow", u"\u94fe\u63a5OBS", None))
        self.pushButton_Obs_delete.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u51fa\u8868", None))
        self.pushButton_Obs2Table.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe\u5165\u8868", None))
        self.pushButton_Source2Table.setText(QCoreApplication.translate("MainWindow", u"\u6765\u6e90\u5165\u8868", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u4e3b\u673a\u5f55\u56fe\u64cd\u4f5c", None))
        self.radioButton_noball.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u7403", None))
        self.radioButton_ball.setText(QCoreApplication.translate("MainWindow", u"\u6709\u7403", None))
        self.checkBox_saveImgs.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u5c4f", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u53c2\u6570", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u955c\u5934\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_del_camera.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_add_camera.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_save_camera.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"\u97f3\u6548\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_add_Audio.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_del_Audio.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_save_Audio.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        ___qtablewidgetitem27 = self.tableWidget_Audio.horizontalHeaderItem(0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem28 = self.tableWidget_Audio.horizontalHeaderItem(1)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"\u6b21\u6570", None));
        ___qtablewidgetitem29 = self.tableWidget_Audio.horizontalHeaderItem(2)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6", None));
        ___qtablewidgetitem30 = self.tableWidget_Audio.horizontalHeaderItem(3)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None));
        self.checkBox_main_music.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f3", None))
        self.radioButton_music_1.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f31", None))
        self.radioButton_music_2.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f32", None))
        self.radioButton_music_3.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f33", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"AI\u8bed\u97f3\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_add_Ai.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_del_Ai.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_save_Ai.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        ___qtablewidgetitem31 = self.tableWidget_Ai.horizontalHeaderItem(0)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem32 = self.tableWidget_Ai.horizontalHeaderItem(1)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"\u6b21\u6570", None));
        ___qtablewidgetitem33 = self.tableWidget_Ai.horizontalHeaderItem(2)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6", None));
        ___qtablewidgetitem34 = self.tableWidget_Ai.horizontalHeaderItem(3)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None));
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"\u70b9\u4f4d\u663e\u793a", None))
        self.checkBox_show_ai.setText(QCoreApplication.translate("MainWindow", u"Ai\u70b9\u4f4d", None))
        self.checkBox_show_audio.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548\u70b9\u4f4d", None))
        self.checkBox_show_orbit.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u8f68\u8ff9", None))
        self.checkBox_show_camera.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934\u70b9\u4f4d", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u7d22\u5c3c\u6444\u50cf\u673a\u8bc6\u522b\u7ed3\u679c", None))
        self.label_main_picture.setText("")
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u6444\u50cf\u673a\u8bc6\u522b\u7ed3\u679c", None))
        self.label_monitor_picture.setText("")
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u6570\u636e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_send.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u5708\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u7d22\u5c3c\u6444\u50cf\u673a\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u6444\u50cf\u673a\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u6838\u5bf9\u7ed3\u679c\uff1a", None))
        self.pushButton_test_2.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
        self.checkBox_ShowUdp.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u670d\u52a1\u5668\u6570\u636e", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u7ed3\u679c:", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"\u5730\u56fe\u5212\u533a\u7f16\u8f91\u5236\u4f5c", None))
        self.pushButton_Draw.setText(QCoreApplication.translate("MainWindow", u"\u753b\u56fe\u5de5\u5177", None))
        self.pushButton_to_TXT.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362TXT", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u6392\u540d", None))
        ___qtablewidgetitem35 = self.tableWidget_Ranking.horizontalHeaderItem(0)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"\u989c\u8272", None));
        ___qtablewidgetitem36 = self.tableWidget_Ranking.horizontalHeaderItem(1)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"\u533a\u57df", None));
        ___qtablewidgetitem37 = self.tableWidget_Ranking.horizontalHeaderItem(2)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"\u5708\u6570", None));
        ___qtablewidgetitem38 = self.tableWidget_Ranking.horizontalHeaderItem(3)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"x", None));
        ___qtablewidgetitem39 = self.tableWidget_Ranking.horizontalHeaderItem(4)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"y", None));
        self.groupBox_20.setTitle("")
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u53c2\u6570\u8bbe\u7f6e", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u65f6\u95f4:", None))
        self.pushButton_save_Ranking.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_area_Ranking.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_lap_Ranking.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u5708\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_Time_Restart_Ranking.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5927\u533a\u57df:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u5708\u6570:", None))
        self.pushButton_reset_Ranking.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u6392\u540d", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u8bbe\u7f6e", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u5012\u8ba1\u65f6\uff1a", None))
        self.checkBox_restart.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6a21\u5f0f", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u7ed3\u679c\u65f6\u95f4\uff1a", None))
        self.lineEdit_time_send_result.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.pushButton_CardRun_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"\u7edf\u8ba1\u7403\u65f6\u95f4\uff1a", None))
        self.lineEdit_time_count_ball.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u7ec8\u70b9\u7403\u6570\uff1a", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8bc6\u522b", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f3\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_3.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e503.mp3", None))
        self.radioButton_music_background_2.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e502\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_2.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e502.mp3", None))
        self.radioButton_music_background_1.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e501\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_1.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e501.mp3", None))
        self.radioButton_music_background_3.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e503\uff1a", None))
        self.groupBox_28.setTitle("")
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"\u786c\u4ef6\u7aef\u53e3\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_cardNo.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_cardNo.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361\u7f51\u7edc\u7f16\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_s485_Axis_No.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_s485_Axis_No.setText(QCoreApplication.translate("MainWindow", u"COM23", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"S485 \u8f74\u590d\u4f4d\u7aef\u53e3\uff1a", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"S485 \u6444\u50cf\u673a\u7aef\u53e3\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_s485_Cam_No.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_s485_Cam_No.setText(QCoreApplication.translate("MainWindow", u"COM1", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"UDP\u63a5\u6536\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_ip.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_ip.setText(QCoreApplication.translate("MainWindow", u"0.0.0.0", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_Port.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_Port.setText(QCoreApplication.translate("MainWindow", u"19734", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u524d\u7aef\u6392\u540d\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_ip.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_ip.setText(QCoreApplication.translate("MainWindow", u"0.0.0.0", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_Port.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_Port.setText(QCoreApplication.translate("MainWindow", u"9999", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u5524\u9192\u8bc6\u522b\u670d\u52a1\u5668\u7f51\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_wakeup_addr.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_wakeup_addr.setText(QCoreApplication.translate("MainWindow", u"http://192.168.0.110:8080", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u6444\u50cf\u5934\u7f51\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_rtsp_url.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_rtsp_url.setText(QCoreApplication.translate("MainWindow", u"rtsp://admin:123456@192.168.0.29:554/Streaming/Channels/101", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"\u5f39\u73e0\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_balls_count.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_balls_count.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u73e0\u6570\u91cf\uff1a", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"\u989c\u8272\u53f7\u7801\u8bbe\u7f6e", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_5.setText(QCoreApplication.translate("MainWindow", u"orange", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_3.setText(QCoreApplication.translate("MainWindow", u"\u7ea2", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_4.setText(QCoreApplication.translate("MainWindow", u"purple", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"9\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_3.setText(QCoreApplication.translate("MainWindow", u"red", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"6\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_10.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_10.setText(QCoreApplication.translate("MainWindow", u"White", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_8.setText(QCoreApplication.translate("MainWindow", u"black", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_2.setText(QCoreApplication.translate("MainWindow", u"\u84dd", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"8\u53f7\uff1a", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"3\u53f7\uff1a", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"1\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_1.setText(QCoreApplication.translate("MainWindow", u"yellow", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"4\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_2.setText(QCoreApplication.translate("MainWindow", u"blue", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_7.setText(QCoreApplication.translate("MainWindow", u"Brown", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"2\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_1.setText(QCoreApplication.translate("MainWindow", u"\u9ec4", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"10\u53f7\uff1a", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"7\u53f7\uff1a", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_6.setText(QCoreApplication.translate("MainWindow", u"green", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_9.setText(QCoreApplication.translate("MainWindow", u"pink", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"5\u53f7\uff1a", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_4.setText(QCoreApplication.translate("MainWindow", u"\u7d2b", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_5.setText(QCoreApplication.translate("MainWindow", u"\u6a59", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_6.setText(QCoreApplication.translate("MainWindow", u"\u7eff", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_7.setText(QCoreApplication.translate("MainWindow", u"\u68d5", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_8.setText(QCoreApplication.translate("MainWindow", u"\u9ed1", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_9.setText(QCoreApplication.translate("MainWindow", u"\u7c89", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_10.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_10.setText(QCoreApplication.translate("MainWindow", u"\u767d", None))
        self.pushButton_Save_Ball.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5f39\u73e0", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
    # retranslateUi

