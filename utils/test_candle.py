import sys
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStatusBar

import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

class CandlestickViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互式蜡烛图：十字线 + 高亮K线")
        self.setMinimumSize(1200, 700)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.canvas = FigureCanvas(Figure(figsize=(12, 8)))
        self.fig = self.canvas.figure
        self.ax_price = self.fig.add_subplot(1, 1, 1)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # 初始化交互变量
        self.cursor_vline = None
        self.cursor_hline = None
        self.selected_rect = None
        self.rects = []

        self.data = self.load_data()
        self.plot_candlestick()

        # 鼠标交互
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

    def load_data(self):
        np.random.seed(42)
        dates = pd.date_range("2024-01-01", periods=60)
        price = np.cumsum(np.random.randn(len(dates)) * 2 + 100)
        df = pd.DataFrame(index=dates)
        df["Open"] = price
        df["Close"] = price + np.random.randn(len(dates)) * 2
        df["High"] = df[["Open", "Close"]].max(axis=1) + np.random.rand(len(dates))
        df["Low"] = df[["Open", "Close"]].min(axis=1) - np.random.rand(len(dates))
        df["Volume"] = np.random.randint(500, 1000, size=len(dates))
        df["Date_Num"] = mdates.date2num(df.index)
        return df

    def plot_candlestick(self):
        df = self.data
        self.ax_price.clear()
        self.rects.clear()

        width = 0.6
        for idx, row in df.iterrows():
            color = "green" if row["Close"] >= row["Open"] else "red"
            # 上下影线
            self.ax_price.plot([row["Date_Num"], row["Date_Num"]], [row["Low"], row["High"]], color=color)
            # 实体矩形
            body = Rectangle((row["Date_Num"] - width / 2, min(row["Open"], row["Close"])),
                             width, abs(row["Close"] - row["Open"]),
                             facecolor=color, edgecolor=color, linewidth=1)
            self.ax_price.add_patch(body)
            self.rects.append((row, body))

        self.ax_price.set_title("蜡烛图（鼠标拖动十字线 + 高亮K线）")
        self.ax_price.set_ylabel("价格")
        self.ax_price.grid(True)

        self.ax_price.xaxis_date()
        self.fig.autofmt_xdate()
        self.canvas.draw()

    def on_mouse_move(self, event):
        if not event.inaxes or event.xdata is None or event.ydata is None:
            return

        xdata = event.xdata
        ydata = event.ydata
        df = self.data

        # 找最近的K线
        idx = (np.abs(df["Date_Num"] - xdata)).argmin()
        row, rect = self.rects[idx]

        # 更新十字线
        if self.cursor_vline is None:
            self.cursor_vline = self.ax_price.axvline(row["Date_Num"], color='gray', linestyle='--', alpha=0.5)
            self.cursor_hline = self.ax_price.axhline(ydata, color='gray', linestyle='--', alpha=0.5)
        else:
            self.cursor_vline.set_xdata([row["Date_Num"], row["Date_Num"]])
            self.cursor_hline.set_ydata([ydata, ydata])

        # 高亮当前K线
        if self.selected_rect:
            self.selected_rect.set_linewidth(1)
            self.selected_rect.set_edgecolor(self.selected_rect.get_facecolor())

        rect.set_edgecolor("yellow")
        rect.set_linewidth(2)
        self.selected_rect = rect

        # 状态栏显示信息
        date = row.name.strftime('%Y-%m-%d')
        msg = f"时间: {date} | 开: {row['Open']:.2f} 高: {row['High']:.2f} 低: {row['Low']:.2f} 收: {row['Close']:.2f} 量: {row['Volume']}"
        self.status.showMessage(msg)

        self.canvas.draw_idle()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CandlestickViewer()
    viewer.show()
    sys.exit(app.exec())
