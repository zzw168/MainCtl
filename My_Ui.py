from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QTableWidgetItem, QMenu

from MainCtl_Ui import Ui_MainWindow
from Main_Controller import Flash_Thead


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
        tb_Step.setColumnHidden(3, True)
        tb_Step.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_Step.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb.setContextMenuPolicy(Qt.CustomContextMenu)
        tb.customContextMenuRequested.connect(self.generateMenu)

    def generateMenu(self, pos):
        tb = self.tableWidget

        menu = QMenu()
        item1 = menu.addAction("刷新")
        item2 = menu.addAction("删除")
        item3 = menu.addAction("插入")
        screenPos = tb.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item1:
            pass
            Flash_Thead.start()
        if action == item2:
            # del_host()
            num = tb.rowCount()
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
        if action == item3:
            table = self.tableWidget_Step
            num = table.rowCount()
            table.setRowCount(num + 1)
            row = table.currentRow()
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
