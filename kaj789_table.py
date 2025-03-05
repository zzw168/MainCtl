import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QTableWidgetItem, QComboBox, QDialog, QMenu
)
import sys

from kaj789_Ui import Ui_Dialog_Kaj789_Ui


class Kaj789Ui(QDialog, Ui_Dialog_Kaj789_Ui):
    def __init__(self):
        super().__init__()

    def setupUi(self, z_dialog):
        super(Kaj789Ui, self).setupUi(z_dialog)

        self.loadFiles()

        tb_kaj789 = self.tableWidget_kaj789

        tb_kaj789.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_kaj789.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_kaj789.horizontalHeader().resizeSection(0, 100)
        tb_kaj789.horizontalHeader().resizeSection(1, 200)
        tb_kaj789.horizontalHeader().resizeSection(2, 100)
        tb_kaj789.horizontalHeader().resizeSection(3, 100)
        tb_kaj789.horizontalHeader().resizeSection(4, 100)
        tb_kaj789.horizontalHeader().resizeSection(5, 200)
        tb_kaj789.horizontalHeader().resizeSection(6, 100)
        tb_kaj789.horizontalHeader().resizeSection(7, 100)

        tb_kaj789.setColumnHidden(0, True)

        tb_kaj789.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_kaj789.customContextMenuRequested.connect(self.resultMenu)

        tb_kaj789.setRowCount(20)
        # 添加测试数据
        for row in range(20):
            for col in range(7):
                if col != 5:  # “备注”列留空，其他列填充数据
                    tb_kaj789.setItem(row, col, QTableWidgetItem(f"数据 {row},{col}"))

        # 连接单元格点击事件
        tb_kaj789.cellClicked.connect(self.showComboBox)

    def resultMenu(self, pos):
        tb_kaj789 = self.tableWidget_kaj789
        row_num = tb_kaj789.currentRow()

        menu = QMenu()
        item0 = menu.addAction("查看图片")
        item1 = menu.addAction("观看录像")
        item2 = menu.addAction("发送赛果")
        item3 = menu.addAction("取消当局")
        item4 = menu.addAction("刷新")

        screenPos = tb_kaj789.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item0:
            exe_path = tb_kaj789.item(row_num, 6).text()
            os.startfile(exe_path)
        if action == item1:
            exe_path = tb_kaj789.item(row_num, 7).text()
            os.startfile(exe_path)
        if action == item2:
            pass
        if action == item3:
            pass
        if action == item4:
            pass
        


    def showComboBox(self, row, col):
        """ 在备注列（第5列）点击后显示 ComboBox """
        if col == 4:  # 备注列索引为 4
            combo = QComboBox()
            combo.addItems(["无", "待审核", "已确认"])  # 选项
            combo.setCurrentText(self.tableWidget_kaj789.item(row, col).text() if self.tableWidget_kaj789.item(row, col) else "无")

            # 连接 activated 信号，在用户选择后隐藏 ComboBox
            combo.activated.connect(lambda index, r=row, c=col: self.saveComboBoxData(r, c, combo))

            self.tableWidget_kaj789.setCellWidget(row, col, combo)
            combo.showPopup()  # 立即展开下拉框

    def saveComboBoxData(self, row, col, combo):
        """ 保存 ComboBox 选中的值，并隐藏 ComboBox """
        text = combo.currentText()
        self.tableWidget_kaj789.setItem(row, col, QTableWidgetItem(text))  # 设置为选中内容
        self.tableWidget_kaj789.removeCellWidget(row, col)  # 隐藏 ComboBox

    def loadFiles(self):
        folder_path = './terms/'
        if folder_path:  # 确保用户选择了文件夹
            self.comboBox_kaj789.clear()  # 清空 ComboBox
            files = os.listdir(folder_path)  # 获取文件夹中的文件
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]  # 过滤出文件（排除文件夹）
            self.comboBox_kaj789.addItems(files)  # 添加文件名到 ComboBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    BallsNumDialog = QDialog()  #
    BallsNum_ui = Kaj789Ui()
    BallsNum_ui.setupUi(BallsNumDialog)
    BallsNumDialog.show()
    sys.exit(app.exec())
