import cv2

# 使用 DSHOW 后端打开摄像头
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# 替换 DSHOW 为其他后端试试（适用于不同系统）
# cap = cv2.VideoCapture(1, cv2.CAP_MSMF)       # Media Foundation (默认，出错了就不要用)


if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取画面")
        break

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
