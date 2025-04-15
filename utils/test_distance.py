import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QStatusBar
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

class InteractivePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("曲线最近点可视化工具（完整版）")
        self.setMinimumSize(1000, 600)

        # 主界面和布局
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # 状态栏
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # 可用颜色
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'brown', 'gray']

        # 初始曲线数据（多个）
        x_vals = np.linspace(0, 4 * np.pi, 500)
        self.curves = [
            {'name': 'sin(x)', 'data': np.column_stack((x_vals, np.sin(x_vals))), 'enabled': True},
            {'name': 'cos(x)', 'data': np.column_stack((x_vals, np.cos(x_vals))), 'enabled': True},
            {'name': '0.5*sin(2x)', 'data': np.column_stack((x_vals, 0.5 * np.sin(2 * x_vals))), 'enabled': True},
        ]
        # 分配颜色
        for i, curve in enumerate(self.curves):
            curve['color'] = self.colors[i % len(self.colors)]

        # 初始点
        self.point = np.array([1.0, 1.5])
        self.dragging = False

        # 图形 & 工具栏
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # 事件绑定
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

        # 初始绘图
        self.plot()

    def load_curve_from_csv(self, path, name=None, enabled=True):
        try:
            data = np.loadtxt(path, delimiter=',')
            if data.shape[1] != 2:
                print(f"[格式错误] {path} 应为两列 (x, y)")
                return
            index = len(self.curves)
            curve = {
                'name': name or f"自定义{index}",
                'data': data,
                'enabled': enabled,
                'color': self.colors[index % len(self.colors)]
            }
            self.curves.append(curve)
            self.plot()
        except Exception as e:
            print(f"[读取失败] {path}: {e}")

    def find_closest_point(self, point):
        min_distance = float('inf')
        closest_point = None
        curve_name = ""
        curve_color = "red"
        for curve in self.curves:
            if not curve.get('enabled', True):
                continue
            data = curve['data']
            distances = np.linalg.norm(data - point, axis=1)
            idx = np.argmin(distances)
            if distances[idx] < min_distance:
                min_distance = distances[idx]
                closest_point = data[idx]
                curve_name = curve['name']
                curve_color = curve.get('color', 'red')
        return closest_point, min_distance, curve_name, curve_color

    def plot(self):
        self.ax.clear()

        # 绘制曲线
        for curve in self.curves:
            if curve.get('enabled', True):
                self.ax.plot(curve['data'][:, 0], curve['data'][:, 1],
                             label=curve['name'], color=curve.get('color', 'black'))

        # 最近点判断
        closest_point, min_distance, curve_name, curve_color = self.find_closest_point(self.point)

        # 点 & 距离线
        self.ax.scatter(*self.point, color='blue', label='已知点', zorder=5)
        self.ax.scatter(*closest_point, color=curve_color, label=f'最近点 - {curve_name}', zorder=5)
        self.ax.plot([self.point[0], closest_point[0]],
                     [self.point[1], closest_point[1]],
                     'k--', label='最短距离')

        self.ax.set_title("拖动蓝点，查看不同曲线的最近点")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

        # 状态栏更新
        self.status.showMessage(
            f"已知点: ({self.point[0]:.2f}, {self.point[1]:.2f}) | "
            f"最近点: ({closest_point[0]:.2f}, {closest_point[1]:.2f}) | "
            f"最短距离: {min_distance:.4f} | 所属曲线: {curve_name}"
        )

    def on_press(self, event):
        if event.inaxes:
            dist = np.linalg.norm(np.array([event.xdata, event.ydata]) - self.point)
            if dist < 0.3:
                self.dragging = True

    def on_release(self, event):
        self.dragging = False

    def on_motion(self, event):
        if self.dragging and event.inaxes:
            self.point = np.array([event.xdata, event.ydata])
            self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractivePlot()

    # 👉 示例：加载自定义 CSV 曲线（可选）
    # window.load_curve_from_csv("your_curve.csv", name="自定义曲线", enabled=True)

    window.show()
    sys.exit(app.exec())
