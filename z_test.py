from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMdiArea, QMdiSubWindow
import sys

class MyUi:
    """主窗口 UI 类。"""
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Main Window")
        MainWindow.setGeometry(100, 100, 800, 600)

        # 添加 QMdiArea 到主窗口中，用于管理子窗口
        self.mdi_area = QMdiArea(MainWindow)
        MainWindow.setCentralWidget(self.mdi_area)

class SpeedUi:
    """子窗口 UI 类。"""
    def setupUi(self, MainWidget):
        MainWidget.setWindowTitle("Speed Widget")
        MainWidget.setGeometry(200, 200, 300, 200)

def main():
    app = QApplication(sys.argv)

    # 创建主窗口
    MainWindow = QMainWindow()
    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # 创建子窗口并添加到 MdiArea 中
    MainWidget = QWidget()
    speed_ui = SpeedUi()
    speed_ui.setupUi(MainWidget)

    sub_window = QMdiSubWindow()  # 创建 MDI 子窗口
    sub_window.setWidget(MainWidget)  # 将子窗口的 widget 设置给 MDI 子窗口
    ui.mdi_area.addSubWindow(sub_window)  # 将 MDI 子窗口添加到主窗口的 MDI 区域
    sub_window.show()  # 显示子窗口

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
