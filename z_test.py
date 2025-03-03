from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget
import sys

class TableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableWidget 点击显示 ComboBox")
        self.resize(400, 300)

        # 创建表格
        self.table = QTableWidget(5, 3)  # 5 行 3 列
        self.table.setHorizontalHeaderLabels(["列1", "列2", "列3"])

        # 添加测试数据
        for row in range(5):
            for col in range(3):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row},{col}"))

        # 连接 item 被点击的信号
        self.table.cellClicked.connect(self.showComboBox)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def showComboBox(self, row, col):
        """ 在单元格中显示 ComboBox """
        combo = QComboBox()
        combo.addItems(["选项1", "选项2", "选项3"])  # 添加选项
        self.table.setCellWidget(row, col, combo)  # 在该单元格放置 ComboBox
def test():
    with open("example.txt", "a", encoding="utf-8") as file:
        file.write("Appending some data.\n")

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = TableWidgetDemo()
    # window.show()
    #
    # sys.exit(app.exec_())
    test()
