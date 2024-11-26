from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGroupBox, QVBoxLayout, QLabel, QSplitter, QWidget
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add QSplitter to Existing GroupBoxes")

        # 创建两个已有的 QGroupBox
        groupbox1 = QGroupBox("Group 1")
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("This is Group 1"))
        groupbox1.setLayout(layout1)

        groupbox2 = QGroupBox("Group 2")
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is Group 2"))
        groupbox2.setLayout(layout2)

        # 创建一个 QSplitter
        splitter = QSplitter(Qt.Horizontal)

        # 将已有的 QGroupBox 添加到 QSplitter 中
        splitter.addWidget(groupbox1)
        splitter.addWidget(groupbox2)

        # 可选：设置初始大小比例
        splitter.setSizes([150, 250])  # 左边 150 像素，右边 250 像素

        # 将 QSplitter 添加到主窗口
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    app.exec()
