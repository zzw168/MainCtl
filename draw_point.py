import json
import cv2
import numpy as np

# === 1. 读取 JSON 文件 ===
with open("9692712.json", "r") as f:
    data = json.load(f)

# === 2. 提取所有框，合并为一个列表（含颜色标签） ===
all_boxes = []
# print(data.keys())
# print(data['yellow'])
# for color, boxes in data.items():
for box in data['White']:
    if box[6] == 2:
        all_boxes.append(box)  # 已包含颜色在 box[5]

# === 3. 初始化变量 ===
index = 0
n = len(all_boxes)

# === 4. 你可以改为读取真实图像 ===
# image_base = np.ones((720, 1280, 3), dtype=np.uint8) * 255
image_base = cv2.imread('.\\11_2.jpg')

# === 5. 主循环：左右键切换显示 ===
while True:
    img = image_base.copy()
    box = all_boxes[index]
    x1, y1, x2, y2 = box[0:4]
    conf = box[4]
    color = box[5]
    label = f"{color} {conf:.2f}"

    # 设置颜色映射
    color_map = {
        "yellow": (0, 255, 255),
        "red": (0, 0, 255),
        "green": (0, 255, 0),
        "blue": (255, 0, 0)
    }
    box_color = color_map.get(color, (255, 255, 255))  # 默认白色

    # 画框 + 标签
    cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 2)
    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 1)
    cv2.putText(img, f"{index+1}/{n}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 显示图像
    cv2.imshow("Box Viewer", img)

    # 按键控制
    key = cv2.waitKey(0)
    if key == 27:  # ESC
        break
    elif key == ord('a') or key == 81:  # 左键 ← 或 A
        index = (index - 1) % n
    elif key == ord('d') or key == 83:  # 右键 → 或 D
        index = (index + 1) % n

cv2.destroyAllWindows()
