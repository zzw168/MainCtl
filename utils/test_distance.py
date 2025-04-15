import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("最近点显示 - PySide6 + Matplotlib")
        self.setMinimumSize(800, 600)

        # 创建主 widget 和布局
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 创建图形区域
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        # 获取 Axes
        self.ax = self.canvas.figure.add_subplot(111)

        # 画图
        self.plot_curve_and_point()

    def plot_curve_and_point(self):
        matplotlib.rcParams['font.family'] = 'SimHei'  # 使用黑体显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        # 曲线点集（y = sin(x)）
        x_vals = np.linspace(0, 4 * np.pi, 500)
        curve = np.column_stack((x_vals, np.sin(x_vals)))

        # 已知点
        point = np.array([1.0, 1.5])

        # 找最近点
        distances = np.linalg.norm(curve - point, axis=1)
        min_index = np.argmin(distances)
        closest_point = curve[min_index]

        # 清空图像，重新绘制
        self.ax.clear()
        self.ax.plot(curve[:, 0], curve[:, 1], label="曲线 y = sin(x)")
        self.ax.scatter(*point, color='blue', label='已知点')
        self.ax.scatter(*closest_point, color='red', label='最近点')
        self.ax.plot([point[0], closest_point[0]], [point[1], closest_point[1]], 'k--', label='最短距离')

        self.ax.set_title("PySide6 嵌入式图形显示")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec())
