import cv2
import time
import queue
import threading
from SaveTheImageToAShared import image_queue_worker

# 设置摄像头参数
def set_cap(cap):  # 设置视频截图参数（不压缩图
    # 片，节省压缩过程时间）
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 60)


    cap.set(cv2.CAP_PROP_BRIGHTNESS, 101)  # 设置亮度，范围一般在0到255之间
    cap.set(cv2.CAP_PROP_CONTRAST, 110)  # 设置对比度，范围一般在0到255之间
    cap.set(cv2.CAP_PROP_SATURATION, 91)  # 设置饱和度，范围一般在0到255之间
    cap.set(cv2.CAP_PROP_HUE, 10)  # 设置色调，范围一般在0到255之间
    cap.set(cv2.CAP_PROP_GAIN, 34)  # 设置增益，范围一般在0到255之间
    cap.set(cv2.CAP_PROP_EXPOSURE, -8)  # 设置曝光时间，通常曝光时间是负值，值越大曝光越长

    # 设置白平衡 U 和 V 值
    cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 4000)  # 设置 U 值
    cap.set(cv2.CAP_PROP_SHARPNESS, 22)
    # 尝试设置摄像头的焦距
    focus_supported = cap.set(cv2.CAP_PROP_FOCUS, 20)  # 焦距范围可能取决于摄像头，一般是 0 到最大值
    # 尝试设置摄像头的变焦
    zoom_supported = cap.set(cv2.CAP_PROP_ZOOM, 20)  # 变焦因子（放大倍数），取决于摄像头
    cap.set(cv2.CAP_PROP_SETTINGS, 1)



    W1 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    H1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps1 = cap.get(cv2.CAP_PROP_FPS)
    print(f"设置{W1}*{H1}  FPS={fps1}")



# 创建队列
image_queue = queue.Queue()
# 创建并启动工作线程
image_queue_threading = threading.Thread(target=image_queue_worker, args=(image_queue,))
image_queue_threading.start()





cap_num = 1
cap = cv2.VideoCapture(cap_num, cv2.CAP_DSHOW)

if not cap.isOpened():
    print(f'无法打开摄像头{cap_num}')

print('设置摄像头：' + str(cap_num))
set_cap(cap)



guid = cap.get(cv2.CAP_PROP_GUID)
print(f"Camera GUID: {guid}")



time1 = time.time()
num = 0

while True:
    time2 = time.time()

    if int((time2 - time1) * 1000) >= 1000:
        time1 = time.time()
        print(num)
        num = 0

        unfinished_tasks = image_queue.unfinished_tasks
        print(f"Unfinished tasks: {unfinished_tasks}")

    num += 1
    ret, frame = cap.read()

    if not ret:
        print(f'无法读取画面{cap_num}')
        break

    # 展示捕获的帧
    cv2.imshow('Captured Frame', frame)
    #
    # image_queue.put(
    #     (f"./images/", f"{str(int(time.time() * 1000))}.jpg", frame))
    #




    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
