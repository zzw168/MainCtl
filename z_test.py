from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtGui import QShowEvent
from kaj789_Ui import Ui_Dialog_Kaj789_Ui

class Kaj789Ui(QDialog, Ui_Dialog_Kaj789_Ui):
    def __init__(self):
        super().__init__()
        self.labels = []  # 可用于存储其他控件

    def setupUi(self, z_dialog):
        super().setupUi(z_dialog)  # 初始化 UI

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)  # 调用父类的 showEvent
        print('~~~~~~~~~~~~~~~')  # 窗口显示时触发


# 在主程序中运行
if __name__ == "__main__":
    app = QApplication([])
    Kaj789_ui = Kaj789Ui()  # 创建 UI 实例
    Kaj789_ui.setupUi(Kaj789_ui)  # 初始化界面
    Kaj789_ui.show()  # 显示窗口，触发 showEvent
    app.exec()  # 进入事件循环
