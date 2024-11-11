from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys


class MainWindow(QMainWindow):
    def closeEvent(self, event):
        # 创建确认对话框
        reply = QMessageBox.question(
            self,
            "确认退出",
            "您确定要退出程序吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # 检查用户的响应
        if reply == QMessageBox.Yes:
            event.accept()  # 接受关闭事件，程序退出
        else:
            event.ignore()  # 忽略关闭事件，程序继续运行


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
