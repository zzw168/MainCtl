import sys
import json
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
)
from PySide6.QtGui import QImage, QPixmap, QKeyEvent
from PySide6.QtCore import Qt

class BoxViewer(QMainWindow):
    def __init__(self, json_path, image_path=None):
        super().__init__()
        self.setWindowTitle("Box Viewer")

        # === 加载数据 ===
        with open(json_path, "r") as f:
            self.data = json.load(f)
        self.all_boxes = []
        for color, boxes in self.data.items():
            for box in boxes:
                self.all_boxes.append(box)
        self.index = 0

        # === 加载图像或创建白底图像 ===
        if image_path:
            self.base_image = cv2.imread(image_path)
        else:
            self.base_image = np.ones((720, 1280, 3), dtype=np.uint8) * 255

        # === 设置界面 ===
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        prev_btn = QPushButton("← 上一个")
        next_btn = QPushButton("下一个 →")

        prev_btn.clicked.connect(self.show_prev)
        next_btn.clicked.connect(self.show_next)

        h_layout = QHBoxLayout()
        h_layout.addWidget(prev_btn)
        h_layout.addWidget(next_btn)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label)
        v_layout.addLayout(h_layout)

        central = QWidget()
        central.setLayout(v_layout)
        self.setCentralWidget(central)

        self.update_view()

    def draw_box(self, image, box):
        x1, y1, x2, y2 = box[0:4]
        conf = box[4]
        color = box[5]
        label = f"{color} {conf:.2f}"

        color_map = {
            "yellow": (0, 255, 255),
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0)
        }
        box_color = color_map.get(color, (255, 255, 255))

        img = image.copy()
        cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 1)
        cv2.putText(img, f"{self.index+1}/{len(self.all_boxes)}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return img

    def update_view(self):
        box = self.all_boxes[self.index]
        image = self.draw_box(self.base_image, box)

        # 转换为 Qt 显示格式
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qt_image)
        self.label.setPixmap(pix)

    def show_prev(self):
        self.index = (self.index - 1) % len(self.all_boxes)
        self.update_view()

    def show_next(self):
        self.index = (self.index + 1) % len(self.all_boxes)
        self.update_view()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [Qt.Key_Left, Qt.Key_A]:
            self.show_prev()
        elif event.key() in [Qt.Key_Right, Qt.Key_D]:
            self.show_next()
        elif event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BoxViewer("9692712.json", "11_2.jpg")  # 可选传入 image_path="image.jpg"
    window.resize(1920, 1080)
    window.show()
    sys.exit(app.exec())
