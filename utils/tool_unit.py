import base64
import json
import math
import time

import cv2
import numpy as np
from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QImage


# 图片处理
def str2image_file(img, filename):
    image_str = img[22:]  # 截掉图片无效部分"data:image/jpg;base64,"
    image_str = image_str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open(filename, 'wb')
    image_json.write(image_byte)  # 将图片存到当前文件的fileimage文件中
    image_json.close()


def str2image(img):
    image_str = img[22:]  # 截掉图片无效部分"data:image/jpg;base64,"
    image_str = image_str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    return image_byte


# 将 QImage 转换为字节数据 (QByteArray) 并检查错误
def qimage_to_bytes(qimage: QImage) -> QByteArray:
    buffer = QByteArray()
    buffer_io = QBuffer(buffer)  # 创建 QBuffer，包装 QByteArray
    buffer_io.open(QIODevice.WriteOnly)  # 以写入模式打开
    if not qimage.save(buffer_io, "PNG"):  # 保存 QImage 为 PNG 格式到缓冲区
        print("QImage 转换为 PNG 失败")
        return QByteArray()
    return buffer


# 把cv2格式转换为img 图片
def frame2img(frame):
    # 将 BGR 图像转换为 RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 将 NumPy 数组转换为 QImage
    height, width, channel = frame.shape
    bytes_per_line = channel * width
    q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return q_img


def succeed(msg: str):
    return "<font color='green'>[%s] %s </font>" % (time.strftime("%H:%M:%S", time.localtime()), msg)


def fail(msg: str):
    return "<font color='red'>[%s] %s </font>" % (time.strftime("%H:%M:%S", time.localtime()), msg)


# 检测正负数
def is_natural_num(z):
    try:
        z = float(z)
        return isinstance(z, float)
    except ValueError:
        return False


def divide_path(path_points, step_length):
    """
    按照固定的步长分割路径。

    参数:
        path_points: 轨迹点列表，格式为 [(x1, y1), (x2, y2), ...]
        step_length: 固定步长

    返回:
        新的路径点列表
    """
    new_points = []

    # 遍历每对连续的路径点
    for i in range(len(path_points) - 1):
        p1 = path_points[i]
        p2 = path_points[i + 1]

        # 计算线段长度
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        segment_length = math.sqrt(dx ** 2 + dy ** 2)

        # 如果线段长度小于步长，直接添加起点和终点
        if segment_length < step_length:
            new_points.append(p1)
            continue

        # 计算单位向量
        num_steps = int(segment_length / step_length)
        unit_vector = (dx / segment_length, dy / segment_length)

        # 在当前段添加等分点
        for j in range(num_steps + 1):
            x = p1[0] + j * step_length * unit_vector[0]
            y = p1[1] + j * step_length * unit_vector[1]
            new_points.append((x, y))

    # 添加最后一个点
    new_points.append(path_points[-1])

    return new_points


def z_sort(z_array, direction=0, index=None):  # 排序函数
    for i in range(0, len(z_array)):  # 冒泡排序
        for j in range(0, len(z_array) - i - 1):
            if index:
                if z_array[j][direction] == 0:  # (大->小)
                    if z_array[j][index] < z_array[j + 1][index]:
                        z_array[j], z_array[j + 1] = z_array[j + 1], z_array[j]
                if z_array[j][direction] == 1:  # (小<-大)
                    if z_array[j][index] > z_array[j + 1][index]:
                        z_array[j], z_array[j + 1] = z_array[j + 1], z_array[j]
            else:
                if z_array[j][direction] == 0:  # (大->小)
                    if z_array[j] < z_array[j + 1]:
                        z_array[j], z_array[j + 1] = z_array[j + 1], z_array[j]
                if z_array[j][direction] == 1:  # (小<-大)
                    if z_array[j] > z_array[j + 1]:
                        z_array[j], z_array[j + 1] = z_array[j + 1], z_array[j]
    return z_array


import aiohttp
import asyncio


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                return await response.text()
        except asyncio.TimeoutError:
            print(f"请求 {url} 超时。")


async def post_request(url, data):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=data, timeout=1) as response:
                if response.status == 200:
                    result = await response.json()  # 假设返回的是 JSON 数据
                    print(f"成功: {result}")
                else:
                    print(f"请求失败，状态码: {response.status}")
        except asyncio.TimeoutError:
            print(f"请求超时: {url}")
        except aiohttp.ClientError as e:
            print(f"请求错误: {e}")


# 异步运行多个 POST 请求
async def post_main(url, data_list):
    # url = "https://example.com/api"
    # data_list = [
    #     {
    #         'requestType': 'set_run_toggle',
    #         'run_toggle': '0',
    #     }
    # ]

    tasks = [post_request(url, data) for data in data_list]  # 创建多个任务
    await asyncio.gather(*tasks)  # 并发执行所有任务
