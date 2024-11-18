import copy
import json
import math
import os
import random
import re
import subprocess
import sys
import threading
import time
from asyncio import timeout
from concurrent.futures import ThreadPoolExecutor
from http.client import responses
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

import cv2
import numpy as np
import psutil
import pynput
import requests
import yaml
from PIL.ImageOps import scale
from PyInstaller.utils.hooks.conda import files
from PySide6 import QtWidgets

from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QPropertyAnimation, QEvent
from PySide6.QtGui import QBrush, QColor, QPixmap, QMouseEvent, QPen, QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu, QMessageBox, QFileDialog, \
    QAbstractButton, QMdiSubWindow, QMdiArea, QDialog

import obsws_python as obs
import pygame

from Speed_Ui import Ui_Dialog_Set_Speed
from utils import tool_unit
from utils.SportCard_unit import *
from utils.tool_unit import *
from utils.Serial485_unit import *
from MainCtl_Ui import *
from utils.pingpong_socket import *
from utils.z_json2txt import *
from utils.z_MySql import *
from utils.kaj789 import *

"************************************OBS_开始****************************************"
"""
    OBS callback 回调函数
    cl_event.callback.register(on_record_state_changed)  # 以这个形式调用，注册回调函数
"""


# 场景新建事件
def on_scene_created(data):
    print(data.scene_uuid)
    print(data.scene_name)
    print(data.is_group)


# 场景切换事件
def on_current_program_scene_changed(data):
    print("程序场景变化")
    print(data.scene_uuid)
    print(data.scene_name)

    get_source_list(data.scene_name)


# 场景预览改变事件
def on_current_preview_scene_changed(data):
    print("预览场景变化")
    print(data.scene_uuid)
    print(data.scene_name)


# 来源变化事件
def on_scene_item_enable_state_changed(data):
    print("来源元素变化")
    print(data.scene_uuid)
    print(data.scene_name)
    print(data.scene_item_id)
    print(data.scene_item_enabled)
    get_source_list(data.scene_name)


# 流状态改变事件
def on_record_state_changed(data):
    global record_data
    print("录制状态变化")
    print(data.output_active)
    print(data.output_state)
    print(data.output_path)
    record_data = [data.output_active, data.output_state, data.output_path]


# 流状态改变事件
def on_stream_state_changed(data):
    print("流状态变化")
    print(data.output_active)
    print(data.output_state)


# 来源变化事件
def on_get_stream_status(data):
    print("直播流状态")
    print(data.output_active)
    print(data.output_reconnecting)
    print(data.output_timecode)
    print(data.output_duration)
    print(data.output_congestion)
    print(data.output_bytes)
    print(data.output_skipped_frames)
    print(data.output_total_frames)


"""
    OBS callback 回调函数 结束
"""


class ObsThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ObsThread, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        global cl_request
        global cl_event
        global flg_start
        try:
            if not flg_start['obs']:
                cl_request = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
                cl_event = obs.EventClient()  # 监听 链接配置在 config.toml 文件中

                cl_event.callback.register(on_current_program_scene_changed)  # 场景变化
                cl_event.callback.register(on_scene_item_enable_state_changed)  # 来源变化
                cl_event.callback.register(on_record_state_changed)  # 录制状态
                cl_event.callback.register(on_stream_state_changed)  # 直播流状态
                cl_event.callback.register(on_get_stream_status)  # 直播流状态
                self._signal.emit(succeed('OBS 启动成功！'))
                flg_start['obs'] = True
        except:
            self._signal.emit(fail('OBS 启动失败！'))
            flg_start['obs'] = False


def obs_signal_accept(msg):
    print(msg)
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    if '成功' in msg:
        get_scenes_list()  # 获取所有场景
        get_source_list(ui.comboBox_Scenes.currentText())


def obs_open():
    if not Obs_Thread.isRunning():
        Obs_Thread.start()


class SourceThread(QObject):
    source_signal = Signal(object)

    def __init__(self):
        super(SourceThread, self).__init__()


def source_signal_accept(msg):
    print(msg)
    source2table()


def source2table():
    try:
        if scene_now != '':
            ui.comboBox_Scenes.setCurrentText(scene_now)
        tb_sources = ui.tableWidget_Sources
        tb_sources.setRowCount(len(source_list))
        for row in range(0, len(source_list)):
            cb = QCheckBox()
            cb.setStyleSheet('QCheckBox{margin:6px};')
            cb.clicked.connect(source_enable)
            tb_sources.setCellWidget(row, 0, cb)
            if source_list[row][0] == True:
                tb_sources.cellWidget(row, 0).setChecked(True)
            print(source_list[row][0])
            for col in range(1, len(source_list[row])):
                item = QTableWidgetItem(str(source_list[row][col]))
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                tb_sources.setItem(row, col, item)
    except:
        print("来源数据进表错误！")


def source_enable():  # 开关来源
    global source_list
    tb_source = ui.tableWidget_Sources
    row_num = tb_source.currentRow()
    source_list[row_num][0] = not (source_list[row_num][0])
    s_enable = source_list[row_num][0]
    cb_scene = ui.comboBox_Scenes
    scene_name = cb_scene.currentText()
    item_id = source_list[row_num][2]
    # print(source_list)
    # 打开,关闭来源
    if flg_start['obs']:
        try:
            cl_request.set_scene_item_enabled(scene_name, item_id, s_enable)  # 打开视频来源
        except:
            ui.textBrowser.append(fail("OBS 开关来源！"))
            flg_start['obs'] = False


def activate_browser():  # 程序开始，刷新浏览器
    obs_scene = obs_data['obs_scene']
    item_ranking = obs_data['source_ranking']
    item_settlement = obs_data['source_settlement']
    if flg_start['obs']:
        try:
            cl_request.set_scene_item_enabled(obs_scene, item_ranking, False)  # 关闭排位组件
            time.sleep(0.5)
            cl_request.set_scene_item_enabled(obs_scene, item_settlement, False)  # 关闭结算页
            time.sleep(1)
            cl_request.set_scene_item_enabled(obs_scene, item_settlement, True)  # 打开结算页
            time.sleep(1)
            tcp_ranking_thread.run_flg = True  # 打开排名线程
            cl_request.set_scene_item_enabled(obs_scene, item_ranking, True)  # 打开排位组件
            time.sleep(1)
            cl_request.set_scene_item_enabled(obs_scene, item_settlement, False)  # 打开结算页
        except:
            print("OBS 开关浏览器出错！")
            flg_start['obs'] = False


def get_scenes_list():  # 刷新所有列表
    if flg_start['obs']:
        try:
            res = cl_request.get_scene_list()  # 获取场景列表
            res_name = cl_request.get_current_program_scene()  # 获取激活的场景
        except:
            ui.textBrowser.append(fail("OBS 刷新所有列表中断！"))
            flg_start['obs'] = False
            return
        print('%s' % res_name.scene_name)
        scene_name = res_name.scene_name
        cb_scenes = ui.comboBox_Scenes
        cb_scenes.clear()
        for i, item in enumerate(res.scenes):
            print(item)
            cb_scenes.addItem(item['sceneName'])
        cb_scenes.setCurrentText(scene_name)


def get_source_list(scene_name):  # 取得来源列表
    global source_list
    global scene_now
    global obs_data
    scene_now = scene_name
    if not flg_start['obs']:
        return
    try:
        res = cl_request.get_scene_item_list(scene_name)
        source_list = []
        if res:
            for item in res.scene_items:
                source_list.append([item['sceneItemEnabled'], item['sourceName'], item['sceneItemId']])
                # print('取得来源列表 %s' % item)
                if item['sourceName'] == ui.lineEdit_source_ranking.text():
                    obs_data['source_ranking'] = int(item['sceneItemId'])
                elif item['sourceName'] == ui.lineEdit_source_picture.text():
                    obs_data['source_picture'] = int(item['sceneItemId'])
                elif item['sourceName'] == ui.lineEdit_source_settlement.text():
                    obs_data['source_settlement'] = int(item['sceneItemId'])
            Source_Thread.source_signal.emit('写表')
    except:
        flg_start['obs'] = False


def scenes_change():  # 变换场景
    if flg_start['obs']:
        scene_name = ui.comboBox_Scenes.currentText()
        try:
            cl_request.set_current_program_scene(scene_name)
        except:
            ui.textBrowser.append(fail("OBS 变换场景链接中断！"))
            flg_start['obs'] = False


# 截取OBS图片
def get_picture(scence_current):
    global lottery_term
    if not flg_start['obs']:
        return ['', '[1]', 'obs']
    try:
        resp = cl_request.get_source_screenshot(scence_current, "jpg", 1920, 1080, 100)
    except:
        flg_start['obs'] = False
        return ['', '[1]', 'obs']
    img = resp.image_data[22:]
    if os.path.exists(ui.lineEdit_Image_Path.text()):
        lottery_term[6] = '%s/obs_%s.jpg' % (ui.lineEdit_Image_Path.text(), lottery_term[0])
        str2image_file(img, lottery_term[6])  # 保存图片
    form_data = {
        'CameraType': 'obs',
        'img': img,
        'sort': '1',  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
    }
    try:
        res = requests.post(url=recognition_addr, data=form_data, timeout=5)
        r_list = eval(res.text)  # 返回 [图片字节码，排名列表，截图标志]
        r_img = r_list[0]
        if os.path.exists(ui.lineEdit_Image_Path.text()):
            image_json = open('%s/obs_%s_end.jpg' % (ui.lineEdit_Image_Path.text(), lottery_term[0]), 'wb')
            image_json.write(r_img)  # 将图片存到当前文件的fileimage文件中
            image_json.close()
        flg_start['ai_end'] = True
        return r_list
    except:
        flg_start['ai_end'] = False
        img = img.encode('ascii')
        image_byte = base64.b64decode(img)
        print('终点识别服务没有开启！')
        return [image_byte, '[1]', 'obs']


# obs 脚本 obs_script_time.py 请求
def obs_script_request():
    res = requests.get(url="%s/start" % obs_script_addr)
    # res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
    # res = requests.get(url="http://127.0.0.1:8899/period?term=开始")
    print(res)


"******************************OBS结束*************************************"

"******************************网络摄像头*************************************"


# 获取网络摄像头图片
def get_rtsp(rtsp_url):
    try:
        ip_address = 'http://%s' % re.search(r'(\d+\.\d+\.\d+\.\d+)', rtsp_url).group(0)
        requests.get(ip_address)
    except:
        return ['', '[1]', 'monitor']
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret:
            if os.path.exists(ui.lineEdit_Image_Path.text()):
                f = '%s/rtsp_%s.jpg' % (ui.lineEdit_Image_Path.text(), lottery_term[0])
                cv2.imwrite(f, frame)
            success, jpeg_data = cv2.imencode('.jpg', frame)
            if success:
                # 将 JPEG 数据转换为 Base64 字符串
                jpg_base64 = base64.b64encode(jpeg_data).decode('ascii')
                try:
                    form_data = {
                        'CameraType': 'monitor',
                        'img': jpg_base64,
                        'sort': '10',  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
                    }
                    res = requests.post(url=recognition_addr, data=form_data, timeout=5)
                    r_list = eval(res.text)  # 返回 [图片字节码，排名列表，截图标志]
                    r_img = r_list[0]
                    if os.path.exists(ui.lineEdit_Image_Path.text()):
                        image_json = open('%s/rtsp_%s_end.jpg' % (ui.lineEdit_Image_Path.text(), lottery_term[0]), 'wb')
                        image_json.write(r_img)  # 将图片存到当前文件的fileimage文件中
                        image_json.close()
                    flg_start['ai_end'] = True
                    return r_list
                except:
                    print('终点识别服务没有开启！')
                    flg_start['ai_end'] = False
                    # img = frame2img(frame)
                    # image_byte = qimage_to_bytes(img)
                    img = jpg_base64.encode('ascii')
                    image_byte = base64.b64decode(img)
                    return [image_byte, '[1]', 'monitor']
            else:
                print("jpg_base64 转换错误！")
                return ['', '[1]', 'monitor']
        else:
            print("无法读取视频帧")
            return ['', '[1]', 'monitor']
    else:
        cap.release()
        print(f'无法打开摄像头')
        return ['', '[1]', 'monitor']


"************************************图像识别_开始****************************************"


# 处理触发点位
def deal_action():
    global action_area
    for rank_num in range(0, len(ranking_array)):  # 循环寻找合适的球位置，镜头追踪
        if action_area[1] == int(ranking_array[rank_num][8]) and action_area[2] == 0:  # 写入标志 0 为任意写入
            if (int(ranking_array[rank_num][6]) > action_area[0] + 3
                    or (int(ranking_array[rank_num][6]) < action_area[0])):
                continue
            action_area[0] = int(ranking_array[rank_num][6])  # 同圈中寻找合适区域
            break
        if action_area[1] < int(ranking_array[rank_num][8]) and action_area[2] == 0:  # 不同圈赋值更大圈数
            action_area[1] = int(ranking_array[rank_num][8])
            if action_area[0] > int(ranking_array[rank_num][6]):  # 不同圈，跨圈情况
                action_area[0] = int(ranking_array[rank_num][6])  # 排第一位的球所在区域
            break


# 处理排名
def deal_rank(integration_qiu_array):
    global ranking_array
    for r_index in range(0, len(ranking_array)):
        replaced = False
        for q_item in integration_qiu_array:
            if ranking_array[r_index][5] == q_item[5]:  # 更新 ranking_array
                if q_item[6] < ranking_array[r_index][6]:  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                    result_count = ranking_array[r_index][6] - q_item[6]
                    if result_count >= max_area_count - balls_count - 6:
                        ranking_array[r_index][8] += 1
                        if ranking_array[r_index][8] > max_lap_count - 1:
                            ranking_array[r_index][8] = 0
                if action_area[0] >= max_area_count - balls_count and action_area[1] >= max_lap_count - 1:
                    area_limit = balls_count
                else:
                    area_limit = 5
                # if ((ranking_array[r_index][6] == 0)  # 等于0 刚初始化，未检测区域
                if ((ranking_array[r_index][6] == 0 and q_item[6] < 5)  # 等于0 刚初始化，未检测区域
                        or (q_item[6] >= ranking_array[r_index][6] and  # 新位置要大于旧位置
                            (q_item[6] - ranking_array[r_index][6] <= area_limit  # 新位置相差旧位置三个区域以内
                                    # or ranking_array[0][6] - ranking_array[r_index][6] > 5
                            ))  # 当新位置与旧位置超过3个区域，则旧位置与头名要超过5个区域才统计
                        or (q_item[6] < 8 and ranking_array[r_index][6] >= max_area_count - balls_count - 6)):  # 跨圈情况
                    for r_i in range(0, len(q_item)):
                        ranking_array[r_index][r_i] = copy.deepcopy(q_item[r_i])  # 更新 ranking_array
                    ranking_array[r_index][9] = 1
                replaced = True
                break
        if not replaced:
            ranking_array[r_index][9] = 0
    # print(ranking_array)
    # print('到这里~~~~')
    sort_ranking()


def sort_ranking():
    global ranking_array
    global ball_sort
    # 1.排序区域
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][6] < ranking_array[j + 1][6]:
                ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 2.区域内排序
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][6] == ranking_array[j + 1][6]:
                if ranking_array[j][7] == 0:  # (左后->右前)
                    if ranking_array[j][0] < ranking_array[j + 1][0]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 1:  # (左前<-右后)
                    if ranking_array[j][0] > ranking_array[j + 1][0]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 10:  # (上前 ↑ 下后)
                    if ranking_array[j][1] > ranking_array[j + 1][1]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
                if ranking_array[j][7] == 11:  # (上后 ↓ 下前)
                    if ranking_array[j][1] < ranking_array[j + 1][1]:
                        ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 3.圈数排序
    for i in range(0, len(ranking_array)):  # 冒泡排序
        for j in range(0, len(ranking_array) - i - 1):
            if ranking_array[j][8] < ranking_array[j + 1][8]:
                ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    # 4.寄存器保存固定每个区域的最新排位（因为ranking_array 变量会因实时动态变动，需要寄存器辅助固定每个区域排位）
    for i in range(0, len(ranking_array)):
        # print(ranking_array[i], '~~~~~~~~~~~')
        if not (ranking_array[i][5] in ball_sort[ranking_array[i][6]][ranking_array[i][8]]):
            ball_sort[ranking_array[i][6]][ranking_array[i][8]].append(copy.deepcopy(ranking_array[i][5]))  # 添加寄存器球排序
            # if ranking_array[i][6] == 35 and ranking_array[i][8] == 1:
            #     print(ball_sort[ranking_array[i][6]][ranking_array[i][8]])
    # 5.按照寄存器位置，重新排序排名同圈数同区域内的球
    for i in range(0, len(ranking_array)):
        for j in range(0, len(ranking_array) - i - 1):
            if (ranking_array[j][6] == ranking_array[j + 1][6]) and (ranking_array[j][8] == ranking_array[j + 1][8]):
                m = 0
                n = 0

                for k in range(0, len(ball_sort[ranking_array[j][6]][ranking_array[j][8]])):
                    if ranking_array[j][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        n = k
                    elif ranking_array[j + 1][5] == ball_sort[ranking_array[j][6]][ranking_array[j][8]][k]:
                        m = k
                if n > m:  # 把区域排位索引最小的球（即排名最前的球）放前面
                    ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]


