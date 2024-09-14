import os
import socket
import sys
import time

import pynput
import yaml

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu
import requests
import ctypes

# from My_Ui import *
from sportCard_unit import *
from MainCtl_Ui import *


class MyUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super(MyUi, self).setupUi(MainWindow)

        tb = self.tableWidget_Results
        tb.horizontalHeader().resizeSection(0, 10)
        tb.horizontalHeader().resizeSection(1, 80)
        tb.setColumnHidden(3, True)
        tb.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_Step = self.tableWidget_Step
        tb_Step.horizontalHeader().resizeSection(0, 10)
        tb_Step.horizontalHeader().resizeSection(1, 80)
        # tb_Step.setColumnHidden(3, True)
        tb_Step.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_Step.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_Step.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_Step.customContextMenuRequested.connect(self.generateMenu)

    def generateMenu(self, pos):
        tb = self.tableWidget_Step

        menu = QMenu()
        item1 = menu.addAction("插入")
        item2 = menu.addAction("删除")
        item3 = menu.addAction("刷新")

        screenPos = tb.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item3:
            pass
            # Color_Thead.start()
        if action == item2:
            # del_host()
            num = tb.rowCount()
            print(num)
            if num != 0:
                p = tb.currentRow()
                for i in range(p, num - 1):
                    # print('%d' % i)
                    for j in range(0, tb.columnCount()):
                        if j == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet('QCheckBox{margin:6px};')
                            cb.setChecked(tb.cellWidget(i + 1, j).isChecked())
                            tb.setCellWidget(i, j, cb)
                        else:
                            item = QTableWidgetItem(tb.item(i + 1, j).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb.setItem(i, j, item)
                tb.setRowCount(num - 1)
        if action == item1:
            table = self.tableWidget_Step
            num = table.rowCount()
            table.setRowCount(num + 1)
            row = table.currentRow()
            if num > 0:  # 下移表格
                for r in range(num, row, -1):
                    cb = QCheckBox()
                    cb.setStyleSheet('QCheckBox{margin:6px};')
                    table.setCellWidget(r, 0, cb)
                    table.cellWidget(r, 0).setChecked(table.cellWidget(r - 1, 0).isChecked())
                    for i in range(1, table.columnCount()):
                        item = QTableWidgetItem(table.item(r - 1, i).text())
                        item.setTextAlignment(Qt.AlignCenter)
                        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                        table.setItem(r, i, item)

                table.cellWidget(row, 0).setChecked(False)
                for i in range(1, table.columnCount()):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(row, i, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                table.setCellWidget(0, 0, cb)

                for i in range(1, table.columnCount()):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(0, i, item)


class ColorThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(ColorThead, self).__init__()

    def run(self) -> None:
        while True:
            if z_status:
                status_color = 'background:rgb(255, 0, 0)'
            else:
                status_color = 'background:rgb(0, 255, 0)'
                pass
            self._signal.emit(status_color)
            time.sleep(1)


class KeyListenerThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(KeyListenerThead, self).__init__()

    def run(self) -> None:
        with pynput.keyboard.Listener(on_press=on_press) as lsn:
            lsn.join()


def on_press(key):
    try:
        if key == key.esc:
            print(key)
    except AttributeError:
        print(key)


# 保存方案
def save_plan():
    global plan_list
    table = ui.tableWidget_Step
    row_num = table.rowCount()
    col_num = table.columnCount()
    if row_num == 0:
        return
    plan_list = []
    local_list = []
    for i in range(0, row_num):
        if table.cellWidget(i, 0).isChecked():
            local_list.append("1")
        else:
            local_list.append("0")
        for j in range(1, col_num - 1):
            # host.append(table.item(i, j).text())
            local_list.append("0" if table.item(i, j).text() == "" else table.item(i, j).text())

        plan_list.append(local_list)
        local_list = []
    print(plan_list)

    comb = ui.comboBox_plan
    plan_num = comb.currentIndex()
    plan_name = comb.currentText()

    file = "./Robot.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        save_list = yaml.safe_load(f)
        f.close()

        save_list['plans']['plan%d' % (plan_num + 1)]['plan_name'] = plan_name
        save_list['plans']['plan%d' % (plan_num + 1)]['plan_list'] = plan_list

        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(save_list, f, allow_unicode=True)
        f.close()


# 载入方案
def deal_yaml():
    global plan_list
    global plan_names
    global plan_all
    file = "./Robot.yml"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            plan_all = yaml.safe_load(f)
            f.close()
            for plan in plan_all['plans']:
                plan_names.append(plan_all['plans'][plan]['plan_name'])

            comb = ui.comboBox_plan
            comb.addItems(plan_names)
            plan_change()
            # _index = comb.currentIndex()
            # plan_list = plan_all['plans']['plan%d' % (_index + 1)]['plan_list']
            #
            # table = ui.tableWidget_Step
            # num = 0
            # for task in plan_list:
            #     table.setRowCount(num + 1)
            #     cb = QCheckBox()
            #     cb.setStyleSheet('QCheckBox{margin:6px};')
            #     table.setCellWidget(num, 0, cb)
            #     if task[0] == '1':
            #         table.cellWidget(num, 0).setChecked(True)
            #
            #     for i in range(1, len(task)):
            #         item = QTableWidgetItem(str(task[i]))
            #         item.setTextAlignment(Qt.AlignCenter)
            #         # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
            #         table.setItem(num, i, item)
            #     num += 1
        except:
            pass
    else:
        print("文件不存在")


# 重命名方案
def plan_rename():
    text = ui.lineEdit_rename.text()
    comb = ui.comboBox_plan
    comb.setItemText(comb.currentIndex(), text)


def sel_all():
    table = ui.tableWidget_Step
    num = table.rowCount()
    for i in range(0, num):
        if ui.checkBox_selectall.isChecked():
            table.cellWidget(i, 0).setChecked(True)
        else:
            table.cellWidget(i, 0).setChecked(False)


def plan_change():
    comb = ui.comboBox_plan
    _index = comb.currentIndex()
    plan_list = plan_all['plans']['plan%d' % (_index + 1)]['plan_list']

    table = ui.tableWidget_Step
    num = 0
    for task in plan_list:
        table.setRowCount(num + 1)
        cb = QCheckBox()
        cb.setStyleSheet('QCheckBox{margin:6px};')
        table.setCellWidget(num, 0, cb)
        if task[0] == '1':
            table.cellWidget(num, 0).setChecked(True)

        for i in range(1, len(task)):
            item = QTableWidgetItem(str(task[i]))
            item.setTextAlignment(Qt.AlignCenter)
            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
            table.setItem(num, i, item)
        num += 1


def flashsignal_accept(status_color):  # 更改颜色
    ui.status_server1.setStyleSheet(status_color)
    ui.status_obs.setStyleSheet(status_color)
    ui.status_server2.setStyleSheet(status_color)
    ui.status_live.setStyleSheet(status_color)
    ui.status_road.setStyleSheet(status_color)
    ui.status_lenses.setStyleSheet(status_color)
    ui.status_Extension.setStyleSheet(status_color)
    ui.status_mainlenses.setStyleSheet(status_color)
    ui.status_Recognition.setStyleSheet(status_color)
    ui.status_track.setStyleSheet(status_color)
    ui.status_sportsCards.setStyleSheet(status_color)


def bt_start():
    global z_status
    ui.widget_9.setVisible(not (ui.widget_9.isVisible()))
    z_status = not (z_status)


def test_cart():
    res = sc.card_open(10)
    print(res)
    # res = sc.card_pos(1, pos=1000000)
    # print(res)
    # res = sc.card_pos(2, pos=1000000)
    # print(res)
    # res = sc.card_update()
    # print(res)
    (res, pValue, pClock) = sc.get_pos()
    print("%s %s %s" % (res, pValue, pClock))
    sc.card_reset()
    # (res, pValue, pClock) = sc.get_pos()
    # print("%s %s %s" % (res, pValue, pClock))


def test():
    ui.textBrowser.append("<font color='green'> okok </font>")


if __name__ == '__main__':
    # sc = SportCard()
    # test_cart()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()

    z_status = True
    sc = SportCard()

    plan_list = []  # 当前方案列表
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料

    deal_yaml()

    KeyListener_Thead = KeyListenerThead()
    KeyListener_Thead.start()

    Color_Thead = ColorThead()  # 更新状态信息线程
    Color_Thead._signal.connect(flashsignal_accept)
    Color_Thead.start()

    ui.pushButton_fsave.clicked.connect(save_plan)
    ui.pushButton_rename.clicked.connect(plan_rename)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.comboBox_plan.currentIndexChanged.connect(plan_change)

    sys.exit(app.exec_())
