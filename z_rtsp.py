import cv2
import base64
import time
import os
import requests
import multiprocessing
import ast

def inner_get_rtsp(rt_url, area_Code, recognition_addr, lottery_term, end2_path, sort_text, check_h, check_v, queue):
    cap = cv2.VideoCapture(rt_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    jpg_base64 = ''

    if cap.isOpened():
        for attempt in range(3):
            ret = False
            frame = None
            for _ in range(3):
                ret, frame = cap.read()

            if ret and frame is not None:
                try:
                    # 裁剪区域
                    if len(area_Code['net']) > 0:
                        area = area_Code['net'][0]['coordinates']
                        x1, x2 = area[0][0], area[1][0]
                        y1, y2 = area[1][1], area[2][1]
                        frame = frame[y1:y2, x1:x2]

                        # 翻转
                        if check_h:
                            frame = cv2.flip(frame, 1)
                        if check_v:
                            frame = cv2.flip(frame, 0)

                    # jpg 编码 + base64
                    success, jpeg_data = cv2.imencode('.jpg', frame)
                    if success:
                        jpg_base64 = base64.b64encode(jpeg_data).decode('ascii')

                        if os.path.exists(end2_path):
                            img_file = os.path.join(end2_path, f'rtsp_{lottery_term[0]}_{int(time.time()*1000)}.jpg')
                            with open(img_file, 'wb') as f:
                                f.write(jpeg_data)

                        # 发送到识别接口
                        form_data = {
                            'CameraType': 'rtsp',
                            'img': jpg_base64,
                            'sort': sort_text,
                        }
                        res = requests.post(url=recognition_addr, data=form_data, timeout=8)
                        res.raise_for_status()

                        # 解析返回
                        r_list = ast.literal_eval(res.text)
                        r_img = r_list[0]

                        if os.path.exists(end2_path):
                            with open(os.path.join(end2_path, f'rtsp_end_{lottery_term[0]}_{int(time.time()*1000)}.jpg'), 'wb') as f:
                                f.write(r_img)

                        # 通过 queue 返回结果
                        queue.put(r_list)
                        cap.release()
                        return
                    else:
                        print("jpg_base64 转换错误！")
                except Exception as e:
                    print("图片处理或识别异常：", e)
            else:
                print("无法读取视频帧")
    else:
        print('无法打开摄像头')

    cap.release()
    queue.put([jpg_base64, '[1]', 'rtsp'])  # 返回空结果

def get_rtsp(r_url, area_Code, recognition_addr, lottery_term, end2_path, sort_text, check_h, check_v, timeout=20):
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=inner_get_rtsp, args=(
        r_url, area_Code, recognition_addr, lottery_term, end2_path, sort_text, check_h, check_v, queue))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        print(f'⛔ get_rtsp 超时（>{timeout}s），自动放弃！')
        return ['', '[1]', 'rtsp']
    else:
        if not queue.empty():
            return queue.get()
        else:
            print('⚠️ inner_get_rtsp 无返回结果')
            return ['', '[1]', 'rtsp']