def reset_ranking_array():
    """
    重置排名数组
    # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    """
    global ranking_array
    global ball_sort
    global con_data
    global action_area
    global z_ranking_res
    global z_ranking_time
    global balls_start
    # global previous_position
    balls_start = 0

    ranking_array = []  # 排名数组
    for i in range(0, len(init_array)):
        ranking_array.append([])
        for j in range(0, len(init_array[i])):
            ranking_array[i].append(init_array[i][j])
    ball_sort = []  # 位置寄存器
    for i in range(0, max_area_count + 1):
        ball_sort.append([])
        for j in range(0, max_lap_count):
            ball_sort[i].append([])
    for i in range(0, len(init_array)):
        for j in range(0, 5):
            if j == 0:
                con_data[i][j] = init_array[i][5]  # con_data 数据表数组
            else:
                con_data[i][j] = 0
    action_area = [0, 0, 0]  # 初始化触发区域
    z_ranking_res = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 初始化网页排名
    z_ranking_time = ['TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'OUT', 'OUT']  # 初始化网页排名时间
    tcp_ranking_thread.sleep_time = 1  # 重置排名数据包发送时间
    if flg_start['obs'] and not ui.checkBox_test.isChecked():
        try:
            res = requests.get(url="%s/reset" % obs_script_addr)
            print(res)
        except:
            print('OBS脚本链接错误！')
            flg_start['obs'] = False
        activate_browser()  # 刷新OBS中排名浏览器


def color_to_num(res):  # 按最新排名排列数组
    global z_ranking_res
    arr_res = []
    for r in res:
        for i in range(0, len(init_array)):
            if r[0] == init_array[i][5]:
                arr_res.append(i + 1)
    for i in range(0, len(arr_res)):
        for j in range(0, len(z_ranking_res)):
            if arr_res[i] == z_ranking_res[j]:
                z_ranking_res[i], z_ranking_res[j] = z_ranking_res[j], z_ranking_res[i]


def camera_to_num(res):  # 按最新排名排列数组
    camera_response = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    arr_res = []
    for r in res:
        for arr in range(0, len(init_array)):
            if r == init_array[arr][5]:
                arr_res.append(arr + 1)
    for arr in range(0, len(arr_res)):
        for cam in range(0, len(camera_response)):
            if arr_res[arr] == camera_response[cam]:
                camera_response[arr], camera_response[cam] = camera_response[cam], camera_response[arr]
    return camera_response


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('你对HTTP服务端发送了POST'.encode('utf-8'))
        # content_length = int(self.headers['Content-Length'])
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("客户端发送的post内容=" + post_data)
        if post_data == "start":
            self.handle_start_command()
        if post_data == "stop":
            self.handle_stop_command()

    def handle_start_command(self):
        reset_ranking_array()
        print('执行开始')

    def handle_stop_command(self):
        print('执行停止')


def load_ballsort_yaml():
    global max_lap_count
    global max_area_count
    file = "./ballsort_config.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        ballsort_all = yaml.safe_load(f)
        max_area_count = int(ballsort_all['max_area_count'])
        max_lap_count = int(ballsort_all['max_lap_count'])

        ui.lineEdit_lap_Ranking.setText(str(max_lap_count))
        ui.lineEdit_area_Ranking.setText(str(max_area_count))
        ui.lineEdit_Time_Restart_Ranking.setText(str(ballsort_all['reset_time']))
        ui.lineEdit_time_send_result.setText(str(ballsort_all['time_send_result']))
        ui.lineEdit_time_count_ball.setText(str(ballsort_all['time_count_ball']))

        f.close()
    else:
        print("文件不存在")


def save_ballsort_yaml():
    global max_lap_count
    global max_area_count
    file = "./ballsort_config.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        ballsort_all = yaml.safe_load(f)
        f.close()
        if (ui.lineEdit_lap_Ranking.text().isdigit()
                and ui.lineEdit_area_Ranking.text().isdigit()
                and ui.lineEdit_Time_Restart_Ranking.text().isdigit()):
            ballsort_all['max_lap_count'] = int(ui.lineEdit_lap_Ranking.text())
            ballsort_all['max_area_count'] = int(ui.lineEdit_area_Ranking.text())
            ballsort_all['reset_time'] = int(ui.lineEdit_Time_Restart_Ranking.text())
            ballsort_all['time_send_result'] = int(ui.lineEdit_time_send_result.text())
            ballsort_all['time_count_ball'] = int(ui.lineEdit_time_count_ball.text())
            max_lap_count = int(ui.lineEdit_lap_Ranking.text())
            max_area_count = int(ui.lineEdit_area_Ranking.text())
            # print(ballsort_conf)
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(ballsort_all, f, allow_unicode=True)
            f.close()
            ui.textBrowser_background_data.setText(
                succeed("%s,%s,%s 保存服务器完成" % (ballsort_all['max_lap_count'],
                                                     ballsort_all['max_area_count'],
                                                     ballsort_all['reset_time'])))
        else:
            ui.textBrowser_background_data.setText(fail("错误，只能输入数字！"))


def init_ranking_table():
    tb_ranking = ui.tableWidget_Ranking
    tb_ranking.setRowCount(10)
    tb_ranking.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
    tb_ranking.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
    for i in range(0, len(con_data)):
        for j in range(0, len(con_data[i])):
            if con_data[i][0] in color_ch.keys():
                if j == 0:
                    item = QTableWidgetItem(color_ch[con_data[i][j]])
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem(str(con_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                tb_ranking.setItem(i, j, item)


class UpdateThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(UpdateThread, self).__init__()
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        tb_ranking = ui.tableWidget_Ranking
        while self.running:
            time.sleep(1)
            for i in range(0, len(con_data)):
                for j in range(0, len(con_data[i])):
                    if con_data[i][0] in color_ch.keys():
                        if j == 0 and tb_ranking.item(i, j).text() != color_ch[con_data[i][j]]:
                            self._signal.emit([i, j, color_ch[con_data[i][j]]])
                        elif j != 0 and tb_ranking.item(i, j).text() != con_data[i][j]:
                            self._signal.emit([i, j, con_data[i][j]])


def ranking_signal_accept(msg):
    tb_ranking = ui.tableWidget_Ranking
    tb_ranking.item(msg[0], msg[1]).setText(str(msg[2]))


class TcpRankingThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TcpRankingThread, self).__init__()
        self.running = True
        self.run_flg = False
        self.send_time_flg = False
        self.sleep_time = 1
        self.send_time_data = [1, time.strftime('%M"%S', time.localtime(time.time()))]

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        tcp_ranking_socket.close()  # 关闭套接字
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            try:
                con, addr = tcp_ranking_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if con:
                    # self._signal.emit("Accepted. {0}, {1}".format(con, str(addr)))
                    with WebsocketServer(con) as ws:
                        # ws.send('pong')
                        while self.run_flg:
                            try:
                                time.sleep(self.sleep_time)
                                if self.send_time_flg:
                                    d = {"mc": self.send_time_data[0], 'data': self.send_time_data[1],
                                         'type': 'time'}
                                else:
                                    d = {'data': z_ranking_res, 'type': 'pm'}
                                    # time.sleep(1)
                                    # d = {"mc": self.send_time_data[0], 'data': '7.98',
                                    #      'type': 'time'}
                                    # print(d)
                                    # d = {'data': np.random.permutation([1, 2, 3, 4, 5, 6, 9, 7, 8, 10]).tolist(),
                                    #      'type': 'pm'}
                                ws.send(json.dumps(d))
                                self.send_time_flg = False
                            except Exception as e:
                                print("pingpong_rank_1 错误：", e)
                                # self._signal.emit("pingpong 错误：%s" % e)
                                break
            except Exception as e:
                print("pingpong_rank_2 错误：", e)
                # self._signal.emit("pingpong 错误：%s" % e)


class TcpResultThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TcpResultThread, self).__init__()
        self.running = True
        self.run_flg = False
        self.send_type = ''

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        tcp_result_socket.close()
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global lottery_term
        while self.running:
            try:
                con, addr = tcp_result_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if not con:
                    continue
                with WebsocketServer(con) as ws:
                    while self.run_flg:
                        time.sleep(1)
                        try:
                            if self.send_type == 'updata':
                                self._signal.emit(succeed('第%s期 结算！%s' % (term, str(z_ranking_res))))
                                datalist = {'type': 'updata',
                                            'data': {'qh': str(term), 'rank': []}}
                                for index in range(len(z_ranking_res)):
                                    if is_natural_num(z_ranking_time[index]):
                                        datalist["data"]['rank'].append(
                                            {"mc": z_ranking_res[index], "time": ('%s"' % z_ranking_time[index])})
                                    else:
                                        datalist["data"]['rank'].append(
                                            {"mc": z_ranking_res[index], "time": ('%s' % z_ranking_time[index])})
                                print(datalist)
                                ws.send(json.dumps(datalist))
                                if not ui.radioButton_test_game.isChecked():  # 非测试模式
                                    result_data = {"raceTrackID": Track_number, "term": str(term),
                                                   "actualResultOpeningTime": betting_end_time,
                                                   "result": z_ranking_res,
                                                   "timings": "[]"}
                                    data_temp = []
                                    for index in range(len(z_ranking_res)):
                                        if is_natural_num(z_ranking_time[index]):
                                            data_temp.append(
                                                {"pm": index + 1, "id": z_ranking_res[index],
                                                 "time": float(z_ranking_time[index])})
                                        else:
                                            data_temp.append(
                                                {"pm": index + 1, "id": z_ranking_res[index],
                                                 "time": z_ranking_time[index]})
                                    result_data["timings"] = json.dumps(data_temp)
                                    # print(result_data)
                                    try:
                                        post_end(term, betting_end_time, 1, Track_number)  # 发送游戏结束信号给服务器
                                        post_result(term, betting_end_time, result_data, Track_number)  # 发送最终排名给服务器
                                        post_upload(term, lottery_term[6], Track_number)  # 上传结果图片
                                    except:
                                        self._signal.emit(fail('post_result 上传结果错误！'))
                                        print('上传结果错误！')

                                    video_name = cl_request.stop_record()  # 关闭录像
                                    lottery_term[7] = video_name.output_path  # 视频保存路径
                                    lottery_term[3] = '已结束'  # 新一期比赛的状态（0.已结束）
                                    lottery_term[4] = str(z_ranking_res)  # 排名
                                    end_time = int(time.time())
                                    lottery_term[8] = str(end_time)
                                    self._signal.emit('save_video')
                                    # lottery2sql()  # 保存数据库
                                    lottery2yaml()  # 保存数据
                                self._signal.emit(succeed('第%s期 结束！' % term))
                                if ui.checkBox_restart.isChecked():
                                    if not ui.radioButton_test_game.isChecked():
                                        self.send_type = ''
                                    else:
                                        self.run_flg = False
                                    ReStart_Thread.run_flg = True  # 1分钟后重启动作
                                else:
                                    self.run_flg = False
                            elif self.send_type == 'time':
                                datalist = {'type': 'time',
                                            'data': str(term)}
                                ws.send(json.dumps(datalist))
                                self.send_type = ''
                                self.run_flg = False
                            else:
                                datalist = {'type': 'pong',
                                            'data': str(term)}
                                ws.send(json.dumps(datalist))

                        except Exception as e:
                            print("pingpong_result_1 错误：%s" % e)
                            # self._signal.emit("pingpong 错误：%s" % e)
                            break
            except Exception as e:
                print("pingpong_result_2 错误：%s" % e)
                self._signal.emit("pingpong_result_2 错误：%s" % e)


def tcp_signal_accept(msg):
    if msg == 'save_video':
        tb_result = ui.tableWidget_Results
        tb_result.item(0, 3).setText(lottery_term[3])  # 新一期比赛的状态（0.已结束）
        tb_result.item(0, 4).setText(lottery_term[4])  # 自动赛果
        tb_result.item(0, 5).setText(lottery_term[5])  # 手动赛果
        tb_result.item(0, 6).setText(lottery_term[6])  # 照片保存路径
        tb_result.item(0, 7).setText(lottery_term[7])  # 视频保存路径
        tb_result.item(0, 8).setText(lottery_term[8])  # 存档时间
    # print(msg)
    else:
        ui.textBrowser_msg.append(msg)
        scroll_to_bottom(ui.textBrowser_msg)


class UdpThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(UdpThread, self).__init__()
        self.run_flg = True
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        udp_socket.close()
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global con_data
        global balls_start
        udp_time_old = 0
        while self.running:
            try:
                # 3. 等待接收对方发送的数据
                recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
                if len(recv_data) < 1:
                    print('UDP无数据！')
                    continue
                if self.run_flg:
                    res = recv_data[0].decode('utf8')
                    if res == '':
                        print('UDP_res无数据！', recv_data[0])
                        continue
                    data_res = eval(res)  # str转换list
                    if len(recv_data) < 2:
                        print('UDP_recv_data无数据！', res)
                        continue
                    self._signal.emit(data_res)
                    if (str(data_res[0]).isdigit()
                            and str(data_res[1][6]) in [str(a) for a in range(1, 16)]):  # UDP数据包时间间隔
                        time_interval = int(data_res[0]) - udp_time_old
                        self._signal.emit(time_interval)
                        udp_time_old = int(data_res[0])
                    array_data = []
                    for i_ in range(1, len(data_res)):  # data_res[0] 是时间戳差值 ms
                        array_data.append(copy.deepcopy(data_res[i_]))
                    # print(array_data)
                    if len(array_data) < 1:
                        continue
                    if len(array_data[0]) < 7:
                        self._signal.emit(fail('array_data:%s < 7数据错误！' % array_data[0]))
                        print('array_data < 7数据错误！', array_data[0])
                        continue
                    array_data = deal_area(array_data, array_data[0][6])  # 收集统计区域内的球
                    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~1', array_data)
                    if array_data is None or len(array_data) < 1:
                        continue
                    if len(array_data[0]) < 8:
                        self._signal.emit(fail('array_data:%s < 8数据错误！' % array_data[0]))
                        print('array_data < 8数据错误！', array_data[0])
                        continue
                    if action_area[0] >= max_area_count - balls_count and action_area[
                        1] >= max_lap_count - 1:  # 在最后面排名阶段，以区域先后为准
                        array_data = filter_max_area(array_data)
                    else:
                        array_data = filter_max_value(array_data)  # 在平时球位置追踪，以置信度为准
                    if array_data is None or len(array_data) < 1:
                        continue
                    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~2', array_data)
                    deal_rank(array_data)
                    balls_start = len(ball_sort[1][0])  # 更新起点球数
                    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~3', ranking_array)
                    deal_action()
                    con_data = []
                    for k in range(0, len(ranking_array)):
                        con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                        con_data.append(
                            [con_item['name'], con_item['position'], con_item['lapCount'], con_item['x1'],
                             con_item['y1']])
                    color_to_num(con_data)

            except Exception as e:
                print("UDP数据接收出错:%s" % e)
                self._signal.emit("UDP数据接收出错:%s" % e)
        # 5. 关闭套接字
        udp_socket.close()


def udp_signal_accept(msg):
    global flg_start
    # print(msg)
    if isinstance(msg, int):
        bt_udp_time = ui.pushButton_udp_time
        if msg > 200:
            bt_udp_time.setText('识别主机超时！%s 毫秒' % msg)
            if bt_udp_time.styleSheet() != 'background:rgb(255, 0, 0)':
                bt_udp_time.setStyleSheet('background:rgb(255, 0, 0)')
        else:
            if bt_udp_time.styleSheet() != 'background:rgb(0, 255, 0)':
                bt_udp_time.setStyleSheet('background:rgb(0, 255, 0)')
                bt_udp_time.setText('图像识别状态正常')
        if int(ui.lineEdit_ball_start.text()) < balls_start:  # 更新起点球数
            ui.lineEdit_balls_start.setText(str(balls_start))
            ui.lineEdit_ball_start.setText(str(balls_start))
        # if int(ui.lineEdit_area.text()) != action_area[0]:  # 更新触发区域
        #     ui.lineEdit_area.setText(str(action_area[0]))
    else:
        if '错误' in msg:
            ui.textBrowser_msg.append(msg)
        if ui.checkBox_ShowUdp.isChecked():
            ui.textBrowser_background_data.append(str(msg))


def load_area():  # 载入位置文件初始化区域列表
    global area_Code
    for key in area_Code.keys():
        track_file = "./txts/%s.txt" % key
        if os.path.exists(track_file):  # 存在就加载数据对应赛道数据
            with open(track_file, 'r') as file:
                content = file.read().split('\n')
            for area in content:
                if area:
                    polgon_array = {'coordinates': [], 'area_code': 0, 'direction': 0}
                    paths = area.split(' ')
                    if len(paths) < 2:
                        print("分区文件错误！")
                        return
                    lines = paths[0].split(',')
                    for line in lines:
                        if line:
                            x, y = line.split('/')
                            polgon_array['coordinates'].append((int(x), int(y)))
                    polgon_array['area_code'] = int(paths[1])
                    if len(paths) > 2:
                        polgon_array['direction'] = int(paths[2])
                    area_Code[key].append(polgon_array)


def deal_area(ball_array, cap_num):  # 找出该摄像头内所有球的区域
    ball_area_array = []
    if len(ball_array) < 1 or cap_num == '':
        return
    for ball in ball_array:
        # print(ball)
        if ball[4] < 0.35:  # 置信度小于 0.45 的数据不处理
            continue
        if len(ball) == 7:
            ball.append(0)
        x = (ball[0] + ball[2]) / 2
        y = (ball[1] + ball[3]) / 2
        point = (x, y)
        if cap_num in area_Code.keys():
            for area in area_Code[cap_num]:
                pts = np.array(area['coordinates'], np.int32)
                res = cv2.pointPolygonTest(pts, point, False)  # -1=在外部,0=在线上，1=在内部
                if res > -1.0 and len(ball) <= 8:
                    ball[6] = area['area_code']
                    ball[7] = area['direction']
                    ball_area_array.append(copy.deepcopy(ball))  # ball结构：x1,y1,x2,y2,置信度,球名,区域号,方向
    return ball_area_array  # ball_area_array = [[x1,y1,x2,y2,置信度,球名,区域号,方向]]


# 33 17 25 29
def filter_max_area(lists):  # 在区域范围内如果出现两个相同的球，则取区域最大的球为准
    max_area = {}
    # print('原', lists)
    for sublist in lists:
        key, area = sublist[5], sublist[6]
        if (key not in max_area) or (area > max_area[key]):
            max_area[key] = copy.deepcopy(area)
    filtered_list = []
    for sublist in lists:
        if sublist[6] == max_area[sublist[5]]:  # 选取同一区域置信度最大的球添加到修正后的队列
            filtered_list.append(copy.deepcopy(sublist))
            # print(filtered_list)
    return filtered_list


def filter_max_value(lists):  # 在区域范围内如果出现两个相同的球，则取置信度最高的球为准
    max_values = {}
    for sublist in lists:
        value, key = sublist[4], sublist[5]
        if key not in max_values or max_values[key] < value:
            max_values[key] = copy.deepcopy(value)
    filtered_list = []
    for sublist in lists:
        if sublist[4] == max_values[sublist[5]]:  # 选取置信度最大的球添加到修正后的队列
            filtered_list.append(copy.deepcopy(sublist))
    return filtered_list


"************************************图像识别_结束****************************************"


class ZUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, z_window):
        super(ZUi, self).setupUi(z_window)

        tb_result = self.tableWidget_Results
        tb_result.horizontalHeader().resizeSection(0, 100)
        tb_result.horizontalHeader().resizeSection(1, 150)
        tb_result.horizontalHeader().resizeSection(2, 50)
        tb_result.horizontalHeader().resizeSection(3, 50)
        tb_result.horizontalHeader().resizeSection(4, 200)
        tb_result.horizontalHeader().resizeSection(5, 200)
        tb_result.horizontalHeader().resizeSection(6, 200)
        tb_result.horizontalHeader().resizeSection(7, 200)
        tb_result.horizontalHeader().resizeSection(8, 150)

        tb_result.setColumnHidden(0, True)
        tb_result.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_result.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_result.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_result.customContextMenuRequested.connect(self.resultMenu)

        # 允许用户调整行表头宽度
        tb_result.setCornerButtonEnabled(True)
        tb_result.verticalHeader().setFixedWidth(100)

        # 获取 CornerButton
        corner_button = tb_result.findChild(QAbstractButton)
        if corner_button:
            # 安装事件过滤器，自定义绘制文字
            corner_button.installEventFilter(self)  # 事件过滤器用于处理重绘

        tb_audio = self.tableWidget_Audio
        tb_audio.horizontalHeader().resizeSection(0, 180)
        tb_audio.horizontalHeader().resizeSection(1, 50)
        tb_audio.horizontalHeader().resizeSection(2, 50)
        tb_audio.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_audio.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_ai = self.tableWidget_Ai
        tb_ai.horizontalHeader().resizeSection(0, 180)
        tb_ai.horizontalHeader().resizeSection(1, 50)
        tb_ai.horizontalHeader().resizeSection(2, 50)
        tb_ai.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_ai.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_step = self.tableWidget_Step
        tb_step.horizontalHeader().resizeSection(0, 30)
        tb_step.horizontalHeader().resizeSection(1, 40)
        tb_step.horizontalHeader().resizeSection(7, 80)
        tb_step.horizontalHeader().resizeSection(8, 50)
        tb_step.horizontalHeader().resizeSection(9, 50)
        tb_step.horizontalHeader().resizeSection(10, 65)
        tb_step.horizontalHeader().resizeSection(11, 40)
        tb_step.horizontalHeader().resizeSection(12, 50)
        tb_step.horizontalHeader().resizeSection(13, 60)
        tb_step.horizontalHeader().resizeSection(14, 50)
        tb_step.horizontalHeader().resizeSection(15, 50)
        tb_step.horizontalHeader().resizeSection(16, 40)
        tb_step.setColumnHidden(8, True)
        tb_step.setColumnHidden(9, True)
        tb_step.setColumnHidden(13, True)
        tb_step.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_step.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        palette = tb_step.palette()
        palette.setColor(QPalette.Highlight, QColor(255, 0, 255))  # 亮粉色
        tb_step.setPalette(palette)

        tb_step.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_step.customContextMenuRequested.connect(self.generateMenu)
        tb_step.setEnabled(False)

        tb_sources = self.tableWidget_Sources
        tb_sources.horizontalHeader().resizeSection(0, 10)
        tb_sources.horizontalHeader().resizeSection(1, 160)
        # tb_sources.horizontalHeader().resizeSection(2, 30)
        # tb_sources.setColumnHidden(2, True)
        tb_sources.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_sources.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

    def eventFilter(self, obj, event):
        # 检测到 CornerButton 的 Paint 事件
        if isinstance(obj, QAbstractButton) and event.type() == QEvent.Paint:
            # 自定义绘制逻辑
            painter = QPainter(obj)
            painter.save()

            # 获取按钮区域
            rect = obj.rect()

            # 绘制背景（模拟按钮的上表面，颜色为 rgb(245, 245, 245)）
            painter.setBrush(QBrush(QColor(245, 245, 245)))  # 浅灰色背景
            painter.setPen(Qt.NoPen)  # 无边框线
            painter.drawRect(rect)

            # 绘制顶部和左侧的高光（模拟光源）
            highlight_pen = QPen(QColor("#ffffff"), 2)  # 白色高光
            painter.setPen(highlight_pen)
            painter.drawLine(rect.topLeft(), rect.topRight())  # 顶部边线
            painter.drawLine(rect.topLeft(), rect.bottomLeft())  # 左侧边线

            # 绘制底部和右侧的阴影
            shadow_pen = QPen(QColor("#a0a0a0"), 2)  # 深灰色阴影
            painter.setPen(shadow_pen)
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())  # 底部边线
            painter.drawLine(rect.topRight(), rect.bottomRight())  # 右侧边线

            # 设置绘制区域和文字样式
            painter.setPen(Qt.black)
            painter.drawText(obj.rect(), Qt.AlignCenter, "期号")

            painter.restore()
            return True  # 阻止默认绘制事件

        return super().eventFilter(obj, event)

    def resultMenu(self, pos):
        global plan_list
        tb_result = self.tableWidget_Results
        row_num = tb_result.currentRow()

        menu = QMenu()
        item0 = menu.addAction("查看图片")
        item1 = menu.addAction("观看录像")
        item2 = menu.addAction("发送赛果")
        item3 = menu.addAction("取消当局")
        item4 = menu.addAction("刷新")

        screenPos = tb_result.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item0:
            exe_path = tb_result.item(row_num, 6).text()
            os.startfile(exe_path)
        if action == item1:
            exe_path = tb_result.item(row_num, 7).text()
            os.startfile(exe_path)
        if action == item2:
            pass
        if action == item3:
            pass
        if action == item4:
            pass

    def generateMenu(self, pos):
        global plan_list
        tb_step = self.tableWidget_Step

        menu = QMenu()
        item0 = menu.addAction("运行")
        item3 = menu.addAction("插入")
        item2 = menu.addAction("删除")
        item1 = menu.addAction("刷新")

        screenPos = tb_step.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item0:
            cmd_run()
        if action == item1:
            plan_refresh()
        if action == item2:
            row_count = tb_step.rowCount()
            col_count = tb_step.columnCount()
            row_num = tb_step.currentRow()
            print(row_count)
            if row_count > 1:
                for row_num in range(row_num, row_count - 1):
                    plan_list[row_num] = copy.deepcopy(plan_list[row_num + 1])
                    print('%d' % row_num)
                    for col in range(0, tb_step.columnCount() - 1):
                        if col == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet("""
                                                QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}
                                                QCheckBox::indicator:checked {
                                                    background-color: lightgreen;
                                                    border: 2px solid green;
                                                }
                                                QCheckBox::indicator:unchecked {
                                                    background-color: lightgray;
                                                    border: 2px solid gray;
                                                }
                                                QCheckBox::indicator {
                                                    width: 10px;
                                                    height: 10px;
                                                }
                                            """)
                            cb.setChecked(tb_step.cellWidget(row_num + 1, col).isChecked())
                            tb_step.setCellWidget(row_num, col, cb)
                        elif col == col_count - 2:
                            cell_widget = tb_step.cellWidget(row_num + 1, col)
                            if cell_widget:
                                if tb_step.item(row_num, col):
                                    tb_step.item(row_num, col).setText('')
                                if isinstance(cell_widget, QCheckBox):
                                    cb = QCheckBox()
                                    cb.setStyleSheet('QCheckBox{margin:6px};')
                                    cb.setText(tb_step.cellWidget(row_num + 1, col).text())
                                    cb.setChecked(tb_step.cellWidget(row_num + 1, col).isChecked())
                                    tb_step.setCellWidget(row_num, col, cb)
                                elif isinstance(cell_widget, QRadioButton):
                                    rb = QRadioButton()
                                    rb.setStyleSheet('QRadioButton{margin:6px};')
                                    rb.setText(tb_step.cellWidget(row_num + 1, col).text())
                                    rb.setChecked(tb_step.cellWidget(row_num + 1, col).isChecked())
                                    tb_step.setCellWidget(row_num, col, rb)
                            else:
                                if tb_step.cellWidget(row_num, col):
                                    tb_step.removeCellWidget(row_num, col)
                                    item = QTableWidgetItem(tb_step.item(row_num + 1, col).text())
                                    item.setTextAlignment(Qt.AlignCenter)
                                    tb_step.setItem(row_num, col, item)
                        elif col == 7:
                            pass
                        else:
                            item = QTableWidgetItem(tb_step.item(row_num + 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb_step.setItem(row_num, col, item)
                tb_step.setRowCount(row_count - 1)
                plan_list.pop(row_num)
        if action == item3:
            tb_step = self.tableWidget_Step
            row_count = tb_step.rowCount()
            col_count = tb_step.columnCount()
            tb_step.setRowCount(row_count + 1)
            plan_list.append([])
            row_num = tb_step.currentRow()
            if row_count > 0:  # 下移表格
                for row in range(row_count, row_num, -1):
                    plan_list[row] = copy.deepcopy(plan_list[row - 1])
                    cb = QCheckBox()
                    cb.setStyleSheet("""
                                        QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}
                                        QCheckBox::indicator:checked {
                                            background-color: lightgreen;
                                            border: 2px solid green;
                                        }
                                        QCheckBox::indicator:unchecked {
                                            background-color: lightgray;
                                            border: 2px solid gray;
                                        }
                                        QCheckBox::indicator {
                                            width: 10px;
                                            height: 10px;
                                        }
                                    """)
                    tb_step.setCellWidget(row, 0, cb)
                    tb_step.cellWidget(row, 0).setChecked(tb_step.cellWidget(row - 1, 0).isChecked())

                    for col in range(1, tb_step.columnCount() - 1):
                        if col == col_count - 2:
                            cell_widget = tb_step.cellWidget(row - 1, col)
                            if cell_widget:
                                if isinstance(cell_widget, QCheckBox):
                                    cb = QCheckBox()
                                    cb.setStyleSheet('QCheckBox{margin:6px};')
                                    cb.setText(tb_step.cellWidget(row - 1, col).text())
                                    cb.setChecked(tb_step.cellWidget(row - 1, col).isChecked())
                                    tb_step.setCellWidget(row, col, cb)
                                elif isinstance(cell_widget, QRadioButton):
                                    rb = QRadioButton()
                                    rb.setStyleSheet('QRadioButton{margin:6px};')
                                    rb.setText(tb_step.cellWidget(row - 1, col).text())
                                    rb.setChecked(tb_step.cellWidget(row - 1, col).isChecked())
                                    tb_step.setCellWidget(row, col, rb)
                            else:
                                if tb_step.cellWidget(row, col):  # 删除本行控件
                                    tb_step.removeCellWidget(row, col)
                                    item = QTableWidgetItem(tb_step.item(row - 1, col).text())
                                    item.setTextAlignment(Qt.AlignCenter)
                                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                                    tb_step.setItem(row, col, item)
                        elif col == 7:
                            btn = QPushButton("速度设置")
                            btn.clicked.connect(load_speed)  # 传递行号
                            tb_step.setCellWidget(row, 7, btn)
                        else:
                            item = QTableWidgetItem(tb_step.item(row - 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                            tb_step.setItem(row, col, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet("""
                                    QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}
                                    
                                    QCheckBox::indicator:checked {
                                    background-color: lightgreen;
                                    border: 2px solid green;
                                    }
                                    QCheckBox::indicator:unchecked {
                                        background-color: lightgray;
                                        border: 2px solid gray;
                                    }
                                    QCheckBox::indicator {
                                        width: 10px;
                                        height: 10px;
                                    }
                                """)
                tb_step.setCellWidget(0, 0, cb)

                for col in range(1, tb_step.columnCount() - 1):
                    if col == 7:
                        btn = QPushButton("速度设置")
                        btn.clicked.connect(load_speed)  # 传递行号
                        tb_step.setCellWidget(0, 7, btn)
                    else:
                        item = QTableWidgetItem('0')
                        item.setTextAlignment(Qt.AlignCenter)
                        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                        tb_step.setItem(0, col, item)


'''
    ReStartThread(QThread) 重启动作
'''


class ReStartThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ReStartThread, self).__init__()
        self.run_flg = False

        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global term
        global betting_start_time
        global betting_end_time
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            if not ui.radioButton_test_game.isChecked():  # 非模拟模式
                response = get_term(Track_number)
                if len(response) > 2:  # 开盘模式，获取期号正常
                    if term == response['term']:
                        self._signal.emit('term')
                        if not ui.checkBox_continue_term.isChecked():
                            time.sleep(3)
                            continue
                        else:
                            ui.checkBox_continue_term.setChecked(False)
                    term = response['term']
                    tcp_result_thread.send_type = 'time'
                    betting_start_time = response['scheduledGameStartTime']
                    betting_end_time = response['scheduledResultOpeningTime']
                    countdown = int(betting_start_time) - int(time.time())
                    print(betting_start_time, countdown)
                    if countdown < 0:  # 时间错误，30秒后开赛
                        betting_start_time = int(time.time())
                        betting_end_time = int(time.time()) + 30
                        countdown = str(30)
                    else:
                        countdown = str(countdown)
                    lottery = get_lottery_term()  # 获取了开盘时间后开盘写表
                    if lottery:
                        self._signal.emit(lottery)
                else:  # 封盘模式，退出循环
                    tcp_result_thread.send_type = 'time'
                    self._signal.emit('error')
                    self.run_flg = False
                    continue
            else:
                countdown = ui.lineEdit_Time_Restart_Ranking.text()
            if countdown.isdigit():
                countdown = int(countdown)
            else:
                countdown = 60
            self._signal.emit('auto_shoot')
            for t in range(countdown, -1, -1):
                if not ui.checkBox_restart.isChecked():
                    self.run_flg = False
                    break
                time.sleep(1)
                self._signal.emit(t)
            if ui.checkBox_restart.isChecked():
                reset_ranking_array()  # 初始化排名，位置变量
                PlanCmd_Thread.run_flg = True
            print("循环启动！")
            self.run_flg = False


def time_signal_accept(msg):
    if isinstance(msg, bool):
        lottery_data2table()
    # print(msg)
    elif msg == 'term':
        ui.lineEdit_term.setText(str(term))
        ui.textBrowser_msg.append(fail('期号重复，3秒后重新获取！'))
        scroll_to_bottom(ui.textBrowser_msg)
    elif msg == 'auto_shoot':
        ui.lineEdit_ball_end.setText('0')
        ui.checkBox_shoot_0.setChecked(True)
        auto_shoot()  # 自动上珠
    elif msg == 'error':
        ui.textBrowser_msg.append(fail('分机服务器没有响应，可能在封盘状态！'))
        scroll_to_bottom(ui.textBrowser_msg)
    elif isinstance(msg, int):
        if int(msg) == 1:
            plan_refresh()
            ui.lineEdit_ball_end.setText('0')
        ui.lineEdit_time.setText(str(msg))
        if not ui.radioButton_test_game.isChecked():  # 非测试模式
            tb_result = ui.tableWidget_Results
            tb_result.item(0, 2).setText(str(msg))


'''
    PosThread(QThread) 检测各轴位置
'''


class PosThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PosThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global pValue
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            if flg_start['card']:
                try:
                    for i in range(0, 5):
                        (res, pValue[i], pClock) = sc.get_pos(i + 1)
                    self._signal.emit(pValue)

                except:
                    pass
            self.run_flg = False


def pos_signal_accept(message):
    try:
        if len(message) == 5:
            for i in range(0, len(message)):
                getattr(ui, 'lineEdit_axis%s' % i).setText(str(message[i]))
        else:
            pass
    except:
        print("轴数据显示错误！")


'''
    CamThread(QThread) 摄像头运动方案线程
'''


class CamThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(CamThread, self).__init__()
        self.camitem = [5, 5]  # [运行挡位,持续时间]
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            time.sleep(0.01)
            if (not self.run_flg) or (not flg_start['s485']):
                continue
            print('串口运行')
            if self.camitem[0] != 0:
                try:
                    print(self.camitem)
                    res = s485.cam_zoom_step(self.camitem[0] - 1)
                    if not res:
                        flg_start['s485'] = False
                        self._signal.emit(fail("s485通信出错！"))
                        self.run_flg = False
                        continue
                    # time.sleep(self.camitem[1])
                    # s485.cam_zoom_off()
                except:
                    print("485 运行出错！")
                    flg_start['s485'] = False
                    self._signal.emit(fail("s485通信出错！"))
            self.run_flg = False


'''
    PlanBallNumThread(QThread) 摄像头运动方案线程
'''


class PlanBallNumThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanBallNumThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global flg_start
        global z_ranking_time
        while self.running:
            time.sleep(0.1)
            if (not self.run_flg) or (not flg_start['card']):
                continue
            print('正在接收运动卡输入信息！')
            try:
                res = sc.GASetDiReverseCount()  # 输入次数归0
                time_now = time.time()
                time_old = time.time()
                sec_ = 0
                num_old = 0
                if res == 0:
                    while True:
                        res, value = sc.GAGetDiReverseCount()
                        # print(res, value)
                        if res == 0:
                            num = int(value[0] / 2)
                            if num != num_old:
                                t = time.time()
                                if num_old < len(z_ranking_time):  # 保存每个球到达终点的时间
                                    z_ranking_time[num_old] = '%.2f' % (t - ranking_time_start)
                                    if not tcp_ranking_thread.send_time_flg:  # 发送排名时间并打开前端排名时间发送标志
                                        tcp_ranking_thread.send_time_data = [num, '%s"' % z_ranking_time[num - 1]]
                                        tcp_ranking_thread.send_time_flg = True
                                self._signal.emit(num)
                                num_old = num
                            if num >= balls_start and not ui.checkBox_Pass_Recognition_Start.isChecked():
                                break
                            elif num >= balls_count and ui.checkBox_Pass_Recognition_Start.isChecked():
                                break
                            elif time.time() - time_now > int(ui.lineEdit_time_count_ball.text()):
                                # 超时则跳出循环计球
                                sc.GASetDiReverseCount()  # 输入次数归0
                                # self._signal.emit(0)
                                break
                            else:
                                time_num = time.time() - time_old
                                if time_num > 1:
                                    time_old = time.time()
                                    sec_ += 1
                                    self._signal.emit(
                                        succeed('计球倒计时：%s' %
                                                str(int(ui.lineEdit_time_count_ball.text()) - sec_)))
                        else:
                            flg_start['card'] = False
                            self._signal.emit(fail("运动板x输入通信出错！"))
                            break
                        time.sleep(0.01)

                    for index in range(num_old - 1, len(z_ranking_time)):
                        if not tcp_ranking_thread.send_time_flg:  # 发送排名时间并打开前端排名时间发送标志
                            tcp_ranking_thread.send_time_data = [index + 1, '%s' % z_ranking_time[index]]
                            tcp_ranking_thread.send_time_flg = True
                        time.sleep(0.5)
                else:
                    print("次数归0 失败！")
                    flg_start['card'] = False
                    self._signal.emit(fail("运动板x输入通信出错！"))

                tcp_ranking_thread.sleep_time = 1  # 恢复正常前端排名数据包发送频率
                tcp_ranking_thread.run_flg = False  # 关闭排名
                ScreenShot_Thread.run_flg = True  # 终点截图识别线程
                Audio_Thread.run_flg = False  # 停止卫星图音效播放线程
                Ai_Thread.run_flg = False  # 停止卫星图AI播放线程
                main_music_worker.toggle_enable_signal.emit(False)
            except:
                print("接收运动卡输入 运行出错！")
                flg_start['card'] = False
                self._signal.emit(fail("运动板x输入通信出错！"))
            self.run_flg = False


def PlanBallNum_signal_accept(msg):
    if isinstance(msg, int):
        ui.lineEdit_ball_end.setText(str(msg))
    elif '计球倒计时' in msg:
        text_lines = ui.textBrowser_msg.toHtml().splitlines()
        if len(text_lines) >= 1:
            if '计球倒计时' in text_lines[-1]:
                text_lines[-1] = msg
                new_text = "\n".join(text_lines)
                ui.textBrowser_msg.setHtml(new_text)
            else:
                ui.textBrowser_msg.append(msg)
                scroll_to_bottom(ui.textBrowser_msg)
    else:
        ui.textBrowser.append(msg)
        ui.textBrowser_msg.append(msg)
        scroll_to_bottom(ui.textBrowser_msg)


'''
    ScreenShotThread(QThread) 结果截图线程
'''


class ScreenShotThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ScreenShotThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global lottery_term
        global betting_end_time
        global Send_Result
        global z_ranking_res
        global main_Camera, monitor_Camera, fit_Camera
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('截图结果识别运行！')
            self._signal.emit(succeed('截图结果识别运行！'))
            t_count = ui.lineEdit_time_send_result.text()
            if t_count.isdigit():
                t_count = int(t_count)
            else:
                t_count = 5
            for t in range(t_count, 0, -1):
                # 开始倒数截图识别
                if int(ui.lineEdit_ball_end.text()) >= balls_start:  # 当全部球到达终点，则跳出倒数
                    break
                print('结果倒数：', t)
                time.sleep(1)
            obs_res = get_picture(ui.lineEdit_source_end.text())  # 拍摄来源
            if obs_res:
                main_Camera = camera_to_num(eval(obs_res[1]))
                self._signal.emit(obs_res)
            monitor_res = get_rtsp(rtsp_url)  # 网络摄像头拍摄
            if monitor_res:
                monitor_Camera = camera_to_num(eval(monitor_res[1]))
                self._signal.emit(monitor_res)

            if obs_res[1] != '[1]' and obs_res[1] == monitor_res[1]:
                print('识别正确:', obs_res[1])
                if len(main_Camera) == len(z_ranking_res):
                    z_ranking_res = main_Camera
            else:
                if not ui.checkBox_Pass_Ranking_Twice.isChecked():
                    pass  # 警报声
                    while True:
                        if Send_Result:
                            send_res = ui.lineEdit_Send_Result.text()
                            if send_res != '':
                                send_list = eval(ui.lineEdit_Send_Result.text())
                                if len(send_list) == len(z_ranking_res):
                                    z_ranking_res = send_list
                                    break
                            else:
                                self._signal.emit('send_res')
                                Send_Result = False
                        time.sleep(1)
                    Send_Result = False
            if not ui.radioButton_test_game.isChecked():  # 非模拟模式
                if ui.checkBox_end_stop.isChecked():  # 本局结束自动封盘
                    ui.radioButton_stop_betting.click()  # 封盘
                if ui.checkBox_end_BlackScreen.isChecked():  # 本局结束自动封盘黑屏
                    ui.checkBox_restart.setChecked(False)
                    ui.radioButton_stop_betting.click()  # 封盘
                    ui.checkBox_black_screen.click()
            if not flg_start['obs']:
                return
            try:
                requests.get(url="%s/stop" % obs_script_addr)  # 发送信号，停止OBS计时
                tcp_result_thread.send_type = 'updata'
                tcp_result_thread.run_flg = True
                cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_settlement'],
                                                  True)  # 打开视频来源
                time.sleep(0.1)
                cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_picture'],
                                                  False)  # 打开视频来源
                time.sleep(0.1)
                cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_ranking'],
                                                  False)  # 打开视频来源
            except:
                print('OBS 切换操作失败！')
                flg_start['obs'] = False

            self.run_flg = False


def ScreenShot_signal_accept(msg):
    try:
        if isinstance(msg, list):
            if len(msg) < 2 or msg[0] == '':
                return
            img = msg[0]
            pixmap = QPixmap()
            pixmap.loadFromData(img)
            pixmap = pixmap.scaled(int(400 * 1.6), int(225 * 1.6))
            if msg[2] == 'obs':
                ui.label_main_picture.setPixmap(pixmap)
                ui.lineEdit_Main_Camera.setText(str(main_Camera))
            elif msg[2] == 'monitor':
                ui.label_monitor_picture.setPixmap(pixmap)
                ui.lineEdit_Backup_Camera.setText(str(monitor_Camera))
            for index in range(len(main_Camera)):
                fit_Camera[index] = (main_Camera[index] == monitor_Camera[index])
            if perfect_Camera == fit_Camera:
                ui.lineEdit_result_send.setText(str(main_Camera))
        elif msg == 'send_res':
            ui.lineEdit_Send_Result.setText(ui.lineEdit_Main_Camera.text())
        else:
            ui.textBrowser.append(str(msg))
            ui.textBrowser_msg.append(str(msg))
            scroll_to_bottom(ui.textBrowser_msg)
    except:
        print('OBS 操作失败！')


'''
    PlanObsThread(QThread) 摄像头运动方案线程
'''


class PlanObsThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanObsThread, self).__init__()
        self.plan_obs = '0'  # [开关,场景名称]
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            time.sleep(0.01)
            if (not self.run_flg) or (not flg_start['obs']):
                continue
            print('OBS运行')
            try:
                if '_' in self.plan_obs:  # 切换场景
                    obs_msg = str.split(self.plan_obs, '_')
                    # print(obs_msg)
                    if obs_msg[0] in ['10', '11']:
                        cl_request.set_current_program_scene(obs_msg[1])
                        self._signal.emit(succeed("OBS 场景切换完成！"))
                    elif obs_msg[0] in ['0', '1']:
                        # print(obs_msg[1])
                        cb_scene = ui.comboBox_Scenes
                        scene_name = cb_scene.currentText()
                        tb_source = ui.tableWidget_Sources
                        for row_num in range(tb_source.rowCount()):
                            if tb_source.item(row_num, 1).text() == obs_msg[1]:
                                item_id = source_list[row_num][2]
                                flg_enable = (True if obs_msg[0] == '1' else False)
                                print(scene_name, item_id, flg_enable)
                                cl_request.set_scene_item_enabled(scene_name, item_id,
                                                                  flg_enable)  # 打开视频来源
                                break
                        self._signal.emit(succeed("OBS 来源切换完成！"))
                else:
                    print('没有切换的场景！')
            except:
                print("OBS 切换中断！")
                flg_start['obs'] = False
                self._signal.emit(fail("OBS 场景切换中断！"))
            self.run_flg = False


