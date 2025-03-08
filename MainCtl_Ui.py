# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainCtl_Ui.ui'
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
        MainWindow.resize(1326, 973)
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
        self.tabWidget_Ranking.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tab_0 = QWidget()
        self.tab_0.setObjectName(u"tab_0")
        self.gridLayout_11 = QGridLayout(self.tab_0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_Results = QTableWidget(self.tab_0)
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
        self.tableWidget_Results.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Results.setTextElideMode(Qt.TextElideMode.ElideRight)
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
        self.radioButton_start_betting = QRadioButton(self.groupBox)
        self.radioButton_start_betting.setObjectName(u"radioButton_start_betting")

        self.gridLayout_9.addWidget(self.radioButton_start_betting, 0, 0, 1, 1)

        self.radioButton_stop_betting = QRadioButton(self.groupBox)
        self.radioButton_stop_betting.setObjectName(u"radioButton_stop_betting")

        self.gridLayout_9.addWidget(self.radioButton_stop_betting, 1, 0, 1, 1)

        self.radioButton_test_game = QRadioButton(self.groupBox)
        self.radioButton_test_game.setObjectName(u"radioButton_test_game")
        self.radioButton_test_game.setChecked(True)

        self.gridLayout_9.addWidget(self.radioButton_test_game, 2, 0, 1, 1)

        self.checkBox_black_screen = QCheckBox(self.groupBox)
        self.checkBox_black_screen.setObjectName(u"checkBox_black_screen")

        self.gridLayout_9.addWidget(self.checkBox_black_screen, 3, 0, 1, 1)


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
        self.status_live.setStyleSheet(u"background:rgb(255, 0, 0)")
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
        self.frame_4 = QFrame(self.groupBox_status_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(70, 0))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_3.addWidget(self.frame_4, 0, 4, 3, 1)

        self.status_card = QToolButton(self.groupBox_status_2)
        self.status_card.setObjectName(u"status_card")
        self.status_card.setMinimumSize(QSize(80, 0))
        self.status_card.setFont(font1)
        self.status_card.setAutoFillBackground(False)
        self.status_card.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_card.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_card.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_card, 0, 2, 1, 2)

        self.status_server = QToolButton(self.groupBox_status_2)
        self.status_server.setObjectName(u"status_server")
        self.status_server.setMinimumSize(QSize(80, 0))
        self.status_server.setFont(font1)
        self.status_server.setAutoFillBackground(False)
        self.status_server.setStyleSheet(u"background:rgb(255, 0, 0)")
        self.status_server.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_server.setAutoRaise(True)
        self.status_server.setArrowType(Qt.ArrowType.NoArrow)

        self.gridLayout_3.addWidget(self.status_server, 0, 0, 1, 1)

        self.status_ai = QToolButton(self.groupBox_status_2)
        self.status_ai.setObjectName(u"status_ai")
        self.status_ai.setFont(font1)
        self.status_ai.setAutoFillBackground(False)
        self.status_ai.setStyleSheet(u"background:rgb(255, 0, 0)")
        self.status_ai.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_ai.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_ai, 0, 1, 1, 1)

        self.status_ai_end = QToolButton(self.groupBox_status_2)
        self.status_ai_end.setObjectName(u"status_ai_end")
        self.status_ai_end.setMinimumSize(QSize(80, 0))
        self.status_ai_end.setFont(font1)
        self.status_ai_end.setAutoFillBackground(False)
        self.status_ai_end.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_ai_end.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_ai_end.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_ai_end, 1, 2, 1, 1)

        self.status_s485 = QToolButton(self.groupBox_status_2)
        self.status_s485.setObjectName(u"status_s485")
        self.status_s485.setMinimumSize(QSize(80, 0))
        self.status_s485.setFont(font1)
        self.status_s485.setAutoFillBackground(False)
        self.status_s485.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_s485.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_s485.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_s485, 1, 1, 1, 1)

        self.status_obs = QToolButton(self.groupBox_status_2)
        self.status_obs.setObjectName(u"status_obs")
        self.status_obs.setMinimumSize(QSize(80, 0))
        self.status_obs.setFont(font1)
        self.status_obs.setAutoFillBackground(False)
        self.status_obs.setStyleSheet(u"background:rgb(0, 255, 0)")
        self.status_obs.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.status_obs.setAutoRaise(True)

        self.gridLayout_3.addWidget(self.status_obs, 1, 0, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_status_2, 0, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_16 = QGridLayout(self.groupBox_3)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.checkBox_Pass_Recognition_Start = QCheckBox(self.groupBox_3)
        self.checkBox_Pass_Recognition_Start.setObjectName(u"checkBox_Pass_Recognition_Start")
        self.checkBox_Pass_Recognition_Start.setMaximumSize(QSize(150, 16777215))
        self.checkBox_Pass_Recognition_Start.setFont(font1)
        self.checkBox_Pass_Recognition_Start.setChecked(False)

        self.gridLayout_16.addWidget(self.checkBox_Pass_Recognition_Start, 0, 0, 1, 2)

        self.checkBox_end_BlackScreen = QCheckBox(self.groupBox_3)
        self.checkBox_end_BlackScreen.setObjectName(u"checkBox_end_BlackScreen")
        self.checkBox_end_BlackScreen.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_end_BlackScreen, 0, 3, 1, 2)

        self.checkBox_Pass_Ranking_Twice = QCheckBox(self.groupBox_3)
        self.checkBox_Pass_Ranking_Twice.setObjectName(u"checkBox_Pass_Ranking_Twice")
        self.checkBox_Pass_Ranking_Twice.setMinimumSize(QSize(180, 0))
        self.checkBox_Pass_Ranking_Twice.setMaximumSize(QSize(180, 16777215))
        self.checkBox_Pass_Ranking_Twice.setFont(font1)
        self.checkBox_Pass_Ranking_Twice.setChecked(False)

        self.gridLayout_16.addWidget(self.checkBox_Pass_Ranking_Twice, 1, 0, 1, 3)

        self.checkBox_end_stop = QCheckBox(self.groupBox_3)
        self.checkBox_end_stop.setObjectName(u"checkBox_end_stop")
        self.checkBox_end_stop.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_end_stop, 1, 3, 1, 2)

        self.checkBox_shoot_0 = QCheckBox(self.groupBox_3)
        self.checkBox_shoot_0.setObjectName(u"checkBox_shoot_0")
        self.checkBox_shoot_0.setMaximumSize(QSize(80, 16777215))
        self.checkBox_shoot_0.setFont(font1)
        self.checkBox_shoot_0.setChecked(True)

        self.gridLayout_16.addWidget(self.checkBox_shoot_0, 2, 0, 1, 1)

        self.lineEdit_balls_auto = QLineEdit(self.groupBox_3)
        self.lineEdit_balls_auto.setObjectName(u"lineEdit_balls_auto")
        self.lineEdit_balls_auto.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_balls_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_balls_auto.setReadOnly(False)

        self.gridLayout_16.addWidget(self.lineEdit_balls_auto, 2, 1, 1, 1)

        self.label_85 = QLabel(self.groupBox_3)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setFont(font1)

        self.gridLayout_16.addWidget(self.label_85, 2, 2, 1, 1)

        self.checkBox_alarm = QCheckBox(self.groupBox_3)
        self.checkBox_alarm.setObjectName(u"checkBox_alarm")
        self.checkBox_alarm.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_alarm, 2, 3, 1, 1)

        self.checkBox_shoot_1 = QCheckBox(self.groupBox_3)
        self.checkBox_shoot_1.setObjectName(u"checkBox_shoot_1")
        self.checkBox_shoot_1.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_shoot_1, 2, 4, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_3, 0, 3, 2, 2)

        self.groupBox_2 = QGroupBox(self.frame_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(375, 16777215))
        self.groupBox_2.setFont(font1)
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.lineEdit_times_count = QLineEdit(self.groupBox_2)
        self.lineEdit_times_count.setObjectName(u"lineEdit_times_count")
        self.lineEdit_times_count.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_times_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_times_count.setReadOnly(True)

        self.gridLayout_8.addWidget(self.lineEdit_times_count, 0, 5, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(85, 16777215))
        self.label_12.setFont(font1)
        self.label_12.setAutoFillBackground(False)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)

        self.lineEdit_term = QLineEdit(self.groupBox_2)
        self.lineEdit_term.setObjectName(u"lineEdit_term")
        self.lineEdit_term.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_8.addWidget(self.lineEdit_term, 0, 2, 1, 1)

        self.checkBox_continue_term = QCheckBox(self.groupBox_2)
        self.checkBox_continue_term.setObjectName(u"checkBox_continue_term")
        self.checkBox_continue_term.setFont(font1)

        self.gridLayout_8.addWidget(self.checkBox_continue_term, 0, 3, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(30, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAutoFillBackground(False)

        self.gridLayout_8.addWidget(self.label_10, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_2, 1, 2, 2, 1)

        self.pushButton_start_game = QPushButton(self.frame_3)
        self.pushButton_start_game.setObjectName(u"pushButton_start_game")
        self.pushButton_start_game.setMinimumSize(QSize(100, 50))
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton_start_game.setFont(font2)
        self.pushButton_start_game.setAutoDefault(False)
        self.pushButton_start_game.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_start_game, 2, 3, 1, 1)

        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_17.addWidget(self.label_3, 0, 6, 1, 1)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(30, 16777215))
        self.label_9.setFont(font1)
        self.label_9.setAutoFillBackground(False)

        self.gridLayout_17.addWidget(self.label_9, 0, 4, 1, 1)

        self.lineEdit_balls_start = QLineEdit(self.frame)
        self.lineEdit_balls_start.setObjectName(u"lineEdit_balls_start")
        self.lineEdit_balls_start.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_balls_start.setFont(font1)
        self.lineEdit_balls_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_balls_start.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineEdit_balls_start, 0, 2, 1, 1)

        self.lineEdit_balls_end = QLineEdit(self.frame)
        self.lineEdit_balls_end.setObjectName(u"lineEdit_balls_end")
        self.lineEdit_balls_end.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_balls_end.setFont(font1)
        self.lineEdit_balls_end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_balls_end.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineEdit_balls_end, 0, 5, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(30, 16777215))
        self.label.setFont(font1)
        self.label.setAutoFillBackground(False)

        self.gridLayout_17.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_17.addWidget(self.label_2, 0, 3, 1, 1)


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
        self.pushButton_Stop_All = QPushButton(self.frame_8)
        self.pushButton_Stop_All.setObjectName(u"pushButton_Stop_All")
        self.pushButton_Stop_All.setMaximumSize(QSize(200, 16777215))
        self.pushButton_Stop_All.setFont(font1)
        self.pushButton_Stop_All.setStyleSheet(u"background:rgb(255, 0, 0)")

        self.horizontalLayout_2.addWidget(self.pushButton_Stop_All)

        self.pushButton_end_all = QPushButton(self.frame_8)
        self.pushButton_end_all.setObjectName(u"pushButton_end_all")
        self.pushButton_end_all.setMaximumSize(QSize(200, 16777215))
        self.pushButton_end_all.setFont(font1)
        self.pushButton_end_all.setStyleSheet(u"background:rgb(255, 255, 0)")

        self.horizontalLayout_2.addWidget(self.pushButton_end_all)


        self.gridLayout_10.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 16777215))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_ready = QPushButton(self.frame_6)
        self.pushButton_ready.setObjectName(u"pushButton_ready")
        self.pushButton_ready.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_ready)

        self.pushButton_start_game_2 = QPushButton(self.frame_6)
        self.pushButton_start_game_2.setObjectName(u"pushButton_start_game_2")
        self.pushButton_start_game_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_start_game_2)

        self.pushButton_close_all = QPushButton(self.frame_6)
        self.pushButton_close_all.setObjectName(u"pushButton_close_all")
        self.pushButton_close_all.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_close_all)

        self.pushButton_collect_ball = QPushButton(self.frame_6)
        self.pushButton_collect_ball.setObjectName(u"pushButton_collect_ball")
        self.pushButton_collect_ball.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_collect_ball)

        self.pushButton_end_game = QPushButton(self.frame_6)
        self.pushButton_end_game.setObjectName(u"pushButton_end_game")
        self.pushButton_end_game.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_end_game)


        self.gridLayout_10.addWidget(self.frame_6, 1, 0, 1, 1)

        self.groupBox_term = QGroupBox(self.frame_2)
        self.groupBox_term.setObjectName(u"groupBox_term")
        self.groupBox_term.setMinimumSize(QSize(0, 200))
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.groupBox_term.setPalette(palette)
        self.groupBox_term.setAutoFillBackground(False)
        self.groupBox_term.setStyleSheet(u"")
        self.gridLayout_5 = QGridLayout(self.groupBox_term)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pushButton_Backup_Camera = QPushButton(self.groupBox_term)
        self.pushButton_Backup_Camera.setObjectName(u"pushButton_Backup_Camera")
        self.pushButton_Backup_Camera.setAutoDefault(False)
        self.pushButton_Backup_Camera.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_Backup_Camera, 3, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_term)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.gridLayout_5.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit_Main_Camera = QLineEdit(self.groupBox_term)
        self.lineEdit_Main_Camera.setObjectName(u"lineEdit_Main_Camera")
        palette1 = QPalette()
        self.lineEdit_Main_Camera.setPalette(palette1)
        self.lineEdit_Main_Camera.setFont(font1)
        self.lineEdit_Main_Camera.setAutoFillBackground(False)
        self.lineEdit_Main_Camera.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.lineEdit_Main_Camera, 2, 1, 1, 1)

        self.checkBox_Auto_Send = QCheckBox(self.groupBox_term)
        self.checkBox_Auto_Send.setObjectName(u"checkBox_Auto_Send")
        self.checkBox_Auto_Send.setFont(font1)

        self.gridLayout_5.addWidget(self.checkBox_Auto_Send, 4, 2, 1, 1)

        self.lineEdit_Send_Result = QLineEdit(self.groupBox_term)
        self.lineEdit_Send_Result.setObjectName(u"lineEdit_Send_Result")
        palette2 = QPalette()
        self.lineEdit_Send_Result.setPalette(palette2)
        font3 = QFont()
        font3.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(16)
        font3.setBold(True)
        self.lineEdit_Send_Result.setFont(font3)
        self.lineEdit_Send_Result.setAutoFillBackground(False)
        self.lineEdit_Send_Result.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.lineEdit_Send_Result, 4, 0, 1, 2)

        self.pushButton_Main_Camera = QPushButton(self.groupBox_term)
        self.pushButton_Main_Camera.setObjectName(u"pushButton_Main_Camera")
        self.pushButton_Main_Camera.setAutoDefault(False)
        self.pushButton_Main_Camera.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_Main_Camera, 2, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_term)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.gridLayout_5.addWidget(self.label_5, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.groupBox_term)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_Send_Result = QPushButton(self.frame_9)
        self.pushButton_Send_Result.setObjectName(u"pushButton_Send_Result")
        self.pushButton_Send_Result.setMaximumSize(QSize(100, 16777215))
        self.pushButton_Send_Result.setAutoDefault(False)
        self.pushButton_Send_Result.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_Send_Result)

        self.pushButton_Cancel_End = QPushButton(self.frame_9)
        self.pushButton_Cancel_End.setObjectName(u"pushButton_Cancel_End")
        self.pushButton_Cancel_End.setMaximumSize(QSize(100, 16777215))
        self.pushButton_Cancel_End.setAutoDefault(False)
        self.pushButton_Cancel_End.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_Cancel_End)

        self.pushButton_Send_End = QPushButton(self.frame_9)
        self.pushButton_Send_End.setObjectName(u"pushButton_Send_End")
        self.pushButton_Send_End.setMaximumSize(QSize(100, 16777215))
        self.pushButton_Send_End.setAutoDefault(False)
        self.pushButton_Send_End.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_Send_End)


        self.gridLayout_5.addWidget(self.frame_9, 5, 0, 1, 3)

        self.pushButton_term = QPushButton(self.groupBox_term)
        self.pushButton_term.setObjectName(u"pushButton_term")
        self.pushButton_term.setMinimumSize(QSize(0, 60))
        font4 = QFont()
        font4.setFamilies([u"Microsoft YaHei UI"])
        font4.setPointSize(16)
        font4.setBold(True)
        self.pushButton_term.setFont(font4)
        self.pushButton_term.setStyleSheet(u"QPushButton { color: red; }")
        self.pushButton_term.setAutoDefault(False)
        self.pushButton_term.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_term, 1, 0, 1, 2)

        self.lineEdit_Backup_Camera = QLineEdit(self.groupBox_term)
        self.lineEdit_Backup_Camera.setObjectName(u"lineEdit_Backup_Camera")
        palette3 = QPalette()
        self.lineEdit_Backup_Camera.setPalette(palette3)
        self.lineEdit_Backup_Camera.setFont(font1)
        self.lineEdit_Backup_Camera.setAutoFillBackground(False)
        self.lineEdit_Backup_Camera.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.lineEdit_Backup_Camera, 3, 1, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_term, 2, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.pushButton_TRAP = QPushButton(self.frame_7)
        self.pushButton_TRAP.setObjectName(u"pushButton_TRAP")

        self.gridLayout_7.addWidget(self.pushButton_TRAP, 0, 0, 1, 1)

        self.pushButton_TRAP_1 = QPushButton(self.frame_7)
        self.pushButton_TRAP_1.setObjectName(u"pushButton_TRAP_1")
        self.pushButton_TRAP_1.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_1.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_1, 0, 1, 1, 1)

        self.pushButton_TRAP_2 = QPushButton(self.frame_7)
        self.pushButton_TRAP_2.setObjectName(u"pushButton_TRAP_2")
        self.pushButton_TRAP_2.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_2.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_2, 0, 2, 1, 1)

        self.pushButton_TRAP_3 = QPushButton(self.frame_7)
        self.pushButton_TRAP_3.setObjectName(u"pushButton_TRAP_3")
        self.pushButton_TRAP_3.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_3.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_3, 0, 3, 1, 1)

        self.pushButton_TRAP_4 = QPushButton(self.frame_7)
        self.pushButton_TRAP_4.setObjectName(u"pushButton_TRAP_4")
        self.pushButton_TRAP_4.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_4.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_4, 0, 4, 1, 1)

        self.pushButton_TRAP_5 = QPushButton(self.frame_7)
        self.pushButton_TRAP_5.setObjectName(u"pushButton_TRAP_5")
        self.pushButton_TRAP_5.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_5.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_5, 0, 5, 1, 1)

        self.pushButton_TRAP_6 = QPushButton(self.frame_7)
        self.pushButton_TRAP_6.setObjectName(u"pushButton_TRAP_6")
        self.pushButton_TRAP_6.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_6.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_6, 0, 6, 1, 1)

        self.pushButton_TRAP_7 = QPushButton(self.frame_7)
        self.pushButton_TRAP_7.setObjectName(u"pushButton_TRAP_7")
        self.pushButton_TRAP_7.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_7.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_7, 0, 7, 1, 1)

        self.pushButton_TRAP_8 = QPushButton(self.frame_7)
        self.pushButton_TRAP_8.setObjectName(u"pushButton_TRAP_8")
        self.pushButton_TRAP_8.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_8.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_8, 0, 8, 1, 1)

        self.pushButton_TRAP_9 = QPushButton(self.frame_7)
        self.pushButton_TRAP_9.setObjectName(u"pushButton_TRAP_9")
        self.pushButton_TRAP_9.setMinimumSize(QSize(20, 0))
        self.pushButton_TRAP_9.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_9, 0, 9, 1, 1)

        self.pushButton_TRAP_10 = QPushButton(self.frame_7)
        self.pushButton_TRAP_10.setObjectName(u"pushButton_TRAP_10")
        self.pushButton_TRAP_10.setMinimumSize(QSize(30, 0))
        self.pushButton_TRAP_10.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_TRAP_10, 0, 10, 1, 1)

        self.pushButton_OUT = QPushButton(self.frame_7)
        self.pushButton_OUT.setObjectName(u"pushButton_OUT")

        self.gridLayout_7.addWidget(self.pushButton_OUT, 1, 0, 1, 1)

        self.pushButton_OUT_1 = QPushButton(self.frame_7)
        self.pushButton_OUT_1.setObjectName(u"pushButton_OUT_1")
        self.pushButton_OUT_1.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_1.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_1, 1, 1, 1, 1)

        self.pushButton_OUT_2 = QPushButton(self.frame_7)
        self.pushButton_OUT_2.setObjectName(u"pushButton_OUT_2")
        self.pushButton_OUT_2.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_2.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_2, 1, 2, 1, 1)

        self.pushButton_OUT_3 = QPushButton(self.frame_7)
        self.pushButton_OUT_3.setObjectName(u"pushButton_OUT_3")
        self.pushButton_OUT_3.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_3.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_3, 1, 3, 1, 1)

        self.pushButton_OUT_4 = QPushButton(self.frame_7)
        self.pushButton_OUT_4.setObjectName(u"pushButton_OUT_4")
        self.pushButton_OUT_4.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_4.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_4, 1, 4, 1, 1)

        self.pushButton_OUT_5 = QPushButton(self.frame_7)
        self.pushButton_OUT_5.setObjectName(u"pushButton_OUT_5")
        self.pushButton_OUT_5.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_5.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_5, 1, 5, 1, 1)

        self.pushButton_OUT_6 = QPushButton(self.frame_7)
        self.pushButton_OUT_6.setObjectName(u"pushButton_OUT_6")
        self.pushButton_OUT_6.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_6.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_6, 1, 6, 1, 1)

        self.pushButton_OUT_7 = QPushButton(self.frame_7)
        self.pushButton_OUT_7.setObjectName(u"pushButton_OUT_7")
        self.pushButton_OUT_7.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_7.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_7, 1, 7, 1, 1)

        self.pushButton_OUT_8 = QPushButton(self.frame_7)
        self.pushButton_OUT_8.setObjectName(u"pushButton_OUT_8")
        self.pushButton_OUT_8.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_8.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_8, 1, 8, 1, 1)

        self.pushButton_OUT_9 = QPushButton(self.frame_7)
        self.pushButton_OUT_9.setObjectName(u"pushButton_OUT_9")
        self.pushButton_OUT_9.setMinimumSize(QSize(20, 0))
        self.pushButton_OUT_9.setMaximumSize(QSize(20, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_9, 1, 9, 1, 1)

        self.pushButton_OUT_10 = QPushButton(self.frame_7)
        self.pushButton_OUT_10.setObjectName(u"pushButton_OUT_10")
        self.pushButton_OUT_10.setMinimumSize(QSize(30, 0))
        self.pushButton_OUT_10.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_7.addWidget(self.pushButton_OUT_10, 1, 10, 1, 1)


        self.gridLayout_10.addWidget(self.frame_7, 3, 0, 1, 1)

        self.groupBox_39 = QGroupBox(self.frame_2)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.groupBox_39.setMinimumSize(QSize(50, 50))
        self.groupBox_39.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_39.setFont(font1)
        self.gridLayout_69 = QGridLayout(self.groupBox_39)
        self.gridLayout_69.setObjectName(u"gridLayout_69")
        self.gridLayout_69.setContentsMargins(-1, 0, -1, 0)
        self.pushButton_Organ = QPushButton(self.groupBox_39)
        self.pushButton_Organ.setObjectName(u"pushButton_Organ")
        self.pushButton_Organ.setMinimumSize(QSize(0, 30))

        self.gridLayout_69.addWidget(self.pushButton_Organ, 0, 0, 1, 1)

        self.pushButton_kaj789 = QPushButton(self.groupBox_39)
        self.pushButton_kaj789.setObjectName(u"pushButton_kaj789")
        self.pushButton_kaj789.setMinimumSize(QSize(0, 30))
        self.pushButton_kaj789.setAutoDefault(False)

        self.gridLayout_69.addWidget(self.pushButton_kaj789, 0, 1, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_39, 4, 0, 1, 1)

        self.textBrowser_msg = QTextBrowser(self.frame_2)
        self.textBrowser_msg.setObjectName(u"textBrowser_msg")
        self.textBrowser_msg.setReadOnly(False)

        self.gridLayout_10.addWidget(self.textBrowser_msg, 5, 0, 1, 1)


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
        self.label_23 = QLabel(self.frame_13)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)

        self.gridLayout_13.addWidget(self.label_23, 0, 8, 1, 1)

        self.label_84 = QLabel(self.frame_13)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setMinimumSize(QSize(60, 0))
        self.label_84.setFont(font1)

        self.gridLayout_13.addWidget(self.label_84, 0, 4, 1, 1)

        self.lineEdit_rename = QLineEdit(self.frame_13)
        self.lineEdit_rename.setObjectName(u"lineEdit_rename")

        self.gridLayout_13.addWidget(self.lineEdit_rename, 0, 9, 1, 1)

        self.checkBox_follow = QCheckBox(self.frame_13)
        self.checkBox_follow.setObjectName(u"checkBox_follow")
        self.checkBox_follow.setFont(font1)
        self.checkBox_follow.setStyleSheet(u"QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}\n"
"            \n"
"            QCheckBox::indicator:checked {\n"
"                background-color: lightgreen;\n"
"                border: 2px solid green;\n"
"            }\n"
"            QCheckBox::indicator:unchecked {\n"
"                background-color: lightgray;\n"
"                border: 2px solid gray;\n"
"            }\n"
"            QCheckBox::indicator {\n"
"                width: 10px;\n"
"                height: 10px;\n"
"            }")
        self.checkBox_follow.setChecked(True)

        self.gridLayout_13.addWidget(self.checkBox_follow, 0, 6, 1, 1)

        self.pushButton_fsave = QPushButton(self.frame_13)
        self.pushButton_fsave.setObjectName(u"pushButton_fsave")
        self.pushButton_fsave.setMinimumSize(QSize(80, 0))
        self.pushButton_fsave.setFont(font1)
        self.pushButton_fsave.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_13.addWidget(self.pushButton_fsave, 0, 3, 1, 1)

        self.pushButton_rename = QPushButton(self.frame_13)
        self.pushButton_rename.setObjectName(u"pushButton_rename")
        self.pushButton_rename.setFont(font1)
        self.pushButton_rename.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_13.addWidget(self.pushButton_rename, 0, 10, 1, 1)

        self.label_22 = QLabel(self.frame_13)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.gridLayout_13.addWidget(self.label_22, 0, 1, 1, 1)

        self.checkBox_test = QCheckBox(self.frame_13)
        self.checkBox_test.setObjectName(u"checkBox_test")
        self.checkBox_test.setFont(font1)
        self.checkBox_test.setStyleSheet(u"QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}\n"
"            \n"
"            QCheckBox::indicator:checked {\n"
"                background-color: lightgreen;\n"
"                border: 2px solid green;\n"
"            }\n"
"            QCheckBox::indicator:unchecked {\n"
"                background-color: lightgray;\n"
"                border: 2px solid gray;\n"
"            }\n"
"            QCheckBox::indicator {\n"
"                width: 10px;\n"
"                height: 10px;\n"
"            }")

        self.gridLayout_13.addWidget(self.checkBox_test, 0, 7, 1, 1)

        self.lineEdit_area = QLineEdit(self.frame_13)
        self.lineEdit_area.setObjectName(u"lineEdit_area")
        self.lineEdit_area.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_area.setReadOnly(True)

        self.gridLayout_13.addWidget(self.lineEdit_area, 0, 5, 1, 1)

        self.checkBox_selectall = QCheckBox(self.frame_13)
        self.checkBox_selectall.setObjectName(u"checkBox_selectall")
        self.checkBox_selectall.setFont(font1)
        self.checkBox_selectall.setStyleSheet(u"QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}\n"
"            \n"
"            QCheckBox::indicator:checked {\n"
"                background-color: lightgreen;\n"
"                border: 2px solid green;\n"
"            }\n"
"            QCheckBox::indicator:unchecked {\n"
"                background-color: lightgray;\n"
"                border: 2px solid gray;\n"
"            }\n"
"            QCheckBox::indicator {\n"
"                width: 10px;\n"
"                height: 10px;\n"
"            }")

        self.gridLayout_13.addWidget(self.checkBox_selectall, 0, 0, 1, 1)

        self.comboBox_plan = QComboBox(self.frame_13)
        self.comboBox_plan.setObjectName(u"comboBox_plan")
        self.comboBox_plan.setMinimumSize(QSize(180, 0))
        self.comboBox_plan.setFont(font1)
        self.comboBox_plan.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_13.addWidget(self.comboBox_plan, 0, 2, 1, 1)


        self.gridLayout_20.addWidget(self.frame_13, 0, 0, 1, 1)

        self.tableWidget_Step = QTableWidget(self.tab_1)
        if (self.tableWidget_Step.columnCount() < 19):
            self.tableWidget_Step.setColumnCount(19)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(5, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(6, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(7, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(8, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(9, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(10, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(11, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(12, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(13, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(14, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(15, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(16, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(17, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_Step.setHorizontalHeaderItem(18, __qtablewidgetitem33)
        self.tableWidget_Step.setObjectName(u"tableWidget_Step")
        self.tableWidget_Step.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
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
        self.groupBox_4 = QGroupBox(self.frame_10)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 248))
        self.groupBox_4.setFont(font1)
        self.groupBox_4.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.groupBox_4.setStyleSheet(u"")
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
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(0, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(1, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_Sources.setHorizontalHeaderItem(2, __qtablewidgetitem36)
        self.tableWidget_Sources.setObjectName(u"tableWidget_Sources")
        self.tableWidget_Sources.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tableWidget_Sources.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Sources.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Sources.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_14.addWidget(self.tableWidget_Sources, 2, 0, 1, 2)

        self.comboBox_Scenes = QComboBox(self.groupBox_4)
        self.comboBox_Scenes.setObjectName(u"comboBox_Scenes")
        self.comboBox_Scenes.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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
        self.pushButton_ObsConnect.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_6.addWidget(self.pushButton_ObsConnect, 0, 0, 1, 1)

        self.pushButton_Obs2Table = QPushButton(self.frame_22)
        self.pushButton_Obs2Table.setObjectName(u"pushButton_Obs2Table")
        self.pushButton_Obs2Table.setMinimumSize(QSize(0, 30))
        self.pushButton_Obs2Table.setFont(font1)
        self.pushButton_Obs2Table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_6.addWidget(self.pushButton_Obs2Table, 1, 0, 1, 1)

        self.pushButton_Source2Table = QPushButton(self.frame_22)
        self.pushButton_Source2Table.setObjectName(u"pushButton_Source2Table")
        self.pushButton_Source2Table.setMinimumSize(QSize(0, 30))
        self.pushButton_Source2Table.setFont(font1)
        self.pushButton_Source2Table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_6.addWidget(self.pushButton_Source2Table, 1, 1, 1, 1)

        self.pushButton_Obs_delete = QPushButton(self.frame_22)
        self.pushButton_Obs_delete.setObjectName(u"pushButton_Obs_delete")
        self.pushButton_Obs_delete.setMinimumSize(QSize(0, 30))
        self.pushButton_Obs_delete.setFont(font1)
        self.pushButton_Obs_delete.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_6.addWidget(self.pushButton_Obs_delete, 0, 1, 1, 1)


        self.gridLayout_14.addWidget(self.frame_22, 0, 0, 1, 2)


        self.gridLayout_34.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.textBrowser = QTextBrowser(self.frame_10)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.textBrowser.setReadOnly(False)

        self.gridLayout_34.addWidget(self.textBrowser, 2, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.frame_10)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFont(font1)
        self.groupBox_6.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        font5 = QFont()
        font5.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.lineEdit_axis0.setFont(font5)
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
        self.lineEdit_axis1.setFont(font5)
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
        self.lineEdit_axis2.setFont(font5)
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
        self.lineEdit_axis3.setFont(font5)
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
        self.lineEdit_axis4.setFont(font5)
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
        self.checkBox_key.setMaximumSize(QSize(75, 16777215))
        self.checkBox_key.setFont(font1)

        self.gridLayout_19.addWidget(self.checkBox_key, 0, 0, 1, 1)

        self.pushButton_ToTable = QPushButton(self.frame_16)
        self.pushButton_ToTable.setObjectName(u"pushButton_ToTable")
        self.pushButton_ToTable.setMinimumSize(QSize(0, 30))
        self.pushButton_ToTable.setFont(font1)
        self.pushButton_ToTable.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_19.addWidget(self.pushButton_ToTable, 0, 2, 1, 1)

        self.checkBox_key_stop = QCheckBox(self.frame_16)
        self.checkBox_key_stop.setObjectName(u"checkBox_key_stop")
        self.checkBox_key_stop.setMaximumSize(QSize(50, 16777215))
        self.checkBox_key_stop.setFont(font1)

        self.gridLayout_19.addWidget(self.checkBox_key_stop, 0, 1, 1, 1)


        self.gridLayout_22.addWidget(self.frame_16, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.groupBox_6)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 100))
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_15)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.frame_18 = QFrame(self.frame_15)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMaximumSize(QSize(70, 16777215))
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_18)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.label_18 = QLabel(self.frame_18)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(60, 0))
        self.label_18.setFont(font1)

        self.gridLayout_21.addWidget(self.label_18, 0, 0, 1, 1)


        self.gridLayout_24.addWidget(self.frame_18, 0, 0, 1, 1)

        self.pushButton_CardStart = QPushButton(self.frame_15)
        self.pushButton_CardStart.setObjectName(u"pushButton_CardStart")
        self.pushButton_CardStart.setMinimumSize(QSize(0, 30))
        self.pushButton_CardStart.setFont(font1)
        self.pushButton_CardStart.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_24.addWidget(self.pushButton_CardStart, 0, 2, 1, 1)

        self.pushButton_CardReset = QPushButton(self.frame_15)
        self.pushButton_CardReset.setObjectName(u"pushButton_CardReset")
        self.pushButton_CardReset.setMinimumSize(QSize(0, 30))
        self.pushButton_CardReset.setFont(font1)
        self.pushButton_CardReset.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_24.addWidget(self.pushButton_CardReset, 1, 2, 1, 1)

        self.pushButton_CardNext = QPushButton(self.frame_15)
        self.pushButton_CardNext.setObjectName(u"pushButton_CardNext")
        self.pushButton_CardNext.setMinimumSize(QSize(0, 30))
        self.pushButton_CardNext.setFont(font1)
        self.pushButton_CardNext.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_24.addWidget(self.pushButton_CardNext, 2, 2, 1, 1)

        self.lineEdit_CardNo = QLineEdit(self.frame_15)
        self.lineEdit_CardNo.setObjectName(u"lineEdit_CardNo")
        self.lineEdit_CardNo.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_CardNo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_CardNo, 0, 1, 1, 1)

        self.pushButton_CardRun = QPushButton(self.frame_15)
        self.pushButton_CardRun.setObjectName(u"pushButton_CardRun")
        self.pushButton_CardRun.setMinimumSize(QSize(0, 30))
        self.pushButton_CardRun.setFont(font1)
        self.pushButton_CardRun.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_CardRun.setStyleSheet(u"background:rgb(0,255,0)")

        self.gridLayout_24.addWidget(self.pushButton_CardRun, 1, 0, 1, 2)

        self.pushButton_CardStop = QPushButton(self.frame_15)
        self.pushButton_CardStop.setObjectName(u"pushButton_CardStop")
        self.pushButton_CardStop.setMinimumSize(QSize(0, 30))
        self.pushButton_CardStop.setFont(font1)
        self.pushButton_CardStop.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_CardStop.setStyleSheet(u"background:rgb(255,0,0)")

        self.gridLayout_24.addWidget(self.pushButton_CardStop, 2, 0, 1, 2)

        self.groupBox_34 = QGroupBox(self.frame_15)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setMaximumSize(QSize(16777215, 150))
        self.groupBox_34.setFont(font1)
        self.gridLayout_61 = QGridLayout(self.groupBox_34)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.checkBox_shoot = QCheckBox(self.groupBox_34)
        self.checkBox_shoot.setObjectName(u"checkBox_shoot")
        self.checkBox_shoot.setFont(font1)
        self.checkBox_shoot.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_61.addWidget(self.checkBox_shoot, 0, 0, 1, 1)

        self.checkBox_start = QCheckBox(self.groupBox_34)
        self.checkBox_start.setObjectName(u"checkBox_start")
        self.checkBox_start.setFont(font1)
        self.checkBox_start.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.checkBox_start.setChecked(False)

        self.gridLayout_61.addWidget(self.checkBox_start, 0, 1, 1, 1)

        self.checkBox_end = QCheckBox(self.groupBox_34)
        self.checkBox_end.setObjectName(u"checkBox_end")
        self.checkBox_end.setFont(font1)
        self.checkBox_end.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.checkBox_end.setChecked(False)

        self.gridLayout_61.addWidget(self.checkBox_end, 0, 2, 1, 1)

        self.checkBox_all = QCheckBox(self.groupBox_34)
        self.checkBox_all.setObjectName(u"checkBox_all")
        self.checkBox_all.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_61.addWidget(self.checkBox_all, 0, 3, 2, 1)

        self.label_78 = QLabel(self.groupBox_34)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setMinimumSize(QSize(60, 0))
        self.label_78.setFont(font1)

        self.gridLayout_61.addWidget(self.label_78, 1, 0, 1, 1)

        self.lineEdit_OutNo = QLineEdit(self.groupBox_34)
        self.lineEdit_OutNo.setObjectName(u"lineEdit_OutNo")
        self.lineEdit_OutNo.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_OutNo.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_OutNo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_61.addWidget(self.lineEdit_OutNo, 1, 1, 1, 1)

        self.checkBox_switch = QCheckBox(self.groupBox_34)
        self.checkBox_switch.setObjectName(u"checkBox_switch")
        self.checkBox_switch.setFont(font1)
        self.checkBox_switch.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout_61.addWidget(self.checkBox_switch, 1, 2, 1, 1)


        self.gridLayout_24.addWidget(self.groupBox_34, 3, 0, 1, 3)


        self.gridLayout_22.addWidget(self.frame_15, 2, 0, 1, 1)


        self.gridLayout_34.addWidget(self.groupBox_6, 0, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_10, 0, 1, 3, 1)

        self.tabWidget_Ranking.addTab(self.tab_1, "")
        self.frame_13.raise_()
        self.frame_23.raise_()
        self.frame_10.raise_()
        self.tableWidget_Step.raise_()
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
        if (self.tableWidget_Audio.columnCount() < 5):
            self.tableWidget_Audio.setColumnCount(5)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_Audio.setHorizontalHeaderItem(4, __qtablewidgetitem41)
        self.tableWidget_Audio.setObjectName(u"tableWidget_Audio")
        self.tableWidget_Audio.setMinimumSize(QSize(0, 0))
        self.tableWidget_Audio.setMaximumSize(QSize(500, 16777215))
        font6 = QFont()
        font6.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font6.setPointSize(12)
        font6.setBold(False)
        self.tableWidget_Audio.setFont(font6)
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
        self.pushButton_save_Ai.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout_44.addWidget(self.pushButton_save_Ai, 0, 2, 1, 1)

        self.tableWidget_Ai = QTableWidget(self.groupBox_19)
        if (self.tableWidget_Ai.columnCount() < 5):
            self.tableWidget_Ai.setColumnCount(5)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(0, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(1, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(2, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(3, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableWidget_Ai.setHorizontalHeaderItem(4, __qtablewidgetitem46)
        self.tableWidget_Ai.setObjectName(u"tableWidget_Ai")
        self.tableWidget_Ai.setMinimumSize(QSize(0, 0))
        self.tableWidget_Ai.setMaximumSize(QSize(500, 380))
        self.tableWidget_Ai.setFont(font6)
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
        self.frame_camera = QFrame(self.tab_3)
        self.frame_camera.setObjectName(u"frame_camera")
        self.frame_camera.setMinimumSize(QSize(0, 10))
        self.frame_camera.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_camera.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_40 = QGridLayout(self.frame_camera)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.gridLayout_40.setContentsMargins(0, 0, 9, 0)
        self.widget = QWidget(self.frame_camera)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(320, 0))
        self.widget.setMaximumSize(QSize(300, 16777215))
        self.gridLayout_65 = QGridLayout(self.widget)
        self.gridLayout_65.setObjectName(u"gridLayout_65")
        self.gridLayout_65.setContentsMargins(0, 0, 0, 0)
        self.groupBox_8 = QGroupBox(self.widget)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(300, 10))
        self.groupBox_8.setMaximumSize(QSize(320, 16777215))
        self.groupBox_8.setFont(font1)
        self.gridLayout_28 = QGridLayout(self.groupBox_8)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.label_89 = QLabel(self.groupBox_8)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_89, 2, 0, 1, 1)

        self.widget_camera_monitor = QWidget(self.groupBox_8)
        self.widget_camera_monitor.setObjectName(u"widget_camera_monitor")
        self.widget_camera_monitor.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_monitor, 1, 1, 1, 2)

        self.widget_camera_sony = QWidget(self.groupBox_8)
        self.widget_camera_sony.setObjectName(u"widget_camera_sony")
        self.widget_camera_sony.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_sony, 0, 1, 1, 2)

        self.widget_camera_fit = QWidget(self.groupBox_8)
        self.widget_camera_fit.setObjectName(u"widget_camera_fit")
        self.widget_camera_fit.setMinimumSize(QSize(230, 38))

        self.gridLayout_28.addWidget(self.widget_camera_fit, 2, 1, 1, 2)

        self.pushButton_Send_Res = QPushButton(self.groupBox_8)
        self.pushButton_Send_Res.setObjectName(u"pushButton_Send_Res")
        self.pushButton_Send_Res.setMinimumSize(QSize(50, 30))
        self.pushButton_Send_Res.setStyleSheet(u"background:rgb(0,255,0)")

        self.gridLayout_28.addWidget(self.pushButton_Send_Res, 4, 0, 1, 3)

        self.label_87 = QLabel(self.groupBox_8)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_87, 0, 0, 1, 1)

        self.checkBox_ShowUdp = QCheckBox(self.groupBox_8)
        self.checkBox_ShowUdp.setObjectName(u"checkBox_ShowUdp")
        self.checkBox_ShowUdp.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.checkBox_ShowUdp, 5, 0, 1, 2)

        self.label_88 = QLabel(self.groupBox_8)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_88, 1, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 30))

        self.gridLayout_28.addWidget(self.label_16, 3, 0, 1, 1)

        self.frame_5 = QFrame(self.groupBox_8)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(264, 54))
        self.frame_5.setFont(font3)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.lineEdit_result_7 = QLineEdit(self.frame_5)
        self.lineEdit_result_7.setObjectName(u"lineEdit_result_7")
        self.lineEdit_result_7.setGeometry(QRect(176, 10, 24, 34))
        self.lineEdit_result_7.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_7.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_7.setFont(font3)
        self.lineEdit_result_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_5 = QLineEdit(self.frame_5)
        self.lineEdit_result_5.setObjectName(u"lineEdit_result_5")
        self.lineEdit_result_5.setGeometry(QRect(126, 10, 24, 34))
        self.lineEdit_result_5.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_5.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_5.setFont(font3)
        self.lineEdit_result_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_3 = QLineEdit(self.frame_5)
        self.lineEdit_result_3.setObjectName(u"lineEdit_result_3")
        self.lineEdit_result_3.setGeometry(QRect(76, 10, 24, 34))
        self.lineEdit_result_3.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_3.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_3.setFont(font3)
        self.lineEdit_result_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_1 = QLineEdit(self.frame_5)
        self.lineEdit_result_1.setObjectName(u"lineEdit_result_1")
        self.lineEdit_result_1.setGeometry(QRect(26, 10, 24, 34))
        self.lineEdit_result_1.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_1.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_1.setFont(font3)
        self.lineEdit_result_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_8 = QLineEdit(self.frame_5)
        self.lineEdit_result_8.setObjectName(u"lineEdit_result_8")
        self.lineEdit_result_8.setGeometry(QRect(201, 10, 24, 34))
        self.lineEdit_result_8.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_8.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_8.setFont(font3)
        self.lineEdit_result_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_6 = QLineEdit(self.frame_5)
        self.lineEdit_result_6.setObjectName(u"lineEdit_result_6")
        self.lineEdit_result_6.setGeometry(QRect(151, 10, 24, 34))
        self.lineEdit_result_6.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_6.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_6.setFont(font3)
        self.lineEdit_result_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_9 = QLineEdit(self.frame_5)
        self.lineEdit_result_9.setObjectName(u"lineEdit_result_9")
        self.lineEdit_result_9.setGeometry(QRect(226, 10, 24, 34))
        self.lineEdit_result_9.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_9.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_9.setFont(font3)
        self.lineEdit_result_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_2 = QLineEdit(self.frame_5)
        self.lineEdit_result_2.setObjectName(u"lineEdit_result_2")
        self.lineEdit_result_2.setGeometry(QRect(51, 10, 24, 34))
        self.lineEdit_result_2.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_2.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_2.setFont(font3)
        self.lineEdit_result_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_4 = QLineEdit(self.frame_5)
        self.lineEdit_result_4.setObjectName(u"lineEdit_result_4")
        self.lineEdit_result_4.setGeometry(QRect(101, 10, 24, 34))
        self.lineEdit_result_4.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_4.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_4.setFont(font3)
        self.lineEdit_result_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_result_0 = QLineEdit(self.frame_5)
        self.lineEdit_result_0.setObjectName(u"lineEdit_result_0")
        self.lineEdit_result_0.setGeometry(QRect(1, 10, 24, 34))
        self.lineEdit_result_0.setMinimumSize(QSize(24, 34))
        self.lineEdit_result_0.setMaximumSize(QSize(26, 16777215))
        self.lineEdit_result_0.setFont(font3)
        self.lineEdit_result_0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_28.addWidget(self.frame_5, 3, 1, 1, 2)

        self.textBrowser_background_data = QTextBrowser(self.groupBox_8)
        self.textBrowser_background_data.setObjectName(u"textBrowser_background_data")
        self.textBrowser_background_data.setMinimumSize(QSize(0, 10))
        self.textBrowser_background_data.setFont(font5)
        self.textBrowser_background_data.setReadOnly(False)

        self.gridLayout_28.addWidget(self.textBrowser_background_data, 6, 0, 1, 3)


        self.gridLayout_65.addWidget(self.groupBox_8, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.widget, 0, 2, 2, 1)

        self.widget_camera = QWidget(self.frame_camera)
        self.widget_camera.setObjectName(u"widget_camera")
        self.groupBox_monitor_cam = QGroupBox(self.widget_camera)
        self.groupBox_monitor_cam.setObjectName(u"groupBox_monitor_cam")
        self.groupBox_monitor_cam.setGeometry(QRect(480, 0, 320, 300))
        self.groupBox_monitor_cam.setMinimumSize(QSize(0, 10))
        self.groupBox_monitor_cam.setFont(font1)
        self.groupBox_monitor_cam.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_33 = QGridLayout(self.groupBox_monitor_cam)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.checkBox_monitor_cam = QCheckBox(self.groupBox_monitor_cam)
        self.checkBox_monitor_cam.setObjectName(u"checkBox_monitor_cam")
        self.checkBox_monitor_cam.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_33.addWidget(self.checkBox_monitor_cam, 0, 0, 1, 1)

        self.label_monitor_picture = QLabel(self.groupBox_monitor_cam)
        self.label_monitor_picture.setObjectName(u"label_monitor_picture")
        self.label_monitor_picture.setMinimumSize(QSize(300, 10))

        self.gridLayout_33.addWidget(self.label_monitor_picture, 1, 0, 1, 3)

        self.pushButton_NetCamera = QPushButton(self.groupBox_monitor_cam)
        self.pushButton_NetCamera.setObjectName(u"pushButton_NetCamera")
        self.pushButton_NetCamera.setMinimumSize(QSize(150, 0))

        self.gridLayout_33.addWidget(self.pushButton_NetCamera, 0, 1, 1, 1)

        self.groupBox_main_camera = QGroupBox(self.widget_camera)
        self.groupBox_main_camera.setObjectName(u"groupBox_main_camera")
        self.groupBox_main_camera.setGeometry(QRect(-10, 0, 320, 300))
        self.groupBox_main_camera.setMinimumSize(QSize(0, 10))
        self.groupBox_main_camera.setFont(font1)
        self.groupBox_main_camera.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_15 = QGridLayout(self.groupBox_main_camera)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.checkBox_main_camera = QCheckBox(self.groupBox_main_camera)
        self.checkBox_main_camera.setObjectName(u"checkBox_main_camera")
        self.checkBox_main_camera.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_15.addWidget(self.checkBox_main_camera, 0, 0, 1, 1)

        self.checkBox_main_camera_set = QCheckBox(self.groupBox_main_camera)
        self.checkBox_main_camera_set.setObjectName(u"checkBox_main_camera_set")

        self.gridLayout_15.addWidget(self.checkBox_main_camera_set, 0, 1, 1, 1)

        self.label_main_picture = QLabel(self.groupBox_main_camera)
        self.label_main_picture.setObjectName(u"label_main_picture")
        self.label_main_picture.setMinimumSize(QSize(300, 10))

        self.gridLayout_15.addWidget(self.label_main_picture, 1, 0, 1, 2)


        self.gridLayout_40.addWidget(self.widget_camera, 0, 1, 1, 1)


        self.gridLayout_26.addWidget(self.frame_camera, 1, 0, 1, 1)

        self.frame_11 = QFrame(self.tab_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 10))
        self.frame_11.setMaximumSize(QSize(16777215, 420))
        self.gridLayout_27 = QGridLayout(self.frame_11)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(9, 0, -1, 0)
        self.groupBox_14 = QGroupBox(self.frame_11)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(450, 420))
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
        self.groupBox_7.setMinimumSize(QSize(500, 420))
        self.groupBox_7.setMaximumSize(QSize(500, 16777215))
        self.groupBox_7.setFont(font1)
        self.gridLayout_4 = QGridLayout(self.groupBox_7)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tableWidget_Ranking = QTableWidget(self.groupBox_7)
        if (self.tableWidget_Ranking.columnCount() < 5):
            self.tableWidget_Ranking.setColumnCount(5)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(0, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(1, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(2, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(3, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableWidget_Ranking.setHorizontalHeaderItem(4, __qtablewidgetitem51)
        self.tableWidget_Ranking.setObjectName(u"tableWidget_Ranking")
        self.tableWidget_Ranking.setMinimumSize(QSize(330, 10))
        self.tableWidget_Ranking.setMaximumSize(QSize(500, 16777215))
        self.tableWidget_Ranking.setFont(font6)
        self.tableWidget_Ranking.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_Ranking.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_Ranking.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_4.addWidget(self.tableWidget_Ranking, 0, 0, 1, 1)


        self.gridLayout_27.addWidget(self.groupBox_7, 0, 1, 1, 1)

        self.widget_20 = QWidget(self.frame_11)
        self.widget_20.setObjectName(u"widget_20")
        self.widget_20.setMinimumSize(QSize(320, 10))
        self.widget_20.setMaximumSize(QSize(200, 16777215))
        self.widget_20.setFont(font1)
        self.gridLayout_29 = QGridLayout(self.widget_20)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setContentsMargins(0, 0, 0, 0)
        self.groupBox_ranking = QGroupBox(self.widget_20)
        self.groupBox_ranking.setObjectName(u"groupBox_ranking")
        self.groupBox_ranking.setMinimumSize(QSize(0, 10))
        self.groupBox_ranking.setMaximumSize(QSize(16777215, 180))
        self.gridLayout_30 = QGridLayout(self.groupBox_ranking)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(-1, 0, -1, 6)
        self.label_15 = QLabel(self.groupBox_ranking)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_15, 2, 0, 1, 1)

        self.pushButton_save_Ranking = QPushButton(self.groupBox_ranking)
        self.pushButton_save_Ranking.setObjectName(u"pushButton_save_Ranking")
        self.pushButton_save_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.pushButton_save_Ranking, 4, 0, 1, 4)

        self.lineEdit_area_Ranking = QLineEdit(self.groupBox_ranking)
        self.lineEdit_area_Ranking.setObjectName(u"lineEdit_area_Ranking")
        self.lineEdit_area_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_area_Ranking, 1, 2, 1, 2)

        self.lineEdit_lap_Ranking = QLineEdit(self.groupBox_ranking)
        self.lineEdit_lap_Ranking.setObjectName(u"lineEdit_lap_Ranking")
        self.lineEdit_lap_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_lap_Ranking, 3, 2, 1, 2)

        self.lineEdit_Time_Restart_Ranking = QLineEdit(self.groupBox_ranking)
        self.lineEdit_Time_Restart_Ranking.setObjectName(u"lineEdit_Time_Restart_Ranking")
        self.lineEdit_Time_Restart_Ranking.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.lineEdit_Time_Restart_Ranking, 2, 2, 1, 2)

        self.label_13 = QLabel(self.groupBox_ranking)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_ranking)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 10))

        self.gridLayout_30.addWidget(self.label_14, 3, 0, 1, 1)

        self.pushButton_udp_time = QPushButton(self.groupBox_ranking)
        self.pushButton_udp_time.setObjectName(u"pushButton_udp_time")
        self.pushButton_udp_time.setMinimumSize(QSize(0, 10))
        self.pushButton_udp_time.setStyleSheet(u"background:rgb(0, 255, 0)")

        self.gridLayout_30.addWidget(self.pushButton_udp_time, 0, 0, 1, 4)


        self.gridLayout_29.addWidget(self.groupBox_ranking, 0, 0, 1, 1)

        self.groupBox_18 = QGroupBox(self.widget_20)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setMinimumSize(QSize(0, 10))
        self.groupBox_18.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_18.setFont(font1)
        self.gridLayout_67 = QGridLayout(self.groupBox_18)
        self.gridLayout_67.setObjectName(u"gridLayout_67")
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


        self.gridLayout_67.addWidget(self.groupBox_25, 0, 0, 1, 2)

        self.groupBox_33 = QGroupBox(self.groupBox_18)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.groupBox_33.setMinimumSize(QSize(0, 10))
        self.gridLayout_47 = QGridLayout(self.groupBox_33)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.label_41 = QLabel(self.groupBox_33)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(0, 10))
        self.label_41.setFont(font1)

        self.gridLayout_47.addWidget(self.label_41, 2, 0, 1, 1)

        self.lineEdit_time_count_ball = QLineEdit(self.groupBox_33)
        self.lineEdit_time_count_ball.setObjectName(u"lineEdit_time_count_ball")
        self.lineEdit_time_count_ball.setMinimumSize(QSize(0, 10))
        self.lineEdit_time_count_ball.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_47.addWidget(self.lineEdit_time_count_ball, 2, 1, 1, 1)

        self.label_28 = QLabel(self.groupBox_33)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 10))
        self.label_28.setFont(font1)

        self.gridLayout_47.addWidget(self.label_28, 0, 0, 1, 1)

        self.label_40 = QLabel(self.groupBox_33)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(0, 10))
        self.label_40.setFont(font1)

        self.gridLayout_47.addWidget(self.label_40, 2, 2, 1, 1)

        self.lineEdit_time_send_result = QLineEdit(self.groupBox_33)
        self.lineEdit_time_send_result.setObjectName(u"lineEdit_time_send_result")
        self.lineEdit_time_send_result.setMinimumSize(QSize(0, 10))
        self.lineEdit_time_send_result.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_47.addWidget(self.lineEdit_time_send_result, 0, 1, 1, 1)

        self.label_29 = QLabel(self.groupBox_33)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(0, 10))
        self.label_29.setFont(font1)

        self.gridLayout_47.addWidget(self.label_29, 0, 2, 1, 1)


        self.gridLayout_67.addWidget(self.groupBox_33, 1, 0, 1, 1)

        self.groupBox_37 = QGroupBox(self.groupBox_18)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setMinimumSize(QSize(0, 10))
        self.gridLayout_48 = QGridLayout(self.groupBox_37)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.pushButton_CardStop_2 = QPushButton(self.groupBox_37)
        self.pushButton_CardStop_2.setObjectName(u"pushButton_CardStop_2")
        self.pushButton_CardStop_2.setMinimumSize(QSize(0, 10))
        self.pushButton_CardStop_2.setFont(font1)
        self.pushButton_CardStop_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_CardStop_2.setStyleSheet(u"background:rgb(248,0,0)")
        self.pushButton_CardStop_2.setCheckable(False)
        self.pushButton_CardStop_2.setChecked(False)

        self.gridLayout_48.addWidget(self.pushButton_CardStop_2, 1, 1, 1, 1)

        self.pushButton_CardClose = QPushButton(self.groupBox_37)
        self.pushButton_CardClose.setObjectName(u"pushButton_CardClose")
        self.pushButton_CardClose.setMinimumSize(QSize(80, 0))
        self.pushButton_CardClose.setFont(font1)
        self.pushButton_CardClose.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_CardClose.setStyleSheet(u"background:rgb(255,240,0)")

        self.gridLayout_48.addWidget(self.pushButton_CardClose, 2, 1, 1, 1)

        self.pushButton_CardRun_2 = QPushButton(self.groupBox_37)
        self.pushButton_CardRun_2.setObjectName(u"pushButton_CardRun_2")
        self.pushButton_CardRun_2.setMinimumSize(QSize(0, 10))
        self.pushButton_CardRun_2.setFont(font1)
        self.pushButton_CardRun_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_CardRun_2.setStyleSheet(u"background:rgb(0,240,0)")

        self.gridLayout_48.addWidget(self.pushButton_CardRun_2, 0, 1, 1, 1)

        self.pushButton_Cardreset = QPushButton(self.groupBox_37)
        self.pushButton_Cardreset.setObjectName(u"pushButton_Cardreset")
        self.pushButton_Cardreset.setMinimumSize(QSize(80, 0))
        self.pushButton_Cardreset.setFont(font1)
        self.pushButton_Cardreset.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_Cardreset.setStyleSheet(u"background:rgb(0,255,220)")

        self.gridLayout_48.addWidget(self.pushButton_Cardreset, 3, 1, 1, 1)


        self.gridLayout_67.addWidget(self.groupBox_37, 1, 1, 2, 1)

        self.groupBox_24 = QGroupBox(self.groupBox_18)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMinimumSize(QSize(0, 10))
        self.gridLayout_43 = QGridLayout(self.groupBox_24)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.lineEdit_ball_start = QLineEdit(self.groupBox_24)
        self.lineEdit_ball_start.setObjectName(u"lineEdit_ball_start")
        self.lineEdit_ball_start.setMinimumSize(QSize(50, 10))
        self.lineEdit_ball_start.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_ball_start.setFont(font1)
        self.lineEdit_ball_start.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.lineEdit_ball_start.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_ball_start, 0, 2, 1, 1)

        self.lineEdit_ball_end = QLineEdit(self.groupBox_24)
        self.lineEdit_ball_end.setObjectName(u"lineEdit_ball_end")
        self.lineEdit_ball_end.setMinimumSize(QSize(50, 10))
        self.lineEdit_ball_end.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_ball_end.setFont(font1)
        self.lineEdit_ball_end.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.lineEdit_ball_end.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_ball_end, 1, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_24)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 10))
        self.label_7.setMaximumSize(QSize(150, 16777215))
        self.label_7.setFont(font1)

        self.gridLayout_43.addWidget(self.label_7, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_24)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 10))
        self.label_8.setMaximumSize(QSize(150, 16777215))
        self.label_8.setFont(font1)

        self.gridLayout_43.addWidget(self.label_8, 0, 1, 1, 1)

        self.frame_32 = QFrame(self.groupBox_24)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMinimumSize(QSize(20, 10))
        self.frame_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_43.addWidget(self.frame_32, 1, 3, 1, 1)

        self.frame_31 = QFrame(self.groupBox_24)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMinimumSize(QSize(20, 10))
        self.frame_31.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_43.addWidget(self.frame_31, 0, 3, 1, 1)


        self.gridLayout_67.addWidget(self.groupBox_24, 2, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_18, 1, 0, 1, 1)


        self.gridLayout_27.addWidget(self.widget_20, 0, 3, 1, 1)


        self.gridLayout_26.addWidget(self.frame_11, 0, 0, 1, 1)

        self.tabWidget_Ranking.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_36 = QGridLayout(self.tab_4)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.gridLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_zzw_2 = QFrame(self.tab_4)
        self.frame_zzw_2.setObjectName(u"frame_zzw_2")
        self.frame_zzw_2.setMaximumSize(QSize(500, 16777215))
        self.frame_zzw_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_zzw_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_54 = QGridLayout(self.frame_zzw_2)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.gridLayout_54.setContentsMargins(0, 0, -1, -1)
        self.groupBox_32 = QGroupBox(self.frame_zzw_2)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setMinimumSize(QSize(0, 0))
        self.groupBox_32.setMaximumSize(QSize(600, 150))
        self.groupBox_32.setFont(font1)
        self.gridLayout_58 = QGridLayout(self.groupBox_32)
        self.gridLayout_58.setObjectName(u"gridLayout_58")
        self.lineEdit_start_count = QLineEdit(self.groupBox_32)
        self.lineEdit_start_count.setObjectName(u"lineEdit_start_count")
        self.lineEdit_start_count.setMinimumSize(QSize(0, 0))
        self.lineEdit_start_count.setFont(font5)
        self.lineEdit_start_count.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_start_count, 0, 3, 1, 1)

        self.checkBox_shoot2 = QCheckBox(self.groupBox_32)
        self.checkBox_shoot2.setObjectName(u"checkBox_shoot2")
        self.checkBox_shoot2.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_shoot2, 3, 2, 1, 1)

        self.lineEdit_alarm = QLineEdit(self.groupBox_32)
        self.lineEdit_alarm.setObjectName(u"lineEdit_alarm")
        self.lineEdit_alarm.setMinimumSize(QSize(0, 0))
        self.lineEdit_alarm.setFont(font5)
        self.lineEdit_alarm.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_alarm.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_alarm, 2, 3, 1, 1)

        self.checkBox_start_2 = QCheckBox(self.groupBox_32)
        self.checkBox_start_2.setObjectName(u"checkBox_start_2")
        self.checkBox_start_2.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_start_2, 2, 0, 1, 1)

        self.lineEdit_shoot_3 = QLineEdit(self.groupBox_32)
        self.lineEdit_shoot_3.setObjectName(u"lineEdit_shoot_3")
        self.lineEdit_shoot_3.setMinimumSize(QSize(0, 0))
        self.lineEdit_shoot_3.setFont(font5)
        self.lineEdit_shoot_3.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_shoot_3, 4, 3, 1, 1)

        self.checkBox_end_2 = QCheckBox(self.groupBox_32)
        self.checkBox_end_2.setObjectName(u"checkBox_end_2")
        self.checkBox_end_2.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_end_2, 4, 0, 1, 1)

        self.checkBox_alarm_2 = QCheckBox(self.groupBox_32)
        self.checkBox_alarm_2.setObjectName(u"checkBox_alarm_2")
        self.checkBox_alarm_2.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_alarm_2, 2, 2, 1, 1)

        self.lineEdit_start = QLineEdit(self.groupBox_32)
        self.lineEdit_start.setObjectName(u"lineEdit_start")
        self.lineEdit_start.setMinimumSize(QSize(0, 0))
        self.lineEdit_start.setFont(font5)
        self.lineEdit_start.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_start, 2, 1, 1, 1)

        self.lineEdit_end = QLineEdit(self.groupBox_32)
        self.lineEdit_end.setObjectName(u"lineEdit_end")
        self.lineEdit_end.setMinimumSize(QSize(0, 0))
        self.lineEdit_end.setFont(font5)
        self.lineEdit_end.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_end, 4, 1, 1, 1)

        self.checkBox_shoot3 = QCheckBox(self.groupBox_32)
        self.checkBox_shoot3.setObjectName(u"checkBox_shoot3")
        self.checkBox_shoot3.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_shoot3, 4, 2, 1, 1)

        self.lineEdit_shoot = QLineEdit(self.groupBox_32)
        self.lineEdit_shoot.setObjectName(u"lineEdit_shoot")
        self.lineEdit_shoot.setMinimumSize(QSize(0, 0))
        self.lineEdit_shoot.setFont(font5)
        self.lineEdit_shoot.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_shoot, 0, 1, 1, 1)

        self.lineEdit_shoot_2 = QLineEdit(self.groupBox_32)
        self.lineEdit_shoot_2.setObjectName(u"lineEdit_shoot_2")
        self.lineEdit_shoot_2.setMinimumSize(QSize(0, 0))
        self.lineEdit_shoot_2.setFont(font5)
        self.lineEdit_shoot_2.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_shoot_2, 3, 3, 1, 1)

        self.checkBox_shake = QCheckBox(self.groupBox_32)
        self.checkBox_shake.setObjectName(u"checkBox_shake")
        self.checkBox_shake.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_shake, 3, 0, 1, 1)

        self.checkBox_start_count = QCheckBox(self.groupBox_32)
        self.checkBox_start_count.setObjectName(u"checkBox_start_count")
        self.checkBox_start_count.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_start_count, 0, 2, 1, 1)

        self.checkBox_shoot1 = QCheckBox(self.groupBox_32)
        self.checkBox_shoot1.setObjectName(u"checkBox_shoot1")
        self.checkBox_shoot1.setFont(font6)

        self.gridLayout_58.addWidget(self.checkBox_shoot1, 0, 0, 1, 1)

        self.lineEdit_shake = QLineEdit(self.groupBox_32)
        self.lineEdit_shake.setObjectName(u"lineEdit_shake")
        self.lineEdit_shake.setMinimumSize(QSize(0, 0))
        self.lineEdit_shake.setFont(font5)
        self.lineEdit_shake.setReadOnly(False)

        self.gridLayout_58.addWidget(self.lineEdit_shake, 3, 1, 1, 1)


        self.gridLayout_54.addWidget(self.groupBox_32, 4, 0, 1, 1)

        self.groupBox_26 = QGroupBox(self.frame_zzw_2)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.groupBox_26.setMinimumSize(QSize(0, 0))
        self.groupBox_26.setMaximumSize(QSize(600, 150))
        self.groupBox_26.setFont(font1)
        self.gridLayout_53 = QGridLayout(self.groupBox_26)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.lineEdit_music_3 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_3.setObjectName(u"lineEdit_music_3")
        self.lineEdit_music_3.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_3.setFont(font5)
        self.lineEdit_music_3.setReadOnly(False)

        self.gridLayout_53.addWidget(self.lineEdit_music_3, 4, 1, 1, 2)

        self.radioButton_music_background_2 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_2.setObjectName(u"radioButton_music_background_2")
        self.radioButton_music_background_2.setFont(font6)
        self.radioButton_music_background_2.setChecked(True)

        self.gridLayout_53.addWidget(self.radioButton_music_background_2, 3, 0, 1, 1)

        self.lineEdit_music_2 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_2.setObjectName(u"lineEdit_music_2")
        self.lineEdit_music_2.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_2.setFont(font5)
        self.lineEdit_music_2.setReadOnly(False)

        self.gridLayout_53.addWidget(self.lineEdit_music_2, 3, 1, 1, 2)

        self.radioButton_music_background_1 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_1.setObjectName(u"radioButton_music_background_1")
        self.radioButton_music_background_1.setFont(font6)

        self.gridLayout_53.addWidget(self.radioButton_music_background_1, 2, 0, 1, 1)

        self.lineEdit_music_1 = QLineEdit(self.groupBox_26)
        self.lineEdit_music_1.setObjectName(u"lineEdit_music_1")
        self.lineEdit_music_1.setMinimumSize(QSize(300, 0))
        self.lineEdit_music_1.setFont(font5)
        self.lineEdit_music_1.setReadOnly(False)

        self.gridLayout_53.addWidget(self.lineEdit_music_1, 2, 1, 1, 2)

        self.radioButton_music_background_3 = QRadioButton(self.groupBox_26)
        self.radioButton_music_background_3.setObjectName(u"radioButton_music_background_3")
        self.radioButton_music_background_3.setFont(font6)

        self.gridLayout_53.addWidget(self.radioButton_music_background_3, 4, 0, 1, 1)


        self.gridLayout_54.addWidget(self.groupBox_26, 0, 0, 1, 1)

        self.groupBox_30 = QGroupBox(self.frame_zzw_2)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.groupBox_30.setMinimumSize(QSize(0, 0))
        self.groupBox_30.setMaximumSize(QSize(600, 230))
        self.groupBox_30.setFont(font1)
        self.gridLayout_56 = QGridLayout(self.groupBox_30)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.lineEdit_scene_name = QLineEdit(self.groupBox_30)
        self.lineEdit_scene_name.setObjectName(u"lineEdit_scene_name")
        self.lineEdit_scene_name.setMinimumSize(QSize(300, 0))
        self.lineEdit_scene_name.setFont(font5)
        self.lineEdit_scene_name.setReadOnly(False)

        self.gridLayout_56.addWidget(self.lineEdit_scene_name, 1, 1, 1, 1)

        self.label_65 = QLabel(self.groupBox_30)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setFont(font6)

        self.gridLayout_56.addWidget(self.label_65, 1, 0, 1, 1)

        self.groupBox_31 = QGroupBox(self.groupBox_30)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMinimumSize(QSize(0, 0))
        self.groupBox_31.setMaximumSize(QSize(600, 180))
        self.groupBox_31.setFont(font1)
        self.gridLayout_57 = QGridLayout(self.groupBox_31)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.label_69 = QLabel(self.groupBox_31)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFont(font6)

        self.gridLayout_57.addWidget(self.label_69, 2, 0, 1, 1)

        self.lineEdit_source_end = QLineEdit(self.groupBox_31)
        self.lineEdit_source_end.setObjectName(u"lineEdit_source_end")
        self.lineEdit_source_end.setMinimumSize(QSize(300, 0))
        self.lineEdit_source_end.setFont(font5)
        self.lineEdit_source_end.setReadOnly(False)

        self.gridLayout_57.addWidget(self.lineEdit_source_end, 4, 1, 1, 1)

        self.lineEdit_source_picture = QLineEdit(self.groupBox_31)
        self.lineEdit_source_picture.setObjectName(u"lineEdit_source_picture")
        self.lineEdit_source_picture.setMinimumSize(QSize(300, 0))
        self.lineEdit_source_picture.setFont(font5)
        self.lineEdit_source_picture.setReadOnly(False)

        self.gridLayout_57.addWidget(self.lineEdit_source_picture, 1, 1, 1, 1)

        self.lineEdit_source_settlement = QLineEdit(self.groupBox_31)
        self.lineEdit_source_settlement.setObjectName(u"lineEdit_source_settlement")
        self.lineEdit_source_settlement.setMinimumSize(QSize(300, 0))
        self.lineEdit_source_settlement.setFont(font5)
        self.lineEdit_source_settlement.setReadOnly(False)

        self.gridLayout_57.addWidget(self.lineEdit_source_settlement, 2, 1, 1, 1)

        self.label_67 = QLabel(self.groupBox_31)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font6)

        self.gridLayout_57.addWidget(self.label_67, 0, 0, 1, 1)

        self.lineEdit_source_ranking = QLineEdit(self.groupBox_31)
        self.lineEdit_source_ranking.setObjectName(u"lineEdit_source_ranking")
        self.lineEdit_source_ranking.setMinimumSize(QSize(300, 0))
        self.lineEdit_source_ranking.setFont(font5)
        self.lineEdit_source_ranking.setReadOnly(False)

        self.gridLayout_57.addWidget(self.lineEdit_source_ranking, 0, 1, 1, 1)

        self.label_68 = QLabel(self.groupBox_31)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setFont(font6)

        self.gridLayout_57.addWidget(self.label_68, 1, 0, 1, 1)

        self.label_70 = QLabel(self.groupBox_31)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setFont(font6)

        self.gridLayout_57.addWidget(self.label_70, 4, 0, 1, 1)


        self.gridLayout_56.addWidget(self.groupBox_31, 2, 0, 1, 2)


        self.gridLayout_54.addWidget(self.groupBox_30, 2, 0, 1, 1)

        self.groupBox_28 = QGroupBox(self.frame_zzw_2)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.groupBox_28.setFont(font1)
        self.gridLayout_59 = QGridLayout(self.groupBox_28)
        self.gridLayout_59.setObjectName(u"gridLayout_59")
        self.textBrowser_save_msg = QTextBrowser(self.groupBox_28)
        self.textBrowser_save_msg.setObjectName(u"textBrowser_save_msg")
        self.textBrowser_save_msg.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textBrowser_save_msg.setReadOnly(False)

        self.gridLayout_59.addWidget(self.textBrowser_save_msg, 0, 2, 1, 1)


        self.gridLayout_54.addWidget(self.groupBox_28, 5, 0, 1, 1)

        self.groupBox_29 = QGroupBox(self.frame_zzw_2)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(0, 0))
        self.groupBox_29.setMaximumSize(QSize(600, 130))
        self.groupBox_29.setFont(font1)
        self.gridLayout_55 = QGridLayout(self.groupBox_29)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.lineEdit_map_picture = QLineEdit(self.groupBox_29)
        self.lineEdit_map_picture.setObjectName(u"lineEdit_map_picture")
        self.lineEdit_map_picture.setMinimumSize(QSize(200, 0))
        self.lineEdit_map_picture.setFont(font5)
        self.lineEdit_map_picture.setReadOnly(False)

        self.gridLayout_55.addWidget(self.lineEdit_map_picture, 0, 1, 1, 1)

        self.label_47 = QLabel(self.groupBox_29)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font6)

        self.gridLayout_55.addWidget(self.label_47, 0, 0, 1, 1)

        self.label_48 = QLabel(self.groupBox_29)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font6)

        self.gridLayout_55.addWidget(self.label_48, 1, 0, 1, 1)

        self.label_83 = QLabel(self.groupBox_29)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setFont(font6)

        self.gridLayout_55.addWidget(self.label_83, 0, 2, 1, 1)

        self.lineEdit_map_size = QLineEdit(self.groupBox_29)
        self.lineEdit_map_size.setObjectName(u"lineEdit_map_size")
        self.lineEdit_map_size.setMinimumSize(QSize(30, 0))
        self.lineEdit_map_size.setFont(font5)
        self.lineEdit_map_size.setReadOnly(False)

        self.gridLayout_55.addWidget(self.lineEdit_map_size, 0, 3, 1, 1)

        self.lineEdit_map_line = QLineEdit(self.groupBox_29)
        self.lineEdit_map_line.setObjectName(u"lineEdit_map_line")
        self.lineEdit_map_line.setMinimumSize(QSize(300, 0))
        self.lineEdit_map_line.setFont(font5)
        self.lineEdit_map_line.setReadOnly(False)

        self.gridLayout_55.addWidget(self.lineEdit_map_line, 1, 1, 1, 3)


        self.gridLayout_54.addWidget(self.groupBox_29, 1, 0, 1, 1)

        self.groupBox_35 = QGroupBox(self.frame_zzw_2)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setMinimumSize(QSize(0, 0))
        self.groupBox_35.setMaximumSize(QSize(600, 300))
        self.groupBox_35.setFont(font1)
        self.gridLayout_62 = QGridLayout(self.groupBox_35)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.label_86 = QLabel(self.groupBox_35)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setFont(font6)

        self.gridLayout_62.addWidget(self.label_86, 0, 0, 1, 1)

        self.lineEdit_saidao_Path = QLineEdit(self.groupBox_35)
        self.lineEdit_saidao_Path.setObjectName(u"lineEdit_saidao_Path")
        self.lineEdit_saidao_Path.setMinimumSize(QSize(100, 0))
        self.lineEdit_saidao_Path.setFont(font5)
        self.lineEdit_saidao_Path.setReadOnly(False)

        self.gridLayout_62.addWidget(self.lineEdit_saidao_Path, 0, 1, 1, 1)

        self.label_94 = QLabel(self.groupBox_35)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setFont(font6)

        self.gridLayout_62.addWidget(self.label_94, 0, 2, 1, 1)

        self.lineEdit_end1_Path = QLineEdit(self.groupBox_35)
        self.lineEdit_end1_Path.setObjectName(u"lineEdit_end1_Path")
        self.lineEdit_end1_Path.setMinimumSize(QSize(100, 0))
        self.lineEdit_end1_Path.setFont(font5)
        self.lineEdit_end1_Path.setReadOnly(False)

        self.gridLayout_62.addWidget(self.lineEdit_end1_Path, 0, 3, 1, 1)

        self.label_93 = QLabel(self.groupBox_35)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setFont(font6)

        self.gridLayout_62.addWidget(self.label_93, 1, 0, 1, 1)

        self.lineEdit_upload_Path = QLineEdit(self.groupBox_35)
        self.lineEdit_upload_Path.setObjectName(u"lineEdit_upload_Path")
        self.lineEdit_upload_Path.setMinimumSize(QSize(100, 0))
        self.lineEdit_upload_Path.setFont(font5)
        self.lineEdit_upload_Path.setReadOnly(False)

        self.gridLayout_62.addWidget(self.lineEdit_upload_Path, 1, 1, 1, 1)

        self.label_95 = QLabel(self.groupBox_35)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setFont(font6)

        self.gridLayout_62.addWidget(self.label_95, 1, 2, 1, 1)

        self.lineEdit_end2_Path = QLineEdit(self.groupBox_35)
        self.lineEdit_end2_Path.setObjectName(u"lineEdit_end2_Path")
        self.lineEdit_end2_Path.setMinimumSize(QSize(100, 0))
        self.lineEdit_end2_Path.setFont(font5)
        self.lineEdit_end2_Path.setReadOnly(False)

        self.gridLayout_62.addWidget(self.lineEdit_end2_Path, 1, 3, 1, 1)

        self.groupBox_36 = QGroupBox(self.groupBox_35)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setMinimumSize(QSize(0, 0))
        self.groupBox_36.setMaximumSize(QSize(600, 130))
        self.groupBox_36.setFont(font1)
        self.gridLayout_63 = QGridLayout(self.groupBox_36)
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.gridLayout_63.setContentsMargins(-1, 0, -1, 9)
        self.label_91 = QLabel(self.groupBox_36)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setFont(font6)

        self.gridLayout_63.addWidget(self.label_91, 0, 0, 1, 1)

        self.label_90 = QLabel(self.groupBox_36)
        self.label_90.setObjectName(u"label_90")
        self.label_90.setFont(font6)

        self.gridLayout_63.addWidget(self.label_90, 0, 2, 1, 1)

        self.lineEdit_sony_sort = QLineEdit(self.groupBox_36)
        self.lineEdit_sony_sort.setObjectName(u"lineEdit_sony_sort")
        self.lineEdit_sony_sort.setMinimumSize(QSize(30, 0))
        self.lineEdit_sony_sort.setFont(font5)
        self.lineEdit_sony_sort.setReadOnly(False)

        self.gridLayout_63.addWidget(self.lineEdit_sony_sort, 0, 1, 1, 1)

        self.lineEdit_monitor_sort = QLineEdit(self.groupBox_36)
        self.lineEdit_monitor_sort.setObjectName(u"lineEdit_monitor_sort")
        self.lineEdit_monitor_sort.setMinimumSize(QSize(30, 0))
        self.lineEdit_monitor_sort.setFont(font5)
        self.lineEdit_monitor_sort.setReadOnly(False)

        self.gridLayout_63.addWidget(self.lineEdit_monitor_sort, 0, 3, 1, 1)


        self.gridLayout_62.addWidget(self.groupBox_36, 2, 0, 1, 4)


        self.gridLayout_54.addWidget(self.groupBox_35, 3, 0, 1, 1)


        self.gridLayout_36.addWidget(self.frame_zzw_2, 0, 1, 2, 1)

        self.frame_zzw_1 = QFrame(self.tab_4)
        self.frame_zzw_1.setObjectName(u"frame_zzw_1")
        self.frame_zzw_1.setMaximumSize(QSize(600, 16777215))
        self.frame_zzw_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_zzw_1.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_51 = QGridLayout(self.frame_zzw_1)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.gridLayout_51.setContentsMargins(-1, 0, -1, -1)
        self.groupBox_17 = QGroupBox(self.frame_zzw_1)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setMinimumSize(QSize(0, 0))
        self.groupBox_17.setMaximumSize(QSize(600, 150))
        self.groupBox_17.setFont(font1)
        self.gridLayout_35 = QGridLayout(self.groupBox_17)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.label_80 = QLabel(self.groupBox_17)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setFont(font6)

        self.gridLayout_35.addWidget(self.label_80, 0, 3, 1, 1)

        self.label_79 = QLabel(self.groupBox_17)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setFont(font6)

        self.gridLayout_35.addWidget(self.label_79, 5, 0, 1, 1)

        self.label_38 = QLabel(self.groupBox_17)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font6)

        self.gridLayout_35.addWidget(self.label_38, 2, 0, 1, 2)

        self.label_36 = QLabel(self.groupBox_17)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font6)

        self.gridLayout_35.addWidget(self.label_36, 1, 0, 1, 2)

        self.lineEdit_cardNo = QLineEdit(self.groupBox_17)
        self.lineEdit_cardNo.setObjectName(u"lineEdit_cardNo")
        self.lineEdit_cardNo.setFont(font5)
        self.lineEdit_cardNo.setReadOnly(False)

        self.gridLayout_35.addWidget(self.lineEdit_cardNo, 0, 2, 1, 1)

        self.lineEdit_s485_Axis_No = QLineEdit(self.groupBox_17)
        self.lineEdit_s485_Axis_No.setObjectName(u"lineEdit_s485_Axis_No")
        self.lineEdit_s485_Axis_No.setFont(font5)
        self.lineEdit_s485_Axis_No.setReadOnly(False)

        self.gridLayout_35.addWidget(self.lineEdit_s485_Axis_No, 1, 2, 1, 3)

        self.lineEdit_Track_number = QLineEdit(self.groupBox_17)
        self.lineEdit_Track_number.setObjectName(u"lineEdit_Track_number")
        self.lineEdit_Track_number.setFont(font5)
        self.lineEdit_Track_number.setReadOnly(False)

        self.gridLayout_35.addWidget(self.lineEdit_Track_number, 0, 4, 1, 1)

        self.label_33 = QLabel(self.groupBox_17)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font6)

        self.gridLayout_35.addWidget(self.label_33, 0, 0, 1, 2)

        self.lineEdit_s485_Cam_No = QLineEdit(self.groupBox_17)
        self.lineEdit_s485_Cam_No.setObjectName(u"lineEdit_s485_Cam_No")
        self.lineEdit_s485_Cam_No.setFont(font5)

        self.gridLayout_35.addWidget(self.lineEdit_s485_Cam_No, 2, 2, 1, 3)

        self.lineEdit_five_axis = QLineEdit(self.groupBox_17)
        self.lineEdit_five_axis.setObjectName(u"lineEdit_five_axis")
        self.lineEdit_five_axis.setFont(font5)

        self.gridLayout_35.addWidget(self.lineEdit_five_axis, 5, 2, 1, 1)

        self.label_81 = QLabel(self.groupBox_17)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setFont(font6)

        self.gridLayout_35.addWidget(self.label_81, 5, 3, 1, 1)

        self.lineEdit_five_key = QLineEdit(self.groupBox_17)
        self.lineEdit_five_key.setObjectName(u"lineEdit_five_key")
        self.lineEdit_five_key.setFont(font5)

        self.gridLayout_35.addWidget(self.lineEdit_five_key, 5, 4, 1, 1)


        self.gridLayout_51.addWidget(self.groupBox_17, 2, 0, 1, 1)

        self.groupBox_net = QGroupBox(self.frame_zzw_1)
        self.groupBox_net.setObjectName(u"groupBox_net")
        self.groupBox_net.setMinimumSize(QSize(0, 0))
        self.groupBox_net.setMaximumSize(QSize(600, 230))
        self.groupBox_net.setFont(font1)
        self.gridLayout_32 = QGridLayout(self.groupBox_net)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.label_82 = QLabel(self.groupBox_net)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setFont(font6)

        self.gridLayout_32.addWidget(self.label_82, 2, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox_net)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font6)

        self.gridLayout_32.addWidget(self.label_30, 1, 3, 1, 1)

        self.lineEdit_rtsp_url = QLineEdit(self.groupBox_net)
        self.lineEdit_rtsp_url.setObjectName(u"lineEdit_rtsp_url")
        self.lineEdit_rtsp_url.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_rtsp_url, 6, 1, 1, 4)

        self.label_19 = QLabel(self.groupBox_net)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font6)

        self.gridLayout_32.addWidget(self.label_19, 0, 3, 1, 1)

        self.lineEdit_TcpServer_ip = QLineEdit(self.groupBox_net)
        self.lineEdit_TcpServer_ip.setObjectName(u"lineEdit_TcpServer_ip")
        self.lineEdit_TcpServer_ip.setFont(font5)
        self.lineEdit_TcpServer_ip.setReadOnly(True)

        self.gridLayout_32.addWidget(self.lineEdit_TcpServer_ip, 1, 2, 1, 1)

        self.lineEdit_result_tcpServer_ip = QLineEdit(self.groupBox_net)
        self.lineEdit_result_tcpServer_ip.setObjectName(u"lineEdit_result_tcpServer_ip")
        self.lineEdit_result_tcpServer_ip.setFont(font5)
        self.lineEdit_result_tcpServer_ip.setReadOnly(True)

        self.gridLayout_32.addWidget(self.lineEdit_result_tcpServer_ip, 2, 2, 1, 1)

        self.lineEdit_obs_script_addr = QLineEdit(self.groupBox_net)
        self.lineEdit_obs_script_addr.setObjectName(u"lineEdit_obs_script_addr")
        self.lineEdit_obs_script_addr.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_obs_script_addr, 8, 1, 1, 4)

        self.label_34 = QLabel(self.groupBox_net)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font6)

        self.gridLayout_32.addWidget(self.label_34, 5, 0, 1, 2)

        self.lineEdit_wakeup_addr = QLineEdit(self.groupBox_net)
        self.lineEdit_wakeup_addr.setObjectName(u"lineEdit_wakeup_addr")
        self.lineEdit_wakeup_addr.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_wakeup_addr, 5, 2, 1, 3)

        self.lineEdit_UdpServer_ip = QLineEdit(self.groupBox_net)
        self.lineEdit_UdpServer_ip.setObjectName(u"lineEdit_UdpServer_ip")
        self.lineEdit_UdpServer_ip.setFont(font5)
        self.lineEdit_UdpServer_ip.setReadOnly(True)

        self.gridLayout_32.addWidget(self.lineEdit_UdpServer_ip, 0, 2, 1, 1)

        self.lineEdit_TcpServer_Port = QLineEdit(self.groupBox_net)
        self.lineEdit_TcpServer_Port.setObjectName(u"lineEdit_TcpServer_Port")
        self.lineEdit_TcpServer_Port.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_TcpServer_Port, 1, 4, 1, 1)

        self.label_46 = QLabel(self.groupBox_net)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font6)

        self.gridLayout_32.addWidget(self.label_46, 8, 0, 1, 1)

        self.lineEdit_UdpServer_Port = QLineEdit(self.groupBox_net)
        self.lineEdit_UdpServer_Port.setObjectName(u"lineEdit_UdpServer_Port")
        self.lineEdit_UdpServer_Port.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_UdpServer_Port, 0, 4, 1, 1)

        self.lineEdit_recognition_addr = QLineEdit(self.groupBox_net)
        self.lineEdit_recognition_addr.setObjectName(u"lineEdit_recognition_addr")
        self.lineEdit_recognition_addr.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_recognition_addr, 7, 1, 1, 4)

        self.label_32 = QLabel(self.groupBox_net)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font6)

        self.gridLayout_32.addWidget(self.label_32, 6, 0, 1, 1)

        self.label_45 = QLabel(self.groupBox_net)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font6)

        self.gridLayout_32.addWidget(self.label_45, 7, 0, 1, 1)

        self.lineEdit_result_tcpServer_port = QLineEdit(self.groupBox_net)
        self.lineEdit_result_tcpServer_port.setObjectName(u"lineEdit_result_tcpServer_port")
        self.lineEdit_result_tcpServer_port.setFont(font5)

        self.gridLayout_32.addWidget(self.lineEdit_result_tcpServer_port, 2, 4, 1, 1)

        self.label_31 = QLabel(self.groupBox_net)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font6)

        self.gridLayout_32.addWidget(self.label_31, 1, 0, 1, 2)

        self.label_17 = QLabel(self.groupBox_net)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font6)

        self.gridLayout_32.addWidget(self.label_17, 0, 0, 1, 2)

        self.label_92 = QLabel(self.groupBox_net)
        self.label_92.setObjectName(u"label_92")
        self.label_92.setFont(font6)

        self.gridLayout_32.addWidget(self.label_92, 2, 3, 1, 1)


        self.gridLayout_51.addWidget(self.groupBox_net, 1, 0, 1, 1)

        self.groupBox_balls = QGroupBox(self.frame_zzw_1)
        self.groupBox_balls.setObjectName(u"groupBox_balls")
        self.groupBox_balls.setFont(font1)
        self.gridLayout_38 = QGridLayout(self.groupBox_balls)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.lineEdit_balls_count = QLineEdit(self.groupBox_balls)
        self.lineEdit_balls_count.setObjectName(u"lineEdit_balls_count")
        self.lineEdit_balls_count.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_balls_count.setFont(font5)
        self.lineEdit_balls_count.setReadOnly(False)

        self.gridLayout_38.addWidget(self.lineEdit_balls_count, 0, 1, 1, 1)

        self.label_35 = QLabel(self.groupBox_balls)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font6)

        self.gridLayout_38.addWidget(self.label_35, 0, 0, 1, 1)

        self.frame_25 = QFrame(self.groupBox_balls)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(300, 0))
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_38.addWidget(self.frame_25, 0, 2, 1, 1)

        self.groupBox_15 = QGroupBox(self.groupBox_balls)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMaximumSize(QSize(600, 600))
        self.groupBox_15.setFont(font1)
        self.gridLayout_52 = QGridLayout(self.groupBox_15)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.label_62 = QLabel(self.groupBox_15)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font6)

        self.gridLayout_52.addWidget(self.label_62, 9, 5, 1, 1)

        self.lineEdit_Color_Eng_5 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_5.setObjectName(u"lineEdit_Color_Eng_5")
        self.lineEdit_Color_Eng_5.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_5.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_5.setFont(font5)
        self.lineEdit_Color_Eng_5.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_5, 5, 2, 1, 1)

        self.lineEdit_Color_Ch_3 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_3.setObjectName(u"lineEdit_Color_Ch_3")
        self.lineEdit_Color_Ch_3.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_3.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_3, 3, 7, 1, 2)

        self.lineEdit_Color_Eng_4 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_4.setObjectName(u"lineEdit_Color_Eng_4")
        self.lineEdit_Color_Eng_4.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_4.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_4.setFont(font5)
        self.lineEdit_Color_Eng_4.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_4, 4, 2, 1, 2)

        self.label_63 = QLabel(self.groupBox_15)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font6)

        self.gridLayout_52.addWidget(self.label_63, 9, 0, 1, 1)

        self.lineEdit_Color_Eng_3 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_3.setObjectName(u"lineEdit_Color_Eng_3")
        self.lineEdit_Color_Eng_3.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_3.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_3.setFont(font5)
        self.lineEdit_Color_Eng_3.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_3, 3, 2, 1, 1)

        self.label_64 = QLabel(self.groupBox_15)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFont(font6)

        self.gridLayout_52.addWidget(self.label_64, 10, 5, 1, 1)

        self.label_59 = QLabel(self.groupBox_15)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font6)

        self.gridLayout_52.addWidget(self.label_59, 6, 0, 1, 1)

        self.lineEdit_Color_Eng_10 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_10.setObjectName(u"lineEdit_Color_Eng_10")
        self.lineEdit_Color_Eng_10.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_10.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_10.setFont(font5)
        self.lineEdit_Color_Eng_10.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_10, 10, 2, 1, 1)

        self.lineEdit_Color_Eng_8 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_8.setObjectName(u"lineEdit_Color_Eng_8")
        self.lineEdit_Color_Eng_8.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_8.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_8.setFont(font5)
        self.lineEdit_Color_Eng_8.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_8, 8, 2, 1, 1)

        self.lineEdit_Color_Ch_2 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_2.setObjectName(u"lineEdit_Color_Ch_2")
        self.lineEdit_Color_Ch_2.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_2.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_2, 2, 7, 1, 2)

        self.label_56 = QLabel(self.groupBox_15)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFont(font6)

        self.gridLayout_52.addWidget(self.label_56, 8, 0, 1, 2)

        self.label_39 = QLabel(self.groupBox_15)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font6)

        self.gridLayout_52.addWidget(self.label_39, 3, 5, 1, 1)

        self.label_37 = QLabel(self.groupBox_15)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font6)

        self.gridLayout_52.addWidget(self.label_37, 3, 0, 1, 1)

        self.label_55 = QLabel(self.groupBox_15)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font6)

        self.gridLayout_52.addWidget(self.label_55, 8, 5, 1, 1)

        self.label_50 = QLabel(self.groupBox_15)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font6)

        self.gridLayout_52.addWidget(self.label_50, 0, 0, 1, 1)

        self.lineEdit_Color_Eng_1 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_1.setObjectName(u"lineEdit_Color_Eng_1")
        self.lineEdit_Color_Eng_1.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_1.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_1.setFont(font5)
        self.lineEdit_Color_Eng_1.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_1, 0, 2, 1, 2)

        self.label_44 = QLabel(self.groupBox_15)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font6)

        self.gridLayout_52.addWidget(self.label_44, 4, 0, 1, 1)

        self.lineEdit_Color_Eng_2 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_2.setObjectName(u"lineEdit_Color_Eng_2")
        self.lineEdit_Color_Eng_2.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_2.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_2.setFont(font5)
        self.lineEdit_Color_Eng_2.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_2, 2, 2, 1, 1)

        self.label_57 = QLabel(self.groupBox_15)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font6)

        self.gridLayout_52.addWidget(self.label_57, 6, 5, 1, 1)

        self.lineEdit_Color_Eng_7 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_7.setObjectName(u"lineEdit_Color_Eng_7")
        self.lineEdit_Color_Eng_7.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_7.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_7.setFont(font5)
        self.lineEdit_Color_Eng_7.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_7, 7, 2, 1, 1)

        self.label_52 = QLabel(self.groupBox_15)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font6)

        self.gridLayout_52.addWidget(self.label_52, 2, 0, 1, 1)

        self.lineEdit_Color_Ch_1 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_1.setObjectName(u"lineEdit_Color_Ch_1")
        self.lineEdit_Color_Ch_1.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_1.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_1, 0, 7, 1, 2)

        self.label_61 = QLabel(self.groupBox_15)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFont(font6)

        self.gridLayout_52.addWidget(self.label_61, 10, 0, 1, 1)

        self.label_54 = QLabel(self.groupBox_15)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font6)

        self.gridLayout_52.addWidget(self.label_54, 7, 0, 1, 2)

        self.label_53 = QLabel(self.groupBox_15)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font6)

        self.gridLayout_52.addWidget(self.label_53, 7, 5, 1, 1)

        self.lineEdit_Color_Eng_6 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_6.setObjectName(u"lineEdit_Color_Eng_6")
        self.lineEdit_Color_Eng_6.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_6.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_6.setFont(font5)
        self.lineEdit_Color_Eng_6.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_6, 6, 2, 1, 1)

        self.label_51 = QLabel(self.groupBox_15)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font6)

        self.gridLayout_52.addWidget(self.label_51, 2, 5, 1, 1)

        self.lineEdit_Color_Eng_9 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Eng_9.setObjectName(u"lineEdit_Color_Eng_9")
        self.lineEdit_Color_Eng_9.setMinimumSize(QSize(100, 0))
        self.lineEdit_Color_Eng_9.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_Color_Eng_9.setFont(font5)
        self.lineEdit_Color_Eng_9.setReadOnly(False)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Eng_9, 9, 2, 1, 1)

        self.label_49 = QLabel(self.groupBox_15)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font6)

        self.gridLayout_52.addWidget(self.label_49, 0, 5, 1, 1)

        self.label_60 = QLabel(self.groupBox_15)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font6)

        self.gridLayout_52.addWidget(self.label_60, 5, 0, 1, 2)

        self.label_58 = QLabel(self.groupBox_15)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setFont(font6)

        self.gridLayout_52.addWidget(self.label_58, 5, 5, 1, 1)

        self.label_43 = QLabel(self.groupBox_15)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font6)

        self.gridLayout_52.addWidget(self.label_43, 4, 5, 1, 2)

        self.lineEdit_Color_Ch_4 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_4.setObjectName(u"lineEdit_Color_Ch_4")
        self.lineEdit_Color_Ch_4.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_4.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_4, 4, 7, 1, 2)

        self.lineEdit_Color_Ch_5 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_5.setObjectName(u"lineEdit_Color_Ch_5")
        self.lineEdit_Color_Ch_5.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_5.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_5, 5, 7, 1, 2)

        self.lineEdit_Color_Ch_6 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_6.setObjectName(u"lineEdit_Color_Ch_6")
        self.lineEdit_Color_Ch_6.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_6.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_6, 6, 7, 1, 2)

        self.lineEdit_Color_Ch_7 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_7.setObjectName(u"lineEdit_Color_Ch_7")
        self.lineEdit_Color_Ch_7.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_7.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_7, 7, 7, 1, 2)

        self.lineEdit_Color_Ch_8 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_8.setObjectName(u"lineEdit_Color_Ch_8")
        self.lineEdit_Color_Ch_8.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_8.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_8, 8, 7, 1, 2)

        self.lineEdit_Color_Ch_9 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_9.setObjectName(u"lineEdit_Color_Ch_9")
        self.lineEdit_Color_Ch_9.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_9.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_9, 9, 7, 1, 2)

        self.lineEdit_Color_Ch_10 = QLineEdit(self.groupBox_15)
        self.lineEdit_Color_Ch_10.setObjectName(u"lineEdit_Color_Ch_10")
        self.lineEdit_Color_Ch_10.setMinimumSize(QSize(280, 0))
        self.lineEdit_Color_Ch_10.setFont(font5)

        self.gridLayout_52.addWidget(self.lineEdit_Color_Ch_10, 10, 7, 1, 2)


        self.gridLayout_38.addWidget(self.groupBox_15, 1, 0, 1, 4)

        self.pushButton_Save_Ball = QPushButton(self.groupBox_balls)
        self.pushButton_Save_Ball.setObjectName(u"pushButton_Save_Ball")

        self.gridLayout_38.addWidget(self.pushButton_Save_Ball, 0, 3, 1, 1)


        self.gridLayout_51.addWidget(self.groupBox_balls, 3, 0, 1, 1)


        self.gridLayout_36.addWidget(self.frame_zzw_1, 0, 0, 2, 1)

        self.groupBox_27 = QGroupBox(self.tab_4)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setMinimumSize(QSize(280, 0))
        self.groupBox_27.setFont(font1)
        self.gridLayout_66 = QGridLayout(self.groupBox_27)
        self.gridLayout_66.setObjectName(u"gridLayout_66")
        self.textBrowser_total_msg = QTextBrowser(self.groupBox_27)
        self.textBrowser_total_msg.setObjectName(u"textBrowser_total_msg")
        self.textBrowser_total_msg.setFont(font6)
        self.textBrowser_total_msg.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textBrowser_total_msg.setReadOnly(False)

        self.gridLayout_66.addWidget(self.textBrowser_total_msg, 5, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.groupBox_27)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 30))
        self.gridLayout_64 = QGridLayout(self.groupBox_5)
        self.gridLayout_64.setObjectName(u"gridLayout_64")
        self.gridLayout_64.setContentsMargins(-1, 3, -1, 9)
        self.checkBox_Flip_Horizontal = QCheckBox(self.groupBox_5)
        self.checkBox_Flip_Horizontal.setObjectName(u"checkBox_Flip_Horizontal")

        self.gridLayout_64.addWidget(self.checkBox_Flip_Horizontal, 0, 0, 1, 1)

        self.checkBox_Flip_Vertica = QCheckBox(self.groupBox_5)
        self.checkBox_Flip_Vertica.setObjectName(u"checkBox_Flip_Vertica")

        self.gridLayout_64.addWidget(self.checkBox_Flip_Vertica, 0, 1, 1, 1)


        self.gridLayout_66.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_20 = QGroupBox(self.groupBox_27)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setMinimumSize(QSize(50, 50))
        self.groupBox_20.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_20.setFont(font1)
        self.gridLayout_60 = QGridLayout(self.groupBox_20)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.gridLayout_60.setContentsMargins(-1, 3, -1, -1)
        self.checkBox_saveImgs_main = QCheckBox(self.groupBox_20)
        self.checkBox_saveImgs_main.setObjectName(u"checkBox_saveImgs_main")
        self.checkBox_saveImgs_main.setFont(font1)

        self.gridLayout_60.addWidget(self.checkBox_saveImgs_main, 0, 0, 1, 1)

        self.checkBox_saveImgs_monitor = QCheckBox(self.groupBox_20)
        self.checkBox_saveImgs_monitor.setObjectName(u"checkBox_saveImgs_monitor")
        self.checkBox_saveImgs_monitor.setFont(font1)

        self.gridLayout_60.addWidget(self.checkBox_saveImgs_monitor, 0, 1, 1, 1)

        self.checkBox_saveImgs_auto = QCheckBox(self.groupBox_20)
        self.checkBox_saveImgs_auto.setObjectName(u"checkBox_saveImgs_auto")
        self.checkBox_saveImgs_auto.setFont(font1)

        self.gridLayout_60.addWidget(self.checkBox_saveImgs_auto, 0, 2, 1, 1)


        self.gridLayout_66.addWidget(self.groupBox_20, 2, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.groupBox_27)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setMinimumSize(QSize(0, 50))
        self.groupBox_10.setMaximumSize(QSize(300, 50))
        self.groupBox_10.setFont(font1)
        self.gridLayout_18 = QGridLayout(self.groupBox_10)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(-1, 3, -1, -1)
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


        self.gridLayout_66.addWidget(self.groupBox_10, 1, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.groupBox_27)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(50, 50))
        self.groupBox_12.setMaximumSize(QSize(16777215, 16777215))
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


        self.gridLayout_66.addWidget(self.groupBox_12, 3, 0, 1, 1)

        self.groupBox_38 = QGroupBox(self.groupBox_27)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setMinimumSize(QSize(0, 0))
        self.groupBox_38.setMaximumSize(QSize(600, 130))
        self.groupBox_38.setFont(font1)
        self.gridLayout_68 = QGridLayout(self.groupBox_38)
        self.gridLayout_68.setObjectName(u"gridLayout_68")
        self.gridLayout_68.setContentsMargins(-1, 0, -1, 9)
        self.lineEdit_login = QLineEdit(self.groupBox_38)
        self.lineEdit_login.setObjectName(u"lineEdit_login")
        self.lineEdit_login.setMinimumSize(QSize(30, 0))
        self.lineEdit_login.setFont(font5)
        self.lineEdit_login.setReadOnly(False)

        self.gridLayout_68.addWidget(self.lineEdit_login, 0, 1, 1, 1)

        self.label_96 = QLabel(self.groupBox_38)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setFont(font6)

        self.gridLayout_68.addWidget(self.label_96, 0, 0, 1, 1)


        self.gridLayout_66.addWidget(self.groupBox_38, 4, 0, 1, 1)


        self.gridLayout_36.addWidget(self.groupBox_27, 0, 2, 2, 1)

        self.tabWidget_Ranking.addTab(self.tab_4, "")

        self.gridLayout.addWidget(self.tabWidget_Ranking, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget_Ranking.setCurrentIndex(0)
        self.pushButton_start_game.setDefault(True)
        self.pushButton_ready.setDefault(True)
        self.pushButton_start_game_2.setDefault(True)
        self.pushButton_close_all.setDefault(True)
        self.pushButton_collect_ball.setDefault(True)
        self.pushButton_end_game.setDefault(True)
        self.pushButton_Backup_Camera.setDefault(True)
        self.pushButton_Main_Camera.setDefault(True)
        self.pushButton_Send_Result.setDefault(True)
        self.pushButton_Cancel_End.setDefault(True)
        self.pushButton_Send_End.setDefault(True)
        self.pushButton_term.setDefault(True)
        self.pushButton_Organ.setDefault(True)
        self.pushButton_kaj789.setDefault(True)
        self.pushButton_fsave.setDefault(True)
        self.pushButton_rename.setDefault(True)
        self.pushButton_ObsConnect.setDefault(True)
        self.pushButton_Obs2Table.setDefault(True)
        self.pushButton_Source2Table.setDefault(True)
        self.pushButton_Obs_delete.setDefault(True)
        self.pushButton_ToTable.setDefault(True)
        self.pushButton_CardStart.setDefault(True)
        self.pushButton_CardReset.setDefault(True)
        self.pushButton_CardNext.setDefault(True)
        self.pushButton_CardRun.setDefault(True)
        self.pushButton_CardStop.setDefault(True)
        self.pushButton_CardStop_2.setDefault(True)
        self.pushButton_CardClose.setDefault(True)
        self.pushButton_CardRun_2.setDefault(True)
        self.pushButton_Cardreset.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e2d\u63a7", None))
        ___qtablewidgetitem = self.tableWidget_Results.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u671f\u53f7", None));
        ___qtablewidgetitem1 = self.tableWidget_Results.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u8dd1\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget_Results.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u5012\u6570", None));
        ___qtablewidgetitem3 = self.tableWidget_Results.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtablewidgetitem4 = self.tableWidget_Results.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u8d5b\u679c", None));
        ___qtablewidgetitem5 = self.tableWidget_Results.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u8d5b\u679c", None));
        ___qtablewidgetitem6 = self.tableWidget_Results.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u8d5b\u679c", None));
        ___qtablewidgetitem7 = self.tableWidget_Results.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u56fe\u7247", None));
        ___qtablewidgetitem8 = self.tableWidget_Results.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u5907\u6ce8", None));
        ___qtablewidgetitem9 = self.tableWidget_Results.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None));
        ___qtablewidgetitem10 = self.tableWidget_Results.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u5f55\u50cf", None));
        ___qtablewidgetitem11 = self.tableWidget_Results.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u65f6\u95f4\u6233", None));
        ___qtablewidgetitem12 = self.tableWidget_Results.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5305", None));
        ___qtablewidgetitem13 = self.tableWidget_Results.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u8865\u53d1\u72b6\u6001", None));
        ___qtablewidgetitem14 = self.tableWidget_Results.horizontalHeaderItem(14)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"\u8865\u4f20\u72b6\u6001", None));
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u76d8\u53e3\u72b6\u6001", None))
        self.radioButton_start_betting.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u76d8", None))
        self.radioButton_stop_betting.setText(QCoreApplication.translate("MainWindow", u"\u5c01\u76d8", None))
        self.radioButton_test_game.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u62df", None))
        self.checkBox_black_screen.setText(QCoreApplication.translate("MainWindow", u"\u9ed1\u5c4f", None))
        self.groupBox_status.setTitle(QCoreApplication.translate("MainWindow", u"\u72b6\u60011", None))
        self.status_live.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u64ad\u72b6\u6001", None))
        self.status_road.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u9053\u72b6\u6001", None))
        self.status_lenses.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934\u72b6\u6001", None))
        self.status_track.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u9053\u72b6\u6001", None))
        self.groupBox_status_2.setTitle(QCoreApplication.translate("MainWindow", u"\u72b6\u60012", None))
        self.status_card.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361", None))
        self.status_server.setText(QCoreApplication.translate("MainWindow", u"\u5206\u673a", None))
        self.status_ai.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8bc6\u522b", None))
        self.status_ai_end.setText(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u670d\u52a1\u5668", None))
        self.status_s485.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u955c\u5934", None))
        self.status_obs.setText(QCoreApplication.translate("MainWindow", u"OBS\u72b6\u6001", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.checkBox_Pass_Recognition_Start.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u8d77\u70b9\u8bc6\u522b", None))
        self.checkBox_end_BlackScreen.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5c40\u7ed3\u675f\u540e\u81ea\u52a8\u9ed1\u5c4f", None))
        self.checkBox_Pass_Ranking_Twice.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u4e8c\u6b21\u6392\u540d", None))
        self.checkBox_end_stop.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5c40\u7ed3\u675f\u540e\u81ea\u52a8\u5c01\u76d8", None))
        self.checkBox_shoot_0.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u4e0a\u73e0", None))
        self.lineEdit_balls_auto.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"\u7c92", None))
        self.checkBox_alarm.setText(QCoreApplication.translate("MainWindow", u"\u5173\u8b66\u62a5", None))
        self.checkBox_shoot_1.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5c04", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u9501\u5b9a\u671f\u53f7", None))
        self.lineEdit_times_count.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u91cd\u590d\u671f\u53f7\uff1a", None))
        self.checkBox_continue_term.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u590d\u6267\u884c", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u5012\u6570\uff1a", None))
        self.pushButton_start_game.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7c92", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\uff1a", None))
        self.lineEdit_balls_start.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_balls_end.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7c92", None))
        self.pushButton_Stop_All.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u9053\u505c\u6b62", None))
        self.pushButton_end_all.setText(QCoreApplication.translate("MainWindow", u"\u6536\u5de5", None))
        self.pushButton_ready.setText(QCoreApplication.translate("MainWindow", u"\u51c6\u5907", None))
        self.pushButton_start_game_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.pushButton_close_all.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u5173", None))
        self.pushButton_collect_ball.setText(QCoreApplication.translate("MainWindow", u"\u6536\u73e0", None))
        self.pushButton_end_game.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f", None))
        self.pushButton_Backup_Camera.setText(QCoreApplication.translate("MainWindow", u"\u9009", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u6444\u50cf\u673a\uff1a  ", None))
        self.checkBox_Auto_Send.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8", None))
        self.pushButton_Main_Camera.setText(QCoreApplication.translate("MainWindow", u"\u9009", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u540e\u5907\u6444\u50cf\u673a\uff1a", None))
        self.pushButton_Send_Result.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u8d5b\u679c", None))
        self.pushButton_Cancel_End.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88\u5f53\u5c40", None))
        self.pushButton_Send_End.setText(QCoreApplication.translate("MainWindow", u"\u6b63\u5e38\u7ed3\u675f", None))
        self.pushButton_term.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u679c\u786e\u8ba4 \u8bc6\u522b\u72b6\u6001", None))
        self.pushButton_TRAP.setText(QCoreApplication.translate("MainWindow", u"\u5361\u73e0", None))
        self.pushButton_TRAP_1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_TRAP_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_TRAP_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_TRAP_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_TRAP_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_TRAP_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_TRAP_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_TRAP_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_TRAP_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_TRAP_10.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pushButton_OUT.setText(QCoreApplication.translate("MainWindow", u"\u98de\u73e0", None))
        self.pushButton_OUT_1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_OUT_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_OUT_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_OUT_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_OUT_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_OUT_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_OUT_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_OUT_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_OUT_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_OUT_10.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.groupBox_39.setTitle("")
        self.pushButton_Organ.setText(QCoreApplication.translate("MainWindow", u"\u673a\u5173\u63a7\u5236", None))
        self.pushButton_kaj789.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u4e8b\u8bb0\u5f55", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_0), QCoreApplication.translate("MainWindow", u"\u76f4\u64ad\u5927\u5385", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u6848\u540d\u79f0\uff1a", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u533a\u57df\uff1a", None))
        self.checkBox_follow.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u8ddf\u8e2a", None))
        self.pushButton_fsave.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u65b9\u6848", None))
        self.pushButton_rename.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u547d\u540d\u65b9\u6848", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u65b9\u6848\uff1a", None))
        self.checkBox_test.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u6a21\u5f0f", None))
        self.lineEdit_area.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.checkBox_selectall.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
        ___qtablewidgetitem15 = self.tableWidget_Step.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"\u5708\u6570", None));
        ___qtablewidgetitem16 = self.tableWidget_Step.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"\u8f741", None));
        ___qtablewidgetitem17 = self.tableWidget_Step.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"\u8f742", None));
        ___qtablewidgetitem18 = self.tableWidget_Step.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"\u8f743", None));
        ___qtablewidgetitem19 = self.tableWidget_Step.horizontalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"\u8f744", None));
        ___qtablewidgetitem20 = self.tableWidget_Step.horizontalHeaderItem(6)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"\u8f745", None));
        ___qtablewidgetitem21 = self.tableWidget_Step.horizontalHeaderItem(7)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6", None));
        ___qtablewidgetitem22 = self.tableWidget_Step.horizontalHeaderItem(8)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u901f", None));
        ___qtablewidgetitem23 = self.tableWidget_Step.horizontalHeaderItem(9)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u901f", None));
        ___qtablewidgetitem24 = self.tableWidget_Step.horizontalHeaderItem(10)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934(1-80)", None));
        ___qtablewidgetitem25 = self.tableWidget_Step.horizontalHeaderItem(11)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6", None));
        ___qtablewidgetitem26 = self.tableWidget_Step.horizontalHeaderItem(12)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"\u673a\u5173", None));
        ___qtablewidgetitem27 = self.tableWidget_Step.horizontalHeaderItem(13)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u4f4d\u7f6e", None));
        ___qtablewidgetitem28 = self.tableWidget_Step.horizontalHeaderItem(14)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None));
        ___qtablewidgetitem29 = self.tableWidget_Step.horizontalHeaderItem(15)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem30 = self.tableWidget_Step.horizontalHeaderItem(16)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"\u8d85\u65f6", None));
        ___qtablewidgetitem31 = self.tableWidget_Step.horizontalHeaderItem(17)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"OBS\u753b\u9762", None));
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"OBS\u7ba1\u7406", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe\uff1a", None))
        ___qtablewidgetitem32 = self.tableWidget_Sources.horizontalHeaderItem(1)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"\u6765\u6e90", None));
        ___qtablewidgetitem33 = self.tableWidget_Sources.horizontalHeaderItem(2)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"id", None));
        self.pushButton_ObsConnect.setText(QCoreApplication.translate("MainWindow", u"\u94fe\u63a5OBS", None))
        self.pushButton_Obs2Table.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe\u5165\u8868", None))
        self.pushButton_Source2Table.setText(QCoreApplication.translate("MainWindow", u"\u6765\u6e90\u5165\u8868", None))
        self.pushButton_Obs_delete.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u51fa\u8868", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u8f741\uff1a", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u8f742\uff1a", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\u8f743\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u8f744\uff1a", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u8f745\uff1a", None))
        self.checkBox_key.setText(QCoreApplication.translate("MainWindow", u"\u952e\u76d8\u5b9a\u4f4d", None))
        self.pushButton_ToTable.setText(QCoreApplication.translate("MainWindow", u"\u5750\u6807\u5165\u8868", None))
        self.checkBox_key_stop.setText(QCoreApplication.translate("MainWindow", u"\u6025\u505c", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361\u53f7\uff1a", None))
        self.pushButton_CardStart.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u8fd0\u52a8\u5361", None))
        self.pushButton_CardReset.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
        self.pushButton_CardNext.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u52a8\u4f5c", None))
        self.pushButton_CardRun.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5f00\u542f", None))
        self.pushButton_CardStop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"\u673a\u5173\u64cd\u4f5c", None))
        self.checkBox_shoot.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5c04", None))
        self.checkBox_start.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9", None))
        self.checkBox_end.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9", None))
        self.checkBox_all.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u53f7\uff1a", None))
        self.lineEdit_OutNo.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.checkBox_switch.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u5173", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u8bbe\u7f6e", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u955c\u5934\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_del_camera.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_add_camera.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_save_camera.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"\u97f3\u6548\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_add_Audio.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_del_Audio.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_save_Audio.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        ___qtablewidgetitem34 = self.tableWidget_Audio.horizontalHeaderItem(0)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem35 = self.tableWidget_Audio.horizontalHeaderItem(1)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"\u6b21\u6570", None));
        ___qtablewidgetitem36 = self.tableWidget_Audio.horizontalHeaderItem(2)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6(\u79d2)", None));
        ___qtablewidgetitem37 = self.tableWidget_Audio.horizontalHeaderItem(3)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u91cf(0-1)", None));
        ___qtablewidgetitem38 = self.tableWidget_Audio.horizontalHeaderItem(4)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None));
        self.checkBox_main_music.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f3", None))
        self.radioButton_music_1.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f31", None))
        self.radioButton_music_2.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f32", None))
        self.radioButton_music_3.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f33", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"AI\u8bed\u97f3\u70b9\u4f4d\u8bbe\u7f6e", None))
        self.pushButton_add_Ai.setText(QCoreApplication.translate("MainWindow", u"\u589e\u52a0\u70b9\u4f4d", None))
        self.pushButton_del_Ai.setText(QCoreApplication.translate("MainWindow", u"\u51cf\u5c11\u70b9\u4f4d", None))
        self.pushButton_save_Ai.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4f4d", None))
        ___qtablewidgetitem39 = self.tableWidget_Ai.horizontalHeaderItem(0)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548", None));
        ___qtablewidgetitem40 = self.tableWidget_Ai.horizontalHeaderItem(1)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"\u6b21\u6570", None));
        ___qtablewidgetitem41 = self.tableWidget_Ai.horizontalHeaderItem(2)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"\u5ef6\u65f6(\u79d2)", None));
        ___qtablewidgetitem42 = self.tableWidget_Ai.horizontalHeaderItem(3)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u91cf(0-1)", None));
        ___qtablewidgetitem43 = self.tableWidget_Ai.horizontalHeaderItem(4)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None));
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"\u70b9\u4f4d\u663e\u793a", None))
        self.checkBox_show_ai.setText(QCoreApplication.translate("MainWindow", u"Ai\u70b9\u4f4d", None))
        self.checkBox_show_audio.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u6548\u70b9\u4f4d", None))
        self.checkBox_show_orbit.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u8f68\u8ff9", None))
        self.checkBox_show_camera.setText(QCoreApplication.translate("MainWindow", u"\u955c\u5934\u70b9\u4f4d", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u6570\u636e", None))
        self.label_89.setText(QCoreApplication.translate("MainWindow", u"\u6838\u5bf9:", None))
        self.pushButton_Send_Res.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u7ed3\u679c", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u6444:", None))
        self.checkBox_ShowUdp.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u670d\u52a1\u5668\u6570\u636e", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_7.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_7.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_5.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_5.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_3.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_3.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_1.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_8.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_8.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_6.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_6.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_9.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_9.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_2.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_4.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_4.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_0.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u7a7a\u683c\u952e_\u4e0b\u4e00\u4e2a</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_monitor_cam.setTitle(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u6444\u50cf\u5934\u8bc6\u522b\u7ed3\u679c", None))
        self.checkBox_monitor_cam.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u53e3\u663e\u793a", None))
        self.label_monitor_picture.setText("")
        self.pushButton_NetCamera.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u6444\u50cf\u5934\u8bbe\u7f6e", None))
        self.groupBox_main_camera.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u6444\u50cf\u5934\u8bc6\u522b\u7ed3\u679c", None))
        self.checkBox_main_camera.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u53e3\u663e\u793a", None))
        self.checkBox_main_camera_set.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u5339\u914d\u7ec8\u70b9\u955c\u5934\u8d5b\u679c", None))
        self.label_main_picture.setText("")
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u6392\u540d", None))
        ___qtablewidgetitem44 = self.tableWidget_Ranking.horizontalHeaderItem(0)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"\u989c\u8272", None));
        ___qtablewidgetitem45 = self.tableWidget_Ranking.horizontalHeaderItem(1)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"\u533a\u57df", None));
        ___qtablewidgetitem46 = self.tableWidget_Ranking.horizontalHeaderItem(2)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"\u5708\u6570", None));
        ___qtablewidgetitem47 = self.tableWidget_Ranking.horizontalHeaderItem(3)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"x", None));
        ___qtablewidgetitem48 = self.tableWidget_Ranking.horizontalHeaderItem(4)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"y", None));
        self.groupBox_ranking.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u53c2\u6570\u8bbe\u7f6e", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u65f6\u95f4:", None))
        self.pushButton_save_Ranking.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_area_Ranking.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u533a\u57df\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_lap_Ranking.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bbe\u7f6e\u6700\u5927\u5708\u6570</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_Time_Restart_Ranking.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5927\u533a\u57df:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u5708\u6570:", None))
        self.pushButton_udp_time.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8bc6\u522b\u72b6\u6001\u6b63\u5e38", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u8bbe\u7f6e", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u5012\u8ba1\u65f6\uff1a", None))
        self.checkBox_restart.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6a21\u5f0f", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"\u7edf\u8ba1\u7403\u65f6\u95f4\uff1a", None))
        self.lineEdit_time_count_ball.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u7ed3\u679c\u65f6\u95f4\uff1a", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.lineEdit_time_send_result.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u79d2", None))
        self.groupBox_37.setTitle("")
        self.pushButton_CardStop_2.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.pushButton_CardClose.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u673a\u5173", None))
        self.pushButton_CardRun_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.pushButton_Cardreset.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
        self.lineEdit_ball_start.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_ball_end.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u7ec8\u70b9\u7403\u6570\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\u7403\u6570\uff1a", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8bc6\u522b", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"\u673a\u5173\u7f16\u53f7\u8bf4\u660e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_start_count.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_start_count.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.checkBox_shoot2.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5c042\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_alarm.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_alarm.setText(QCoreApplication.translate("MainWindow", u"14", None))
        self.checkBox_start_2.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\u95f8\u95e8\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_shoot_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_shoot_3.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.checkBox_end_2.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u5347\u964d\uff1a", None))
        self.checkBox_alarm_2.setText(QCoreApplication.translate("MainWindow", u"\u8b66\u544a\u706f\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_start.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_start.setText(QCoreApplication.translate("MainWindow", u"2", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_end.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_end.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.checkBox_shoot3.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5c043\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_shoot.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_shoot.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_shoot_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_shoot_2.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.checkBox_shake.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\u9707\u52a8\uff1a", None))
        self.checkBox_start_count.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u70b9\u5012\u6570\uff1a", None))
        self.checkBox_shoot1.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5c04\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_shake.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_shake.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u9898\u97f3\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_3.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e503.mp3", None))
        self.radioButton_music_background_2.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e502\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_2.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e502.mp3", None))
        self.radioButton_music_background_1.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e501\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_music_1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_music_1.setText(QCoreApplication.translate("MainWindow", u"./mp3/07_\u51b0\u539f\u80cc\u666f\u97f3\u4e501.mp3", None))
        self.radioButton_music_background_3.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u97f3\u4e503\uff1a", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"OBS\u573a\u666f\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_scene_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_scene_name.setText(QCoreApplication.translate("MainWindow", u"\u73b0\u573a", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u573a\u666f\u540d\u79f0\uff1a", None))
        self.groupBox_31.setTitle(QCoreApplication.translate("MainWindow", u"\u6765\u6e90\u5207\u6362\u8bbe\u7f6e", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u7b97\u9875\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_source_end.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_source_end.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b91", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_source_picture.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_source_picture.setText(QCoreApplication.translate("MainWindow", u"\u753b\u4e2d\u753b", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_source_settlement.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_source_settlement.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u7b97\u9875", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u65f6\u95f4\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_source_ranking.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_source_ranking.setText(QCoreApplication.translate("MainWindow", u"\u6392\u540d\u65f6\u95f4\u7ec4\u4ef6", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"\u753b\u4e2d\u753b\uff1a", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u622a\u56fe\uff1a", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c\u4fe1\u606f", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"\u536b\u661f\u56fe\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_map_picture.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_map_picture.setText(QCoreApplication.translate("MainWindow", u"./img/09_\u6c99\u6f20.jpg", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u6587\u4ef6\uff1a", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u6587\u4ef6\uff1a", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"\u5730\u56fe\u5c3a\u5bf8\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_map_size.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_map_size.setText(QCoreApplication.translate("MainWindow", u"860", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_map_line.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_map_line.setText(QCoreApplication.translate("MainWindow", u"./img/09_\u6c99\u6f20.json", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("MainWindow", u"\u7ed3\u679c\u56fe\u7247\u4fdd\u5b58", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"\u8d5b\u9053\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_saidao_Path.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_saidao_Path.setText(QCoreApplication.translate("MainWindow", u"Z:/\u6570\u636e/\u7011\u5e03_\u8d5b\u9053", None))
        self.label_94.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b91\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_end1_Path.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_end1_Path.setText(QCoreApplication.translate("MainWindow", u"D:/\u6570\u636e/\u7011\u5e03_\u7ec8\u70b9/obs", None))
        self.label_93.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u62a5\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_upload_Path.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_upload_Path.setText(QCoreApplication.translate("MainWindow", u"D:/\u6570\u636e/\u4e0a\u62a5", None))
        self.label_95.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b92\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_end2_Path.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_end2_Path.setText(QCoreApplication.translate("MainWindow", u"D:/\u6570\u636e/\u7011\u5e03_\u7ec8\u70b9/rtsp", None))
        self.groupBox_36.setTitle(QCoreApplication.translate("MainWindow", u"\u6392\u5e8f\u65b9\u5411", None))
        self.label_91.setText(QCoreApplication.translate("MainWindow", u"\u7d22\u5c3c\u6444\u50cf\u5934:", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u6444\u50cf\u5934\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_sony_sort.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_sony_sort.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_monitor_sort.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_monitor_sort.setText(QCoreApplication.translate("MainWindow", u"11", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"\u786c\u4ef6\u7aef\u53e3\u8bbe\u7f6e", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u9053\u7f16\u53f7\uff1a", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361\u4e94\u8f74\u65b9\u5411\uff1a", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"S485 \u6444\u50cf\u673a\u7aef\u53e3\uff1a", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"S485 \u8f74\u590d\u4f4d\u7aef\u53e3\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_cardNo.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_cardNo.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_s485_Axis_No.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_s485_Axis_No.setText(QCoreApplication.translate("MainWindow", u"COM23", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Track_number.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Track_number.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u52a8\u5361\u7f51\u7edc\u7f16\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_s485_Cam_No.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_s485_Cam_No.setText(QCoreApplication.translate("MainWindow", u"COM1", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_five_axis.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_five_axis.setText(QCoreApplication.translate("MainWindow", u"[-1,1,1,1,-1]", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"\u952e\u76d8\u65b9\u5411\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_five_key.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_five_key.setText(QCoreApplication.translate("MainWindow", u"[-1,1,1,1,-1]", None))
        self.groupBox_net.setTitle(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"\u524d\u7aef\u7ec8\u70b9\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_rtsp_url.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_rtsp_url.setText(QCoreApplication.translate("MainWindow", u"rtsp://admin:123456@192.168.0.29:554/Streaming/Channels/101", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_ip.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_ip.setText(QCoreApplication.translate("MainWindow", u"0.0.0.0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_tcpServer_ip.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_tcpServer_ip.setText(QCoreApplication.translate("MainWindow", u"0.0.0.0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_obs_script_addr.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_obs_script_addr.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:8899", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u5524\u9192\u8bc6\u522b\u670d\u52a1\u5668\u7f51\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_wakeup_addr.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_wakeup_addr.setText(QCoreApplication.translate("MainWindow", u"['http://192.168.0.110:8080']", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_ip.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_ip.setText(QCoreApplication.translate("MainWindow", u"0.0.0.0", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_Port.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_TcpServer_Port.setText(QCoreApplication.translate("MainWindow", u"9999", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"OBS\u811a\u672c\u7f51\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_Port.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_UdpServer_Port.setText(QCoreApplication.translate("MainWindow", u"19734", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_recognition_addr.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_recognition_addr.setText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:6066", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u6444\u50cf\u5934\u7f51\u5740\uff1a", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u70b9\u8bc6\u522b\u4e3b\u673a\u7f51\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_tcpServer_port.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_tcpServer_port.setText(QCoreApplication.translate("MainWindow", u"8888", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u524d\u7aef\u6392\u540d\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"UDP\u63a5\u6536\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
        self.label_92.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.groupBox_balls.setTitle(QCoreApplication.translate("MainWindow", u"\u5f39\u73e0\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_balls_count.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_balls_count.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u73e0\u6570\u91cf\uff1a", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"\u989c\u8272\u53f7\u7801\u8bbe\u7f6e", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_5.setText(QCoreApplication.translate("MainWindow", u"orange", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_3.setText(QCoreApplication.translate("MainWindow", u"\u7ea2", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_4.setText(QCoreApplication.translate("MainWindow", u"purple", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"9\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_3.setText(QCoreApplication.translate("MainWindow", u"red", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"6\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_10.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_10.setText(QCoreApplication.translate("MainWindow", u"White", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_8.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_8.setText(QCoreApplication.translate("MainWindow", u"black", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_2.setText(QCoreApplication.translate("MainWindow", u"\u84dd", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"8\u53f7\uff1a", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"3\u53f7\uff1a", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"1\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_1.setText(QCoreApplication.translate("MainWindow", u"yellow", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"4\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_2.setText(QCoreApplication.translate("MainWindow", u"blue", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_7.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_7.setText(QCoreApplication.translate("MainWindow", u"Brown", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"2\u53f7\uff1a", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_1.setText(QCoreApplication.translate("MainWindow", u"\u9ec4", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"10\u53f7\uff1a", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"7\u53f7\uff1a", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_6.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_6.setText(QCoreApplication.translate("MainWindow", u"green", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_9.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Eng_9.setText(QCoreApplication.translate("MainWindow", u"pink", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"5\u53f7\uff1a", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u":", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_4.setText(QCoreApplication.translate("MainWindow", u"\u7d2b", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_5.setText(QCoreApplication.translate("MainWindow", u"\u6a59", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_6.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_6.setText(QCoreApplication.translate("MainWindow", u"\u7eff", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_7.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_7.setText(QCoreApplication.translate("MainWindow", u"\u68d5", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_8.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_8.setText(QCoreApplication.translate("MainWindow", u"\u9ed1", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_9.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_9.setText(QCoreApplication.translate("MainWindow", u"\u7c89", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_10.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_Color_Ch_10.setText(QCoreApplication.translate("MainWindow", u"\u767d", None))
        self.pushButton_Save_Ball.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5f39\u73e0", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"\u8f85\u52a9\u63a7\u5236", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u6444\u50cf\u673a\u63a7\u5236", None))
        self.checkBox_Flip_Horizontal.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5e73\u7ffb\u8f6c", None))
        self.checkBox_Flip_Vertica.setText(QCoreApplication.translate("MainWindow", u"\u5bf9\u89d2\u7ffb\u8f6c", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"\u6444\u50cf\u5934\u5f55\u56fe\u64cd\u4f5c", None))
        self.checkBox_saveImgs_main.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u6444\u50cf\u5934", None))
        self.checkBox_saveImgs_monitor.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u6444\u50cf\u5934", None))
        self.checkBox_saveImgs_auto.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u4e3b\u673a\u5f55\u56fe\u64cd\u4f5c", None))
        self.radioButton_noball.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u7403", None))
        self.radioButton_ball.setText(QCoreApplication.translate("MainWindow", u"\u6709\u7403", None))
        self.checkBox_saveImgs.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u5c4f", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"\u5730\u56fe\u5212\u533a\u7f16\u8f91\u5236\u4f5c", None))
        self.pushButton_Draw.setText(QCoreApplication.translate("MainWindow", u"\u753b\u56fe\u5de5\u5177", None))
        self.pushButton_to_TXT.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362TXT", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("MainWindow", u"\u7ba1\u7406", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_login.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_login.setText("")
        self.label_96.setText(QCoreApplication.translate("MainWindow", u"\u7ba1\u7406\u8d26\u53f7:", None))
        self.tabWidget_Ranking.setTabText(self.tabWidget_Ranking.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
    # retranslateUi

