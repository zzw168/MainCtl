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
from urllib3 import request


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
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
        if post_data['CameraType'][0] in ['obs', 'monitor']:
            if post_data['CameraType'][0] == 'obs':
                model = YOLO('./best0.pt')
            else:
                model = YOLO('./best9.pt')
            image_str = post_data['img'][0].encode('ascii')
            image_byte = base64.b64decode(image_str)  # 图片字符串转为64位字节
            np_array = np.frombuffer(image_byte, np.uint8)  # 内存中图片字节转换为np数组阵列
            img = cv2.imdecode(np_array, 1)  # 转为HWC    # np数组转换为cv2格式图片流

            results = model.predict(
                source=img,
                conf=0.65,
                save=True,
                save_txt=True,
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
                cv2.rectangle(img, (array[0], array[1]), (array[2], array[3]), color=(0, 255, 0), thickness=5)
                cv2.putText(img, "%s" % (array[5]), (array[0], array[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.3,
                            color=(0, 0, 255), thickness=3)
                # cv2.putText(img, "%s %s" % (array[5], array[4]), (array[0], array[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                #             fontScale=2,
                #             color=(0, 0, 255), thickness=5)

                qiu_array.append(array)
            if post_data['sort'][0] == '0':
                qiu_array.sort(key=lambda x: (x[0]), reverse=True)
            elif post_data['sort'][0] == '1':
                qiu_array.sort(key=lambda x: (x[0]), reverse=False)
            elif post_data['sort'][0] == '10':
                qiu_array.sort(key=lambda y: (y[1]), reverse=True)
            else:
                qiu_array.sort(key=lambda y: (y[1]), reverse=False)
            qiu_rank = []
            for i in range(len(qiu_array)):
                if qiu_array[i][5] not in qiu_rank:
                    qiu_rank.append(qiu_array[i][5])
            qiu_rank = json.dumps(qiu_rank)
            print(str(qiu_rank))
            # cv2 图片转换为图片字符串
            img_encode = cv2.imencode('.jpg', img)[1]
            data_encode = np.array(img_encode)
            byte_encode = data_encode.tobytes()  # 转换为内存字节码
            # print(type(byte_encode))
            re_data = [byte_encode, qiu_rank, post_data['CameraType'][0]]
            self.wfile.write(str(re_data).encode('utf8'))
        else:
            self.wfile.write(str('ok').encode('utf8'))

    print('执行开始')


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
    # qiu_rank()
    # 线程启动
    run_server()
