import sys
import json
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class AnnotationViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("标注查看器（下拉筛选）")
        self.setGeometry(200, 200, 1000, 800)

        self.image_path = None
        self.json_path = None
        self.raw_data = {}
        self.all_boxes = []
        self.filtered_boxes = []
        self.index = 0

        self.label = QLabel("请加载图片和 JSON 文件", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.btn_open_image = QPushButton("选择图片")
        self.btn_open_json = QPushButton("选择 JSON")
        self.btn_prev = QPushButton("← 上一个")
        self.btn_next = QPushButton("→ 下一个")

        self.btn_open_image.clicked.connect(self.open_image)
        self.btn_open_json.clicked.connect(self.open_json)
        self.btn_prev.clicked.connect(self.prev_box)
        self.btn_next.clicked.connect(self.next_box)

        self.color_combo = QComboBox()
        self.index_combo = QComboBox()
        self.color_combo.currentIndexChanged.connect(self.apply_filter)
        self.index_combo.currentIndexChanged.connect(self.apply_filter)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_open_image)
        btn_layout.addWidget(self.btn_open_json)
        btn_layout.addWidget(self.btn_prev)
        btn_layout.addWidget(self.btn_next)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("颜色选择:"))
        filter_layout.addWidget(self.color_combo)
        filter_layout.addWidget(QLabel("镜头选择:"))
        filter_layout.addWidget(self.index_combo)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.image_path = file_path
            self.load_data()

    def open_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 JSON 文件", "", "JSON Files (*.json)")
        if file_path:
            self.json_path = file_path
            self.load_data()

    def load_data(self):
        if not self.json_path:
            return
        if self.image_path:
            self.base_image = cv2.imread(self.image_path)
        else:
            self.base_image = np.ones((720, 1280, 3), dtype=np.uint8) * 255

        try:
            with open(self.json_path, "r") as f:
                self.raw_data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"读取 JSON 出错：{e}")
            return

        self.all_boxes = []
        for color, boxes in self.raw_data.items():
            for box in boxes:
                box = list(box)
                box.append(color)  # 添加颜色字段到 box[7]
                self.all_boxes.append(box)

        if not self.all_boxes:
            QMessageBox.warning(self, "无数据", "JSON 文件中未找到任何标注框")
            return

        self.rebuild_filters()
        self.apply_filter()

    def rebuild_filters(self):
        self.color_combo.blockSignals(True)
        self.index_combo.blockSignals(True)

        self.color_combo.clear()
        self.index_combo.clear()

        self.color_combo.addItem("全部")
        for color in sorted(self.raw_data.keys()):
            self.color_combo.addItem(color)

        self.index_combo.addItem("全部")
        all_indices = sorted({box[6] for box in self.all_boxes})
        for idx in all_indices:
            self.index_combo.addItem(str(idx))

        self.color_combo.blockSignals(False)
        self.index_combo.blockSignals(False)

    def apply_filter(self):
        color_sel = self.color_combo.currentText()
        index_sel = self.index_combo.currentText()

        self.filtered_boxes = []

        for color, boxes in self.raw_data.items():
            if color_sel != "全部" and color != color_sel:
                continue
            for box in boxes:
                if index_sel != "全部" and str(box[6]) != index_sel:
                    continue
                box = list(box)
                box.append(color)  # box[7] 是颜色
                self.filtered_boxes.append(box)

        if not self.filtered_boxes:
            self.label.setText("筛选后无可显示数据")
            self.btn_prev.setEnabled(False)
            self.btn_next.setEnabled(False)
            return

        self.index = 0
        self.btn_prev.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.update_view()

    def update_view(self):
        if not self.filtered_boxes:
            return
        box = self.filtered_boxes[self.index]
        img = self.draw_box(self.base_image.copy(), box)
        self.show_image(img)

    def draw_box(self, image, box):
        x1, y1, x2, y2 = map(int, box[:4])
        conf = box[4]
        idx = box[6]
        color = box[5]
        label = f"{color} {conf:.2f} ID:{idx}"

        color_map = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0),
                            'pink': (255, 0, 255), 'yellow': (0, 255, 255), 'black': (0, 0, 0),
                            'purple': (128, 0, 128), 'orange': (0, 165, 255),
                            'White': (255, 248, 248),
                            'Brown': (19, 69, 139)}
        box_color = color_map.get(color, (255, 255, 255))

        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        cv2.putText(image, f"{self.index + 1}/{len(self.filtered_boxes)}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return image

    def show_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_img).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

    def next_box(self):
        if self.index + 1 < len(self.filtered_boxes):
            self.index += 1
            self.update_view()

    def prev_box(self):
        if self.index > 0:
            self.index -= 1
            self.update_view()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.prev_box()
        elif event.key() == Qt.Key_Right:
            self.next_box()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AnnotationViewer()
    viewer.show()
    sys.exit(app.exec())
