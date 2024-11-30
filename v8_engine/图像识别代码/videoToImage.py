import locale
import sys
import traceback

import cv2
import threading
import time
import queue
import numpy as np


from commonDef import run_server, processing_frames, reset_frame_size, init_camera, reconfig, processing_frames_end,start_udp_server,listside,target_height,target_width,masks
from SaveTheImageToAShared import image_queue_worker

import python_trt as myTr

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

canvas = np.zeros((1620, 1920, 3), dtype=np.uint8)


# 定义多边形的坐标
rect_coords_dict = listside


def run():
    global  canvas, config

    # 创建队列
    image_queue = queue.Queue()
    # 创建并启动工作线程
    image_queue_threading = threading.Thread(target=image_queue_worker, args=(image_queue,))
    image_queue_threading.start()

    config['model'] = myTr.Detector(model_path=b"best8.engine", dll_path=r"yolov8.dll")

    # 正式
    cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow("display", 1100, 800)

    resConfigtime = reconfig(config, 0)


    config['video_arr'] = []
    for i, cap in config['imgSimilarList'].items():
        config['video_arr'].append(cap['num'])

    config['video_arr'] = sorted(config['video_arr'])


    cap_num_list = {}
    for v in config['video_arr']:
        cap_num_list[str(v)] = int(v)

    cap_array = init_camera(cap_num_list, config)


    print('开始')

    try:

        while True:

            if int(time.time()) > config['closeCountdown']:
                config['run_toggle'] = False

            if config['run_toggle']:

                time11 = time.time()

                if canvas is None:
                    canvas = np.zeros((1620, 1920, 3), dtype=np.uint8)
                    cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)  # 创建一个具有扩展GUI的窗口
                    cv2.resizeWindow("display", 1100, 800)  # 设置窗口大小为1100x1000像素

                resConfigtime = reconfig(config, resConfigtime)

                integration_frame_array = {}
                for v in config['video_arr']:
                    integration_frame_array[str(v)] = False

                for i, cap in cap_array.items():


                    res1 = processing_frames(i, cap, True, config, image_queue,True,0)
                    processing_frames_end(res1, i, cap, cap_array, integration_frame_array,config)

                # unfinished_tasks = image_queue.unfinished_tasks
                # print(f"Unfinished tasks: {unfinished_tasks}")


                resized_images = reset_frame_size(integration_frame_array, target_width, target_height,config)





                if config['imgSimilarList'].get('11') is not None and resized_images[config['imgSimilarList']['11']['num']] is not False:
                    canvas[0:target_height, 0:960] = resized_images[config['imgSimilarList']['11']['num']]  # 左上部
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[11], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[11], mask_non_zero, canvas[0:target_height, 0:960])  # 根据掩码进行复制

                if config['imgSimilarList'].get('9') is not None and resized_images[config['imgSimilarList']['9']['num']] is not False:
                    canvas[target_height:1080, 0:960] = resized_images[config['imgSimilarList']['9']['num']]  # 左中部
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[9], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[9], mask_non_zero, canvas[target_height:1080, 0:960])  # 根据掩码进行复制

                if config['imgSimilarList'].get('7') is not None and resized_images[config['imgSimilarList']['7']['num']] is not False:
                    canvas[1080:1620, 0:960] = resized_images[config['imgSimilarList']['7']['num']]  # 左下部
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[7], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[7], mask_non_zero, canvas[1080:1620, 0:960])  # 根据掩码进行复制


                if config['imgSimilarList'].get('12') is not None and resized_images[config['imgSimilarList']['12']['num']] is not False:
                    canvas[0:target_height, target_width:1920] = resized_images[config['imgSimilarList']['12']['num']]  # 右上角
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[12], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[12], mask_non_zero, canvas[0:target_height, target_width:1920])  # 根据掩码进行复制

                if config['imgSimilarList'].get('10') is not None and resized_images[config['imgSimilarList']['10']['num']] is not False:
                    canvas[target_height:1080, target_width:1920] = resized_images[config['imgSimilarList']['10']['num']]  # 右中部
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[10], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[10], mask_non_zero, canvas[target_height:1080, target_width:1920])  # 根据掩码进行复制

                if config['imgSimilarList'].get('8') is not None and resized_images[config['imgSimilarList']['8']['num']] is not False:
                    canvas[1080:1620, target_width:1920] = resized_images[config['imgSimilarList']['8']['num']]  # 右下角  5
                    if config['show_edges']:
                        mask_non_zero = (cv2.cvtColor(masks[8], cv2.COLOR_BGR2GRAY) != 0).astype(np.uint8)  # 创建单通道掩码，非零值为1
                        cv2.copyTo(masks[8], mask_non_zero, canvas[1080:1620, target_width:1920])  # 根据掩码进行复制



                time22 = time.time()
                print(str(int((time22 - time11) * 1000)) + "---------")


                cv2.imshow("display", canvas)
                cv2.waitKey(1)

            else:

                canvas = None

                cv2.destroyAllWindows()

                time.sleep(2)

    except Exception as e:
        # 捕获所有代码运行中的异常
        print(f"发生错误: {e}")
        traceback.print_exc()  # 输出详细的错误堆栈

    except KeyboardInterrupt:
        # 当检测到Ctrl+C时，执行以下代码
        print("检测到中断，正在安全关闭程序...")
    except SystemExit:
        # 捕获SystemExit异常，确保finally块执行
        print("系统退出")
    finally:

        # 在退出时关闭摄像头或其他资源
        for i, cap in cap_array.items():
            cap.release()

        cv2.destroyAllWindows()

        print("已释放资源")
        sys.exit(0)  # 确保

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
        'server_address_data': ("192.168.0.228", 19734),
        'nameLists': {},
        'saveImgRun': 0,
        'saveImgNum': '',
        'saveImgPath': './testimg3',
        'save_ball_num': '',
        'saveBackground': 0,
        'run_toggle': True,
        'closeCountdown': int(time.time()) + 600,
        'w': 1920,
        'h': 1080,
        'fps': 600,
        'runtime': 0,
        'show_edges': True,
        'video_arr': [],
    }


    run_server_var = threading.Thread(target=run_server, args=('', 8080, config))
    run_server_var.start()

    run_server_udp = threading.Thread(target=start_udp_server, args=('', 19735, config))
    run_server_udp.start()

    run()

# pip3 install pyinstaller

# pyinstaller  -F -n "videoToImage" videoToImage.py

# pyinstaller  -n "videoToImage" videoToImage.py



