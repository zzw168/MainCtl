import copy
import json
import math
import os
import random
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import cv2
import numpy as np
import pynput
import requests
import yaml
from PyInstaller.utils.hooks.conda import files

from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QPropertyAnimation
from PySide6.QtGui import QBrush, QColor, QPixmap, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu, QMessageBox, QFileDialog

import obsws_python as obs
import pygame

from utils.SportCard_unit import *
from utils.tool_unit import *
from utils.Serial485_unit import *
from MainCtl_Ui import *
from utils.pingpong_socket import *
from utils.z_json2txt import *

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
    print("录制状态变化")
    print(data.output_active)
    print(data.output_state)
    print(data.output_path)


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


class ObsThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ObsThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        global cl_requst
        global cl_event
        global flg_start
        try:
            if not flg_start['obs']:
                cl_requst = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
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
    if '成功' in msg:
        get_scenes_list()  # 获取所有场景
        get_source_list(ui.comboBox_Scenes.currentText())


def obs_open():
    if not Obs_Thead.isRunning():
        Obs_Thead.start()


class SourceThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(SourceThead, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            self._signal.emit('写表')
            self.run_flg = False


def source_signal_accept(msg):
    print(msg)
    source2table()


def source2table():
    global source_list
    try:
        if scene_now != '':
            ui.comboBox_Scenes.setCurrentText(scene_now)
        tb_sources = ui.tableWidget_Sources
        tb_sources.setRowCount(len(source_list))
        for i in range(0, len(source_list)):
            cb = QCheckBox()
            cb.setStyleSheet('QCheckBox{margin:6px};')
            cb.clicked.connect(source_enable)
            tb_sources.setCellWidget(i, 0, cb)
            if source_list[i][0] == True:
                tb_sources.cellWidget(i, 0).setChecked(True)
            print(source_list[i][0])
            for j in range(1, len(source_list[i])):
                item = QTableWidgetItem(str(source_list[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                tb_sources.setItem(i, j, item)
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
    try:
        cl_requst.set_scene_item_enabled(scene_name, item_id, s_enable)  # 打开视频来源
    except:
        ui.textBrowser.append(fail("OBS 开关来源！"))


def activate_browser():  # 程序开始，刷新浏览器
    tb_source = ui.tableWidget_Sources
    for row_num in range(tb_source.rowCount()):
        # print(tb_source.item(row_num, 1))
        if tb_source.item(row_num, 1).text() == '浏览器':
            item_id = source_list[row_num][2]
            try:
                print('现场', item_id, False)
                cl_requst.set_scene_item_enabled('现场', item_id, False)  # 打开视频来源
                time.sleep(1)
                cl_requst.set_scene_item_enabled('现场', item_id, True)  # 打开视频来源
            except:
                ui.textBrowser.append(fail("OBS 开关浏览器出错！"))
            break


def get_scenes_list():  # 刷新所有列表
    try:
        res = cl_requst.get_scene_list()  # 获取场景列表
        res_name = cl_requst.get_current_program_scene()  # 获取激活的场景
    except:
        ui.textBrowser.append(fail("OBS 刷新所有列表中断！"))
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
    scene_now = scene_name
    res = cl_requst.get_scene_item_list(scene_name)
    source_list = []
    if res:
        for item in res.scene_items:
            source_list.append([item['sceneItemEnabled'], item['sourceName'], item['sceneItemId']])
            # print('取得来源列表 %s' % item)
        Source_Thead.run_flg = True


def scenes_change():  # 变换场景
    scene_name = ui.comboBox_Scenes.currentText()
    try:
        cl_requst.set_current_program_scene(scene_name)
    except:
        ui.textBrowser.append(fail("OBS 变换场景链接中断！"))


# 截取OBS图片
def get_picture(scence_current):
    # cl_requst.get_source_screenshot(scence_current, "jpg", 1920, 1080, 100)
    # time.sleep(1)
    resp = cl_requst.get_source_screenshot(scence_current, "jpg", 1920, 1080, 100)
    img = resp.image_data[22:]
    form_data = {
        'CameraType': 'obs',
        'img': img,
        'sort': '1',  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
    }
    try:
        res = requests.post(url="http://127.0.0.1:6066", data=form_data, timeout=5)
        r_list = eval(res.text)  # 返回 [图片字节码，排名列表]
        return r_list
    except:
        img = img.encode('ascii')
        image_byte = base64.b64decode(img)
        return [image_byte, '[1]', 'obs']
        print('终点识别服务没有开启！')


# obs 脚本 obs_script_time.py 请求
def obs_script_request():
    res = requests.get(url="http://127.0.0.1:8899/start")
    # res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
    # res = requests.get(url="http://127.0.0.1:8899/period?term=开始")
    print(res)


"******************************OBS结束*************************************"

"******************************网络摄像头*************************************"


# 获取网络摄像头图片
def get_rtsp(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
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
                    res = requests.post(url="http://127.0.0.1:6066", data=form_data, timeout=5)
                    r_list = eval(res.text)  # 返回 [图片字节码，排名列表]
                    return r_list
                except:
                    print('终点识别服务没有开启！')
                    # img = frame2img(frame)
                    # image_byte = qimage_to_bytes(img)
                    img = jpg_base64.encode('ascii')
                    image_byte = base64.b64decode(img)
                    return [image_byte, '[1]', 'monitor']
        else:
            print("无法读取视频帧")
    else:
        print(f'无法打开摄像头')


"************************************图像识别_开始****************************************"


# 处理触发点位
def deal_action():
    global action_area
    for rank_num in range(0, len(ranking_array)):  # 循环寻找合适的球位置，镜头追踪
        if action_area[1] == int(ranking_array[rank_num][8]):
            if (int(ranking_array[rank_num][6]) > action_area[0] + 3
                    or (int(ranking_array[rank_num][6]) < action_area[0])):
                continue
            action_area[0] = int(ranking_array[rank_num][6])  # 同圈中寻找合适区域
            break
        if action_area[1] < int(ranking_array[rank_num][8]):  # 不同圈赋值更大圈数
            action_area[1] = int(ranking_array[rank_num][8])
            print('区域更新~~~~~~~~', action_area[1])
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
                    if result_count >= max_area_count - ball_num - 15:
                        ranking_array[r_index][8] += 1
                        if ranking_array[r_index][8] > max_lap_count - 1:
                            ranking_array[r_index][8] = 0
                if action_area[0] >= max_area_count - ball_num and action_area[1] >= max_lap_count - 1:
                    area_limit = ball_num
                else:
                    area_limit = 5
                # if ((ranking_array[r_index][6] == 0)  # 等于0 刚初始化，未检测区域
                if ((ranking_array[r_index][6] == 0 and q_item[6] < 5)  # 等于0 刚初始化，未检测区域
                        or (q_item[6] >= ranking_array[r_index][6] and  # 新位置要大于旧位置
                            (q_item[6] - ranking_array[r_index][6] <= area_limit  # 新位置相差旧位置三个区域以内
                             or ranking_array[0][6] - ranking_array[r_index][6] > 5
                            ))  # 当新位置与旧位置超过3个区域，则旧位置与头名要超过5个区域才统计
                        or (q_item[6] < 8 and ranking_array[r_index][6] >= max_area_count - ball_num - 6)):  # 跨圈情况
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
    # global previous_position
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
    action_area = [1, 0]  # 初始化触发区域
    z_ranking_res = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 初始化网页排名
    z_ranking_time = ['TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'TRAP', 'OUT', 'OUT']  # 初始化网页排名时间
    tcp_ranking_thread.sleep_time = 1  # 重置排名数据包发送时间
    if flg_start['obs']:
        try:
            res = requests.get(url="http://127.0.0.1:8899/reset")
            print(res)
        except:
            print('OBS脚本链接错误！')


# print(ball_sort)


def to_num(res):  # 按最新排名排列数组
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
        for i in range(0, len(init_array)):
            if r == init_array[i][5]:
                arr_res.append(i + 1)
    for i in range(0, len(arr_res)):
        for j in range(0, len(camera_response)):
            if arr_res[i] == camera_response[j]:
                camera_response[i], camera_response[j] = camera_response[j], camera_response[i]
    return camera_response


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('你对HTTP服务端发送了POST'.encode('utf-8'))
        content_length = int(self.headers['Content-Length'])
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
    global reset_time
    global init_array
    global color_ch
    global udpServer_addr
    global tcpServer_addr
    global httpServer_addr
    global udpClient_addr
    global wakeup_addr
    global ball_num
    global rtsp_url
    file = "./ballsort_config.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        f_ = yaml.safe_load(f)
        max_area_count = f_['max_area_count']
        max_lap_count = f_['max_lap_count']
        reset_time = f_['reset_time']
        init_array = f_['init_array']
        color_ch = f_['color_ch']
        udpServer_addr = (f_['udpServer_addr'][0], f_['udpServer_addr'][1])
        tcpServer_addr = (f_['tcpServer_addr'][0], f_['tcpServer_addr'][1])
        httpServer_addr = (f_['httpServer_addr'][0], f_['httpServer_addr'][1])
        udpClient_addr = (f_['udpClient_addr'][0], f_['udpClient_addr'][1])
        wakeup_addr = (f_['wakeup_addr'])
        ball_num = (f_['ball_num'])
        rtsp_url = (f_['rtsp_url'])

        ui.lineEdit_lap_Ranking.setText(str(max_lap_count))
        ui.lineEdit_area_Ranking.setText(str(max_area_count))
        ui.lineEdit_time_Ranking.setText(str(reset_time))

        f.close()
    else:
        print("文件不存在")


def save_ballsort_yaml():
    global max_lap_count
    global max_area_count
    global reset_time
    file = "./ballsort_config.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        ballsort_conf = yaml.safe_load(f)
        f.close()
        if (ui.lineEdit_lap_Ranking.text().isdigit()
                and ui.lineEdit_area_Ranking.text().isdigit()
                and ui.lineEdit_time_Ranking.text().isdigit()):
            ballsort_conf['max_lap_count'] = int(ui.lineEdit_lap_Ranking.text())
            ballsort_conf['max_area_count'] = int(ui.lineEdit_area_Ranking.text())
            ballsort_conf['reset_time'] = int(ui.lineEdit_time_Ranking.text())
            max_lap_count = int(ui.lineEdit_lap_Ranking.text())
            max_area_count = int(ui.lineEdit_area_Ranking.text())
            reset_time = int(ui.lineEdit_time_Ranking.text())
            ui.lineEdit_Countdown.setText(str(reset_time))
            # print(ballsort_conf)
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(ballsort_conf, f, allow_unicode=True)
            f.close()
            ui.textBrowser_background_data.setText(
                succeed("%s,%s,%s 保存服务器完成" % (ballsort_conf['max_lap_count'],
                                                     ballsort_conf['max_area_count'],
                                                     ballsort_conf['reset_time'])))
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


class TcpRankingThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TcpRankingThead, self).__init__()
        self.running = True
        self.run_flg = True
        self.send_time_flg = False
        self.sleep_time = 0.1
        self.send_time_data = [1, time.strftime('%M"%S', time.localtime(time.time()))]

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            try:
                con, addr = tcp_ranking_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if con:
                    self._signal.emit("Accepted. {0}, {1}".format(con, str(addr)))
                    with WebsocketServer(con) as ws:
                        # ws.send('pong')
                        while True:
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
                                # print("pingpong 错误：", e)
                                self._signal.emit("pingpong 错误：%s" % e)
                                break
            except Exception as e:
                # print(e)
                self._signal.emit("pingpong 错误：%s" % e)
                # break


class TcpResultThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TcpResultThead, self).__init__()
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            try:
                con, addr = tcp_result_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if con:
                    self._signal.emit("Accepted. {0}, {1}".format(con, str(addr)))
                    with WebsocketServer(con) as ws:
                        datalist = {
                            'type': 'updata',
                            'data': {
                                'qh': "9555059",
                                'rank': [{"mc": z_ranking_res[0], "time": z_ranking_time[0]},
                                         {"mc": z_ranking_res[1], "time": z_ranking_time[1]},
                                         {"mc": z_ranking_res[2], "time": z_ranking_time[2]},
                                         {"mc": z_ranking_res[3], "time": z_ranking_time[3]},
                                         {"mc": z_ranking_res[4], "time": z_ranking_time[4]},
                                         {"mc": z_ranking_res[5], "time": z_ranking_time[5]},
                                         {"mc": z_ranking_res[6], "time": z_ranking_time[6]},
                                         {"mc": z_ranking_res[7], "time": z_ranking_time[7]},
                                         {"mc": z_ranking_res[8], "time": z_ranking_time[8]},
                                         {"mc": z_ranking_res[9], "time": z_ranking_time[9]}]}}
                        ws.send(json.dumps(datalist))
            except Exception as e:
                # print(e)
                self._signal.emit("pingpong 错误：%s" % e)
                # break


def tcp_signal_accept(msg):
    print()
    ui.textBrowser_background_data.append(msg)


class UdpThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(UdpThead, self).__init__()
        self.run_flg = True
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        global con_data
        while self.running:
            try:
                # 3. 等待接收对方发送的数据
                recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
                if recv_data[0] is None:
                    print('UDP无数据！', recv_data[0])
                    continue
                if self.run_flg:
                    res = recv_data[0].decode('utf8')
                    if res == '':
                        print('UDP_res无数据！', recv_data[0])
                        continue
                    data_res = eval(res)  # str转换list
                    self._signal.emit(data_res)
                    array_data = []
                    for i_ in range(1, len(data_res)):  # data_res[0] 是时间戳差值 ms
                        array_data.append(copy.deepcopy(data_res[i_]))
                    # print(array_data)
                    array_data = deal_area(array_data, array_data[0][6])  # 收集统计区域内的球
                    if not array_data:
                        continue
                    if action_area[0] >= max_area_count - ball_num and action_area[
                        1] >= max_lap_count - 1:  # 在最后面排名阶段，以区域先后为准
                        array_data = filter_max_area(array_data)
                    else:
                        array_data = filter_max_value(array_data)  # 在平时球位置追踪，以置信度为准
                    deal_rank(array_data)
                    deal_action()
                    con_data = []
                    for k in range(0, len(ranking_array)):
                        con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                        con_data.append(
                            [con_item['name'], con_item['position'], con_item['lapCount'], con_item['x1'],
                             con_item['y1']])
                    to_num(con_data)

            except Exception as e:
                print("UDP数据接收出错:%s" % e)
                self._signal.emit("UDP数据接收出错:%s" % e)
        # 5. 关闭套接字
        udp_socket.close()


def udp_signal_accept(msg):
    # print(msg)
    if ui.checkBox_ShowUdp.isChecked():
        ui.textBrowser_background_data.append(str(msg))


class ResetThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ResetThead, self).__init__()
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(5)
            if (ranking_array[0][8] == max_lap_count - 1 and ranking_array[0][6] == max_area_count
                    and ui.checkBox_reset_Ranking.isChecked()):
                for t in range(reset_time, 0, -1):
                    if not ui.checkBox_reset_Ranking.isChecked():
                        break
                    self._signal.emit(t)
                    time.sleep(1)
                if ui.checkBox_reset_Ranking.isChecked():
                    reset_ranking_array()
                    self._signal.emit('提示:球排名数据已自动重置！')


def reset_signal_accept(msg):
    ui.textBrowser_background_data.clear()
    init_ranking_table()


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
    for ball in ball_array:
        if ball[4] < 0.35:  # 置信度小于 0.45 的数据不处理
            continue
        ball.append(0)
        x = (ball[0] + ball[2]) / 2
        y = (ball[1] + ball[3]) / 2
        point = (x, y)
        if cap_num in area_Code.keys():
            for area in area_Code[cap_num]:
                pts = np.array(area['coordinates'], np.int32)
                Result = cv2.pointPolygonTest(pts, point, False)  # -1=在外部,0=在线上，1=在内部
                if Result > -1.0:
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
            max_area[key] = area
    filtered_list = []
    for sublist in lists:
        if (sublist[6] == max_area[sublist[5]]):  # 选取同一区域置信度最大的球添加到修正后的队列
            filtered_list.append(copy.deepcopy(sublist))
            # print(filtered_list)
    return filtered_list


def filter_max_value(lists):  # 在区域范围内如果出现两个相同的球，则取置信度最高的球为准
    max_values = {}
    for sublist in lists:
        value, key = sublist[4], sublist[5]
        if key not in max_values or max_values[key] < value:
            max_values[key] = value
    filtered_list = []
    for sublist in lists:
        if sublist[4] == max_values[sublist[5]]:  # 选取置信度最大的球添加到修正后的队列
            filtered_list.append(copy.deepcopy(sublist))
    return filtered_list


"************************************图像识别_结束****************************************"


class MyUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super(MyUi, self).setupUi(MainWindow)

        tb = self.tableWidget_Results
        tb.horizontalHeader().resizeSection(0, 10)
        tb.horizontalHeader().resizeSection(1, 5)
        tb.horizontalHeader().resizeSection(2, 10)
        # tb.horizontalHeader().resizeSection(1, 80)
        # tb.setColumnHidden(3, True)
        tb.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

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

        tb_Step = self.tableWidget_Step
        tb_Step.horizontalHeader().resizeSection(0, 10)
        tb_Step.horizontalHeader().resizeSection(1, 40)
        tb_Step.horizontalHeader().resizeSection(7, 50)
        tb_Step.horizontalHeader().resizeSection(8, 50)
        tb_Step.horizontalHeader().resizeSection(9, 50)
        tb_Step.horizontalHeader().resizeSection(10, 60)
        tb_Step.horizontalHeader().resizeSection(11, 40)
        tb_Step.horizontalHeader().resizeSection(12, 50)
        tb_Step.horizontalHeader().resizeSection(13, 60)
        tb_Step.horizontalHeader().resizeSection(14, 50)
        tb_Step.horizontalHeader().resizeSection(15, 50)
        tb_Step.setColumnHidden(13, True)
        tb_Step.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_Step.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

        tb_Step.setContextMenuPolicy(Qt.CustomContextMenu)
        tb_Step.customContextMenuRequested.connect(self.generateMenu)

        tb_sources = self.tableWidget_Sources
        tb_sources.horizontalHeader().resizeSection(0, 10)
        tb_sources.horizontalHeader().resizeSection(1, 160)
        # tb_sources.horizontalHeader().resizeSection(2, 30)
        tb_sources.setColumnHidden(2, True)
        tb_sources.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_sources.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")

    def generateMenu(self, pos):
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
            # del_host()
            row_count = tb_step.rowCount()
            col_count = tb_step.columnCount()
            print(row_count)
            if row_count != 0:
                p = tb_step.currentRow()
                for row in range(p, row_count - 1):
                    print('%d' % row)
                    for col in range(0, tb_step.columnCount() - 1):
                        if col == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet('QCheckBox{margin:6px};')
                            cb.setChecked(tb_step.cellWidget(row + 1, col).isChecked())
                            tb_step.setCellWidget(row, col, cb)
                        elif col == col_count - 2:
                            cell_widget = tb_step.cellWidget(row + 1, col)
                            if cell_widget:
                                if tb_step.item(row, col):
                                    tb_step.item(row, col).setText('')
                                if isinstance(cell_widget, QCheckBox):
                                    cb = QCheckBox()
                                    cb.setStyleSheet('QCheckBox{margin:6px};')
                                    cb.setText(tb_step.cellWidget(row + 1, col).text())
                                    cb.setChecked(tb_step.cellWidget(row + 1, col).isChecked())
                                    tb_step.setCellWidget(row, col, cb)
                                elif isinstance(cell_widget, QRadioButton):
                                    rb = QRadioButton()
                                    rb.setStyleSheet('QRadioButton{margin:6px};')
                                    rb.setText(tb_step.cellWidget(row + 1, col).text())
                                    rb.setChecked(tb_step.cellWidget(row + 1, col).isChecked())
                                    tb_step.setCellWidget(row, col, rb)
                            else:
                                if tb_step.cellWidget(row, col):
                                    tb_step.removeCellWidget(row, col)
                                    item = QTableWidgetItem(tb_step.item(row + 1, col).text())
                                    item.setTextAlignment(Qt.AlignCenter)
                                    tb_step.setItem(row, col, item)
                        else:
                            item = QTableWidgetItem(tb_step.item(row + 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb_step.setItem(row, col, item)
                tb_step.setRowCount(row_count - 1)
        if action == item3:
            tb_step = self.tableWidget_Step
            row_count = tb_step.rowCount()
            col_count = tb_step.columnCount()
            tb_step.setRowCount(row_count + 1)
            row = tb_step.currentRow()
            if row_count > 0:  # 下移表格
                for r in range(row_count, row, -1):
                    cb = QCheckBox()
                    cb.setStyleSheet('QCheckBox{margin:6px};')
                    tb_step.setCellWidget(r, 0, cb)
                    tb_step.cellWidget(r, 0).setChecked(tb_step.cellWidget(r - 1, 0).isChecked())
                    for col in range(1, tb_step.columnCount() - 1):
                        if col == col_count - 2:
                            cell_widget = tb_step.cellWidget(r - 1, col)
                            if cell_widget:
                                if isinstance(cell_widget, QCheckBox):
                                    cb = QCheckBox()
                                    cb.setStyleSheet('QCheckBox{margin:6px};')
                                    cb.setText(tb_step.cellWidget(r - 1, col).text())
                                    cb.setChecked(tb_step.cellWidget(r - 1, col).isChecked())
                                    tb_step.setCellWidget(r, col, cb)
                                elif isinstance(cell_widget, QRadioButton):
                                    rb = QRadioButton()
                                    rb.setStyleSheet('QRadioButton{margin:6px};')
                                    rb.setText(tb_step.cellWidget(r - 1, col).text())
                                    rb.setChecked(tb_step.cellWidget(r - 1, col).isChecked())
                                    tb_step.setCellWidget(r, col, rb)
                            else:
                                if tb_step.cellWidget(r, col):  # 删除本行控件
                                    tb_step.removeCellWidget(r, col)
                                    item = QTableWidgetItem(tb_step.item(r - 1, col).text())
                                    item.setTextAlignment(Qt.AlignCenter)
                                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                                    tb_step.setItem(r, col, item)
                        else:
                            item = QTableWidgetItem(tb_step.item(r - 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                            tb_step.setItem(r, col, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                tb_step.setCellWidget(0, 0, cb)

                for r in range(1, tb_step.columnCount() - 1):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    tb_step.setItem(0, r, item)


'''
    ReStartThead(QThread) 重启动作
'''


class ReStartThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ReStartThead, self).__init__()
        self.run_flg = False

        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            countdown = ui.lineEdit_Countdown.text()
            if countdown.isdigit():
                countdown = int(countdown)
            else:
                countdown = 300
            for t in range(countdown, 0, -1):
                if not ui.checkBox_restart.isChecked():
                    self.run_flg = False
                    break
                time.sleep(1)
                self._signal.emit(t)
            if ui.checkBox_restart.isChecked():
                reset_ranking_array()  # 初始化排名，位置变量
                activate_browser()  # 刷新OBS中排名浏览器
                PlanCmd_Thead.run_flg = True
            # print("循环启动！")
            self.run_flg = False


def time_signal_accept(msg):
    # print(msg)
    if int(msg) == 1:
        plan_refresh()
        ui.lineEdit_ball_num.setText('0')
    ui.lineEdit_time.setText(str(msg))


'''
    PosThead(QThread) 检测各轴位置
'''


class PosThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PosThead, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

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
                    # time.sleep(0.1)
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
    CamThead(QThread) 摄像头运动方案线程
'''


class CamThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(CamThead, self).__init__()
        self.camitem = [5, 5]  # [运行挡位,持续时间]
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(0.01)
            if (not self.run_flg) or (not flg_start['s485']):
                continue
            print('串口运行')
            if self.camitem[0] != 0:
                try:
                    res = s485.cam_zoom_move(self.camitem[0])
                    if not res:
                        flg_start['s485'] = False
                        self._signal.emit(fail("s485通信出错！"))
                        continue
                    time.sleep(self.camitem[1])
                    s485.cam_zoom_on_off()
                except:
                    print("485 运行出错！")
                    flg_start['s485'] = False
                    self._signal.emit(fail("s485通信出错！"))
            self.run_flg = False


'''
    PlanBallNumThead(QThread) 摄像头运动方案线程
'''


class PlanBallNumThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanBallNumThead, self).__init__()
        self.run_flg = False

        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        global flg_start
        while self.running:
            time.sleep(0.1)
            if (not self.run_flg) or (not flg_start['card']):
                continue
            print('正在接收运动卡输入信息！')
            try:
                res = sc.GASetDiReverseCount()  # 输入次数归0
                time_now = time.time()
                num_old = 0
                if res == 0:
                    while True:
                        res, value = sc.GAGetDiReverseCount()
                        # print(res, value)
                        if res == 0:
                            num = int(value[0] / 2)
                            if num != num_old:
                                t = time.time()
                                if num_old < len(z_ranking_time):
                                    # minute = int((t - ranking_time_start) / 60)
                                    # Second = int((t - ranking_time_start) % 60)
                                    # z_ranking_time[num_old] = "%s'%s" % (minute, Second)
                                    z_ranking_time[num_old] = '%.2f"' % (t - ranking_time_start)
                                    if not tcp_ranking_thread.send_time_flg:
                                        tcp_ranking_thread.send_time_data = [num, z_ranking_time[num - 1]]
                                        tcp_ranking_thread.send_time_flg = True
                                self._signal.emit(num)
                                num_old = num
                            if num >= ball_num:
                                break
                            elif time.time() - time_now > int(ui.lineEdit_time_count_ball.text()):
                                sc.GASetDiReverseCount()  # 输入次数归0
                                # self._signal.emit(0)
                                break
                        else:
                            flg_start['card'] = False
                            self._signal.emit(fail("运动板x输入通信出错！"))
                            break
                        time.sleep(0.01)
                    tcp_ranking_thread.sleep_time = 1  # 恢复正常排名数据包发送频率
                    ScreenShot_Thead.run_flg = True  # 终点截图识别线程
                    Audio_Thead.run_flg = False
                    ui.checkBox_main_music.setChecked(False)
                else:
                    print("次数归0 失败！")
                    flg_start['card'] = False
                    self._signal.emit(fail("运动板x输入通信出错！"))
            except:
                print("接收运动卡输入 运行出错！")
                flg_start['card'] = False
                self._signal.emit(fail("运动板x输入通信出错！"))
            self.run_flg = False


def PlanBallNum_signal_accept(msg):
    print('球数 %s' % msg)
    if isinstance(msg, int):
        ui.lineEdit_ball_num.setText(str(msg))
    else:
        ui.textBrowser.append(msg)


'''
    ScreenShotThead(QThread) 结果截图线程
'''


class ScreenShotThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(ScreenShotThead, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('截图结果识别运行！')
            try:
                for t in range(int(ui.lineEdit_time_sendresult.text()), 0, -1):
                    if int(ui.lineEdit_ball_num.text()) >= 8:
                        break
                    print('结果倒数：', t)
                    time.sleep(1)
                obs_res = get_picture('终点1')  # 拍摄来源
                if obs_res:
                    self._signal.emit(obs_res)
                monitor_res = get_rtsp(rtsp_url)
                if monitor_res:
                    self._signal.emit(monitor_res)
                res = requests.get(url="http://127.0.0.1:8899/stop")  # 发送信号，停止OBS计时
                print('比赛结束:', res)
                if obs_res[1] == monitor_res[1]:
                    print('识别正确:', obs_res[1])
                tb_source = ui.tableWidget_Sources
                for row_num in range(0, tb_source.rowCount()):
                    if tb_source.item(row_num, 1).text() == '浏览器':
                        item_id = source_list[row_num][2]
                        flg_enable = False
                        res = cl_requst.set_scene_item_enabled('现场', item_id,
                                                               flg_enable)  # 打开视频来源
                        print(res)
                    if tb_source.item(row_num, 1).text() == '画中画':
                        item_id = source_list[row_num][2]
                        flg_enable = False
                        res = cl_requst.set_scene_item_enabled('现场', item_id,
                                                               flg_enable)  # 打开视频来源
                        print(res)
                    if tb_source.item(row_num, 1).text() == '结算页':
                        item_id = source_list[row_num][2]
                        flg_enable = True
                        res = cl_requst.set_scene_item_enabled('现场', item_id,
                                                               flg_enable)  # 打开视频来源
                        print(res)
                if ui.checkBox_restart.isChecked():
                    ReStart_Thead.run_flg = True  # 1分钟后重启动作
                    print('1分钟后重启动作!')
            except:
                print("截图识别中断！")
                flg_start['obs'] = False
                self._signal.emit(fail("结果截图识别中断！"))
            self.run_flg = False


def ScreenShot_signal_accept(msg):
    global main_Camera, monitor_Camera, fit_Camera
    try:
        if isinstance(msg, list):
            img = msg[0]
            msg_list = eval(msg[1])
            pixmap = QPixmap()
            pixmap.loadFromData(img)
            pixmap = pixmap.scaled(int(400 * 1.6), int(225 * 1.6))
            if msg[2] == 'obs':
                ui.label_main_picture.setPixmap(pixmap)
                main_Camera = camera_to_num(msg_list)
            elif msg[2] == 'monitor':
                ui.label_monitor_picture.setPixmap(pixmap)
                monitor_Camera = camera_to_num(msg_list)
            for index in range(len(main_Camera)):
                fit_Camera[index] = (main_Camera[index] == monitor_Camera[index])
            if perfect_Camera == fit_Camera:
                ui.lineEdit_result_send.setText(str(main_Camera[:8]))
            msg_list = eval(msg[1])

            color_list = ''
            for m in msg_list:
                if m in color_ch.keys():
                    color_list = '%s %s' % (color_list, color_ch[m])
            ui.textBrowser_background_data.append(color_list)
        else:
            ui.textBrowser.append(str(msg))
    except:
        print('OBS 操作失败！')


'''
    PlanObsThead(QThread) 摄像头运动方案线程
'''


class PlanObsThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanObsThead, self).__init__()
        self.plan_obs = '0'  # [开关,场景名称]
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

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
                        cl_requst.set_current_program_scene(obs_msg[1])
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
                                cl_requst.set_scene_item_enabled(scene_name, item_id,
                                                                 flg_enable)  # 打开视频来源
                                break
                    elif obs_msg[0] in ['12']:
                        # print(obs_msg[1])
                        obs_res = get_picture(obs_msg[1])  # 拍摄来源
                        if obs_res:
                            self._signal.emit(obs_res)
                        monitor_res = get_rtsp(rtsp_url)
                        if monitor_res:
                            print(monitor_res[0][:60])
                            self._signal.emit(monitor_res)
                else:
                    print('没有切换的场景！')
            except:
                print("OBS 截图中断！")
                flg_start['obs'] = False
                self._signal.emit(fail("OBS 场景切换中断！"))
            self.run_flg = False


def PlanObs_signal_accept(msg):
    global main_Camera, monitor_Camera, fit_Camera
    try:
        if isinstance(msg, list):
            img = msg[0]
            msg_list = eval(msg[1])
            pixmap = QPixmap()
            pixmap.loadFromData(img)
            pixmap = pixmap.scaled(int(400 * 1.6), int(225 * 1.6))
            if msg[2] == 'obs':
                ui.label_main_picture.setPixmap(pixmap)
                main_Camera = camera_to_num(msg_list)
            elif msg[2] == 'monitor':
                ui.label_monitor_picture.setPixmap(pixmap)
                monitor_Camera = camera_to_num(msg_list)
            for index in range(len(main_Camera)):
                fit_Camera[index] = (main_Camera[index] == monitor_Camera[index])
            if perfect_Camera == fit_Camera:
                ui.lineEdit_result_send.setText(str(main_Camera[:8]))
            msg_list = eval(msg[1])

            color_list = ''
            for m in msg_list:
                if m in color_ch.keys():
                    color_list = '%s %s' % (color_list, color_ch[m])
            ui.textBrowser_background_data.append(color_list)
        else:
            ui.textBrowser.append(str(msg))
    except:
        print('OBS 操作失败！')


'''
    AxisThead(QThread) 轴复位线程
'''


class AxisThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(AxisThead, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        global flg_start
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            print('串口运行')
            try:
                if flg_start['s485']:
                    self._signal.emit(succeed('轴复位开始！'))
                    datas = s485.get_axis_pos()
                    print(datas)
                    if datas:
                        for data in datas:
                            if data['nAxisNum'] in [1, 5]:  # 轴一，轴五，方向反过来，所以要设置负数
                                data['highPos'] = -data['highPos']
                            res = sc.GASetPrfPos(data['nAxisNum'], data['highPos'])
                            if res == 0:
                                flg_start['card'] = True
                                Pos_Thead.run_flg = True
                                sc.card_move(int(data['nAxisNum']), 0)
                        res = sc.card_update()
                        if res == 0:
                            self._signal.emit(succeed('轴复位完成！'))
                        else:
                            self._signal.emit(fail('运动卡链接出错！'))
                else:
                    self._signal.emit(fail('复位串口未连接！'))
            except:
                print("轴复位出错！")
                self._signal.emit(fail('轴复位出错！'))
            self.run_flg = False


'''
    CmdThead(QThread) 执行运动方案线程
'''


class PlanCmdThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(PlanCmdThead, self).__init__()
        self.run_flg = False
        self.cmd_next = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        global action_area
        global ranking_time_start
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            if flg_start['card'] and action_area[1] < max_lap_count:
                Audio_Thead.run_flg = True
                ui.checkBox_main_music.setChecked(True)
                self._signal.emit(succeed("运动流程：开始！"))
                self.cmd_next = False  # 初始化手动快速跳过下一步动作标志
                cb_index = ui.comboBox_plan.currentIndex()
                for plan_num in range(0, len(plan_list)):
                    print('第 %s 个动作，识别在第 %s 区 %s 圈！' % (plan_num + 1, action_area[0], action_area[1]))
                    if (not self.run_flg) or (not flg_start['card']):
                        print('动作未开始！')
                        break
                    if plan_list[plan_num][0] == '1' and (
                            (action_area[1] < int(plan_list[plan_num][1]) or (
                                    int(plan_list[plan_num][1]) == 0))):  # 是否勾选,且在圈数范围内
                        self._signal.emit(plan_num)
                        try:
                            sc.card_move(1, int(plan_list[plan_num][2]), vel=int(plan_list[plan_num][7]),
                                         dAcc=float(plan_list[plan_num][8]),
                                         dDec=float(plan_list[plan_num][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(2, int(plan_list[plan_num][3]), vel=int(plan_list[plan_num][7]),
                                         dAcc=float(plan_list[plan_num][8]),
                                         dDec=float(plan_list[plan_num][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(3, int(plan_list[plan_num][4]), vel=int(plan_list[plan_num][7]),
                                         dAcc=float(plan_list[plan_num][8]),
                                         dDec=float(plan_list[plan_num][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(4, int(plan_list[plan_num][5]), vel=int(plan_list[plan_num][7]),
                                         dAcc=float(plan_list[plan_num][8]),
                                         dDec=float(plan_list[plan_num][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(5, int(plan_list[plan_num][6]), vel=int(plan_list[plan_num][7]),
                                         dAcc=float(plan_list[plan_num][8]),
                                         dDec=float(plan_list[plan_num][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            res = sc.card_update()
                            if res != 0:
                                print("运动板通信出错！")
                                flg_start['card'] = False
                                self._signal.emit(fail("运动板通信出错！"))

                            # print("开启机关")
                            if int(plan_list[plan_num][12]) != 0:
                                if '-' in plan_list[plan_num][12]:
                                    sc.GASetExtDoBit(abs(int(plan_list[plan_num][12])) - 1, 0)
                                else:
                                    sc.GASetExtDoBit(abs(int(plan_list[plan_num][12])) - 1, 1)
                                if plan_list[plan_num][12] == '2':  # 闸门机关打开即开始计时
                                    ranking_time_start = time.time()
                                    if flg_start['obs']:
                                        try:
                                            res = requests.get(url="http://127.0.0.1:8899/start")
                                            print('比赛开始：', res, ranking_time_start)
                                        except:
                                            print('OBS脚本开始错误！')
                            if int(plan_list[plan_num][15]) > 0:  # 播放音效
                                tb_audio = ui.tableWidget_Audio
                                audio_row_count = tb_audio.rowCount()
                                # print('~~~~~~~~~~~~~~~~~~~~音效', plan_list[plan_num][15])
                                if int(plan_list[plan_num][15]) - 1 < audio_row_count:
                                    sound_file = tb_audio.item(int(plan_list[plan_num][15]) - 1, 0).text()
                                    sound_times = int(tb_audio.item(int(plan_list[plan_num][15]) - 1, 1).text())
                                    sound_delay = int(tb_audio.item(int(plan_list[plan_num][15]) - 1, 2).text()) * 1000
                                    print(sound_file, sound_times, sound_delay)
                                    # 加载音效
                                    sound_effect = pygame.mixer.Sound(sound_file)
                                    sound_effect.play(loops=sound_times, maxtime=sound_delay)  # 播放音效
                        except:
                            print("运动板运行出错！")
                            flg_start['card'] = False
                            self._signal.emit(fail("运动板通信出错！"))

                        if ui.checkBox_test.isChecked():
                            time.sleep(2)  # 测试期间停两秒切换下一个动作
                        elif int(plan_list[plan_num][14]) <= 0:
                            pass  # 负数则直接下一个动作
                        else:
                            t_over = 0
                            while True:  # 正式运行，等待球进入触发区域再进行下一个动作
                                if not self.run_flg:
                                    print('动作等待中！')
                                    break
                                if (int(camera_points[int(plan_list[plan_num][14])][cb_index + 1][0][0])
                                        in [action_area[0], action_area[0] - 1, action_area[0] + 1]):
                                    break
                                # if int(plan_list[plan_num][13]) in [action_area[0], action_area[0] - 1, action_area[0] + 1]:
                                #     break
                                t_over += 1
                                if t_over == 60:
                                    print('等待超时！')
                                    break
                                if self.cmd_next:
                                    break
                                time.sleep(0.1)
                        if self.cmd_next:  # 快速执行下一个动作
                            self.cmd_next = False
                            continue
                        if self.run_flg:
                            if int(plan_list[plan_num][11]) != 0:  # 摄像头延时，也可以用作动作延时
                                if int(plan_list[plan_num][10]) != 0:  # 摄像头缩放
                                    PlanCam_Thead.camitem = [int(plan_list[plan_num][10]),
                                                             int(plan_list[plan_num][11])]
                                    PlanCam_Thead.run_flg = True  # 摄像头线程
                                time.sleep(int(plan_list[plan_num][11]))
                            plan_col_count = len(plan_list[plan_num])
                            if '_' in plan_list[plan_num][plan_col_count - 1]:
                                PlanObs_Thead.plan_obs = plan_list[plan_num][plan_col_count - 1]
                                PlanObs_Thead.run_flg = True  # 切换场景线程
                                print('######################', len(plan_list), plan_num)
                            if (len(plan_list) - 6 <= plan_num) and (
                                    action_area[1] >= max_lap_count - 1):
                                if len(plan_list) - 3 <= plan_num:
                                    PlanBallNum_Thead.run_flg = True  # 终点计数器线程
                                    tcp_ranking_thread.sleep_time = 0.1  # 终点时间发送设置
                                if not ui.checkBox_test.isChecked():  # 非测试模式才关闭
                                    # 流程完成则打开终点开关，关闭闸门，关闭弹射
                                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                                    sc.GASetExtDoBit(0, 0)  # 关闭弹射
                        if plan_num == len(plan_list) - 1:
                            action_area[0] = 1
                            action_area[1] += 1
                if not ui.checkBox_test.isChecked() and not self.run_flg:  # 非测试模式才关闭
                    # 流程完成则打开终点开关，关闭闸门，关闭弹射
                    print('另外开关~~~~~~~~~')
                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                    sc.GASetExtDoBit(0, 0)  # 关闭弹射
                if ui.checkBox_test.isChecked():  # 如果是测试模式，不用算圈数
                    self.run_flg = False
            else:
                if not ui.checkBox_test.isChecked():  # 非测试模式，流程结束始终关闭闸门
                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                    sc.GASetExtDoBit(0, 0)  # 关闭弹射
                self._signal.emit(succeed("运动流程：完成！"))
                print('动作已完成！')
                if not flg_start['card']:
                    self._signal.emit(fail("运动卡未链接！"))
                self.run_flg = False


def signal_accept(message):
    global p_now
    # print(message)
    try:
        if isinstance(message, int):
            # print('动作位置 %s %s' % (message, p_now))
            if ui.checkBox_follow.isChecked():
                tb_step = ui.tableWidget_Step
                col_num = tb_step.columnCount()
                # print(col_num)
                for col in range(1, col_num - 2):
                    tb_step.item(p_now, col).setBackground(QBrush(QColor(255, 255, 255)))
                    tb_step.item(message, col).setBackground(QBrush(QColor(255, 0, 255)))
                p_now = message
        else:
            ui.textBrowser.append(str(message))
            if str(message) == succeed("运动流程：完成！"):
                p_now = 0
    except:
        print("运行数据处理出错！")


class KeyListenerThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(KeyListenerThead, self).__init__()

    def run(self) -> None:
        with pynput.keyboard.Listener(on_press=keyboard_press, on_release=keyboard_release) as lsn:
            lsn.join()


def keyboard_release(key):
    global flg_key_run
    if ui.checkBox_key.isChecked() and flg_start['card']:
        try:
            if key == key.up:
                print('前')
                # sc.card_stop(2)
                flg_key_run = True
                sc.card_setpos(2, pValue[1] + 30000)
                sc.card_update()

            if key == key.down:
                print('后')
                # sc.card_stop(2)
                flg_key_run = True
                sc.card_setpos(2, pValue[1] - 30000)
                sc.card_update()

            if key == key.left:
                print('左')
                # sc.card_stop(1)
                flg_key_run = True
                sc.card_setpos(1, pValue[0] + 30000)
                sc.card_update()

            if key == key.right:
                print('右')
                # sc.card_stop(1)
                flg_key_run = True
                sc.card_setpos(1, pValue[0] - 30000)
                sc.card_update()

            if key == key.insert:
                print('上')
                flg_key_run = True
                sc.card_setpos(3, pValue[2] - 30000)
                sc.card_update()

            if key == key.delete:
                print('下')
                flg_key_run = True
                sc.card_setpos(3, pValue[2] + 30000)
                sc.card_update()

            if key == key.home:
                print('头左')
                flg_key_run = True
                sc.card_setpos(4, pValue[3] - 30000)
                sc.card_update()

            if key == key.end:
                print('头右')
                flg_key_run = True
                sc.card_setpos(4, pValue[3] + 30000)
                sc.card_update()

            if key == key.page_up:
                print('头上')
                flg_key_run = True
                sc.card_setpos(5, pValue[4] - 30000)
                sc.card_update()

            if key == key.page_down:
                print('头下')
                flg_key_run = True
                sc.card_setpos(5, pValue[4] + 30000)
                sc.card_update()

        except AttributeError:
            pass
            # print(key)
        try:
            if key.char == '-':
                s485.cam_zoom_on_off()
            elif key.char == '+':
                s485.cam_zoom_on_off()
        except:
            pass
            # print(key)
        Pos_Thead.run_flg = False


def keyboard_press(key):
    global flg_key_run
    # if key == key.:
    #     pass
    if ui.checkBox_key.isChecked() and flg_start['card']:
        try:
            Pos_Thead.run_flg = True
            if key == key.up:
                print('前')
                if flg_key_run:
                    sc.card_move(2, pos=2000000)
                    sc.card_update()
                    flg_key_run = False

            elif key == key.down:
                print('后')
                if flg_key_run:
                    sc.card_move(2, pos=-2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.left:
                print('左')
                if flg_key_run:
                    sc.card_move(1, pos=2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.right:
                print('右')
                if flg_key_run:
                    sc.card_move(1, pos=-2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.insert:
                print('上')
                if flg_key_run:
                    sc.card_move(3, pos=-2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.delete:
                print('下')
                if flg_key_run:
                    sc.card_move(3, pos=2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.home:
                print('头左')
                if flg_key_run:
                    sc.card_move(4, pos=-2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.end:
                print('头右')
                if flg_key_run:
                    sc.card_move(4, pos=2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_up:
                print('头下')
                if flg_key_run:
                    sc.card_move(5, pos=-2000000)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_down:
                print('头上')
                if flg_key_run:
                    sc.card_move(5, pos=2000000)
                    sc.card_update()
                    flg_key_run = False
        except AttributeError:
            # print(key)
            pass
        try:
            if key.char == '+':
                s485.cam_zoom_move(5)
            elif key.char == '-':
                s485.cam_zoom_move(-5)
        except:
            pass
            # print(key)


# 保存方案
def save_plan_yaml():
    global plan_list
    global plan_all
    tb_step = ui.tableWidget_Step
    row_num = tb_step.rowCount()
    col_count = tb_step.columnCount()
    if row_num == 0:
        return
    plan_list = []
    local_list = []
    for row in range(0, row_num):
        if tb_step.cellWidget(row, 0):
            if tb_step.cellWidget(row, 0).isChecked():
                local_list.append("1")
            else:
                local_list.append("0")
        for col in range(1, col_count - 2):
            local_list.append(
                "0" if (not tb_step.item(row, col) or tb_step.item(row, col).text() == '') else tb_step.item(row,
                                                                                                             col).text())
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
                "0" if (not tb_step.item(row, col_count - 2) or tb_step.item(row,
                                                                             col_count - 2).text() == '') else tb_step.item(
                    row,
                    col_count - 2).text())
        plan_list.append(local_list)
        local_list = []
    print(plan_list)

    comb = ui.comboBox_plan
    plan_num = comb.currentIndex()
    plan_name = comb.currentText()

    file = "Plan_config.yml"
    if os.path.exists(file):
        plan_all['plans']['plan%d' % (plan_num + 1)]['plan_name'] = plan_name
        plan_all['plans']['plan%d' % (plan_num + 1)]['plan_list'] = plan_list
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


def save_main_yaml():
    file = "main_config.yml"
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                main_all = yaml.safe_load(f)
                if ui.lineEdit_time_sendresult.text().isdigit():
                    main_all['time_send_result'] = ui.lineEdit_time_sendresult.text()
                if ui.lineEdit_time_count_ball.text().isdigit():
                    main_all['time_count_ball'] = ui.lineEdit_time_count_ball.text()
                if ui.lineEdit_Countdown.text().isdigit():
                    main_all['Countdown'] = ui.lineEdit_Countdown.text()
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(main_all, f, allow_unicode=True)
            f.close()
            ui.textBrowser.append(succeed('方案保存：成功'))
        except:
            ui.textBrowser.append(fail('方案保存：失败'))
        print("保存成功~！")


def load_main_yaml():
    file = "main_config.yml"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            main_all = yaml.safe_load(f)
            f.close()
            ui.lineEdit_CarNo.setText(str(main_all['cardNo']))
            ui.lineEdit_time_sendresult.setText(str(main_all['time_send_result']))
            ui.lineEdit_time_count_ball.setText(str(main_all['time_count_ball']))
            ui.lineEdit_Countdown.setText(str(main_all['Countdown']))

            s485.s485_Axis_No = main_all['s485_Axis_No']
            s485.s485_Cam_No = main_all['s485_Cam_No']
        except:
            pass
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
        cb.setStyleSheet('QCheckBox{margin:6px};')
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
                        "0" if not plan[col] else plan[col])
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    tb_step.setItem(num, col, item)
            else:
                item = QTableWidgetItem(str(plan[col]))
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


# 进入下一步动作
def cmd_next():
    PlanCmd_Thead.cmd_next = True


# 关闭动作循环
def cmd_stop():
    PlanCmd_Thead.run_flg = False
    reset_ranking_array()


# 打开运动卡
def card_start():
    global flg_start
    cardnum = ui.lineEdit_CarNo.text()
    if cardnum.isdigit() and not (flg_start['card']):
        res = sc.card_open(int(cardnum))
        print(res)
        if res == 0:
            # flg_start['card'] = True
            ui.textBrowser.append(succeed('启动板卡：%s' % card_res[res]))
        else:
            ui.textBrowser.append(res)
    else:
        ui.textBrowser.append(fail('运动卡已链接~！'))

    if not flg_start['s485']:
        flg_start['s485'] = s485.cam_open()
        if flg_start['s485']:
            Axis_Thead.run_flg = True  # 轴复位
        ui.textBrowser.append(succeed('串口链接：%s' % flg_start['s485']))
    else:
        ui.textBrowser.append(fail('串口链接：%s' % flg_start['s485']))
    if not flg_start['obs']:
        if not Obs_Thead.isRunning():
            Obs_Thead.start()


def cmd_run():
    global p_now
    save_plan_yaml()
    p_now = 0
    reset_ranking_array()
    activate_browser()  # 刷新OBS中排名浏览器
    PlanCmd_Thead.run_flg = True


def card_reset():
    Axis_Thead.run_flg = True


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
    if col in [0, col_count - 2] or row < 0 or col < 0:
        return
    try:
        # print(len(plan_list[row]), col)
        if col > len(plan_list[row]) - 1:
            if tb_step.item(row, col):
                tb_step.item(row, col).setText('')
        elif not is_natural_num(tb_step.item(row, col).text()):
            if tb_step.item(row, col):
                tb_step.item(row, col).setText(plan_list[row][col])
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
            r = requests.post(url=wakeup_addr, data=form_data)
            print(r.text)
            if r == 'ok':
                flg_start['ai'] = True
        except:
            print('图像识别主机通信失败！')
        time.sleep(300)


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
        # 'saveImgNum': '0,1,2,3,4,5,6,7,8',
        'saveImgNum': '1',
        # 'saveImgPath': 'D:/saidao',
    }
    try:
        r = requests.post(url=wakeup_addr, data=form_data)
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
                    part = len(map_orbit) / (max_area_count - ball_num + 1)
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
        map_data = ['./img/09_沙漠.jpg', './img/09_沙漠.json']  # 卫星地图资料
        img = map_data[0]
        pixmap = QPixmap(img)
        # 设置label的尺寸
        self.setMaximumSize(picture_size, picture_size)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

        self.color_names = {'red': QColor(255, 0, 0), 'green': QColor(0, 255, 0), 'blue': QColor(0, 0, 255),
                            'pink': QColor(255, 0, 255), 'yellow': QColor(255, 255, 0), 'black': QColor(0, 0, 0),
                            'purple': QColor(128, 0, 128), 'orange': QColor(255, 165, 0)}
        # , 'White': QColor(248, 248, 255),
        # 'Brown': QColor(139, 69, 19)}

        self.path_points = []
        with open(map_data[1], 'r', encoding='utf-8') as fcc_file:
            fcc_data = json.load(fcc_file)
        scale = picture_size / 860  # 缩放比例
        for p in fcc_data[0]["content"]:
            self.path_points.append((p['x'] * scale, p['y'] * scale))
        self.path_points = divide_path(self.path_points, step_length)
        if scale == 1:
            map_orbit = self.path_points

        self.ball_space = ball_space  # 球之间的距离
        self.ball_radius = ball_radius  # 小球半径
        # self.num_balls = 8  # 8个小球
        self.speed = 1  # 小球每次前进的步数（可以根据需要调整）
        self.flash_time = flash_time
        self.positions = []  # 每个球的当前位置索引
        for num in range(ball_num):
            self.positions.append([num * self.ball_space, QColor(255, 0, 0)])

        # 创建定时器，用于定时更新球的位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)  # 定时触发更新
        self.timer.start(self.flash_time)  # 每1秒更新一次

    def update_positions(self):
        # 更新每个小球的位置
        p_num = 0
        for num in range(0, len(ranking_array)):
            if ranking_array[num][5] in self.color_names.keys():
                color = self.color_names[ranking_array[num][5]]
                if ranking_array[num][6] == 0:  # 起点
                    if p_num == 0:
                        index = len(ranking_array) * self.ball_space
                    else:
                        index = len(ranking_array) * self.ball_space - p_num * self.ball_space
                elif (ranking_array[num][6] >= max_area_count - ball_num + 1
                      and ranking_array[num][8] >= max_lap_count - 1):  # 最后一圈处理
                    if p_num == 0:
                        index = len(self.path_points) - 1
                    else:
                        index = len(self.path_points) - 1 - p_num * self.ball_space
                elif ranking_array[num][8] == action_area[1]:  # 同圈才运动
                    area_num = max_area_count - ball_num  # 跟踪区域数量
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
                    area_num = max_area_count - ball_num  # 跟踪区域数量
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
                # if index >= len(self.path_points):
                #     self.positions[p_num][0] = 0  # 回到起点循环运动
                p_num += 1

        # 触发重绘
        self.update()

    # 通过重载paintEvent方法进行自定义绘制
    def paintEvent(self, event):
        # 调用父类的 paintEvent 以确保 QLabel 正常显示文本或图片
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if ui.checkBox_show_orbit.isChecked():
            for index in range(len(self.path_points)):
                part = len(self.path_points) / (max_area_count - ball_num + 1)
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
        for i in range(len(self.positions)):
            index = self.positions[i][0]  # 获取当前球的路径索引
            if index in range(len(self.path_points)):
                x, y = self.path_points[index]
                # 设置球的颜色
                painter.setBrush(QBrush(self.positions[i][1], Qt.SolidPattern))
                # 绘制球
                painter.drawEllipse(int(x - self.ball_radius), int(y - self.ball_radius),
                                    self.ball_radius * 2, self.ball_radius * 2)

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
            ui.textBrowser.append(succeed('方案保存：成功'))
        except:
            ui.textBrowser.append(fail('方案保存：失败'))
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

    audio_points_count = len(audio_points) - 1
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

    ai_points_count = len(ai_points)
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
                res = QMessageBox.warning(ui, '提示', '其他方案存在该点位！是否强制删除？',
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
                res = QMessageBox.warning(ui, '提示', '其他方案存在该点位！是否强制删除？',
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
                res = QMessageBox.warning(ui, '提示', '其他方案存在该点位！是否强制删除？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                print(res)
                if res == QMessageBox.No:
                    return
        ai_points[ai_points_count][0].delete_self()
        ai_points.pop(ai_points_count)

    ai_points_count = len(ai_points)
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


def play_audio():
    pass


"****************************************卫星图_结束***********************************************"

"****************************************分机结果_开始***********************************************"


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
                ui.lineEdit_result_send.setText(str(main_Camera[:8]))
            elif self.Camera_index == 'monitor_Camera':
                ui.lineEdit_result_send.setText(str(monitor_Camera[:8]))
        elif event.button() == Qt.RightButton:
            print("QLabel 被右键点击")


"****************************************分机结果_结束***********************************************"


class AudioThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(AudioThead, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        area_old = 0
        while self.running:
            time.sleep(0.2)
            if not self.run_flg:
                continue
            if len(audio_points) <= 0:
                continue
            plan_index = ui.comboBox_plan.currentIndex() + 1  # 方案索引
            for index in range(1, len(audio_points)):
                # print(audio_points[index][plan_index][0][0])
                if audio_points[index][plan_index][0][0] > 0 and (area_old != action_area) and (
                        audio_points[index][plan_index][0][0] == action_area[0]):
                    tb_audio = ui.tableWidget_Audio
                    sound_file = tb_audio.item(index - 1, 0).text()
                    sound_times = int(tb_audio.item(index - 1, 1).text())
                    sound_delay = int(tb_audio.item(index - 1, 2).text())
                    print(sound_file, sound_times, sound_delay)
                    # 加载音效
                    sound_effect = pygame.mixer.Sound(sound_file)
                    sound_effect.play(loops=sound_times, maxtime=sound_delay * 1000)  # 播放音效
                    area_old = copy.deepcopy(action_area)
                    print('~~~~~~~~~~~~~', area_old, audio_points[index][plan_index][0][0], action_area[0])
                    break


def audio_signal_accept(msg):
    try:
        pass
    except:
        print("轴数据显示错误！")


def pygame_loop():
    # 主循环，确保程序运行一段时间来听到音乐和音效
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)  # 每100ms检查一次


def music_ctl():
    if ui.checkBox_main_music.isChecked():
        for index in range(1, 4):
            if getattr(ui, 'radioButton_music_%s' % index).isChecked():
                mp3_name = './mp3/07_冰原背景音乐%s.mp3' % index
                break
        # 加载并播放背景音乐
        pygame.mixer.music.load(mp3_name)
        pygame.mixer.music.play(-1)  # 循环播放背景音乐
    else:
        pygame.mixer.music.stop()


class TestThead(QThread):
    _signal = Signal(object)

    def __init__(self):
        super(TestThead, self).__init__()
        self.run_flg = False
        self.obs_name = '终点1'
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出

    def run(self) -> None:
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            # cl_requst.save_source_screenshot(self.obs_name, "jpg", 'd:/img/%s/%s.jpg' % (self.obs_name, time.time()),
            #                                  1920, 1080, 100)
            # time.sleep(2)
            # 加载并播放音频文件
            pygame.mixer.music.load('./mp3/example.mp3')
            pygame.mixer.music.play()

            # 等待音频播放完成
            while pygame.mixer.music.get_busy():
                pass
            self.run_flg = False


def test_signal_accept(msg):
    try:
        pass
    except:
        print("轴数据显示错误！")


def card_close_all():
    if flg_start['card']:
        for index in range(0, 16):
            sc.GASetExtDoBit(index, 0)
            time.sleep(0.1)
        ui.textBrowser.append(succeed('已经关闭所有机关！'))


def my_test():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~')
    # 加载音效
    sound_effect = pygame.mixer.Sound('D:/pythonProject/Main_controller/mp3/07_冰原起泡准备声1.wav')
    sound_effect.play(loops=10, maxtime=5000)  # 播放音效
    # activate_browser()
    # Test_Thead.obs_name = '终点2'
    # Test_Thead.run_flg = not (Test_Thead.run_flg)
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


class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.aboutToQuit.connect(self.onAboutToQuit)

    @Slot()
    def onAboutToQuit(self):
        print("Exiting the application.")
        try:
            # data_list = [
            #     {
            #         'requestType': 'set_run_toggle',
            #         'run_toggle': '0',
            #     }
            # ]
            # 运行事件循环
            # asyncio.run(post_main(wakeup_addr, data_list))
            # 当准备退出时，关闭所有服务
            PlanCmd_Thead.stop()
            PlanObs_Thead.stop()
            PlanCam_Thead.stop()
            PlanBallNum_Thead.stop()
            reset_thread.stop()
            tcp_ranking_thread.stop()
            udp_thread.stop()
            Update_Thread.stop()
            Test_Thead.stop()
            Axis_Thead.stop()
            Pos_Thead.stop()
            ReStart_Thead.stop()
            Source_Thead.stop()
        except KeyboardInterrupt:
            # 处理键盘中断，例如用户按下Ctrl+C
            pass

        finally:
            # 等待所有线程结束
            print("All servers are closed. Exiting.")


if __name__ == '__main__':
    app = MyApp(sys.argv)
    MainWindow = QMainWindow()

    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()

    z_status = True
    sc = SportCard()  # 运动卡
    s485 = Serial485()  # 摄像头

    plan_list = []  # 当前方案列表 [0.选中,1.圈数,2.左右,3.前后,4.上下,5.头旋转,6.头上下,7.速度,8.加速,9.减速,10.镜头缩放,11.缩放时长,12.机关,13.运动位置,14.卫星图位置,col_count - 2.OBS画面]
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料
    pValue = [0, 0, 0, 0, 0]  # 各轴位置
    p_now = 0  # 保存方案运行位置
    flg_key_run = True  # 键盘控制标志
    flg_start = {'card': False, 's485': False, 'obs': False, 'ai': False, 'ai_end': False, 'server1': False,
                 'server2': False}  # 各硬件启动标志

    load_plan_yaml()
    load_main_yaml()

    KeyListener_Thead = KeyListenerThead()  # 启用键盘监听
    KeyListener_Thead.start()

    PlanCmd_Thead = PlanCmdThead()  # 总运行方案
    PlanCmd_Thead._signal.connect(signal_accept)
    PlanCmd_Thead.start()

    PlanObs_Thead = PlanObsThead()  # OBS场景切换方案
    PlanObs_Thead._signal.connect(PlanObs_signal_accept)
    PlanObs_Thead.start()

    PlanCam_Thead = CamThead()  # 摄像头运行方案
    PlanCam_Thead._signal.connect(signal_accept)
    PlanCam_Thead.start()

    PlanBallNum_Thead = PlanBallNumThead()  # 统计过终点的球数
    PlanBallNum_Thead._signal.connect(PlanBallNum_signal_accept)
    PlanBallNum_Thead.start()

    ScreenShot_Thead = ScreenShotThead()  # 统计过终点的球数
    ScreenShot_Thead._signal.connect(ScreenShot_signal_accept)
    ScreenShot_Thead.start()

    Axis_Thead = AxisThead()  # 轴复位
    Axis_Thead._signal.connect(signal_accept)
    Axis_Thead.start()

    Pos_Thead = PosThead()  # 实时监控各轴位置
    Pos_Thead._signal.connect(pos_signal_accept)
    Pos_Thead.start()

    ReStart_Thead = ReStartThead()  # 循环模式
    ReStart_Thead._signal.connect(time_signal_accept)
    ReStart_Thead.start()

    Audio_Thead = AudioThead()  # 音频线程
    Audio_Thead._signal.connect(audio_signal_accept)
    Audio_Thead.start()

    Test_Thead = TestThead()  # 测试线程
    Test_Thead._signal.connect(test_signal_accept)
    Test_Thead.start()

    ui.pushButton_fsave.clicked.connect(save_plan_yaml)
    ui.pushButton_rename.clicked.connect(plan_rename)
    ui.pushButton_CardStart.clicked.connect(card_start)
    ui.pushButton_CardStop.clicked.connect(cmd_stop)
    ui.pushButton_CardRun.clicked.connect(cmd_run)
    ui.pushButton_CardRun_2.clicked.connect(cmd_run)
    ui.pushButton_CardReset.clicked.connect(card_reset)
    ui.pushButton_ToTable.clicked.connect(p_to_table)
    ui.pushButton_Obs2Table.clicked.connect(obs_to_table)
    ui.pushButton_Source2Table.clicked.connect(source_to_table)
    ui.pushButton_Obs_delete.clicked.connect(obs_remove_table)
    ui.pushButton_CardNext.clicked.connect(cmd_next)
    ui.pushButton_to_TXT.clicked.connect(json_txt)
    ui.pushButton_Draw.clicked.connect(open_draw)
    ui.pushButton_test_2.clicked.connect(my_test)
    ui.pushButton_CardCloseAll.clicked.connect(card_close_all)

    ui.checkBox_saveImgs.clicked.connect(save_images)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.comboBox_plan.currentIndexChanged.connect(plan_refresh)
    ui.tableWidget_Step.itemChanged.connect(table_change)

    ui.lineEdit_time_sendresult.editingFinished.connect(save_main_yaml)
    ui.lineEdit_time_count_ball.editingFinished.connect(save_main_yaml)
    ui.lineEdit_Countdown.editingFinished.connect(save_main_yaml)

    """
        OBS 处理
    """
    source_list = []  # OBS来源列表
    scene_now = ''
    cl_requst = ''  # 请求
    cl_event = ''  # 监听

    Obs_Thead = ObsThead()  # OBS启动线程
    Obs_Thead._signal.connect(obs_signal_accept)

    Source_Thead = SourceThead()  # OBS来源入表线程
    Source_Thead._signal.connect(source_signal_accept)
    Source_Thead.start()

    ui.pushButton_ObsConnect.clicked.connect(obs_open)
    ui.comboBox_Scenes.currentTextChanged.connect(scenes_change)

    "**************************OBS*****************************"

    "**************************图像识别算法_开始*****************************"
    # set_run_toggle 发送请求运行数据
    camera_num = 8  # 摄像头数量
    area_Code = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}  # 摄像头代码列表
    load_area()  # 初始化区域划分
    # print(area_Code)

    action_area = [1, 0]  # 触发镜头向下一个位置活动的点位
    ball_num = 8  # 运行球数
    ranking_array = []  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]
    ball_sort = []  # 位置寄存器

    # 初始化数据
    max_lap_count = 1  # 最大圈
    max_area_count = 39  # 统计一圈的位置差
    reset_time = 60  # 等待结束重置时间
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
    udpServer_addr = ('0.0.0.0', 8080)  # 接收图像识别结果
    tcpServer_addr = ('0.0.0.0', 9999)  # pingpong 发送网页排名
    result_tcpServer_addr = ('0.0.0.0', 8888)  # pingpong 发送网页排名
    httpServer_addr = ('0.0.0.0', 8081)  # 接收网络数据包控制
    udpClient_addr = ("192.168.0.161", 19733)  # 数据发送给其他服务器
    wakeup_addr = "http://192.168.0.110:8080"  # 唤醒服务器线程
    rtsp_url = 'rtsp://admin:123456@192.168.0.29:554/Streaming/Channels/101'  # 主码流
    load_ballsort_yaml()
    # print(map_data)

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

    # 自动重置排名线程
    reset_thread = ResetThead()
    reset_thread._signal.connect(reset_signal_accept)
    reset_thread.start()

    # 1. Udp 接收数据
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(udpServer_addr)
        print('Udp_socket Server Started.')
        udp_thread = UdpThead()
        udp_thread._signal.connect(udp_signal_accept)
        udp_thread.start()
    except:
        # 使用infomation信息框
        QMessageBox.information(ui, "UDP", "UDP端口被占用")
        # sys.exit()

    # pingpong 发送排名
    tcp_ranking_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ranking_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_ranking_socket.bind(tcpServer_addr)
    tcp_ranking_socket.listen(1)
    print('Pingpong Server Started.')
    tcp_ranking_thread = TcpRankingThead()  # 前端网页以pingpong形式发送排名数据
    tcp_ranking_thread._signal.connect(tcp_signal_accept)
    tcp_ranking_thread.start()

    tcp_result_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_result_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_result_socket.bind(result_tcpServer_addr)
    tcp_result_socket.listen(5)
    tcp_result_thread = TcpResultThead()  # 前端网页以pingpong形式发送结果数据
    tcp_result_thread._signal.connect(tcp_signal_accept)
    tcp_result_thread.start()

    # 唤醒图像识别主机线程
    wakeup_ser = threading.Thread(target=wakeup_server, daemon=True)
    wakeup_ser.start()

    # 启动 HTTPServer 接收外部命令控制本程序
    httpd = HTTPServer(httpServer_addr, SimpleHTTPRequestHandler)
    http_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    http_thread.start()

    # 更新数据表线程
    Update_Thread = UpdateThread()
    Update_Thread._signal.connect(ranking_signal_accept)
    Update_Thread.start()

    ui.pushButton_save_Ranking.clicked.connect(save_ballsort_yaml)
    ui.pushButton_reset_Ranking.clicked.connect(reset_ranking_array)

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

    # pygame 声音循环线程
    game_loop = threading.Thread(target=pygame_loop, daemon=True)
    game_loop.start()
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

    "**************************分机结果_结束*****************************"

    sys.exit(app.exec())
