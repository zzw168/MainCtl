import base64
import json
import os
import sys
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

import cv2
import numpy as np
import requests
from ultralytics import YOLO
from PIL import ImageFont, ImageDraw, Image
from urllib3 import request


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.models = {
            'obs': YOLO('./best_obs.pt'),
            'monitor': YOLO('./best_rtsp.pt')
        }
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        self.wfile.write(str('ok').encode('utf8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data)

        if 'CameraType' not in post_data or 'img' not in post_data:
            self.send_response(400)
            self.wfile.write("Missing required parameters.".encode('utf-8'))
            return

        if post_data['CameraType'][0] in ['obs', 'monitor']:
            model = self.models['obs'] if post_data['CameraType'][0] == 'obs' else self.models['monitor']
            np_array = np.frombuffer(base64.b64decode(post_data['img'][0].encode('ascii')), np.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            results = model.predict(
                source=img,
                conf=0.25,
                save=False,
                save_txt=False,
                save_conf=False,
                save_crop=False,
                visualize=False,
                # name=r'\\DESKTOP-HTBOISO\images\txt',
            )
            names = results[0].names
            qiu_array = []
            for r in results[0].boxes.data:
                array = [int(r[0].item()), int(r[1].item()), int(r[2].item()), int(r[3].item()),
                         round(r[4].item(), 2), names[int(r[5].item())]]
                cv2.rectangle(img, (array[0], array[1]), (array[2], array[3]), color=color_rects[array[5]], thickness=5)

                # 计算边界框的中心点
                if post_data['sort'][0] in ['0', '1']:
                    center_x = (array[0] + array[2]) // 2
                    center_y = array[1] - 35
                else:
                    center_x = array[0] - 35
                    center_y = (array[1] + array[3]) // 2

                # 在中心点绘制填充的圆球
                cv2.circle(
                    img,
                    (center_x, center_y),  # 圆心坐标
                    radius=30,  # 圆的半径
                    color=color_rects[array[5]],  # 圆的颜色
                    thickness=-1  # 填充圆球
                )
                if post_data['sort'][0] in ['0', '1']:
                    text_x = (array[0] + array[2]) // 2 - 13
                    text_y = array[1] - 22
                else:
                    text_x = array[0] - 50
                    text_y = (array[1] + array[3]) // 2 + 13
                if color_ch[array[5]] in ['1', '10']:
                    if color_ch[array[5]] == '10':
                        text_x -= 15
                    cv2.putText(img, "%s" % (color_ch[array[5]]), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1.3,
                                color=(0, 0, 0), thickness=3)
                else:
                    cv2.putText(img, "%s" % (color_ch[array[5]]), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1.3,
                                color=(248, 248, 255), thickness=3)
                # font_path = 'simhei.ttf'  # 你的中文字体文件路径，例如黑体
                # font_size = 50  # 字体大小
                # # 使用 Pillow 绘制中文
                #
                # img = draw_chinese_text(img, color_ch[array[5]], (x, y), font_path, font_size,
                #                         color_names[array[5]])
                qiu_array.append(array)
            if post_data['sort'][0] == '0':
                qiu_array.sort(key=lambda x: (x[0]), reverse=True)
            elif post_data['sort'][0] == '1':
                qiu_array.sort(key=lambda x: (x[0]), reverse=False)
            elif post_data['sort'][0] == '11':
                qiu_array.sort(key=lambda y: (y[1]), reverse=True)
            else:
                qiu_array.sort(key=lambda y: (y[1]), reverse=False)
            qiu_rank = []
            for i in range(len(qiu_array)):
                if qiu_array[i][5] not in qiu_rank:
                    qiu_rank.append(qiu_array[i][5])
            qiu_rank = json.dumps(qiu_rank)
            # cv2 图片转换为图片字符串
            byte_encode = np.array(cv2.imencode('.jpg', img)[1]).tobytes()  # 转换为内存字节码
            # print(type(byte_encode))
            re_data = [byte_encode, qiu_rank, post_data['CameraType'][0]]
            self.wfile.write(str(re_data).encode('utf8'))
        else:
            self.wfile.write(str('ok').encode('utf8'))

    print('执行开始')


def draw_chinese_text(image, text, position, font_path, font_size, color):
    # 转换 OpenCV 图像为 PIL 图像
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)

    # 绘制文字
    draw.text(position, text, font=font, fill=color)

    # 转回 OpenCV 图像
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def check_port_in_use(host, port):
    """检查指定的端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False  # 端口未被占用
        except OSError:
            return True  # 端口被占用


def run_server():
    server_address = ('0.0.0.0', 6066)

    # 检测端口是否被占用
    if check_port_in_use(*server_address):
        print(f"Error: Port {server_address[1]} is already in use.")
        sys.exit(1)  # 优雅退出程序

    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Starting server on port 6066...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


if __name__ == '__main__':
    color_names = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
                   'pink': (255, 0, 255), 'yellow': (255, 255, 0), 'black': (0, 0, 0),
                   'purple': (128, 0, 128), 'orange': (255, 165, 0), 'White': (248, 248, 255),
                   'Brown': (139, 69, 19)}
    color_rects = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0),
                   'pink': (255, 0, 255), 'yellow': (0, 255, 255), 'black': (0, 0, 0),
                   'purple': (128, 0, 128), 'orange': (0, 165, 255), 'White': (255, 248, 248),
                   'Brown': (19, 69, 139)}
    color_ch = {'yellow': '1',
                'blue': '2',
                'red': '3',
                'purple': '4',
                'orange': '5',
                'green': '6',
                'Brown': '7',
                'black': '8',
                'pink': '9',
                'White': '10'}
    # color_ch = {'yellow': '黄',
    #             'blue': '蓝',
    #             'red': '红',
    #             'purple': '紫',
    #             'orange': '橙',
    #             'green': '绿',
    #             'Brown': '棕',
    #             'black': '黑',
    #             'pink': '粉',
    #             'White': '白'}
    run_server()
