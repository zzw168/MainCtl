import base64
import json
import math
import socket
import time

import cv2
import numpy as np
import psutil
from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QImage
import os

from scipy.interpolate import interp1d
import shutil

def limit_folder_count(parent_path, max_folders=5):
    # 获取子目录列表，并按修改时间排序（最早修改的在前）
    folders = sorted(
        [os.path.join(parent_path, f) for f in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path, f))],
        key=os.path.getmtime
    )

    # 计算多出的文件夹数量
    excess_folders = len(folders) - max_folders

    # 删除多余的旧文件夹
    if excess_folders > 0:
        for i in range(excess_folders):
            shutil.rmtree(folders[i])
            print(f"Deleted folder: {folders[i]}")


def limit_folder_size(folder_path, max_files=5000):  # 保持文件夹里最大文件数量
    # 获取文件列表，并按修改时间排序（最早修改的在前）
    files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
        key=os.path.getmtime
    )

    # 计算多出的文件数量
    excess_files = len(files) - max_files

    # 如果文件数量超过限制，删除最旧的文件
    if excess_files > 0:
        for i in range(excess_files):
            os.remove(files[i])
            print(f"Deleted: {files[i]}")


# 示例：监控 "C:/logs" 文件夹，并保持最大数量 5000
# limit_folder_size("C:/logs", 5000)


def check_network_with_ip():
    interfaces = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()
    for interface, stats in interfaces.items():
        if stats.isup:
            ip_info = addresses.get(interface, [])
            mac = [addr.address for addr in ip_info if addr.family == psutil.AF_LINK]
            ip = [addr.address for addr in ip_info if addr.family == socket.AF_INET]
            print(f"Interface {interface} {mac} is UP!")
            if mac:
                return [interface, mac[0], ip[0]]
        else:
            print(f"Interface {interface} is DOWN!")


# 图片处理
def str2image_file(img, filename):
    image_str = img.encode('ascii')
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

def interpolate_y_from_x(polyline, x_value):
    if len(polyline) < 2:
        return None

    # 去重处理
    seen = {}
    for x, y in polyline:
        if x not in seen:
            seen[x] = y
    points = sorted(seen.items())  # 去重后按 x 排序

    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]

    if len(x_vals) < 2:
        return None

    try:
        interpolator = interp1d(x_vals, y_vals, bounds_error=False, fill_value="extrapolate")
        result = float(interpolator(x_value))
        if not math.isfinite(result):
            return None
        return result
    except Exception as e:
        print(f"插值异常: {e}")
        return None

from scipy.interpolate import interp1d
import math

def interpolate_x_from_y(polyline, y_value):
    """
    给定 polyline 和某个 y 值，返回对应的 x 值（通过线性插值）
    :param polyline: list of (x, y)
    :param y_value: float，目标 y
    :return: float 或 None，插值得到的 x
    """
    if len(polyline) < 2:
        return None

    # 去重：确保 y 不重复，否则 interp1d 会报错
    seen = {}
    for x, y in polyline:
        if y not in seen:
            seen[y] = x
    points = sorted(seen.items())  # 现在是 (y, x)

    y_vals = [p[0] for p in points]
    x_vals = [p[1] for p in points]

    if len(y_vals) < 2:
        return None

    try:
        interpolator = interp1d(y_vals, x_vals, bounds_error=False, fill_value="extrapolate")
        result = float(interpolator(y_value))
        if not math.isfinite(result):
            return None
        return result
    except Exception as e:
        print(f"插值异常: {e}")
        return None



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
            x = int(p1[0] + j * step_length * unit_vector[0])
            y = int(p1[1] + j * step_length * unit_vector[1])
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

if __name__ == '__main__':
    # polyline = [(0, 0), (100, 100), (200, 0)]
    # y_target = 100
    #
    # x_at_50 = interpolate_x_from_y(polyline, y_target)
    # print(f"Y = {y_target} 对应的 X ≈ {x_at_50}")
    polyline = [(0, 0), (100, 100), (200, 0)]
    x_target = 140

    y_at_150 = interpolate_y_from_x(polyline, x_target)
    print(f"X = {x_target} 对应的 Y ≈ {y_at_150}")

