from ultralytics import YOLO
import cv2
import threading
import time
import queue
import numpy as np

from commonDef import run_server, processing_frames, reset_frame_size, init_camera, reconfig, processing_frames_end, \
    listside, start_udp_server
from SaveTheImageToAShared import image_queue_worker

import python_trt as myTr

# pip install scikit-image numpy matplotlib
# pip install ultralytics
# pip install opencv-python
# pip install scikit-image


target_width, target_height = 960, 540  # 1920, 1000
canvas = np.zeros((1620, 1920, 3), dtype=np.uint8)

# 定义多边形的坐标
rect_coords_dict = listside

# 原始图像尺寸
original_width = 1280
original_height = 720


# 根据目标尺寸进行比例缩放
def scale_coords(coords, target_width, target_height, original_width, original_height):
    return [(int(x * target_width / original_width), int(y * target_height / original_height)) for x, y in coords]


# 生成等比例缩放的遮罩
masks = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}
for i in range(1, 13):  # Assuming you have 6 sets of coordinates
    coords = rect_coords_dict[i]
    scaled_coords = scale_coords(coords, target_width, target_height, original_width, original_height)
    mask = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    pts = np.array(scaled_coords, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(mask, [pts], isClosed=True, color=(0, 255, 0), thickness=6)
    masks[i] = mask


def run():
    global target_width, target_height, canvas, config, mask

    # 创建队列
    image_queue = queue.Queue()
    # 创建并启动工作线程
    image_queue_threading = threading.Thread(target=image_queue_worker, args=(image_queue,))
    image_queue_threading.start()

    config['model'] = YOLO("best.pt")
    # config['model'] = myTr.Detector(model_path=b"./trt/best_fp16.trt", dll_path="./trt/yolov8.dll")

    # 正式

    cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow("display", 1100, 800)

    # cap_num_list = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}

    cap_num_list = {'0': 0}

    cap_array = init_camera(cap_num_list, config)

    print('开始')

    # 获取当前时间戳
    startImgtime = 0
    resConfigtime = 0

    while True:

        if int(time.time()) > config['closeCountdown']:
            config['run_toggle'] = False

        if config['run_toggle']:

            time11 = time.time()

            if config['model'] == False:
                config['model'] = YOLO("best.pt")
                # config['model'] = myTr.Detector(model_path=b"./trt/best_fp16.trt", dll_path="./trt/yolov8.dll")

                canvas = np.zeros((1620, 1920, 3), dtype=np.uint8)

                cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)  # 创建一个具有扩展GUI的窗口
                cv2.resizeWindow("display", 1100, 800)  # 设置窗口大小为1100x1000像素

            resConfigtime = reconfig(config, resConfigtime)

            integration_frame_array = {'0': False, '1': False, '2': False, '3': False, '4': False, '5': False}

            time11_1 = time.time()
            for i, cap in cap_array.items():

                cap_num = int(i)

                ret, frame = cap.read()



                indexes_num_equals_2 = [key for key, value in config['imgSimilarList'].items() if
                                        value['num'] == int(cap_num)]

                if indexes_num_equals_2:

                    indexes_num_equals_1 = indexes_num_equals_2[0]

                    if config['flipList'][str(cap_num)] != -2:
                        frame = cv2.flip(frame, config['flipList'][str(cap_num)])

                    if indexes_num_equals_1 == '3':
                        height2, width2 = frame.shape[:2]
                        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                        frame = cv2.resize(frame, (height2, width2))


                res1 = frame


                if indexes_num_equals_2:
                    indexes_num_equals_1 = indexes_num_equals_2[0]
                    print(indexes_num_equals_1)
                    image_queue.put(
                        (f"./img/", f"{str(indexes_num_equals_1) + '-' + str(int(time.time() * 1000))}.jpg", frame))

                processing_frames_end(res1, i, cap, cap_array, integration_frame_array, config)

            unfinished_tasks = image_queue.unfinished_tasks
            print(f"Unfinished tasks: {unfinished_tasks}")

            if unfinished_tasks > 3000:
                time.sleep(90)

            resized_images = reset_frame_size(integration_frame_array, target_width, target_height, config)

            if resized_images[config['imgSimilarList']['11']['num']] is not False and config['imgSimilarList'].get(
                    '11') is not None and config['imgSimilarList']['11']['num'] < len(resized_images):
                canvas[0:target_height, 0:960] = resized_images[config['imgSimilarList']['11']['num']]  # 左上部
                if config['show_edges']:
                    canvas[0:target_height, 0:960] = cv2.addWeighted(canvas[0:target_height, 0:960], 1, masks[11], 1, 0)

            if resized_images[config['imgSimilarList']['9']['num']] is not False and config['imgSimilarList'].get(
                    '9') is not None and config['imgSimilarList']['9']['num'] < len(resized_images):
                canvas[target_height:1080, 0:960] = resized_images[config['imgSimilarList']['9']['num']]  # 左中部
                if config['show_edges']:
                    canvas[target_height:1080, 0:960] = cv2.addWeighted(canvas[target_height:1080, 0:960], 1, masks[9],
                                                                        1, 0)

            if resized_images[config['imgSimilarList']['7']['num']] is not False and config['imgSimilarList'].get(
                    '7') is not None and config['imgSimilarList']['7']['num'] < len(resized_images):
                canvas[1080:1620, 0:960] = resized_images[config['imgSimilarList']['7']['num']]  # 左下部
                if config['show_edges']:
                    canvas[1080:1620, 0:960] = cv2.addWeighted(canvas[1080:1620, 0:960], 1, masks[7], 1, 0)

            if resized_images[config['imgSimilarList']['12']['num']] is not False and config['imgSimilarList'].get(
                    '12') is not None and config['imgSimilarList']['12']['num'] < len(resized_images):
                canvas[0:target_height, target_width:1920] = resized_images[
                    config['imgSimilarList']['12']['num']]  # 右上角
                if config['show_edges']:
                    canvas[0:target_height, target_width:1920] = cv2.addWeighted(
                        canvas[0:target_height, target_width:1920], 1, masks[12], 1, 0)

            if resized_images[config['imgSimilarList']['10']['num']] is not False and config['imgSimilarList'].get(
                    '10') is not None and config['imgSimilarList']['10']['num'] < len(resized_images):
                canvas[target_height:1080, target_width:1920] = resized_images[
                    config['imgSimilarList']['10']['num']]  # 右中部
                if config['show_edges']:
                    canvas[target_height:1080, target_width:1920] = cv2.addWeighted(
                        canvas[target_height:1080, target_width:1920], 1, masks[10], 1, 0)

            if resized_images[config['imgSimilarList']['8']['num']] is not False and config['imgSimilarList'].get(
                    '8') is not None and config['imgSimilarList']['8']['num'] < len(resized_images):
                canvas[1080:1620, target_width:1920] = resized_images[config['imgSimilarList']['8']['num']]  # 右下角  5
                if config['show_edges']:
                    canvas[1080:1620, target_width:1920] = cv2.addWeighted(canvas[1080:1620, target_width:1920], 1,
                                                                           masks[8], 1, 0)

            cv2.imshow("display", canvas)
            cv2.waitKey(1)

            time22 = time.time()
            print(str(int((time22 - time11) * 1000)) + "---------")

        else:

            del canvas
            canvas = False

            del config['model']
            config['model'] = False

            cv2.destroyAllWindows()

            time.sleep(2)


