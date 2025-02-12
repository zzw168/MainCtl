from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QEvent, Signal
import sys

from Camera_Ui import Ui_Camera_Dialog


class CameraUi(QDialog, Ui_Camera_Dialog):
    signal = Signal()  # 定义一个信号

    def __init__(self):
        super().__init__()

    def setupUi(self, z_dialog):
        super(CameraUi, self).setupUi(z_dialog)

    def hideEvent(self, event: QEvent):
        print("Main Camera UI 窗口被隐藏！")  # 这里执行你的逻辑
        event.accept()  # 允许隐藏

app = QApplication(sys.argv)
main_camera_ui = CameraUi()
main_camera_ui.show()

# 3 秒后隐藏窗口
# QApplication.instance().processEvents()
main_camera_ui.hide()

sys.exit(app.exec())
