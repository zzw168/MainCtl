import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 支持中文
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

class InteractivePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互式最近点显示")
        self.setMinimumSize(800, 600)

        # 创建主Widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # 曲线数据
        self.x_vals = np.linspace(0, 4 * np.pi, 500)
        self.curve = np.column_stack((self.x_vals, np.sin(self.x_vals)))

        # 初始已知点
        self.point = np.array([1.0, 1.5])

        # 创建图形和画布
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        # 绑定鼠标点击事件
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # 首次绘图
        self.plot()

    def find_closest_point(self, point):
        distances = np.linalg.norm(self.curve - point, axis=1)
        min_index = np.argmin(distances)
        return self.curve[min_index]

    def plot(self):
        closest_point = self.find_closest_point(self.point)

        self.ax.clear()
        self.ax.plot(self.curve[:, 0], self.curve[:, 1], label="曲线 y = sin(x)")
        self.ax.scatter(*self.point, color='blue', label='已知点', zorder=5)
        self.ax.scatter(*closest_point, color='red', label='最近点', zorder=5)
        self.ax.plot(
            [self.point[0], closest_point[0]],
            [self.point[1], closest_point[1]],
            'k--', label='最短距离'
        )
        self.ax.set_title("点击图像设置已知点")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def on_click(self, event):
        # 如果点击在图像区域内
        if event.inaxes:
            self.point = np.array([event.xdata, event.ydata])
            self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractivePlot()
    window.show()
    sys.exit(app.exec())