if __name__ == "__main__":

    config = {
        'myimgsz': 1920,
        'imgSimilarList': {},
        'allCamerasTurnedOnList': {},
        'flipList': {
            '0': -2,
            '1': -2,
            '2': -2,
            '3': -2,
            '4': -2,
            '5': -2,
        },
        'model': None,
        'server_address_data': ("192.168.0.58", 19734),
        'nameLists': {},
        'saveImgRun': 0,
        'saveImgNum': '',
        'saveImgPath': './testimg3',
        'saveBackground': 0,
        'run_toggle': True,
        'closeCountdown': int(time.time()) + 600,
        'w': 1920,
        'h': 1080,
        'fps': 60,
        'runtime': 0,
        'show_edges': True,
    }

    nameListssub = {'yellow': 0, 'blue': 0, 'red': 0, 'purple': 0, 'orange': 0, 'green': 0, 'Brown': 0, 'black': 0,
                    'pink': 0, 'White': 0, 'xx_s_yello': 0, 'xx_s_white': 0, 'xx_s_red': 0, 'xx_s_black': 0}

    for i in range(6):
        config['nameLists'][str(i)] = nameListssub.copy()

    run_server_var = threading.Thread(target=run_server, args=('', 8080, config))
    run_server_var.start()

    run_server_udp = threading.Thread(target=start_udp_server, args=('', 19735, config))
    run_server_udp.start()

    run()
