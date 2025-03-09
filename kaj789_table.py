import json
import os

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QShowEvent
from PySide6.QtWidgets import (
    QApplication, QTableWidgetItem, QComboBox, QDialog, QMenu, QAbstractButton
)
import sys

from kaj789_Ui import Ui_Dialog_Kaj789_Ui
from utils.kaj789 import post_end, post_result, post_upload, post_marble_results


class Kaj789Ui(QDialog, Ui_Dialog_Kaj789_Ui):
    def __init__(self):
        super().__init__()
        self.labels = []

    def setupUi(self, z_dialog):
        super().setupUi(z_dialog)
        self.loadFiles()
        self.comboBox_kaj789.currentIndexChanged.connect(self.load_json_file)
        tb_result = self.tableWidget_Results
        tb_result.horizontalHeader().resizeSection(0, 100)
        tb_result.horizontalHeader().resizeSection(1, 150)
        tb_result.horizontalHeader().resizeSection(2, 40)
        tb_result.horizontalHeader().resizeSection(3, 50)
        tb_result.horizontalHeader().resizeSection(4, 170)
        tb_result.horizontalHeader().resizeSection(5, 170)
        tb_result.horizontalHeader().resizeSection(6, 80)
        tb_result.horizontalHeader().resizeSection(7, 80)
        tb_result.horizontalHeader().resizeSection(8, 80)
        tb_result.horizontalHeader().resizeSection(9, 150)
        tb_result.horizontalHeader().resizeSection(10, 150)
        tb_result.horizontalHeader().resizeSection(11, 150)
        tb_result.horizontalHeader().resizeSection(12, 80)
        tb_result.horizontalHeader().resizeSection(13, 80)
        tb_result.horizontalHeader().resizeSection(13, 80)

        tb_result.setColumnHidden(0, True)
        tb_result.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_result.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        # 允许用户调整行表头宽度
        tb_result.setCornerButtonEnabled(True)
        tb_result.verticalHeader().setFixedWidth(100)

        # 获取 CornerButton
        corner_button = tb_result.findChild(QAbstractButton)
        if corner_button:
            # 安装事件过滤器，自定义绘制文字
            corner_button.installEventFilter(self)  # 事件过滤器用于处理重绘

        tb_result.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_result.customContextMenuRequested.connect(self.resultMenu)

        # 连接单元格点击事件
        tb_result.cellClicked.connect(self.showComboBox)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)  # 调用父类的 showEvent
        self.load_json_file()

    def eventFilter(self, obj, event):
        # 检测到 CornerButton 的 Paint 事件
        if isinstance(obj, QAbstractButton) and event.type() == QEvent.Paint:
            # 自定义绘制逻辑
            painter = QPainter(obj)
            painter.save()

            # 获取按钮区域
            rect = obj.rect()

            # 绘制背景（模拟按钮的上表面，颜色为 rgb(245, 245, 245)）
            painter.setBrush(QBrush(QColor(245, 245, 245)))  # 浅灰色背景
            painter.setPen(Qt.NoPen)  # 无边框线
            painter.drawRect(rect)

            # 绘制顶部和左侧的高光（模拟光源）
            highlight_pen = QPen(QColor("#ffffff"), 2)  # 白色高光
            painter.setPen(highlight_pen)
            painter.drawLine(rect.topLeft(), rect.topRight())  # 顶部边线
            painter.drawLine(rect.topLeft(), rect.bottomLeft())  # 左侧边线

            # 绘制底部和右侧的阴影
            shadow_pen = QPen(QColor("#a0a0a0"), 2)  # 深灰色阴影
            painter.setPen(shadow_pen)
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())  # 底部边线
            painter.drawLine(rect.topRight(), rect.bottomRight())  # 右侧边线

            # 设置绘制区域和文字样式
            painter.setPen(Qt.black)
            painter.drawText(obj.rect(), Qt.AlignCenter, "期号")

            painter.restore()
            return True  # 阻止默认绘制事件

        return super().eventFilter(obj, event)

    def resultMenu(self, pos):
        tb_kaj789 = self.tableWidget_Results
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
            exe_path = tb_kaj789.item(row_num, 9).text()
            os.startfile(exe_path)
        if action == item1:
            exe_path = tb_kaj789.item(row_num, 10).text()
            os.startfile(exe_path)
        if action == item2:
            pass
        if action == item3:
            pass
        if action == item4:
            pass

    def showComboBox(self, row, col):
        """ 在备注列（第5列）点击后显示 ComboBox """
        if col == 8:  # 备注列索引为 4
            combo = QComboBox()
            combo.addItems(['Invalid Term', 'TRAP', 'OUT', ''])  # 选项
            combo.setCurrentText(
                self.tableWidget_Results.item(row, col).text() if self.tableWidget_Results.item(row, col) else "")

            # 连接 activated 信号，在用户选择后隐藏 ComboBox
            combo.activated.connect(lambda index, r=row, c=col: self.saveComboBoxData(r, c, combo))

            self.tableWidget_Results.setCellWidget(row, col, combo)
            combo.showPopup()  # 立即展开下拉框

    def saveComboBoxData(self, row, col, combo):
        """ 保存 ComboBox 选中的值，并隐藏 ComboBox """
        text = combo.currentText()
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_Results.setItem(row, col, item)  # 设置为选中内容
        self.tableWidget_Results.removeCellWidget(row, col)  # 隐藏 ComboBox

    def loadFiles(self):
        folder_path = './terms/'
        if folder_path:  # 确保用户选择了文件夹
            self.comboBox_kaj789.clear()  # 清空 ComboBox
            files = os.listdir(folder_path)  # 获取文件夹中的文件
            files = [f for f in files if
                     (os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".json"))]  # 过滤出文件（排除文件夹）
            if files:
                self.comboBox_kaj789.addItems(files)  # 添加文件名到 ComboBox

    def load_json_file(self):
        """读取 ComboBox 选中的 JSON 文件并显示"""
        selected_file = self.comboBox_kaj789.currentText()
        file = "./terms/%s" % selected_file
        if not selected_file.endswith(".json"):
            return
        try:
            if os.path.exists(file):
                lottery_list = []
                lottery_kaj789 = [''] * 15
                self.labels = []
                self.tableWidget_Results.setRowCount(0)
                with open(file, "r", encoding="utf-8") as f:
                    for line in f:
                        print(json.loads(line))  # 逐行解析 JSON
                        lottery_list.append(json.loads(line))
                for row in range(len(lottery_list)):
                    for col in range(len(lottery_list[row])):
                        lottery_kaj789[col] = lottery_list[row][col]
                    lottery_data2table(self.tableWidget_Results, lottery_kaj789, self.labels)
        except Exception as e:
            print(f"读取错误: {e}")

    def resend_end(self, Track_number, run_type, term_status):
        tb_kaj789 = self.tableWidget_Results
        row = tb_kaj789.currentRow()
        term = tb_kaj789.item(row, 0)
        betting_end_time = tb_kaj789.item(row, 11)
        result_data = json.loads(tb_kaj789.item(row, 12))
        img_path = tb_kaj789.item(row, 9)
        term_comment = tb_kaj789.item(row, 8)
        for i in range(5):
            if run_type == 'post_end':
                res_end = post_end(term, betting_end_time, term_status,
                                   Track_number)  # 发送游戏结束信号给服务器
                if res_end == 'OK':
                    if term_status == 1:
                        run_type = 'post_result'
                    else:
                        pass
                else:
                    continue
            if run_type == 'post_result':
                res_result = post_result(term, betting_end_time, result_data,
                                         Track_number)  # 发送最终排名给服务器
                if res_result == 'OK':
                    run_type = 'post_upload'
                else:
                    continue
            if run_type == 'post_upload' and os.path.exists(img_path):
                res_upload = post_upload(term, img_path, Track_number)  # 上传结果图片
                if res_upload != 'OK':
                    continue
                else:
                    lottery_term[7] = "上传成功"
                    break
            if term_comment != '':
                res_marble_results = post_marble_results(term, term_comment,
                                                         Track_number)  # 上传备注信息
                lottery_term[8] = term_comment
                if str(term) in res_marble_results:
                    lottery2json()  # 保存数据
                term_comment = ''
                break


def lottery_data2table(tb_result, lottery_t, labels):  # 赛事入表
    row_count = tb_result.rowCount()
    col_count = tb_result.columnCount()
    tb_result.setRowCount(row_count + 1)

    labels.insert(0, str(lottery_t[0]))
    tb_result.setVerticalHeaderLabels(labels)
    tb_result.verticalHeaderItem(len(labels) - 1).setTextAlignment(Qt.AlignCenter)

    for col in range(0, col_count):
        item = QTableWidgetItem('')
        item.setTextAlignment(Qt.AlignCenter)
        tb_result.setItem(row_count, col, item)
    if row_count > 0:  # 下移表格
        for row in range(row_count, 0, -1):
            for col in range(0, col_count):
                tb_result.item(row, col).setText(tb_result.item(row - 1, col).text())
    for index, value in enumerate(lottery_t):
        tb_result.item(0, index).setText(str(value))


def kaj789_showEvent(kaj789_ui):
    kaj789_ui.load_json_file()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    BallsNum_ui = Kaj789Ui()
    BallsNum_ui.setupUi(BallsNum_ui)
    BallsNum_ui.show()

    sys.exit(app.exec())