def PlanObs_signal_accept(msg):
    ui.textBrowser.append(str(msg))


'''
    ShootThread(QThread) 弹射上珠线程
'''


class ShootThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ShootThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('弹射上珠线程！')
            try:
                shoot_index = int(ui.lineEdit_shoot.text()) - 1
                sc.GASetExtDoBit(shoot_index, 1)
                time.sleep(0.5)
                end_index = int(ui.lineEdit_end.text()) - 1
                sc.GASetExtDoBit(end_index, 0)
                while self.run_flg:
                    time.sleep(1)
                    if (ui.lineEdit_balls_auto.text().isdigit()
                            and int(ui.lineEdit_balls_start.text()) >= int(ui.lineEdit_balls_auto.text())):
                        break
                    elif (ui.lineEdit_balls_auto.text().isdigit()
                          and balls_start >= int(ui.lineEdit_balls_auto.text())):
                        break
                shoot_index = int(ui.lineEdit_shoot.text()) - 1
                sc.GASetExtDoBit(shoot_index, 0)
                self.run_flg = False
            except:
                print("弹射上珠参数出错！")
                self._signal.emit(fail("弹射上珠参数出错！"))
            self.run_flg = False


def shoot_signal_accept(msg):
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)


'''
    AxisThread(QThread) 轴复位线程
'''


class AxisThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(AxisThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global flg_start
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('串口运行')
            try:
                self._signal.emit(succeed('轴复位开始！'))
                s485_data = s485.get_axis_pos()
                # print(s485_data)
                if len(s485_data) > 0:
                    for data in s485_data:
                        # if data['nAxisNum'] in [1, 5]:  # 轴一，轴五，方向反过来，所以要设置负数
                        data['highPos'] = data['highPos'] * five_axis[data['nAxisNum'] - 1]
                        # print(data['nAxisNum'], data['highPos'])
                        res = sc.GASetPrfPos(data['nAxisNum'], data['highPos'])
                        if res == 0:
                            sc.card_move(int(data['nAxisNum']), 0)
                    res = sc.card_update()
                    if res == 0:
                        flg_start['card'] = True
                        Pos_Thread.run_flg = True
                        self._signal.emit(succeed('轴复位完成！'))
                    else:
                        flg_start['card'] = False
                        self._signal.emit(fail('运动卡链接出错！'))
                    flg_start['s485'] = True
                else:
                    flg_start['s485'] = False
                    self._signal.emit(fail('复位串口未连接！'))
            except:
                print("轴复位出错！")
                flg_start['s485'] = False
                self._signal.emit(fail('轴复位出错！'))
            self.run_flg = False


'''
    CmdThread(QThread) 执行运动方案线程
'''


class PlanCmdThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanCmdThread, self).__init__()
        self.run_flg = False
        self.cmd_next = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global action_area
        global ranking_time_start
        global lottery_term
        axis_list = [1, 2, 4, 8, 16]
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            if (ui.checkBox_shoot_0.isChecked()
                    and (ui.lineEdit_balls_auto.text().isdigit()
                         and int(ui.lineEdit_balls_start.text()) < int(ui.lineEdit_balls_auto.text()))):
                continue  # 如果选择了自动上珠，必须等到珠上齐才开始游戏
            if flg_start['card'] and action_area[1] < max_lap_count:
                if not ui.checkBox_test.isChecked():  # 如果是测试模式，不播放主题音乐
                    main_music_worker.toggle_enable_signal.emit(True)
                Audio_Thread.run_flg = True  # 开启音频播放线程
                Ai_Thread.run_flg = True  # 开启AI播放线程
                self._signal.emit(succeed("运动流程：开始！"))
                self.cmd_next = False  # 初始化手动快速跳过下一步动作标志
                cb_index = ui.comboBox_plan.currentIndex()
                for plan_index in range(0, len(plan_list)):
                    print('第 %s 个动作，识别在第 %s 区 %s 圈！' % (plan_index + 1, action_area[0], action_area[1]))
                    if (not self.run_flg) or (not flg_start['card']):  # 强制停止线程
                        print('动作未开始！')
                        break
                    if (plan_list[plan_index][0] == '1' and  # 是否勾选,且在圈数范围内
                            (action_area[1] < int(float(plan_list[plan_index][1][0])) or  # 运行圈数在设定圈数范围内
                             (int(float(plan_list[plan_index][1][0])) == 0))):  # 或者设定圈数的值为 0 时，可以忽略圈数执行
                        self._signal.emit(plan_index)  # 控制列表跟踪变色的信号

                        try:
                            # print("开启机关")
                            if int(float(plan_list[plan_index][12][0])) != 0:
                                if '-' in plan_list[plan_index][12][0]:  # 带负号即关闭机关
                                    sc.GASetExtDoBit(abs(int(float(plan_list[plan_index][12][0]))) - 1, 0)
                                else:  # 不带负号即开启机关
                                    sc.GASetExtDoBit(abs(int(float(plan_list[plan_index][12][0]))) - 1, 1)
                                if plan_list[plan_index][12][0] == ui.lineEdit_start.text():  # '2'闸门机关打开
                                    requests.get(url="%s/start" % obs_script_addr)  # 开始OBS的python脚本计时
                                    ranking_time_start = time.time()  # 每个球的起跑时间
                                    if not ui.radioButton_test_game.isChecked():  # 非模拟模式
                                        post_start(term, betting_start_time, Track_number)  # 发送开始信号给服务器
                                        lottery_term[3] = '进行中'  # 新一期比赛的状态（1.进行中）
                                        self._signal.emit('进行中')  # 修改结果列表中的赛事状态
                                        if flg_start['obs']:  # 非测试模式:
                                            try:
                                                cl_request.start_record()  # 开启OBS录像
                                            except:
                                                print('OBS脚本开始错误！')

                            if (plan_list[plan_index][15][0].isdigit()
                                    and int(plan_list[plan_index][15][0]) > 0):  # 播放音效
                                tb_audio = ui.tableWidget_Audio
                                audio_row_count = tb_audio.rowCount()
                                # print('~~~~~~~~~~~~~~~~~~~~音效', plan_list[plan_num][15])
                                if int(plan_list[plan_index][15][0]) - 1 < audio_row_count:
                                    sound_file = tb_audio.item(int(plan_list[plan_index][15][0]) - 1, 0).text()
                                    sound_times = int(tb_audio.item(int(plan_list[plan_index][15][0]) - 1, 1).text())
                                    sound_delay = int(
                                        tb_audio.item(int(plan_list[plan_index][15][0]) - 1, 2).text()) * 1000
                                    print(sound_file, sound_times, sound_delay)
                                    # 加载音效
                                    sound_effect = pygame.mixer.Sound(sound_file)
                                    sound_effect.play(loops=sound_times, maxtime=sound_delay)  # 播放音效
                            # 轴运动
                            axis_bit = 0  # 非延迟轴统计
                            max_delay_time = 0  # 记录最大延迟时间
                            delay_list = []  # 延迟的轴列表
                            for index, speed_item in enumerate(plan_list[plan_index][7]):
                                sc.card_move(index + 1, int(float(plan_list[plan_index][index + 2][0])),
                                             vel=abs(int(float(speed_item[0]))),
                                             dAcc=float(speed_item[1]),
                                             dDec=float(speed_item[2]),
                                             dVelStart=0.1, dSmoothTime=0)
                                if float(speed_item[3]) == 0:
                                    axis_bit += axis_list[index]
                                else:
                                    delay_list.append([axis_list[index], float(format(float(speed_item[3]), ".3f"))])
                                if max_delay_time < float(format(float(speed_item[3]), ".3f")):
                                    max_delay_time = float(format(float(speed_item[3]), ".3f"))
                            if axis_bit != 0:  # 非延迟轴
                                res = sc.card_update(axis_bit)
                                if res != 0:
                                    print("运动板通信出错！")
                                    flg_start['card'] = False
                                    self._signal.emit(fail("运动板通信出错！"))
                            old_time = 0
                            for t in range(0, int(max_delay_time * 100) + 1):  # 延迟轴
                                for index in range(len(delay_list)):
                                    if t >= delay_list[index][1] * 100 > old_time:
                                        sc.card_update(delay_list[index][0])
                                        old_time = t
                                time.sleep(0.01)
                        except:
                            print("运动板运行出错！")
                            self._signal.emit(fail("运动板通信出错！"))

                        if self.run_flg:
                            try:
                                if float(plan_list[plan_index][11][0]) > 0:
                                    time.sleep(float(plan_list[plan_index][11][0]))  # 延时，等待镜头缩放完成
                                # 摄像头缩放
                                if 0 < int(float(plan_list[plan_index][10][0])) <= 5:  # 摄像头缩放
                                    PlanCam_Thread.camitem = [int(float(plan_list[plan_index][10][0])),
                                                              float(plan_list[plan_index][11][0])]
                                    PlanCam_Thread.run_flg = True  # 摄像头线程
                            except:
                                print("摄像头数据出错！")
                                self._signal.emit(fail("摄像头数据出错！"))
                        try:
                            if ui.checkBox_test.isChecked():
                                if float(plan_list[plan_index][16][0]) >= 0:
                                    time.sleep(float(plan_list[plan_index][16][0]))
                                else:
                                    time.sleep(2)  # 测试模式停两秒切换下一个动作
                            elif float(plan_list[plan_index][14][0]) == 0:
                                pass  # 0则直接下一个动作
                            elif float(plan_list[plan_index][14][0]) < 0:
                                time.sleep(abs(float(plan_list[plan_index][14][0])))  # 负数则等待对应秒数再进行下一个动作
                            else:
                                t_over = 0
                                while True:  # 正式运行，等待球进入触发区域再进行下一个动作
                                    if not self.run_flg:
                                        print('动作等待中！')
                                        break
                                    if not plan_list[plan_index][14][0].isdigit():
                                        self._signal.emit(fail("%s 卫星图号出错！" % plan_list[plan_index][14][0]))
                                        break
                                    # 判断镜头点位在运行区域内则进入下一个动作循环
                                    self._signal.emit({'map_action': map_label_big.map_action})
                                    if (int(camera_points[abs(int(float(plan_list[plan_index][14][0])))]
                                            [cb_index + 1][0][0]) - 100
                                            < map_label_big.map_action
                                            <= int(camera_points[abs(int(float(plan_list[plan_index][14][0])))]
                                                   [cb_index + 1][0][0])):
                                        break
                                    t_over += 1
                                    if plan_list[plan_index][16][0] != '0':
                                        if t_over >= abs(float(plan_list[plan_index][16][0])) * 10:  # 每个动作超时时间
                                            self._signal.emit(fail('第 %s 个动作 等待超时！' % str(plan_index + 1)))
                                            print('等待超时！')
                                            break
                                    else:
                                        if t_over >= 150:
                                            self._signal.emit(fail('第 %s 个动作 等待超过15秒！' % str(plan_index + 1)))
                                            print('等待超过15秒！')
                                            break
                                    if self.cmd_next:  # 手动进入下一个动作
                                        break
                                    time.sleep(0.1)
                        except:
                            print("动作等待数据出错！")
                            self._signal.emit(fail("动作等待数据出错！"))
                        if self.cmd_next:  # 快速执行下一个动作
                            self._signal.emit(succeed("跳过动作 %s！" % (plan_index + 1)))
                            self.cmd_next = False
                            continue
                        if self.run_flg:
                            try:
                                # 场景切换
                                plan_col_count = len(plan_list[plan_index])  # 固定最后一项为OBS场景切换
                                if '_' in plan_list[plan_index][plan_col_count - 1]:
                                    PlanObs_Thread.plan_obs = plan_list[plan_index][plan_col_count - 1]
                                    PlanObs_Thread.run_flg = True  # 切换场景线程
                            except:
                                print("场景数据出错！")
                                self._signal.emit(fail("场景数据出错！"))
                            if (not ui.checkBox_test.isChecked()
                                    and (len(plan_list) - 6 <= plan_index)
                                    and (action_area[1] >= max_lap_count - 1)):  # 到达最后一圈终点前区域，则打开终点及相应机关
                                # 计球器
                                if len(plan_list) - 2 == plan_index:  # 到达最后两个动作时，触发球计数器启动
                                    PlanBallNum_Thread.run_flg = True  # 终点计数器线程
                                    tcp_ranking_thread.sleep_time = 0.1  # 终点前端排名时间发送设置
                                # 最后几个动作内，打开终点开关，关闭闸门，关闭弹射
                                sc.GASetExtDoBit(3, 1)  # 打开终点开关
                                sc.GASetExtDoBit(1, 0)  # 关闭闸门
                                sc.GASetExtDoBit(0, 0)  # 关闭弹射
                            # 圈数统计
                            if (not ui.checkBox_test.isChecked()
                                    and plan_index == len(plan_list) - 1):  # 每执行完最后一个动作，action_area[1]圈数自动增加一圈
                                map_label_big.map_action = 0
                                action_area[2] = 1  # 写入标志 1 为独占写入
                                action_area[0] = 0
                                action_area[1] += 1
                                action_area[2] = 0  # 写入标志 0 为任意写入
                # 强制中断情况处理
                if not ui.checkBox_test.isChecked() and not self.run_flg:  # 强制中断情况下的动作
                    # 强制中断则打开终点开关，关闭闸门，关闭弹射
                    print('另外开关~~~~~~~~~')
                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                    sc.GASetExtDoBit(0, 0)  # 关闭弹射
                    main_music_worker.toggle_enable_signal.emit(False)
                    self._signal.emit(succeed("运动流程：中断！"))
                if ui.checkBox_test.isChecked():
                    self._signal.emit(succeed("测试流程：完成！"))
                    self.run_flg = False  # 测试模式，不自动关闭任何机关
            else:  # 运行出错，或者超出圈数，流程完成时执行
                if not ui.checkBox_test.isChecked():  # 非测试模式，流程结束始终关闭闸门
                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                    sc.GASetExtDoBit(0, 0)  # 关闭弹射
                self._signal.emit(succeed("运动流程：完成！"))
                print('动作已完成！')
                if not flg_start['card']:
                    self._signal.emit(fail("运动卡未链接！"))
                self.run_flg = False


def signal_accept(msg):
    # print(message)
    try:
        if isinstance(msg, int):
            # print('动作位置 %s %s' % (message, p_now))
            if ui.checkBox_follow.isChecked():
                tb_step = ui.tableWidget_Step
                tb_step.selectRow(msg)  # 默认停留在触发行
        elif isinstance(msg, dict):
            if 'map_action' in msg.keys():
                ui.lineEdit_area.setText(str(msg['map_action']))
        elif msg == '进行中':
            tb_result = ui.tableWidget_Results
            tb_result.item(0, 3).setText(lottery_term[3])  # 新一期比赛的状态（1.进行中）
        else:
            ui.textBrowser.append(str(msg))
            ui.textBrowser_msg.append(str(msg))
            scroll_to_bottom(ui.textBrowser_msg)
    except:
        print("运行数据处理出错！")


"""
    ui工作线程
"""


class UiWorker(QObject):
    toggle_enable_signal = Signal(object)

    def __init__(self, z_object):
        super().__init__()
        self.z_object = z_object
        self.toggle_enable_signal.connect(self.toggle_enable)

    def toggle_enable(self, msg):
        if isinstance(self.z_object, QTableWidget):
            self.z_object.setEnabled(msg)
        elif isinstance(self.z_object, QCheckBox):
            self.z_object.setChecked(msg)
        elif isinstance(self.z_object, QTextBrowser):
            self.z_object.append(msg)
        else:
            print(f"Unsupported object type: {type(self.z_object)}")


def keyboard_release(key):
    global flg_key_run
    if ui.checkBox_key.isChecked() and flg_start['card']:
        try:
            if key == key.up:
                print('前')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[1] = pValue[1] + 30000 * int(five_key[1])
                if pValue[1] <= 0:
                    pValue[1] = 0
                ui.lineEdit_axis1.setText(str(pValue[1]))
                sc.card_setpos(2, pValue[1])
                sc.card_update()

            if key == key.down:
                print('后')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[1] = pValue[1] - 30000 * int(five_key[1])
                if pValue[1] <= 0:
                    pValue[1] = 0
                ui.lineEdit_axis1.setText(str(pValue[1]))
                sc.card_setpos(2, pValue[1])
                sc.card_update()

            if key == key.left:
                print('左')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[0] = pValue[0] - 30000 * int(five_key[0])
                if pValue[0] <= 0:
                    pValue[0] = 0
                ui.lineEdit_axis0.setText(str(pValue[0]))
                sc.card_setpos(1, pValue[0])
                sc.card_update()

            if key == key.right:
                print('右')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[0] = pValue[0] + 30000 * int(five_key[0])
                if pValue[0] <= 0:
                    pValue[0] = 0
                ui.lineEdit_axis0.setText(str(pValue[0]))
                sc.card_setpos(1, pValue[0])
                sc.card_update()

            if key == key.insert:
                print('上')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[2] = pValue[2] - 30000 * int(five_key[2])
                if pValue[2] <= 0:
                    pValue[2] = 0
                ui.lineEdit_axis2.setText(str(pValue[2]))
                sc.card_setpos(3, pValue[2])
                sc.card_update()

            if key == key.delete:
                print('下')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[2] = pValue[2] + 30000 * int(five_key[2])
                if pValue[2] <= 0:
                    pValue[2] = 0
                ui.lineEdit_axis2.setText(str(pValue[2]))
                sc.card_setpos(3, pValue[2])
                sc.card_update()

            if key == key.home:
                print('头左')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[3] = pValue[3] - 30000 * int(five_key[3])
                ui.lineEdit_axis3.setText(str(pValue[3]))
                sc.card_setpos(4, pValue[3])
                sc.card_update()

            if key == key.end:
                print('头右')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[3] = pValue[3] + 30000 * int(five_key[3])
                ui.lineEdit_axis3.setText(str(pValue[3]))
                sc.card_setpos(4, pValue[3])
                sc.card_update()

            if key == key.page_up:
                print('头上')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[4] = pValue[4] + 30000 * int(five_key[4])
                ui.lineEdit_axis4.setText(str(pValue[4]))
                sc.card_setpos(5, pValue[4])
                sc.card_update()

            if key == key.page_down:
                print('头下')
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[4] = pValue[4] - 30000 * int(five_key[4])
                ui.lineEdit_axis4.setText(str(pValue[4]))
                sc.card_setpos(5, pValue[4])
                sc.card_update()

        except AttributeError:
            pass
            # print(key)
        try:
            if key.char == '/':
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                s485.cam_zoom_off()
            elif key.char == '*':
                tb_step_worker.toggle_enable_signal.emit(ui.checkBox_test.isChecked())
                s485.cam_zoom_off()
        except:
            pass
            # print(key)
        Pos_Thread.run_flg = False


