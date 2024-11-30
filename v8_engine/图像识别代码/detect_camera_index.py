
import cv2
import numpy as np


from commonDef import run_server, processing_frames, reset_frame_size, init_camera, reconfig, processing_frames_end,start_udp_server,listside,get_frame



canvas = np.zeros((2000, 100, 3), dtype=np.uint8)


# 定义多边形的坐标
rect_coords_dict = listside

# 原始图像尺寸
original_width = 1920
original_height = 1080


def run():
    global canvas, config

    cv2.namedWindow("display", cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow("display", 100, 800)

    cap_num_list = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'11':11,'12':12,'13':13,'14':14}
    cap_array = init_camera(cap_num_list, config)

    while True:

        video_frame_arr = {'0': False, '1': False, '2': False, '3': False, '4': False, '5': False, '6': False,
                           '7': False, '8': False, '9': False, '10': False, '11': False, '12': False, '13': False,
                           '14': False}

        for i, cap in cap_array.items():

            ret, frame = cap.read()

            if not ret:
                print(f"读取帧失败 --- {i}")

            else:

                frame = cv2.resize(frame, (100, 80))


                cv2.putText(frame, str(i), (30, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=2,
                            color=(0, 0, 255), thickness=3)

                video_frame_arr[i] = frame



        for i, v in video_frame_arr.items():
            i = int(i)  # 将字符串 i 转换为整数

            if v is not False:
                # 进行坐标的计算时，i 现在是整数
                canvas[int(80 * i):int(80 * (i + 1)), 0:100] = v



        cv2.imshow("display", canvas)
        cv2.waitKey(1)


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
        'closeCountdown':  6000000,
        'w': 1920,
        'h': 1080,
        'fps': 600,
        'runtime': 0,
        'show_edges': True,
        'video_arr': [],
    }

    run()

