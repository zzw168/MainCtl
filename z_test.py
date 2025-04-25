# import obsws_python as obs
#
# # 连接到 OBS WebSocket
# client = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
#
# # 刷新 "浏览器来源"（Browser Source）
# client.press_input_properties_button("浏览器", "refreshnocache")
#
# # 断开连接
# client.disconnect()
#
# print("已刷新浏览器来源")

# import numpy as np
# from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
#
# x = np.array([0, 1, 2, 3])
# y = np.array([0, 1, 4, 9])
#
# # f = interp1d(x, y, kind='next')  # 三次样条插值
# # f = interp1d(x, y, kind='previous')  # 三次样条插值
# # f = interp1d(x, y, kind='nearest')  # 三次样条插值
# f = interp1d(x, y, kind='cubic')  # 三次样条插值
# # f = interp1d(x, y, kind='linear')  # 线性插值
# # f = interp1d(x, y, kind='quadratic')  # 二次插值
#
# x_new = np.linspace(0, 3, 100)
# y_new = f(x_new)
#
# plt.plot(x, y, 'o', label='aaa')
# plt.plot(x_new, y_new, '-', label='bbb')
# plt.legend()
# plt.show()

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent
from PySide6.QtCore import Qt, QPointF
import sys

class DraggableCurveWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("可添加/拖动点的连续曲线")
        self.resize(800, 600)

        self.points = []  # 所有控制点
        self.dragging_point_index = -1  # 当前正在拖动的点索引
        self.point_radius = 6

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 画曲线
        if len(self.points) >= 2:
            pen = QPen(QColor(0, 150, 255), 2)
            painter.setPen(pen)
            for i in range(len(self.points) - 1):
                painter.drawLine(self.points[i], self.points[i + 1])

        # 画控制点
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 100, 100))
        for pt in self.points:
            painter.drawEllipse(pt, self.point_radius, self.point_radius)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            index = self.get_near_point_index(pos)
            if index != -1:
                # 开始拖动已有点
                self.dragging_point_index = index
            else:
                # 添加新点
                self.points.append(QPointF(pos))
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging_point_index != -1:
            pos = event.position()
            self.points[self.dragging_point_index] = QPointF(pos)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging_point_index = -1

    def get_near_point_index(self, pos: QPointF, threshold=10) -> int:
        for i, pt in enumerate(self.points):
            if (pt - pos).manhattanLength() < threshold:
                return i
        return -1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DraggableCurveWidget()
    window.show()
    sys.exit(app.exec())