def keyboard_press(key):
    global flg_key_run
    try:
        if key == key.enter:
            if not ui.radioButton_start_betting.isChecked():
                cmd_stop()
    except:
        pass
    if ui.checkBox_key.isChecked() and flg_start['card']:
        try:
            Pos_Thread.run_flg = True
            if key == key.up:
                print('前')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = 2000000 * int(five_key[1])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(2, pos=pos)
                    sc.card_update()
                    flg_key_run = False

            elif key == key.down:
                print('后')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = -2000000 * int(five_key[1])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(2, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.left:
                print('左')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = -2000000 * int(five_key[0])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(1, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.right:
                print('右')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = 2000000 * int(five_key[0])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(1, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.insert:
                print('上')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = -2000000 * int(five_key[2])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(3, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.delete:
                print('下')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    pos = 2000000 * int(five_key[2])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(3, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.home:
                print('头左')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    sc.card_move(4, pos=-2000000 * int(five_key[3]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.end:
                print('头右')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    sc.card_move(4, pos=2000000 * int(five_key[3]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_up:
                print('头下')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    sc.card_move(5, pos=2000000 * int(five_key[4]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_down:
                print('头上')
                if flg_key_run:
                    tb_step_worker.toggle_enable_signal.emit(False)
                    sc.card_move(5, pos=-2000000 * int(five_key[4]), vel=50)
                    sc.card_update()
                    flg_key_run = False
        except AttributeError:
            # print(key)
            pass
        try:
            if key.char == '/':
                tb_step_worker.toggle_enable_signal.emit(False)
                s485.cam_zoom_move(5)
            elif key.char == '*':
                tb_step_worker.toggle_enable_signal.emit(False)
                s485.cam_zoom_move(-5)
        except:
            pass
            # print(key)


def accept_speed():
    global plan_list
    tb_speed = speed_ui.tableWidget_Set_Speed
    speed_row_count = tb_speed.rowCount()
    speed_col_count = tb_speed.columnCount()
    speed_list = []
    for row in range(speed_row_count):
        speed_item = []
        for col in range(speed_col_count):
            speed_item.append(tb_speed.item(row, col).text())
        speed_list.append(copy.deepcopy(speed_item))
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    plan_list[row_num][7] = copy.deepcopy(speed_list)
    tb_step.cellWidget(row_num, 7).setStyleSheet('background:rgb(0, 255, 0)')


def reject_speed():
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    tb_step.cellWidget(row_num, 7).setStyleSheet('background:rgb(255, 0, 0)')


def load_speed():
    speed_ui.checkBox_auto_line.setChecked(False)
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    speed_list = plan_list[row_num][7]
    tb_speed = speed_ui.tableWidget_Set_Speed
    for row in range(len(speed_list)):
        for col in range(len(speed_list[row])):
            tb_speed.item(row, col).setText(speed_list[row][col])
    SpeedDialog.show()


# 保存方案
def save_plan_yaml():
    global plan_list
    global plan_all
    tb_step = ui.tableWidget_Step
    row_num = tb_step.rowCount()
    col_count = tb_step.columnCount()
    if row_num == 0:
        return
    plan_list_temp = []
    local_list = []
    for row in range(0, row_num):
        if tb_step.cellWidget(row, 0):
            if tb_step.cellWidget(row, 0).isChecked():
                local_list.append("1")
            else:
                local_list.append("0")
        for col in range(1, col_count - 2):
            if col == 7:
                local_list.append(copy.deepcopy(plan_list[row][col]))
            else:
                local_list.append(
                    ["0"] if (not tb_step.item(row, col) or tb_step.item(row, col).text() == '')
                    else [tb_step.item(row, col).text()])

        cell_widget = tb_step.cellWidget(row, col_count - 2)
        if cell_widget:
            if isinstance(cell_widget, QCheckBox):
                if cell_widget.isChecked():
                    local_list.append(str("1_%s" % cell_widget.text()))
                else:
                    local_list.append(str("0_%s" % cell_widget.text()))
            if isinstance(cell_widget, QRadioButton):
                if cell_widget.isChecked():
                    local_list.append(str("11_%s" % cell_widget.text()))
                else:
                    local_list.append(str("10_%s" % cell_widget.text()))
        else:
            local_list.append(
                ["0"] if (not tb_step.item(row, col_count - 2)
                          or tb_step.item(row, col_count - 2).text() == '')
                else [tb_step.item(row, col_count - 2).text()])
        plan_list_temp.append(local_list)
        local_list = []
    # print(plan_list)
    plan_list = copy.deepcopy(plan_list_temp)

    comb = ui.comboBox_plan
    plan_num = comb.currentIndex()
    plan_name = comb.currentText()

    file = "Plan_config.yml"
    if os.path.exists(file):
        plan_all['plans']['plan%d' % (plan_num + 1)]['plan_name'] = plan_name
        plan_all['plans']['plan%d' % (plan_num + 1)]['plan_list'] = plan_list_temp
        try:
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(plan_all, f, allow_unicode=True)
            f.close()
            ui.textBrowser.append(succeed('方案保存：成功'))
        except:
            ui.textBrowser.append(fail('方案保存：失败'))
        print("保存成功~！")


# 载入方案
def load_plan_yaml():
    global plan_names
    global plan_all
    global camera_points
    file = "Plan_config.yml"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            plan_all = yaml.safe_load(f)
            f.close()
            for plan in plan_all['plans']:
                plan_names.append(plan_all['plans'][plan]['plan_name'])

            comb = ui.comboBox_plan
            comb.addItems(plan_names)
            plan_refresh()
        except:
            pass
    else:
        print("文件不存在")


def plan_refresh():  # 刷新方案列表
    global plan_list
    comb = ui.comboBox_plan
    _index = comb.currentIndex()
    plan_list = plan_all['plans']['plan%d' % (_index + 1)]['plan_list']

    tb_step = ui.tableWidget_Step
    col_count = tb_step.columnCount()
    for num, plan in enumerate(plan_list):
        tb_step.setRowCount(num + 1)
        cb = QCheckBox()
        cb.setStyleSheet("""
            QCheckBox{margin:6px;padding-left: 1px;padding-top: 1px;}
            
            QCheckBox::indicator:checked {
                background-color: lightgreen;
                border: 2px solid green;
            }
            QCheckBox::indicator:unchecked {
                background-color: lightgray;
                border: 2px solid gray;
            }
            QCheckBox::indicator {
                width: 10px;
                height: 10px;
            }
        """)
        tb_step.setCellWidget(num, 0, cb)
        if plan[0] == '1':
            tb_step.cellWidget(num, 0).setChecked(True)
        for col in range(1, len(plan)):
            if col == col_count - 2:
                if tb_step.item(num, col):
                    tb_step.item(num, col).setText('')
                if tb_step.cellWidget(num, col):
                    tb_step.removeCellWidget(num, col)
                s_num = str(plan[col]).find('_')
                if s_num != -1:
                    obs_check = str(plan[col])[0:s_num]
                    obs_name = str(plan[col])[s_num + 1:]
                    # print(obs_check, obs_name)
                    if obs_check in ['0', '1']:
                        cb = QCheckBox()
                        cb.setStyleSheet('QCheckBox{margin:6px};')
                        cb.setText(obs_name)
                        if obs_check == '1':
                            cb.setChecked(True)
                        tb_step.setCellWidget(num, col_count - 2, cb)
                    elif obs_check in ['10', '11']:
                        rb = QRadioButton()
                        rb.setStyleSheet('QRadioButton{margin:6px};')
                        rb.setText(obs_name)
                        if obs_check == '11':
                            rb.setChecked(True)
                        tb_step.setCellWidget(num, col_count - 2, rb)
                else:
                    item = QTableWidgetItem(
                        "0" if not plan[col] else plan[col][0])
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    tb_step.setItem(num, col, item)
            elif col == 7:
                btn = QPushButton("速度设置")
                btn.clicked.connect(load_speed)  # 传递行号
                tb_step.setCellWidget(num, col, btn)
            else:
                item = QTableWidgetItem(str(plan[col][0]))
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                tb_step.setItem(num, col, item)
    for index in range(len(camera_points)):  # 卫星图刷新
        num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
        camera_points[index][0].move(*camera_points[index][num][1])  # 设置初始位置
        camera_points[index][0].show()
    for index in range(len(audio_points)):  # 卫星图刷新
        num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
        audio_points[index][0].move(*audio_points[index][num][1])  # 设置初始位置
        audio_points[index][0].show()
    for index in range(len(ai_points)):  # 卫星图刷新
        num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
        ai_points[index][0].move(*ai_points[index][num][1])  # 设置初始位置
        ai_points[index][0].show()


def save_main_yaml():
    global init_array
    global color_ch
    global udpServer_addr
    global tcpServer_addr
    global result_tcpServer_addr
    global wakeup_addr
    global balls_count
    global rtsp_url
    global recognition_addr
    global obs_script_addr
    global map_data
    global five_axis
    global five_key

    file = "main_config.yml"
    if os.path.exists(file):
        try:
            with (open(file, "r", encoding="utf-8") as f):
                main_all = yaml.safe_load(f)
                # print(main_all)
                main_all['cardNo'] = ui.lineEdit_cardNo.text()
                main_all['s485_Axis_No'] = ui.lineEdit_s485_Axis_No.text()
                main_all['s485_Cam_No'] = ui.lineEdit_s485_Cam_No.text()
                main_all['five_axis'] = eval(ui.lineEdit_five_axis.text())
                main_all['five_key'] = eval(ui.lineEdit_five_key.text())
                main_all['balls_count'] = ui.lineEdit_balls_count.text()
                main_all['wakeup_addr'] = eval(ui.lineEdit_wakeup_addr.text())
                main_all['rtsp_url'] = ui.lineEdit_rtsp_url.text()
                main_all['recognition_addr'] = ui.lineEdit_recognition_addr.text()
                main_all['obs_script_addr'] = ui.lineEdit_obs_script_addr.text()
                main_all['tcpServer_addr'][1] = ui.lineEdit_TcpServer_Port.text()
                main_all['result_tcpServer_addr'][1] = ui.lineEdit_result_tcpServer_port.text()
                main_all['udpServer_addr'][1] = ui.lineEdit_UdpServer_Port.text()
                main_all['map_picture'] = ui.lineEdit_map_picture.text()
                main_all['map_size'] = ui.lineEdit_map_size.text()
                main_all['map_line'] = ui.lineEdit_map_line.text()
                main_all['Image_Path'] = ui.lineEdit_Image_Path.text()
                main_all['scene_name'] = ui.lineEdit_scene_name.text()
                main_all['source_ranking'] = ui.lineEdit_source_ranking.text()
                main_all['source_picture'] = ui.lineEdit_source_picture.text()
                main_all['source_settlement'] = ui.lineEdit_source_settlement.text()
                main_all['source_end'] = ui.lineEdit_source_end.text()
                for index in range(1, 4):
                    main_all['music_%s' % index][1] = getattr(ui, 'lineEdit_music_%s' % index).text()
                    main_all['music_%s' % index][0] = getattr(ui, 'radioButton_music_background_%s' % index).isChecked()
                for index in range(1, 11):
                    eng = getattr(ui, 'lineEdit_Color_Eng_%s' % index).text()
                    ch = getattr(ui, 'lineEdit_Color_Ch_%s' % index).text()
                    main_all['init_array'][index - 1][5] = eng
                    main_all['color_ch'][eng] = ch

                # 赋值变量
                init_array = main_all['init_array']
                color_ch = main_all['color_ch']
                wakeup_addr = main_all['wakeup_addr']
                balls_count = int(main_all['balls_count'])
                rtsp_url = main_all['rtsp_url']
                recognition_addr = main_all['recognition_addr']
                obs_script_addr = main_all['obs_script_addr']
                s485.s485_Axis_No = main_all['s485_Axis_No']
                s485.s485_Cam_No = main_all['s485_Cam_No']
                five_axis = main_all['five_axis']
                five_key = main_all['five_key']
                map_data = [main_all['map_picture'], main_all['map_line'], main_all['map_size']]
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(main_all, f, allow_unicode=True)
            f.close()
            ui.textBrowser_save_msg.append(succeed('方案保存：成功'))
        except:
            ui.textBrowser_save_msg.append(fail('方案保存：失败'))
        print("保存成功~！")


def load_main_yaml():
    global init_array
    global color_ch
    global udpServer_addr
    global tcpServer_addr
    global result_tcpServer_addr
    global wakeup_addr
    global balls_count
    global rtsp_url
    global recognition_addr
    global obs_script_addr
    global map_data
    global five_axis
    global five_key
    global Track_number
    file = "main_config.yml"
    if os.path.exists(file):
        # try:
        f = open(file, 'r', encoding='utf-8')
        main_all = yaml.safe_load(f)
        # print(main_all)
        f.close()

        ui.lineEdit_cardNo.setText(main_all['cardNo'])
        ui.lineEdit_CardNo.setText(main_all['cardNo'])
        ui.lineEdit_s485_Axis_No.setText(main_all['s485_Axis_No'])
        ui.lineEdit_s485_Cam_No.setText(main_all['s485_Cam_No'])
        ui.lineEdit_five_axis.setText(str(main_all['five_axis']))
        ui.lineEdit_five_key.setText(str(main_all['five_key']))
        ui.lineEdit_balls_count.setText(main_all['balls_count'])
        ui.lineEdit_balls_auto.setText(main_all['balls_count'])
        ui.lineEdit_wakeup_addr.setText(str(main_all['wakeup_addr']))
        ui.lineEdit_rtsp_url.setText(main_all['rtsp_url'])
        ui.lineEdit_recognition_addr.setText(main_all['recognition_addr'])
        ui.lineEdit_obs_script_addr.setText(main_all['obs_script_addr'])
        ui.lineEdit_TcpServer_Port.setText(main_all['tcpServer_addr'][1])
        ui.lineEdit_result_tcpServer_port.setText(main_all['result_tcpServer_addr'][1])
        ui.lineEdit_UdpServer_Port.setText(main_all['udpServer_addr'][1])
        ui.lineEdit_map_picture.setText(main_all['map_picture'])
        ui.lineEdit_map_size.setText(main_all['map_size'])
        ui.lineEdit_map_line.setText(main_all['map_line'])
        ui.lineEdit_Image_Path.setText(main_all['Image_Path'])
        ui.lineEdit_scene_name.setText(main_all['scene_name'])
        ui.lineEdit_source_ranking.setText(main_all['source_ranking'])
        ui.lineEdit_source_picture.setText(main_all['source_picture'])
        ui.lineEdit_source_settlement.setText(main_all['source_settlement'])
        ui.lineEdit_source_end.setText(main_all['source_end'])
        ui.lineEdit_shoot.setText(main_all['lineEdit_shoot'])
        ui.lineEdit_start.setText(main_all['lineEdit_start'])
        ui.lineEdit_shake.setText(main_all['lineEdit_shake'])
        ui.lineEdit_end.setText(main_all['lineEdit_end'])
        ui.lineEdit_Track_number.setText(main_all['Track_number'])
        ui.pushButton_start_game.setEnabled(main_all['pushButton_start_game'])
        for index in range(1, 4):
            getattr(ui, 'lineEdit_music_%s' % index).setText(main_all['music_%s' % index][1])
            getattr(ui, 'radioButton_music_%s' % index).setChecked(main_all['music_%s' % index][0])
            getattr(ui, 'radioButton_music_background_%s' % index).setChecked(main_all['music_%s' % index][0])
        for index in range(1, 11):
            eng = main_all['init_array'][index - 1][5]
            ch = main_all['color_ch'][eng]
            getattr(ui, 'lineEdit_Color_Eng_%s' % index).setText(eng)
            getattr(ui, 'lineEdit_Color_Ch_%s' % index).setText(ch)
        # 赋值变量
        init_array = main_all['init_array']
        color_ch = main_all['color_ch']
        udpServer_addr = (main_all['udpServer_addr'][0], int(main_all['udpServer_addr'][1]))
        tcpServer_addr = (main_all['tcpServer_addr'][0], int(main_all['tcpServer_addr'][1]))
        result_tcpServer_addr = (main_all['result_tcpServer_addr'][0], int(main_all['result_tcpServer_addr'][1]))
        wakeup_addr = main_all['wakeup_addr']
        balls_count = abs(int(float(main_all['balls_count'])))
        rtsp_url = main_all['rtsp_url']
        recognition_addr = main_all['recognition_addr']
        obs_script_addr = main_all['obs_script_addr']
        s485.s485_Axis_No = main_all['s485_Axis_No']
        s485.s485_Cam_No = main_all['s485_Cam_No']
        map_data = [main_all['map_picture'], main_all['map_line'], main_all['map_size']]
        five_axis = main_all['five_axis']
        five_key = main_all['five_key']
        Track_number = main_all['Track_number']
    # except:
    #     print('初始化出错~！')
    else:
        print("文件不存在")


# 重命名方案
def plan_rename():
    text = ui.lineEdit_rename.text()
    if text != '':
        comb = ui.comboBox_plan
        comb.setItemText(comb.currentIndex(), text)


def sel_all():
    tb_step = ui.tableWidget_Step
    num = tb_step.rowCount()
    for row in range(0, num):
        if ui.checkBox_selectall.isChecked():
            tb_step.cellWidget(row, 0).setChecked(True)
        else:
            tb_step.cellWidget(row, 0).setChecked(False)


def edit_enable():
    tb_step = ui.tableWidget_Step
    if ui.checkBox_test.isChecked():
        tb_step.setEnabled(True)
    else:
        tb_step.setEnabled(False)


def cmd_run():
    save_plan_yaml()
    plan_refresh()
    reset_ranking_array()
    ui.radioButton_test_game.setChecked(True)  # 模拟模式
    auto_shoot()  # 自动上珠
    PlanCmd_Thread.run_flg = True


def cmd_loop():
    ui.radioButton_start_betting.click()  # 开盘
    ReStart_Thread.run_flg = True


# 进入下一步动作
def cmd_next():
    PlanCmd_Thread.cmd_next = True


# 关闭动作循环
def cmd_stop():
    PlanCmd_Thread.run_flg = False  # 停止运动
    ReStart_Thread.run_flg = False  # 停止循环
    Audio_Thread.run_flg = False  # 停止卫星图音效播放线程
    Ai_Thread.run_flg = False  # 停止卫星图AI播放线程
    sc.card_stop()  # 立即停止


def card_start():
    if not CardStart_Thread.isRunning():
        CardStart_Thread.start()


def card_reset():
    Axis_Thread.run_flg = True


def card_close_all():
    if not flg_start['card']:
        return
    for index in range(0, 16):
        sc.GASetExtDoBit(index, 0)
        time.sleep(0.1)
    ui.textBrowser.append(succeed('已经关闭所有机关！'))
    ui.textBrowser_msg.append(succeed('已经关闭所有机关！'))


# 实时轴位置入表
def p_to_table():
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    if row_num > -1:
        for i in range(0, len(pValue)):
            tb_step.item(row_num, i + 2).setText(str(pValue[i]))


def obs_to_table():
    scene = ui.comboBox_Scenes.currentText()
    if scene:
        tb_step = ui.tableWidget_Step
        row_count = tb_step.currentRow()
        col_count = tb_step.columnCount()
        if row_count > -1:
            if tb_step.item(row_count, col_count - 2):
                tb_step.item(row_count, col_count - 2).setText('')
            if tb_step.cellWidget(row_count, col_count - 2):
                tb_step.removeCellWidget(row_count, col_count - 2)
            cb = QRadioButton()
            cb.setText(scene)
            cb.setStyleSheet('QCheckBox{margin:6px};')
            tb_step.setCellWidget(row_count, col_count - 2, cb)
            # print(tb_step.cellWidget(row_num, col_count - 2).text())


def source_to_table():
    sources_row_num = ui.tableWidget_Sources.currentRow()
    if sources_row_num > -1:
        tb_step = ui.tableWidget_Step
        row_count = tb_step.currentRow()
        col_count = tb_step.columnCount()
        if row_count > -1:
            if tb_step.item(row_count, col_count - 2):
                tb_step.item(row_count, col_count - 2).setText('')
            if tb_step.cellWidget(row_count, col_count - 2):
                tb_step.removeCellWidget(row_count, col_count - 2)
            rb = QCheckBox()
            rb.setText(ui.tableWidget_Sources.item(sources_row_num, 1).text())
            rb.setChecked(True)
            rb.setStyleSheet('QCheckBox{margin:6px};')
            tb_step.setCellWidget(row_count, col_count - 2, rb)
            # print(tb_step.cellWidget(row_num, col_count - 2).text())


def obs_remove_table():
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    col_count = tb_step.columnCount()
    if row_num > -1 and tb_step.cellWidget(row_num, col_count - 2):
        tb_step.removeCellWidget(row_num, col_count - 2)


# 禁止输入非数字
def table_change():
    global plan_list
    tb_step = ui.tableWidget_Step
    col_count = tb_step.columnCount()
    row = tb_step.currentRow()
    col = tb_step.currentColumn()
    # print("%s %s" % (row, col))
    if col in [0, 7, col_count - 2] or row < 0 or col < 0:
        return
    try:
        # print(len(plan_list[row]), col)
        if col > len(plan_list[row]) - 1:
            if tb_step.item(row, col):
                tb_step.item(row, col).setText('')
        elif not is_natural_num(tb_step.item(row, col).text()):
            if tb_step.item(row, col):
                tb_step.item(row, col).setText(plan_list[row][col][0])
    except:
        print("数据表操作出错！")


def wakeup_server():
    global flg_start
    form_data = {
        'requestType': 'set_run_toggle',
        'run_toggle': '1',
    }
    while True:
        try:
            for index in range(len(wakeup_addr)):
                r = requests.post(url=wakeup_addr[index], data=form_data)
                print(r.text)
                if r == 'ok':
                    flg_start['ai'] = True
        except:
            print('图像识别主机通信失败！')
            flg_start['ai'] = False
        time.sleep(300)


def stop_server():  # 关闭识别服务器
    global flg_start
    form_data = {
        'requestType': 'set_run_toggle',
        'run_toggle': '0',
    }
    try:
        cmd_stop()
        for index in range(len(wakeup_addr)):
            r = requests.post(url=wakeup_addr[index], data=form_data)
            print(r.text)
            if r == 'ok':
                flg_start['ai'] = False
    except:
        print('图像识别主机通信失败！')
        flg_start['ai'] = False


def save_images():
    if ui.checkBox_saveImgs.isChecked():
        saveImgRun = 1  # 1 录图开启标志
    else:
        saveImgRun = 0  # 1 录图关闭标志
    if ui.radioButton_ball.isChecked():
        saveBackground = 0  # 0 有球录图标志
    else:
        saveBackground = 1  # 0 无球录图标志
    form_data = {
        'saveImgRun': saveImgRun,
        'saveBackground': saveBackground,
        'saveImgNum': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
        # 'saveImgNum': '1',
        # 'saveImgPath': 'D:/saidao',
    }
    try:
        for index in range(len(wakeup_addr)):
            r = requests.post(url=wakeup_addr[index], data=form_data)
            print(r.text)
    except:
        print('图像识别主机通信失败！')


def json_txt():
    if json_to_txt():
        ui.textBrowser_background_data.append(succeed('区域文件转TXT成功！'))
    else:
        ui.textBrowser_background_data.append(fail('区域文件转TXT失败！'))


"****************************************卫星图_开始***********************************************"


class DraggableLabel(QLabel):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        # self.setFixedSize(150, 70)  # 设置标签大小
        self.color = color
        # 设置字体样式
        font = QFont("Arial", 24, QFont.Bold)  # 字体：Arial，大小：16，加粗
        font.setItalic(False)  # 设置斜体
        self.setFont(font)

        # 设置背景和边框样式
        self.setStyleSheet(
            "color: %s;" % color  # 字体颜色为红色
        )
        self.dragging = False
        self.start_pos = QPoint(0, 0)
        self.label_text = text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            # 使用 position().toPoint() 获取点击位置
            self.start_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging:
            # 计算新位置：将事件位置映射到父控件坐标系
            parent_pos = self.mapToParent(event.position().toPoint() - self.start_pos)
            self.move(parent_pos)
            # print("内部坐标：", self.pos())

    def mouseReleaseEvent(self, event):
        global camera_points
        global audio_points
        global ai_points
        if event.button() == Qt.LeftButton:
            self.dragging = False
            # 打印标签相对于父控件的内部坐标
            x = self.pos().x() + self.width() / 2
            y = self.pos().y() + self.height() / 2
            area_part = 0
            for index in range(len(map_orbit)):
                if abs(map_orbit[index][0] - x) < 10 and abs(map_orbit[index][1] - y) < 10:
                    if self.color == 'red':
                        area_part = index
                    else:
                        part = len(map_orbit) / (max_area_count - balls_count + 1)
                        area_part = index // part
                    x = int(map_orbit[index][0])
                    y = int(map_orbit[index][1])
                    self.move(int(x - self.width() / 2), int(y - self.height() / 2))
                    break
            num = ui.comboBox_plan.currentIndex() + 1  # 按方案索引保存
            if self.color == 'red':
                camera_points[int(self.label_text)][num][0] = [int(area_part)]
                camera_points[int(self.label_text)][num][1] = [int(x - self.width() / 2), int(y - self.height() / 2)]
            if self.color == 'blue':
                audio_points[int(self.label_text)][num][0] = [int(area_part)]
                audio_points[int(self.label_text)][num][1] = [int(x - self.width() / 2), int(y - self.height() / 2)]
            if self.color == 'green':
                ai_points[int(self.label_text)][num][0] = [int(area_part)]
                ai_points[int(self.label_text)][num][1] = [int(x - self.width() / 2), int(y - self.height() / 2)]
            save_points(self.color)
            print("内部坐标：", [int(x - self.width() / 2), int(y - self.height() / 2)])

    def delete_self(self):
        """从父控件中删除自己"""
        print(f"删除：{self.text()}")
        self.setParent(None)  # 解除父控件引用
        self.deleteLater()  # 安排删除自身


class MapLabel(QLabel):
    def __init__(self, picture_size=860, ball_space=11, ball_radius=10, flash_time=30, step_length=2, parent=None):
        super().__init__(parent)
        global map_orbit
        self.map_action = 0  # 地图触发点位
        img = map_data[0]
        pixmap = QPixmap(img)
        self.picture_size = picture_size
        # 设置label的尺寸
        self.setMaximumSize(picture_size, picture_size)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

        self.color_names = {'red': QColor(255, 0, 0), 'green': QColor(0, 255, 0), 'blue': QColor(0, 0, 255),
                            'pink': QColor(255, 0, 255), 'yellow': QColor(255, 255, 0), 'black': QColor(0, 0, 0),
                            'purple': QColor(128, 0, 128), 'orange': QColor(255, 165, 0)
            , 'White': QColor(248, 248, 255),
                            'Brown': QColor(139, 69, 19)}

        self.path_points = []
        with open(map_data[1], 'r', encoding='utf-8') as fcc_file:
            fcc_data = json.load(fcc_file)
        if picture_size == 860:
            map_scale = 1
        else:
            map_scale = picture_size / int(map_data[2])  # 缩放比例
        for p in fcc_data[0]["content"]:
            self.path_points.append((p['x'] * map_scale, p['y'] * map_scale))
        self.path_points = divide_path(self.path_points, step_length)
        if map_scale == 1:
            map_orbit = self.path_points

        self.ball_space = ball_space  # 球之间的距离
        self.ball_radius = ball_radius  # 小球半径
        # self.num_balls = 8  # 8个小球
        self.speed = 1  # 小球每次前进的步数（可以根据需要调整）
        self.flash_time = flash_time
        self.positions = []  # 每个球的当前位置索引
        for num in range(balls_count):
            self.positions.append([num * self.ball_space, QColor(255, 0, 0), 0])

        # 创建定时器，用于定时更新球的位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)  # 定时触发更新
        self.timer.start(self.flash_time)  # 每1秒更新一次

    def update_positions(self):
        # 更新每个小球的位置
        p_num = 0
        for num in range(0, balls_count):
            if ranking_array[num][5] in self.color_names.keys():
                color = self.color_names[ranking_array[num][5]]
                if ranking_array[num][6] == 0:  # 起点
                    if p_num == 0:
                        index = len(ranking_array) * self.ball_space
                    else:
                        index = len(ranking_array) * self.ball_space - p_num * self.ball_space
                elif (ranking_array[num][6] >= max_area_count - balls_count + 1
                      and ranking_array[num][8] >= max_lap_count - 1):  # 最后一圈处理
                    if p_num == 0:
                        index = len(self.path_points) - 1
                    else:
                        index = len(self.path_points) - 1 - p_num * self.ball_space
                elif ranking_array[num][8] == action_area[1]:  # 同圈才运动
                    area_num = max_area_count - balls_count  # 跟踪区域数量
                    p = int(len(self.path_points) * (ranking_array[num][6] / area_num)) - 1
                    color = self.color_names[ranking_array[num][5]]
                    if p - self.positions[p_num][0] > 50:
                        self.speed = 3
                    elif 30 >= p - self.positions[p_num][0] >= 25:
                        self.speed = 2
                    elif p < self.positions[p_num][0]:
                        self.speed = 0
                    else:
                        self.speed = 1
                    if self.positions[p_num][0] > len(self.path_points) - self.ball_radius - 1:
                        index = 0
                    elif p_num == 0:
                        index = self.positions[p_num][0] + self.speed
                    elif (0 < self.positions[p_num - 1][0] - self.positions[p_num][0] < self.ball_space
                          and int(len(self.path_points) * (5 / area_num)) < self.positions[p_num][0] < len(
                                self.path_points) - self.ball_space):
                        index = self.positions[p_num][0] - self.ball_radius
                    else:
                        index = self.positions[p_num][0] + self.speed
                else:  # 不同圈情况
                    area_num = max_area_count - balls_count  # 跟踪区域数量
                    p = int(len(self.path_points) * (ranking_array[num][6] / area_num)) - 1
                    color = self.color_names[ranking_array[num][5]]
                    if p - self.positions[p_num][0] > 50:
                        self.speed = 3
                    elif 30 >= p - self.positions[p_num][0] >= 25:
                        self.speed = 2
                    elif p < self.positions[p_num][0]:
                        self.speed = 0
                    else:
                        self.speed = 1
                    index = self.positions[p_num][0] + self.speed
                    if index > len(self.path_points) - self.ball_radius - 1:
                        index = len(self.path_points) - 1
                self.positions[p_num][0] = index
                self.positions[p_num][1] = color
                for color_index in range(len(init_array)):
                    if init_array[color_index][5] == ranking_array[num][5]:
                        self.positions[p_num][2] = color_index + 1
                        break
                # if index >= len(self.path_points):
                #     self.positions[p_num][0] = 0  # 回到起点循环运动
                p_num += 1
        if self.positions[0][0] - self.map_action < 300:
            self.map_action = self.positions[0][0]  # 赋值实时位置
        # 触发重绘
        self.update()

    # 通过重载paintEvent方法进行自定义绘制
    def paintEvent(self, event):
        # 调用父类的 paintEvent 以确保 QLabel 正常显示文本或图片
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if ui.checkBox_show_orbit.isChecked():  # 绘制路径
            for index in range(len(self.path_points)):
                part = len(self.path_points) / (max_area_count - balls_count + 1)
                if index % int(part) == 0:
                    painter.setBrush(QBrush(QColor(255, 0, 0), Qt.SolidPattern))
                    font = QFont("Arial", 12, QFont.Bold)  # 字体：Arial，大小：16，加粗
                    painter.setFont(font)
                    painter.setPen('green')
                    painter.drawText(int(self.path_points[index][0]), int(self.path_points[index][1]),
                                     str(index // int(part)))
                    painter.drawEllipse(int(self.path_points[index][0]), int(self.path_points[index][1]),
                                        10, 10)
                else:
                    painter.setBrush(QBrush(QColor(0, 255, 0), Qt.SolidPattern))
                    painter.drawEllipse(int(self.path_points[index][0]), int(self.path_points[index][1]),
                                        2, 2)

        # 绘制每个小球
        for index_position in range(len(self.positions)):
            index = self.positions[index_position][0]  # 获取当前球的路径索引
            if index in range(len(self.path_points)):
                x, y = self.path_points[index]
                # 设置球的颜色
                painter.setBrush(QBrush(self.positions[index_position][1], Qt.SolidPattern))
                # 绘制球
                painter.drawEllipse(int(x - self.ball_radius), int(y - self.ball_radius),
                                    self.ball_radius * 2, self.ball_radius * 2)
                if self.picture_size == 860:
                    if str(self.positions[index_position][2]) == '1':
                        font = QFont("Arial", 12, QFont.Bold)  # 字体：Arial，大小：16，加粗
                        painter.setFont(font)
                        painter.setPen('gray')
                        painter.drawText(int(x - self.ball_radius / 2), int(y + self.ball_radius / 2),
                                         str(self.positions[index_position][2]))
                    elif str(self.positions[index_position][2]) == '10':
                        font = QFont("Arial", 11, QFont.Bold)  # 字体：Arial，大小：16，加粗
                        painter.setFont(font)
                        painter.setPen('black')
                        painter.drawText(int(x - self.ball_radius / 2 - 4), int(y + self.ball_radius / 2),
                                         str(self.positions[index_position][2]))
                    else:
                        font = QFont("Arial", 12, QFont.Bold)  # 字体：Arial，大小：16，加粗
                        painter.setFont(font)
                        painter.setPen('white')
                        painter.drawText(int(x - self.ball_radius / 2), int(y + self.ball_radius / 2),
                                         str(self.positions[index_position][2]))

    def mouseReleaseEvent(self, event: QMouseEvent):
        """释放鼠标时停止拖动"""
        if event.button() == Qt.LeftButton:
            print(event.position().toPoint())


def save_points(color):
    points_save = []
    table_save = []
    if color == 'red':
        file = "camera_points.yml"
        for index in range(len(camera_points)):
            points_save.append([index, [(camera_points[index][1][0]), (camera_points[index][1][1])],
                                [(camera_points[index][2][0]), (camera_points[index][2][1])],
                                [(camera_points[index][3][0]), (camera_points[index][3][1])]])
    elif color == 'blue':
        file = "audio_points.yml"
        for index in range(len(audio_points)):
            points_save.append([index, [(audio_points[index][1][0]), (audio_points[index][1][1])],
                                [(audio_points[index][2][0]), (audio_points[index][2][1])],
                                [(audio_points[index][3][0]), (audio_points[index][3][1])]])
        tb_audio = ui.tableWidget_Audio
        row_count = tb_audio.rowCount()
        col_count = tb_audio.columnCount()
        for row in range(row_count):
            row_data = []
            for col in range(col_count - 1):
                if tb_audio.item(row, col).text() == '':
                    tb_audio.item(row, col).setText('0')
                row_data.append(tb_audio.item(row, col).text())
            table_save.append(row_data)
    elif color == 'green':
        file = "ai_points.yml"
        for index in range(len(ai_points)):
            points_save.append([index, [(ai_points[index][1][0]), (ai_points[index][1][1])],
                                [(ai_points[index][2][0]), (ai_points[index][2][1])],
                                [(ai_points[index][3][0]), (ai_points[index][3][1])]])
        tb_ai = ui.tableWidget_Ai
        row_count = tb_ai.rowCount()
        col_count = tb_ai.columnCount()
        for row in range(row_count):
            row_data = []
            for col in range(col_count - 1):
                if tb_ai.item(row, col).text() == '':
                    tb_ai.item(row, col).setText('0')
                row_data.append(tb_ai.item(row, col).text())
            table_save.append(row_data)
    else:
        return
    if os.path.exists(file):
        try:
            with open(file, "w", encoding="utf-8") as f:
                if color == 'red':
                    yaml.dump({'camera_points': points_save}, f, allow_unicode=True)
                elif color == 'blue':
                    yaml.dump({'audio_points': points_save, 'audio_table': table_save}, f, allow_unicode=True)
                elif color == 'green':
                    yaml.dump({'ai_points': points_save, 'ai_table': table_save}, f, allow_unicode=True)
            f.close()
            ui.textBrowser.append(succeed('%s点位保存：成功' % color))
        except:
            ui.textBrowser.append(fail('%s点位保存：失败' % color))
        print("保存成功~！")


def load_points_yaml(color):
    global camera_points
    global audio_points
    global ai_points
    if color == 'red':
        file = "camera_points.yml"
    elif color == 'blue':
        file = "audio_points.yml"
    elif color == 'green':
        file = "ai_points.yml"
    else:
        return
    # file = "camera_points.yml"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            points_all = yaml.safe_load(f)
            f.close()
            if color == 'red':
                camera_points = points_all['camera_points']
                for index in range(len(camera_points)):
                    camera_points[index][0] = DraggableLabel(str(index), color, map_label_big)
                    num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
                    camera_points[index][0].move(*camera_points[index][num][1])  # 设置初始位置
                    camera_points[index][0].show()
            if color == 'blue':
                audio_points = points_all['audio_points']
                for index in range(len(audio_points)):
                    audio_points[index][0] = DraggableLabel(str(index), color, map_label_big)
                    num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
                    audio_points[index][0].move(*audio_points[index][num][1])  # 设置初始位置
                    audio_points[index][0].show()
                audio_table = points_all['audio_table']
                tb_audio = ui.tableWidget_Audio
                tb_audio.setRowCount(len(audio_table))
                row_count = tb_audio.rowCount()
                col_count = tb_audio.columnCount()
                for row in range(row_count):
                    for col in range(col_count - 1):
                        audio_item = QTableWidgetItem(str(audio_table[row][col]))
                        audio_item.setTextAlignment(Qt.AlignCenter)
                        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                        tb_audio.setItem(row, col, audio_item)
                    btn = QPushButton("选择文件")
                    btn.clicked.connect(lambda _, r=row: open_file_dialog(tb_audio, r))  # 传递行号
                    tb_audio.setCellWidget(row, col_count - 1, btn)

            if color == 'green':
                ai_points = points_all['ai_points']
                for index in range(len(ai_points)):
                    ai_points[index][0] = DraggableLabel(str(index), color, map_label_big)
                    num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
                    ai_points[index][0].move(*ai_points[index][num][1])  # 设置初始位置
                    ai_points[index][0].show()
                ai_table = points_all['ai_table']
                tb_ai = ui.tableWidget_Ai
                tb_ai.setRowCount(len(ai_table))
                row_count = tb_ai.rowCount()
                col_count = tb_ai.columnCount()
                for row in range(row_count):
                    for col in range(col_count - 1):
                        ai_item = QTableWidgetItem(str(ai_table[row][col]))
                        ai_item.setTextAlignment(Qt.AlignCenter)
                        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                        tb_ai.setItem(row, col, ai_item)
                    btn = QPushButton("选择文件")
                    btn.clicked.connect(lambda _, r=row: open_file_dialog(tb_ai, r))  # 传递行号
                    tb_ai.setCellWidget(row, col_count - 1, btn)
        except:
            pass
    else:
        print("文件不存在")


def open_file_dialog(tb, r):
    # 打开文件选择对话框
    file_path, _ = QFileDialog.getOpenFileName(tb, "选择文件")
    if file_path:
        # 更新对应行的文件路径
        tb.item(r, 0).setText(file_path)


def add_camera_points():
    global camera_points
    # 加载图标并放置在窗口中心
    camera_points_count = len(camera_points)
    num = ui.comboBox_plan.currentIndex() + 1
    if num == 1:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [0, [camera_points_count * 20, 0]], [0, [0, 0]], [0, [0, 0]]])
    if num == 2:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [0, [0, 0]], [0, [camera_points_count * 20, 0]], [0, [0, 0]]])
    if num == 3:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [0, [0, 0]], [0, [0, 0]], [0, [camera_points_count * 20, 0]]])
    camera_points[camera_points_count][0].move(*camera_points[camera_points_count][num][1])  # 设置初始位置
    camera_points[camera_points_count][0].show()


def add_audio_points():
    global audio_points
    # 加载图标并放置在窗口中心
    audio_points_count = len(audio_points)
    num = ui.comboBox_plan.currentIndex() + 1
    if num == 1:
        audio_points.append(
            [DraggableLabel(str(audio_points_count), 'blue', map_label_big),
             [0, [audio_points_count * 20, 0]], [0, [0, 0]], [0, [0, 0]]])
    if num == 2:
        audio_points.append(
            [DraggableLabel(str(audio_points_count), 'blue', map_label_big),
             [0, [0, 0]], [0, [audio_points_count * 20, 0]], [0, [0, 0]]])
    if num == 3:
        audio_points.append(
            [DraggableLabel(str(audio_points_count), 'blue', map_label_big),
             [0, [0, 0]], [0, [0, 0]], [0, [audio_points_count * 20, 0]]])
    audio_points[audio_points_count][0].move(*audio_points[audio_points_count][num][1])  # 设置初始位置
    audio_points[audio_points_count][0].show()

    audio_points_count = len(audio_points) - 1  # 不要0号，所以少一行
    tb = ui.tableWidget_Audio
    tb.setRowCount(audio_points_count)
    row_count = tb.rowCount() - 1
    col_count = tb.columnCount()
    for col in range(col_count - 1):
        audio_item = QTableWidgetItem('0')
        audio_item.setTextAlignment(Qt.AlignCenter)
        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
        tb.setItem(row_count, col, audio_item)
    btn = QPushButton("选择文件")
    btn.clicked.connect(lambda _, r=row_count: open_file_dialog(tb, r))  # 传递行号
    tb.setCellWidget(row_count, col_count - 1, btn)


def add_ai_points():
    global ai_points
    # 加载图标并放置在窗口中心
    ai_points_count = len(ai_points)
    num = ui.comboBox_plan.currentIndex() + 1
    if num == 1:
        ai_points.append(
            [DraggableLabel(str(ai_points_count), 'green', map_label_big),
             [0, [ai_points_count * 20, 0]], [0, [0, 0]], [0, [0, 0]]])
    if num == 2:
        ai_points.append(
            [DraggableLabel(str(ai_points_count), 'green', map_label_big),
             [0, [0, 0]], [0, [ai_points_count * 20, 0]], [0, [0, 0]]])
    if num == 3:
        ai_points.append(
            [DraggableLabel(str(ai_points_count), 'green', map_label_big),
             [0, [0, 0]], [0, [0, 0]], [0, [ai_points_count * 20, 0]]])
    ai_points[ai_points_count][0].move(*ai_points[ai_points_count][num][1])  # 设置初始位置
    ai_points[ai_points_count][0].show()

    ai_points_count = len(ai_points) - 1
    tb = ui.tableWidget_Ai
    tb.setRowCount(ai_points_count)
    row_count = tb.rowCount() - 1
    col_count = tb.columnCount()
    for col in range(col_count - 1):
        ai_item = QTableWidgetItem('0')
        ai_item.setTextAlignment(Qt.AlignCenter)
        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
        tb.setItem(row_count, col, ai_item)
    btn = QPushButton("选择文件")
    btn.clicked.connect(lambda _, r=row_count: open_file_dialog(tb, r))  # 传递行号
    tb.setCellWidget(row_count, col_count - 1, btn)


def del_camera_points():
    global camera_points
    camera_points_count = len(camera_points) - 1
    num = ui.comboBox_plan.currentIndex() + 1
    if camera_points_count > 0:
        for index in range(1, len(camera_points[camera_points_count])):
            if num != index and camera_points[camera_points_count][index][0] != 0:  # 如果其中有一个方案存在坐标，则不删
                print('存在非空方案！')
                res = QMessageBox.warning(z_window, '提示', '其他方案存在该点位！是否强制删除？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                print(res)
                if res == QMessageBox.No:
                    return
        camera_points[camera_points_count][0].delete_self()
        camera_points.pop(camera_points_count)


def del_audio_points():
    global audio_points
    audio_points_count = len(audio_points) - 1
    num = ui.comboBox_plan.currentIndex() + 1
    if audio_points_count > 0:
        for index in range(1, len(audio_points[audio_points_count])):
            if num != index and audio_points[audio_points_count][index][0] != 0:  # 如果其中有一个方案存在坐标，则不删
                print('存在非空方案！')
                res = QMessageBox.warning(z_window, '提示', '其他方案存在该点位！是否强制删除？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                print(res)
                if res == QMessageBox.No:
                    return
        audio_points[audio_points_count][0].delete_self()
        audio_points.pop(audio_points_count)
    audio_points_count = len(audio_points) - 1
    if audio_points_count >= 0:
        tb = ui.tableWidget_Audio
        tb.setRowCount(audio_points_count)


def del_ai_points():
    global ai_points
    ai_points_count = len(ai_points) - 1
    num = ui.comboBox_plan.currentIndex() + 1
    if ai_points_count > 0:
        for index in range(1, len(ai_points[ai_points_count])):
            if num != index and ai_points[ai_points_count][index][0] != 0:  # 如果其中有一个方案存在坐标，则不删
                print('存在非空方案！')
                res = QMessageBox.warning(z_window, '提示', '其他方案存在该点位！是否强制删除？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                print(res)
                if res == QMessageBox.No:
                    return
        ai_points[ai_points_count][0].delete_self()
        ai_points.pop(ai_points_count)
    ai_points_count = len(ai_points) - 1
    if ai_points_count >= 0:
        tb = ui.tableWidget_Ai
        tb.setRowCount(ai_points_count)


def show_points(color):
    if color == 'red':
        if ui.checkBox_show_camera.isChecked():
            for index in range(len(camera_points)):
                camera_points[index][0].show()
        else:
            for index in range(len(camera_points)):
                camera_points[index][0].hide()
    if color == 'blue':
        if ui.checkBox_show_audio.isChecked():
            for index in range(len(audio_points)):
                audio_points[index][0].show()
        else:
            for index in range(len(audio_points)):
                audio_points[index][0].hide()
    if color == 'green':
        if ui.checkBox_show_ai.isChecked():
            for index in range(len(ai_points)):
                ai_points[index][0].show()
        else:
            for index in range(len(ai_points)):
                ai_points[index][0].hide()


class AudioThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(AudioThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        area_old = 0
        while self.running:
            time.sleep(0.2)
            if not self.run_flg:
                continue
            if len(audio_points) <= 1:
                continue
            plan_index = ui.comboBox_plan.currentIndex() + 1  # 方案索引
            for index in range(1, len(audio_points)):
                # print(audio_points[index][plan_index][0])
                if (audio_points[index][plan_index][0][0] > 0
                        and (area_old != action_area)
                        and (audio_points[index][plan_index][0][0] == action_area[0])):
                    tb_audio = ui.tableWidget_Audio
                    sound_file = tb_audio.item(index - 1, 0).text()
                    sound_times = int(tb_audio.item(index - 1, 1).text())
                    sound_delay = int(tb_audio.item(index - 1, 2).text())
                    print(sound_file, sound_times, sound_delay)
                    # 加载音效
                    sound_effect = pygame.mixer.Sound(sound_file)
                    sound_effect.play(loops=sound_times, maxtime=sound_delay * 1000)  # 播放音效
                    area_old = copy.deepcopy(action_area)
                    print('Audio~~~~~~~~~~~~~', area_old, audio_points[index][plan_index][0][0], action_area[0])
                    break


def audio_signal_accept(msg):
    try:
        print(msg)
    except:
        print("轴数据显示错误！")


class AiThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(AiThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        area_old = 0
        while self.running:
            time.sleep(0.2)
            if not self.run_flg:
                continue
            if len(ai_points) <= 1:
                continue
            plan_index = ui.comboBox_plan.currentIndex() + 1  # 方案索引
            for index in range(1, len(ai_points)):
                # print(ai_points[index][plan_index][0][0])
                if (ai_points[index][plan_index][0][0] > 0
                        and (area_old != action_area)
                        and (ai_points[index][plan_index][0][0] == action_area[0])):
                    tb_ai = ui.tableWidget_Ai
                    sound_file = tb_ai.item(index - 1, 0).text()
                    sound_times = int(tb_ai.item(index - 1, 1).text())
                    sound_delay = int(tb_ai.item(index - 1, 2).text())
                    print(sound_file, sound_times, sound_delay)
                    # 加载音效
                    sound_effect = pygame.mixer.Sound(sound_file)
                    sound_effect.play(loops=sound_times, maxtime=sound_delay * 1000)  # 播放音效
                    area_old = copy.deepcopy(action_area)
                    print('Ai~~~~~~~~~~~~~', area_old, ai_points[index][plan_index][0][0], action_area[0])
                    break


def ai_signal_accept(msg):
    try:
        print(msg)
    except:
        print("轴数据显示错误！")


def music_ctl():
    if ui.checkBox_main_music.isChecked():
        for index in range(1, 4):
            if getattr(ui, 'radioButton_music_%s' % index).isChecked():
                mp3_name = getattr(ui, 'lineEdit_music_%s' % index).text()
                # 加载并播放背景音乐
                pygame.mixer.music.load(mp3_name)
                pygame.mixer.music.play(-1)  # 循环播放背景音乐
                break
    else:
        pygame.mixer.music.stop()


def play_audio():
    pass


"****************************************卫星图_结束***********************************************"

"****************************************摄像头识别结果_开始***********************************************"


class CameraLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Camera_index = 'main_Camera'
        self.img_data = []  # 图资料
        for num in range(0, 10):
            self.img_data.append('./img/ball/%s.png' % str(num + 1))
        self.images = [QPixmap(img) for img in self.img_data]
        self.fit_images = [QPixmap('./img/ball/No.png'), QPixmap('./img/ball/Yes.png')]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)  # 定时触发更新
        self.timer.start(1000)  # 每1秒更新一次

    def update_positions(self):
        # 触发重绘
        self.update()

    # 通过重载paintEvent方法进行自定义绘制
    def paintEvent(self, event):
        # 调用父类的 paintEvent 以确保 QLabel 正常显示文本或图片
        super().paintEvent(event)

        """绘制并排显示的图片"""
        painter = QPainter(self)

        # 当前 x 轴绘制位置
        x_offset = 0
        x_space = 2

        # 逐个绘制图片
        for index in range(8):
            ball_radius = 23
            rect = QRect(x_offset, 0, ball_radius, ball_radius)
            # 使用高质量的缩放方式
            if self.Camera_index == 'main_Camera':
                scaled_img = self.images[main_Camera[index] - 1].scaled(rect.size(), Qt.KeepAspectRatio,
                                                                        Qt.SmoothTransformation)
            elif self.Camera_index == 'monitor_Camera':
                scaled_img = self.images[monitor_Camera[index] - 1].scaled(rect.size(), Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation)
            else:
                scaled_img = self.fit_images[fit_Camera[index]].scaled(rect.size(), Qt.KeepAspectRatio,
                                                                       Qt.SmoothTransformation)
            painter.drawPixmap(rect, scaled_img)  # 在 (x_offset, 50) 位置绘制图片
            x_offset += ball_radius + x_space  # 更新下一个图片的 x_offset

    # 重写鼠标按下事件处理函数
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("QLabel 被左键点击")
            if self.Camera_index == 'main_Camera':
                ui.lineEdit_result_send.setText(str(main_Camera))
                ui.lineEdit_Send_Result.setText(str(main_Camera))
            elif self.Camera_index == 'monitor_Camera':
                ui.lineEdit_result_send.setText(str(monitor_Camera))
                ui.lineEdit_Send_Result.setText(str(monitor_Camera))
        elif event.button() == Qt.RightButton:
            print("QLabel 被右键点击")


"****************************************摄像头识别结果_结束***********************************************"

"****************************************直播大厅_开始****************************************************"


def lottery_sql_init():
    global lottery_term
    try:
        conn = create_connection("127.0.0.1", "root", "root", "lottery")
        if conn:
            timestamp = time.time()
            local_time = time.localtime(timestamp)
            start_time = time.strftime("%Y-%m-%d 00:00:00", local_time)
            end_time = time.strftime("%Y-%m-%d 23:59:59", local_time)

            select_query = "SELECT * FROM lottery WHERE date BETWEEN %s AND %s"
            res = fetch_query(conn, select_query, [start_time, end_time])
            # print("Query Results:", type(res), res)
            conn.close()
            # for row in range(len(res) - 1, -1, -1):
            for row in range(len(res)):
                for col in range(len(res[row])):
                    lottery_term[col] = res[row][col]
                # print(lottery_term)
                lottery_data2table()
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def lottery_yaml_init():
    file = "./lottery_data.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        lottery_all = yaml.safe_load(f)
        f.close()
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        lottery_list = lottery_all['lottery_list']
        for row in range(len(lottery_list)):
            if time.strftime("%Y-%m-%d", time.localtime(int(lottery_list[row][8]))) == current_date:
                for col in range(len(lottery_list[row])):
                    lottery_term[col] = lottery_list[row][col]
                lottery_data2table()


def lottery2yaml():
    file = "./lottery_data.yml"
    if os.path.exists(file):
        # try:
        f = open(file, 'r', encoding='utf-8')
        lottery_all = yaml.safe_load(f)
        f.close()
        lottery_list = lottery_all['lottery_list']
        current_date = time.time()
        list_temp = []
        for index in range(len(lottery_list)):
            if int(lottery_list[index][8]) > current_date - 604800:
                list_temp.append(copy.deepcopy(lottery_list[index]))
        list_temp.append(lottery_term)
        lottery_all['lottery_date'] = current_date
        lottery_all['lottery_list'] = copy.deepcopy(list_temp)
        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(lottery_all, f, allow_unicode=True)
        f.close()


def lottery2sql():  # 保存数据库
    global lottery_term
    try:
        conn = create_connection("127.0.0.1", "root", "root", "lottery")
        if conn:
            insert_query = ("INSERT INTO lottery (term, start_time, count, status, auto_result,"
                            " confirmation_result, picture_path, video_path, date) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            execute_query(conn, insert_query, [lottery_term[0], lottery_term[1]
                , lottery_term[2], lottery_term[3], lottery_term[4]
                , lottery_term[5], lottery_term[6], lottery_term[7]
                , lottery_term[8]])
            conn.close()
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def get_lottery_term():  # 创建开奖记录
    global lottery_term
    global flg_start
    try:
        lottery_term[0] = term
        local_time = time.localtime(betting_start_time)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        lottery_term[1] = start_time
        lottery_term[2] = '0'
        lottery_term[3] = '未开始'  # 新一期比赛的状态（2.未开始）
        lottery_term[4] = ''
        lottery_term[5] = ''
        lottery_term[6] = ''
        lottery_term[7] = ''
        lottery_term[8] = ''
        flg_start['server'] = True
        return True
    except:
        print('分机链接错误！')
        flg_start['server'] = False
        return False


def lottery_data2table():  # 赛事入表
    global labels
    global lottery_term
    tb_result = ui.tableWidget_Results
    row_count = tb_result.rowCount()
    col_count = tb_result.columnCount()
    tb_result.setRowCount(row_count + 1)

    labels.insert(0, str(lottery_term[0]))
    tb_result.setVerticalHeaderLabels(labels)
    tb_result.verticalHeaderItem(len(labels) - 1).setTextAlignment(Qt.AlignCenter)

    for col in range(0, col_count):
        item = QTableWidgetItem('')
        item.setTextAlignment(Qt.AlignCenter)
        tb_result.setItem(row_count, col, item)
    if row_count > 0:  # 下移表格
        for row in range(row_count, 0, -1):
            for col in range(0, col_count):
                tb_result.item(row, col).setText(tb_result.item(row - 1, col).text())
    for index, value in enumerate(lottery_term):
        tb_result.item(0, index).setText(str(value))


"""
    运动卡开启线程
"""


class CardStartThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(CardStartThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global flg_start
        cardnum = ui.lineEdit_CardNo.text()
        if cardnum.isdigit() and not (flg_start['card']):
            res = sc.card_open(int(cardnum))
            print(res)
            if res == 0:
                self._signal.emit(succeed('启动板卡：%s' % card_res[res]))
            else:
                self._signal.emit(fail('板卡链接失败：%s' % card_res[res]))
        else:
            self._signal.emit(fail('运动卡已链接~！'))

        if not flg_start['s485']:
            flg_start['s485'] = s485.cam_open()
            if flg_start['s485']:
                Axis_Thread.run_flg = True  # 轴复位
            self._signal.emit(succeed('串口链接：%s' % flg_start['s485']))
        else:
            self._signal.emit(fail('串口链接：%s' % flg_start['s485']))
        if not flg_start['obs']:
            if not Obs_Thread.isRunning():
                Obs_Thread.start()
        if not flg_start['ai']:
            try:
                for index in range(len(wakeup_addr)):
                    res = requests.get(wakeup_addr[index])
                    if res.text == 'ok':
                        flg_start['ai'] = True
            except:
                flg_start['ai'] = False


def CardStart_signal_accept(msg):
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)


"""
    状态测试线程
"""


class TestStatusThread(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TestStatusThread, self).__init__()
        self.run_flg = True
        self.obs_name = ui.lineEdit_source_end.text()
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global flg_start
        global axis_reset
        while self.running:
            if not self.run_flg:
                continue
            cardnum = ui.lineEdit_CardNo.text()
            if cardnum.isdigit() and not (flg_start['card']):
                res = sc.card_open(int(cardnum))
                print(res)
                if res == 0:
                    flg_start['card'] = True
                    if axis_reset and flg_start['card']:  # 轴复位一次
                        Axis_Thread.run_flg = True
                        res_sql = query_sql()  # 加载网络设置 一次
                        self._signal.emit(res_sql)
                        axis_reset = False

            if not flg_start['ai_end']:  # 测试结果识别服务
                test_ai_end()
            else:
                time.sleep(3)

            if not flg_start['server']:  # 测试期号服务器
                try:
                    if test_server(Track_number):
                        flg_start['server'] = True
                    else:
                        flg_start['server'] = False
                except:
                    flg_start['server'] = False

            if not flg_start['s485']:
                flg_start['s485'] = s485.cam_open()

            if not flg_start['obs']:
                if not Obs_Thread.isRunning():
                    Obs_Thread.start()

            if not flg_start['ai']:  # 识别服务器
                try:
                    for index in range(len(wakeup_addr)):
                        res = requests.get(wakeup_addr[index])
                        if res.text == 'ok':
                            flg_start['ai'] = True
                except:
                    flg_start['ai'] = False

            self._signal.emit('标志')


def test_status_signal_accept(msg):
    if isinstance(msg, dict):
        tb_msg = ui.textBrowser_total_msg
        for k in msg:
            tb_msg.append('%s: %s' % (k, msg[k]))
        if "赛道名称" in msg.keys():
            z_window.setWindowTitle(msg["赛道名称"])
        else:
            z_window.setWindowTitle(ui.lineEdit_map_picture.text()[6: -5])
    else:
        for flg in flg_start.keys():
            if flg_start[flg]:
                if getattr(ui, 'status_%s' % flg).styleSheet() != 'background:rgb(0, 255, 0)':
                    getattr(ui, 'status_%s' % flg).setStyleSheet('background:rgb(0, 255, 0)')
            else:
                if getattr(ui, 'status_%s' % flg).styleSheet() != 'background:rgb(255, 0, 0)':
                    getattr(ui, 'status_%s' % flg).setStyleSheet('background:rgb(255, 0, 0)')


def start_ai_end_bat():
    current_working_dir = os.getcwd()
    subprocess.Popen(
        [r"%s\start_recognition.bat" % current_working_dir],
        shell=True)
    print(r"%s\start_recognition.bat" % current_working_dir)


def test_ai_end():
    global flg_start
    try:
        res = requests.get(recognition_addr, timeout=5)
        print(res.text)
        if res.text == 'ok':
            flg_start['ai_end'] = True
    except:
        start_ai_end_bat()
        flg_start['ai_end'] = False


def black_screen():  # OBS黑屏
    if ui.checkBox_black_screen.isChecked() and flg_start['obs']:
        try:
            cl_request.set_current_program_scene('黑屏')
        except:
            print('obs 黑屏 错误！')
            ui.textBrowser_msg.append(fail('obs 黑屏 错误！'))
            flg_start['obs'] = False
    else:
        try:
            cl_request.set_current_program_scene(obs_data['obs_scene'])
        except:
            print('obs %s 错误！' % obs_data['obs_scene'])
            ui.textBrowser_msg.append(fail('obs %s 错误！' % obs_data['obs_scene']))
            flg_start['obs'] = False


def organ_shoot():  # 弹射开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_shoot.text()) - 1
        if ui.checkBox_shoot.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_start():  # 开启开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_start.text()) - 1
        if ui.checkBox_start.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_end():  # 结束开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_end.text()) - 1
        if ui.checkBox_end.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_number():  # 号码开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_OutNo.text()) - 1
        if ui.checkBox_switch.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def main2result():
    if ui.lineEdit_Main_Camera.text() != '':
        ui.lineEdit_Send_Result.setText(ui.lineEdit_Main_Camera.text())


def backup2result():
    if ui.lineEdit_Backup_Camera.text() != '':
        ui.lineEdit_Send_Result.setText(ui.lineEdit_Backup_Camera.text())


def cancel_betting():
    res = post_marble_results(term, 'Invalid Term', Track_number)
    if 'Invalid Term' in res:
        lottery_term[5] = '取消比赛'


def send_result():
    global Send_Result
    Send_Result = True
    # result_list = eval(ui.lineEdit_Send_Result.text())
    # result_data = {"raceTrackID": Track_number, "term": str(term),
    #                "actualResultOpeningTime": betting_end_time,
    #                "result": result_list,
    #                "timings": []}
    # for index in range(len(result_list)):
    #     result_data["timings"].append(
    #         {"pm": index + 1, "id": result_list[index], "time": float(z_ranking_time[index])})
    # post_end(term, betting_end_time, 0, Track_number)  # 发送游戏结束信号给服务器， 0: 不正常
    # post_result(term, betting_end_time, result_data, Track_number)  # 发送最终排名给服务器


def start_betting():
    ui.checkBox_restart.setChecked(True)
    ui.checkBox_test.setChecked(False)
    post_status(True, Track_number)


def stop_betting():
    ui.checkBox_restart.setChecked(False)
    ReStart_Thread.run_flg = False  # 停止循环
    post_status(False, Track_number)


def auto_shoot():  # 自动上珠
    global balls_start
    global ball_sort
    if ui.checkBox_shoot_0.isChecked():
        ball_sort[1][0] = []
        balls_start = 0
        ui.lineEdit_balls_start.setText('0')
        ui.lineEdit_ball_start.setText('0')
        Shoot_Thread.run_flg = True
    else:
        Shoot_Thread.run_flg = False


"****************************************直播大厅_结束****************************************************"
"****************************************参数设置_开始****************************************************"


def query_sql():
    # 创建数据库连接
    try:
        conn = create_connection("192.168.0.80", "root", "root", "dataini")

        if conn:
            local_ip = tool_unit.check_network_with_ip()

            # 查询配置表的 SQL 语句
            user_value = local_ip[1]  # 网卡号
            key_value = "电压输出%"  # 读取字段
            key_value2 = "网络摄像机%"  # 读取字段
            key_value3 = "赛道名称%"  # 读取字段
            key_value4 = "图像识别IP"  # 读取字段
            key_value5 = "全局配置.IP%"  # 读取字段
            key_values = ["电压输出", "网络摄像机", "赛道名称", "图像识别IP", "全局配置.IP"]
            # select_query = "SELECT * FROM config WHERE `user`=%s AND `key`=%s"
            select_query = ("SELECT * FROM config WHERE `user`=%s "
                            "AND (`key` LIKE %s "
                            "OR `key` LIKE %s "
                            "OR `key` LIKE %s "
                            "OR `key` = %s "
                            "OR `key` LIKE %s)")
            res = fetch_query(conn, select_query,
                              [user_value,
                               key_value,
                               key_value2,
                               key_value3,
                               key_value4,
                               key_value5])
            # print("Query Results:", type(res), res)
            text_sql = {}
            for index in range(len(res)):
                for k in key_values:
                    if res[index][3] != '0' and (k in res[index][2]):
                        text_sql[res[index][2]] = res[index][3]
            # 关闭连接
            conn.close()
            return text_sql
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


"****************************************参数设置_结束****************************************************"


def my_test():
    global term
    print('~~~~~~~~~~~~~~~~~~~~~~~~~')
    lottery2yaml()
    # s = int(ui.lineEdit_result_send.text())
    # s485.cam_zoom_step(s)
    # time.sleep(5)
    # term = '800001'
    # tcp_result_thread.send_type = 'time'
    # print(Obs_Thread.isRunning())
    # cl_request.start_record()
    # time.sleep(5)
    # print(record_data[2])
    # cl_request.stop_record()
    # res = requests.get(recognition_addr)
    # print(res.text)
    # print(ui.pushButton_udp_time.styleSheet())
    # res = requests.get(wakeup_addr)
    # print(res.text)
    # res = requests.get(recognition_addr)
    # print(res.text)
    # check_network_with_ip()
    # result_data2table()
    # save_main_yaml()
    # 加载音效
    # sound_effect = pygame.mixer.Sound('D:/pythonProject/Main_controller/mp3/07_冰原起泡准备声1.wav')
    # sound_effect.play(loops=10, maxtime=5000)  # 播放音效
    # activate_browser()
    # Test_Thread.obs_name = '终点2'
    # Test_Thread.run_flg = not (Test_Thread.run_flg)
    # resp = cl_requst.get_source_screenshot('终点2', "jpg", 1920, 1080, 100)
    # img = str2image(resp.image_data)
    # pixmap = QPixmap()
    # pixmap.loadFromData(img)
    # pixmap = pixmap.scaled(800, 450)
    # transform = QTransform()  ##需要用到pyqt5中QTransform函数
    # transform.rotate(90)  ##设置旋转角度——顺时针旋转90°
    # pixmap = pixmap.transformed(transform)  ##对image进行旋转
    # lab_p = ui.label_monitor_picture
    # lab_p.setPixmap(pixmap)

    # img = get_picture('终点1')[0]
    # # resp = cl_requst.get_source_screenshot('终点1', "jpg", 1920, 1080, 100)
    # # img = str2image(resp.image_data)
    # pixmap = QPixmap()
    # pixmap.loadFromData(img)
    # pixmap = pixmap.scaled(400 * 1.6, 225 * 1.6)
    # # transform = QTransform()  ##需要用到pyqt5中QTransform函数
    # # transform.rotate(-90)  ##设置旋转角度——顺时针旋转90°
    # # pixmap = pixmap.transformed(transform)  ##对image进行旋转
    # lab_p = ui.label_main_picture
    # lab_p.setPixmap(pixmap)

    # # resp = cl_requst.get_source_screenshot('终点2', "jpg", 1920, 1080, 100)
    # # resp = cl_requst.save_source_screenshot('终点1', "jpg", 'd:/img/%s.jpg' % (time.time()), 1920, 1080, 100)
    # # resp = cl_requst.save_source_screenshot('终点2', "jpg", 'd:/img/%s.jpg' % (time.time()), 1920, 1080, 100)


# 滚动到 textBrowser 末尾
def scroll_to_bottom(text_browser: QTextBrowser):
    # 获取 QTextCursor 并移动到文档结尾
    cursor = text_browser.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    text_browser.setTextCursor(cursor)
    text_browser.ensureCursorVisible()


class ZApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.aboutToQuit.connect(self.onAboutToQuit)

    @Slot()
    def onAboutToQuit(self):
        print("Exiting the application.")
        try:
            # 停止所有服务线程
            self.stop_all_threads()

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Stopping application.")

        finally:
            print("Waiting for all threads to exit...")
            self.join_all_threads()
            print("All servers are closed. Exiting.")

    def stop_all_threads(self):
        """停止所有线程的函数。"""
        try:
            PlanCmd_Thread.stop()
            PlanObs_Thread.stop()
            PlanCam_Thread.stop()
            PlanBallNum_Thread.stop()
            tcp_ranking_thread.stop()
            tcp_result_thread.stop()
            udp_thread.stop()
            Update_Thread.stop()
            TestStatus_Thread.stop()
            Axis_Thread.stop()
            Pos_Thread.stop()
            ReStart_Thread.stop()
            Audio_Thread.stop()
            Ai_Thread.stop()
            TestStatus_Thread.stop()
            listener.stop()
            ScreenShot_Thread.stop()
            Shoot_Thread.stop()
            pygame.quit()
        except Exception as e:
            print(f"Error stopping threads: {e}")

    def join_all_threads(self):
        """等待所有线程退出。"""
        try:
            PlanCmd_Thread.wait()
            PlanObs_Thread.wait()
            PlanCam_Thread.wait()
            PlanBallNum_Thread.wait()
            tcp_ranking_thread.wait()
            tcp_result_thread.wait()
            udp_thread.wait()
            Update_Thread.wait()
            TestStatus_Thread.wait()
            Axis_Thread.wait()
            Pos_Thread.wait()
            ReStart_Thread.wait()
            Audio_Thread.wait()
            Ai_Thread.wait()
            TestStatus_Thread.wait()
            listener.join()
            ScreenShot_Thread.wait()
            Shoot_Thread.wait()
        except Exception as e:
            print(f"Error waiting threads: {e}")


class ZMainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口图标
        self.setWindowIcon(QIcon("./icon.ico"))

    def closeEvent(self, event):
        if ui.radioButton_start_betting.isChecked():
            QMessageBox.information(self, "开盘中", "正在开盘中，禁止直接退出！")
            event.ignore()  # 忽略关闭事件，程序继续运行
        else:
            # 创建确认对话框
            reply = QMessageBox.question(
                self,
                "退出",
                "您确定要退出程序吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            # 检查用户的响应
            if reply == QMessageBox.Yes:
                event.accept()  # 接受关闭事件，程序退出
            else:
                event.ignore()  # 忽略关闭事件，程序继续运行


"************************************SPEED_UI*********************************************"


class SpeedUi(QDialog, Ui_Dialog_Set_Speed):
    def __init__(self):
        super().__init__()

    def setupUi(self, z_dialog):
        super(SpeedUi, self).setupUi(z_dialog)

        tb_speed = self.tableWidget_Set_Speed

        tb_speed.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_speed.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")


def auto_line():  # 相对上一个动作走直线
    if speed_ui.checkBox_auto_line.isChecked():
        tb_speed = speed_ui.tableWidget_Set_Speed
        tb_step = ui.tableWidget_Step
        row_index = tb_step.currentRow()
        x_0 = 0
        y_0 = 0
        if row_index > 0:
            x_0 = int(tb_step.item(row_index - 1, 2).text())
            y_0 = int(tb_step.item(row_index - 1, 3).text())
        x = abs(int(tb_step.item(row_index, 2).text()) - x_0)
        y = abs(int(tb_step.item(row_index, 3).text()) - y_0)
        x_speed = int(tb_speed.item(0, 0).text())
        y_speed = int(x_speed * (y / x))
        tb_speed.item(1, 0).setText(str(y_speed))


"************************************SPEED_UI*********************************************"

if __name__ == '__main__':
    app = ZApp(sys.argv)

    z_window = ZMainwindow()
    ui = ZUi()
    ui.setupUi(z_window)
    z_window.show()

    SpeedDialog = QDialog(z_window)
    speed_ui = SpeedUi()
    speed_ui.setupUi(SpeedDialog)

    speed_ui.buttonBox.accepted.connect(accept_speed)
    speed_ui.buttonBox.rejected.connect(reject_speed)
    speed_ui.checkBox_auto_line.checkStateChanged.connect(auto_line)
    speed_ui.tableWidget_Set_Speed.itemChanged.connect(auto_line)

    sc = SportCard()  # 运动卡
    s485 = Serial485()  # 摄像头

    plan_list = []  # 当前方案列表 [0.选中,1.圈数,2.左右,3.前后,4.上下,5.头旋转,6.头上下,7.速度,8.加速,9.减速,10.镜头缩放,11.缩放时长,12.机关,13.运动位置,14.卫星图位置,col_count - 2.OBS画面]
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料
    pValue = [0, 0, 0, 0, 0]  # 各轴位置
    flg_key_run = True  # 键盘控制标志
    axis_reset = True  # 轴复位标志
    flg_start = {'card': False, 's485': False, 'obs': False, 'ai': False, 'ai_end': False, 'server': False}  # 各硬件启动标志

    load_plan_yaml()

    tb_step_worker = UiWorker(ui.tableWidget_Step)
    main_music_worker = UiWorker(ui.checkBox_main_music)

    listener = pynput.keyboard.Listener(on_press=keyboard_press, on_release=keyboard_release)
    listener.start()  # 键盘监听线程 1

    PlanCmd_Thread = PlanCmdThread()  # 总运行方案 2
    PlanCmd_Thread._signal.connect(signal_accept)
    PlanCmd_Thread.start()

    PlanObs_Thread = PlanObsThread()  # OBS场景切换方案 3
    PlanObs_Thread._signal.connect(PlanObs_signal_accept)
    PlanObs_Thread.start()

    Shoot_Thread = ShootThread()  # 自动上球 3
    Shoot_Thread._signal.connect(shoot_signal_accept)
    Shoot_Thread.start()

    PlanCam_Thread = CamThread()  # 摄像头运行方案 4
    PlanCam_Thread._signal.connect(signal_accept)
    PlanCam_Thread.start()

    PlanBallNum_Thread = PlanBallNumThread()  # 统计过终点的球数 5
    PlanBallNum_Thread._signal.connect(PlanBallNum_signal_accept)
    PlanBallNum_Thread.start()

    ScreenShot_Thread = ScreenShotThread()  # 终点截图识别线程 6
    ScreenShot_Thread._signal.connect(ScreenShot_signal_accept)
    ScreenShot_Thread.start()

    Axis_Thread = AxisThread()  # 轴复位 7
    Axis_Thread._signal.connect(signal_accept)
    Axis_Thread.start()

    Pos_Thread = PosThread()  # 实时监控各轴位置 8
    Pos_Thread._signal.connect(pos_signal_accept)
    Pos_Thread.start()

    ReStart_Thread = ReStartThread()  # 循环模式 9
    ReStart_Thread._signal.connect(time_signal_accept)
    ReStart_Thread.start()

    Audio_Thread = AudioThread()  # 音频线程 10
    Audio_Thread._signal.connect(audio_signal_accept)
    Audio_Thread.start()

    Ai_Thread = AiThread()  # Ai语言线程 11
    Ai_Thread._signal.connect(ai_signal_accept)
    Ai_Thread.start()

    CardStart_Thread = CardStartThread()  # 运动卡开启线程 12
    CardStart_Thread._signal.connect(CardStart_signal_accept)

    TestStatus_Thread = TestStatusThread()  # 测试线程 13
    TestStatus_Thread._signal.connect(test_status_signal_accept)
    TestStatus_Thread.start()

    ui.pushButton_fsave.clicked.connect(save_plan_yaml)
    ui.pushButton_rename.clicked.connect(plan_rename)
    ui.pushButton_CardStart.clicked.connect(card_start)
    ui.pushButton_CardStop.clicked.connect(cmd_stop)
    ui.pushButton_CardStop_2.clicked.connect(cmd_stop)
    ui.pushButton_CardRun.clicked.connect(cmd_run)
    ui.pushButton_CardRun_2.clicked.connect(cmd_run)
    ui.pushButton_CardReset.clicked.connect(card_reset)
    ui.pushButton_Cardreset.clicked.connect(card_reset)
    ui.pushButton_ToTable.clicked.connect(p_to_table)
    ui.pushButton_Obs2Table.clicked.connect(obs_to_table)
    ui.pushButton_Source2Table.clicked.connect(source_to_table)
    ui.pushButton_Obs_delete.clicked.connect(obs_remove_table)
    ui.pushButton_CardNext.clicked.connect(cmd_next)
    ui.pushButton_to_TXT.clicked.connect(json_txt)
    ui.pushButton_Draw.clicked.connect(open_draw)
    ui.pushButton_test_2.clicked.connect(my_test)
    ui.pushButton_CardCloseAll.clicked.connect(card_close_all)
    ui.pushButton_CardClose.clicked.connect(card_close_all)

    ui.pushButton_start_game.clicked.connect(cmd_loop)

    ui.checkBox_saveImgs.clicked.connect(save_images)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.checkBox_test.checkStateChanged.connect(edit_enable)

    ui.checkBox_shoot.checkStateChanged.connect(organ_shoot)
    ui.checkBox_start.checkStateChanged.connect(organ_start)
    ui.checkBox_end.checkStateChanged.connect(organ_end)
    ui.checkBox_switch.checkStateChanged.connect(organ_number)

    ui.comboBox_plan.currentIndexChanged.connect(plan_refresh)
    ui.tableWidget_Step.itemChanged.connect(table_change)

    """
        OBS 处理
    """
    source_list = []  # OBS来源列表
    obs_data = {'obs_scene': ui.lineEdit_scene_name.text(), 'source_ranking': 36, 'source_picture': 13,
                'source_settlement': 26}  # 各来源ID号初始化{'现场', '排名时间组件', '画中画', '结算页'}
    record_data = [False, 'OBS_WEBSOCKET_OUTPUT_STARTING', None]  # OBS 录像状态数据
    scene_now = ''
    cl_request = ''  # 请求
    cl_event = ''  # 监听

    Obs_Thread = ObsThread()  # OBS启动线程
    Obs_Thread._signal.connect(obs_signal_accept)

    Source_Thread = SourceThread()  # OBS来源入表 13
    Source_Thread.source_signal.connect(source_signal_accept)

    ui.pushButton_ObsConnect.clicked.connect(obs_open)
    ui.comboBox_Scenes.activated.connect(scenes_change)

    "**************************OBS*****************************"

    "**************************图像识别算法_开始*****************************"
    # set_run_toggle 发送请求运行数据
    camera_num = 15  # 摄像头数量
    area_Code = {1: [], 2: [], 3: [], 4: [], 5: [],
                 6: [], 7: [], 8: [], 9: [], 10: [],
                 11: [], 12: [], 13: [], 14: [], 15: [], 16: []}  # 摄像头代码列表
    load_area()  # 初始化区域划分
    # print(area_Code)

    action_area = [0, 0, 0]  # 触发镜头向下一个位置活动的点位 action_area[区域, 圈数, 可写]
    balls_count = 8  # 运行球数
    balls_start = 0  # 起点球数量
    ranking_array = []  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]
    ball_sort = []  # 位置寄存器 ball_sort[[[]*max_lap_count]*max_area_count + 1]

    # 初始化数据
    max_lap_count = 1  # 最大圈
    max_area_count = 39  # 统计一圈的位置差
    init_array = [
        [0, 0, 0, 0, 0, 'yellow', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'blue', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'red', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'purple', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'orange', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'green', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'Brown', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'black', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'pink', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 'White', 0, 0, 0, 0]
    ]
    color_ch = {'yellow': '黄',
                'blue': '蓝',
                'red': '红',
                'purple': '紫',
                'orange': '橙',
                'green': '绿',
                'Brown': '棕',
                'black': '黑',
                'pink': '粉',
                'White': '白'}
    udpServer_addr = ('0.0.0.0', 19734)  # 接收图像识别结果
    tcpServer_addr = ('0.0.0.0', 9999)  # pingpong 发送网页排名
    result_tcpServer_addr = ('0.0.0.0', 8888)  # pingpong 发送网页排名
    httpServer_addr = ('0.0.0.0', 8081)  # 接收网络数据包控制
    udpClient_addr = ("192.168.0.161", 19733)  # 数据发送给其他服务器
    wakeup_addr = ["http://192.168.0.110:8080"]  # 唤醒服务器网址
    recognition_addr = "http://127.0.0.1:6066"  # 终点识别主机网址
    obs_script_addr = "http://127.0.0.1:8899"  # OBS 脚本网址
    rtsp_url = 'rtsp://admin:123456@192.168.0.29:554/Streaming/Channels/101'  # 主码流
    map_data = ['./img/09_沙漠.jpg', './img/09_沙漠.json', '860']  # 卫星地图资料
    five_axis = [1, 1, 1, 1, 1]
    five_key = [1, 1, 1, 1, 1]
    Track_number = "J"  # 轨道直播编号

    load_main_yaml()
    load_ballsort_yaml()

    # 初始化列表
    con_data = []  # 排名数组
    z_ranking_res = []  # 球号排名数组(发送给前端网页排名显示)
    z_ranking_time = []  # 球号排名数组(发送给前端网页排名显示)
    ranking_time_start = time.time()  # 比赛开始时间
    for i in range(0, len(init_array)):
        con_data.append([])
        z_ranking_res.append(i + 1)  # z_ranking_res[1,2,3,4,5,6,7,8,9,10]  初始化网页排名
        z_ranking_time.append('TRAP')  # z_ranking_time[1,2,3,4,5,6,7,8,9,10]    初始化网页排名时间
        for j in range(0, 5):
            if j == 0:
                con_data[i].append(init_array[i][5])  # con_data[[yellow,0,0,0,0]]
            else:
                con_data[i].append(0)
    init_ranking_table()  # 初始化排名数据表

    # 1. Udp 接收数据 14
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(udpServer_addr)
        print('Udp_socket Server Started.')
        udp_thread = UdpThread()
        udp_thread._signal.connect(udp_signal_accept)
        udp_thread.start()
    except:
        # 使用infomation信息框
        QMessageBox.information(z_window, "UDP", "UDP端口被占用")
        # sys.exit()

    # pingpong 发送排名 15
    tcp_ranking_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ranking_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_ranking_socket.bind(tcpServer_addr)
    tcp_ranking_socket.listen(1)
    print('Pingpong Server Started.')
    tcp_ranking_thread = TcpRankingThread()  # 前端网页以pingpong形式发送排名数据
    tcp_ranking_thread._signal.connect(tcp_signal_accept)
    tcp_ranking_thread.start()

    tcp_result_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_result_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_result_socket.bind(result_tcpServer_addr)
    tcp_result_socket.listen(5)
    tcp_result_thread = TcpResultThread()  # 前端网页以pingpong形式发送结果数据 16
    tcp_result_thread._signal.connect(tcp_signal_accept)
    tcp_result_thread.start()

    # 唤醒图像识别主机线程 17
    wakeup_ser = threading.Thread(target=wakeup_server, daemon=True)
    wakeup_ser.start()

    # 启动 HTTPServer 接收外部命令控制本程序 18
    httpd = HTTPServer(httpServer_addr, SimpleHTTPRequestHandler)
    http_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    http_thread.start()

    # 更新数据表线程 19
    Update_Thread = UpdateThread()
    Update_Thread._signal.connect(ranking_signal_accept)
    Update_Thread.start()

    ui.pushButton_save_Ranking.clicked.connect(save_ballsort_yaml)

    ui.lineEdit_time_send_result.editingFinished.connect(save_ballsort_yaml)
    ui.lineEdit_time_count_ball.editingFinished.connect(save_ballsort_yaml)

    # 初始化球数组，位置寄存器
    reset_ranking_array()  # 重置排名数组
    "**************************图像识别算法_结束*****************************"

    "**************************卫星图_开始*****************************"
    camera_points = []  # 摄像机移动点位 camera_points[[label内存],[区域号],[卫星图坐标]]
    audio_points = []  # 音效点位 audio_points[[label内存],[区域号],[卫星图坐标]]
    ai_points = []  # AI点位 ai_points[[label内存],[区域号],[卫星图坐标]]
    map_orbit = []  # 地图轨迹

    map_label_big = MapLabel()
    layout_big = QVBoxLayout(ui.widget_map_big)
    layout_big.setContentsMargins(0, 0, 0, 0)
    layout_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 添加自定义的 QLabel 到布局中
    layout_big.addWidget(map_label_big)

    map_label = MapLabel(picture_size=350, ball_space=21, ball_radius=5, flash_time=20, step_length=0.5)
    map_layout = QVBoxLayout(ui.widget_map)
    map_layout.setContentsMargins(0, 0, 0, 0)
    map_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 添加自定义的 QLabel 到布局中
    map_layout.addWidget(map_label)

    # 初始化混音器
    pygame.mixer.init()

    ui.checkBox_main_music.checkStateChanged.connect(music_ctl)
    ui.radioButton_music_1.clicked.connect(music_ctl)
    ui.radioButton_music_2.clicked.connect(music_ctl)
    ui.radioButton_music_3.clicked.connect(music_ctl)

    load_points_yaml('red')
    load_points_yaml('blue')
    load_points_yaml('green')

    ui.pushButton_add_camera.clicked.connect(add_camera_points)
    ui.pushButton_del_camera.clicked.connect(del_camera_points)
    ui.pushButton_add_Audio.clicked.connect(add_audio_points)
    ui.pushButton_del_Audio.clicked.connect(del_audio_points)
    ui.pushButton_add_Ai.clicked.connect(add_ai_points)
    ui.pushButton_del_Ai.clicked.connect(del_ai_points)
    ui.pushButton_save_camera.clicked.connect(lambda: save_points('red'))
    ui.pushButton_save_Audio.clicked.connect(lambda: save_points('blue'))
    ui.pushButton_save_Ai.clicked.connect(lambda: save_points('green'))
    ui.checkBox_show_camera.clicked.connect(lambda: show_points('red'))
    ui.checkBox_show_audio.clicked.connect(lambda: show_points('blue'))
    ui.checkBox_show_ai.clicked.connect(lambda: show_points('green'))

    "**************************摄像头结果_开始*****************************"
    main_Camera = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 主镜头结果
    monitor_Camera = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 监控镜头结果
    fit_Camera = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 两个镜头的对比
    perfect_Camera = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 完美情况

    main_camera_layout = QVBoxLayout(ui.widget_camera_sony)
    main_camera_layout.setContentsMargins(0, 9, 0, 0)
    main_camera_label = CameraLabel()
    main_camera_label.Camera_index = 'main_Camera'
    main_camera_layout.addWidget(main_camera_label)

    monitor_camera_layout = QVBoxLayout(ui.widget_camera_monitor)
    monitor_camera_layout.setContentsMargins(0, 9, 0, 0)
    monitor_camera_label = CameraLabel()
    monitor_camera_label.Camera_index = 'monitor_Camera'
    monitor_camera_layout.addWidget(monitor_camera_label)

    fit_camera_layout = QVBoxLayout(ui.widget_camera_fit)
    fit_camera_layout.setContentsMargins(0, 5, 0, 5)
    fit_camera_label = CameraLabel()
    fit_camera_label.Camera_index = 'fit_Camera'
    fit_camera_layout.addWidget(fit_camera_label)

    "**************************摄像头结果_结束*****************************"
    "**************************参数设置_开始*****************************"
    ui.lineEdit_UdpServer_Port.editingFinished.connect(save_main_yaml)
    ui.lineEdit_TcpServer_Port.editingFinished.connect(save_main_yaml)
    ui.lineEdit_result_tcpServer_port.editingFinished.connect(save_main_yaml)
    ui.lineEdit_wakeup_addr.editingFinished.connect(save_main_yaml)
    ui.lineEdit_rtsp_url.editingFinished.connect(save_main_yaml)
    ui.lineEdit_recognition_addr.editingFinished.connect(save_main_yaml)
    ui.lineEdit_obs_script_addr.editingFinished.connect(save_main_yaml)
    ui.lineEdit_cardNo.editingFinished.connect(save_main_yaml)
    ui.lineEdit_CardNo.editingFinished.connect(save_main_yaml)
    ui.lineEdit_s485_Axis_No.editingFinished.connect(save_main_yaml)
    ui.lineEdit_s485_Cam_No.editingFinished.connect(save_main_yaml)
    ui.lineEdit_five_axis.editingFinished.connect(save_main_yaml)
    ui.lineEdit_five_key.editingFinished.connect(save_main_yaml)
    ui.lineEdit_map_picture.editingFinished.connect(save_main_yaml)
    ui.lineEdit_map_size.editingFinished.connect(save_main_yaml)
    ui.lineEdit_map_line.editingFinished.connect(save_main_yaml)
    ui.lineEdit_Image_Path.editingFinished.connect(save_main_yaml)
    ui.lineEdit_scene_name.editingFinished.connect(save_main_yaml)
    ui.lineEdit_source_ranking.editingFinished.connect(save_main_yaml)
    ui.lineEdit_source_picture.editingFinished.connect(save_main_yaml)
    ui.lineEdit_source_settlement.editingFinished.connect(save_main_yaml)
    ui.lineEdit_source_end.editingFinished.connect(save_main_yaml)
    ui.lineEdit_music_1.editingFinished.connect(save_main_yaml)
    ui.lineEdit_music_2.editingFinished.connect(save_main_yaml)
    ui.lineEdit_music_3.editingFinished.connect(save_main_yaml)
    ui.radioButton_music_background_1.clicked.connect(save_main_yaml)
    ui.radioButton_music_background_2.clicked.connect(save_main_yaml)
    ui.radioButton_music_background_3.clicked.connect(save_main_yaml)
    ui.pushButton_Save_Ball.clicked.connect(save_main_yaml)

    "**************************参数设置_结束*****************************"
    "**************************直播大厅_开始*****************************"
    labels = []
    lottery_term = ['0'] * 9  # 开奖记录 lottery_term[期号, 开跑时间, 倒数, 状态, 自动赛果, 确认赛果, 图片, 录像, 时间戳]
    # start_lottery_server_bat()  # 模拟开奖王服务器
    lottery_yaml_init()

    term = '8000'  # 期号
    betting_start_time = 0  # 比赛预定开始时间
    betting_end_time = 0  # 比赛预定结束时间
    stream_url = ''  # 流链接
    Send_Result = False  # 发送结果标志位

    ui.radioButton_start_betting.clicked.connect(start_betting)  # 开盘
    ui.radioButton_stop_betting.clicked.connect(stop_betting)  # 封盘
    # ui.radioButton_test_game.clicked.connect(lambda: ui.checkBox_test.setChecked(True))
    ui.checkBox_black_screen.checkStateChanged.connect(black_screen)

    ui.pushButton_ready.clicked.connect(card_start)
    ui.pushButton_start_game_2.clicked.connect(cmd_run)
    ui.pushButton_close_all.clicked.connect(card_close_all)
    ui.pushButton_collect_ball.clicked.connect(lambda: ui.checkBox_end.setChecked(True))
    ui.pushButton_end_game.clicked.connect(cmd_stop)
    ui.pushButton_Stop_All.clicked.connect(cmd_stop)
    ui.pushButton_end_all.clicked.connect(stop_server)
    ui.pushButton_Main_Camera.clicked.connect(main2result)
    ui.pushButton_Backup_Camera.clicked.connect(backup2result)
    ui.pushButton_Cancel_Result.clicked.connect(cancel_betting)
    ui.pushButton_Send_Result.clicked.connect(send_result)

    "**************************直播大厅_结束*****************************"

    sys.exit(app.exec())
