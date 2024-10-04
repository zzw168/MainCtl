import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import cv2
import numpy as np
import pynput
import requests
import yaml

from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu

import obsws_python as obs

from utils.SportCard_unit import *
from utils.tool_unit import *
from utils.Serial485_unit import *
from MainCtl_Ui import *
from utils.pingpong_socket import *

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
    _signal = pyqtSignal(object)

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
    _signal = pyqtSignal(object)

    def __init__(self):
        super(SourceThead, self).__init__()
        self.run_flg = False

    def run(self) -> None:
        while True:
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
    tb_source = ui.tableWidget_Sources
    row_num = tb_source.currentRow()
    source_list[row_num][0] = not (source_list[row_num][0])
    source_enable = source_list[row_num][0]
    cb_scene = ui.comboBox_Scenes
    scene_name = cb_scene.currentText()
    item_id = source_list[row_num][2]
    # print(source_list)
    # 打开,关闭来源
    try:
        cl_requst.set_scene_item_enabled(scene_name, item_id, source_enable)  # 打开视频来源
    except:
        ui.textBrowser.append(fail("OBS 链接中断！"))


def get_scenes_list():  # 刷新所有列表
    try:
        res = cl_requst.get_scene_list()  # 获取场景列表
        res_name = cl_requst.get_current_program_scene()  # 获取激活的场景
    except:
        ui.textBrowser.append(fail("OBS 链接中断！"))
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
    for item in res.scene_items:
        source_list.append([item['sceneItemEnabled'], item['sourceName'], item['sceneItemId']])
        # print('取得来源列表 %s' % item)
    Source_Thead.run_flg = True


def scenes_change():  # 变换场景
    scene_name = ui.comboBox_Scenes.currentText()
    try:
        cl_requst.set_current_program_scene(scene_name)
    except:
        ui.textBrowser.append(fail("OBS 链接中断！"))


# 截取OBS图片
def get_picture(scence_current):
    resp = cl_requst.get_source_screenshot(scence_current, "jpg", None, None, 100)
    # print(resp.image_data)
    img = str2image(resp.image_data)
    # str2image_file(resp.image_data, './a.jpg')
    pixmap = QPixmap()
    pixmap.loadFromData(img)
    pixmap = pixmap.scaled(800, 450)
    lab_p = ui.label_picture
    lab_p.setPixmap(pixmap)


"******************************OBS结束*************************************"

"************************************图像识别_开始****************************************"


def deal_rank(integration_qiu_array):
    global ranking_array
    for r_index in range(0, len(ranking_array)):
        replaced = False
        for q_item in integration_qiu_array:
            if ranking_array[r_index][5] == q_item[5]:  # 更新 ranking_array
                if q_item[6] < ranking_array[r_index][6]:  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                    result_count = ranking_array[r_index][6] - q_item[6]
                    if result_count >= max_area_count - 6:
                        ranking_array[r_index][8] += 1
                        if ranking_array[r_index][8] > max_lap_count - 1:
                            ranking_array[r_index][8] = 0
                if ((ranking_array[r_index][6] == 0)  # 等于0 刚初始化，未检测区域
                        or (q_item[6] >= ranking_array[r_index][6] and  # 新位置要大于旧位置
                            (q_item[6] - ranking_array[r_index][6] <= 3  # 新位置相差旧位置三个区域以内
                             or ranking_array[0][6] - ranking_array[r_index][
                                 6] > 5))  # 当新位置与旧位置超过3个区域，则旧位置与头名要超过5个区域才统计
                        or (q_item[6] < 8 and ranking_array[r_index][6] >= max_area_count - 8)):  # 跨圈情况
                    for r_i in range(0, len(q_item)):
                        ranking_array[r_index][r_i] = q_item[r_i]  # 更新 ranking_array
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
        if not (ranking_array[i][5] in ball_sort[ranking_array[i][6]][ranking_array[i][8]]):
            ball_sort[ranking_array[i][6]][ranking_array[i][8]].append(ranking_array[i][5])  # 添加寄存器球排序
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
    action_area = 1
    # print(ball_sort)


def to_num(res):  # 按最新排名排列数组
    global z_response
    arr_res = []
    for r in res:
        for i in range(0, len(init_array)):
            if r[0] == init_array[i][5]:
                arr_res.append(i + 1)
    for i in range(0, len(arr_res)):
        for j in range(0, len(z_response)):
            if arr_res[i] == z_response[j]:
                z_response[i], z_response[j] = z_response[j], z_response[i]


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

        ui.lineEdit_lap_Ranking.setText(str(max_lap_count))
        ui.lineEdit_region_Ranking.setText(str(max_area_count))
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
                and ui.lineEdit_region_Ranking.text().isdigit()
                and ui.lineEdit_time_Ranking.text().isdigit()):
            ballsort_conf['max_lap_count'] = int(ui.lineEdit_lap_Ranking.text())
            ballsort_conf['max_area_count'] = int(ui.lineEdit_region_Ranking.text())
            ballsort_conf['reset_time'] = int(ui.lineEdit_time_Ranking.text())
            max_lap_count = int(ui.lineEdit_lap_Ranking.text())
            max_area_count = int(ui.lineEdit_region_Ranking.text())
            reset_time = int(ui.lineEdit_time_Ranking.text())
            # print(ballsort_conf)
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(ballsort_conf, f, allow_unicode=True)
                ui.textBrowser_msg_Ranking.setText(
                    succeed("%s,%s,%s 保存服务器完成" % (ballsort_conf['max_lap_count'],
                                                         ballsort_conf['max_area_count'],
                                                         ballsort_conf['reset_time'])))
        else:
            ui.textBrowser_msg_Ranking.setText(fail("错误，只能输入数字！"))


def init_ranking_table():
    table = ui.tableWidget_Ranking
    table.setRowCount(10)
    table.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
    table.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
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
                table.setItem(i, j, item)


class UpdateThread(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(UpdateThread, self).__init__()

    def run(self) -> None:
        table = ui.tableWidget_Ranking

        while True:
            time.sleep(1)
            for i in range(0, len(con_data)):
                for j in range(0, len(con_data[i])):
                    if con_data[i][0] in color_ch.keys():
                        if j == 0 and table.item(i, j).text() != color_ch[con_data[i][j]]:
                            self._signal.emit([i, j, color_ch[con_data[i][j]]])
                        elif j != 0 and table.item(i, j).text() != con_data[i][j]:
                            self._signal.emit([i, j, con_data[i][j]])


def ranking_signal_accept(msg):
    table = ui.tableWidget_Ranking
    table.item(msg[0], msg[1]).setText(str(msg[2]))


class TcpThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(TcpThead, self).__init__()

    def run(self) -> None:
        while True:
            try:
                con, addr = tcp_socket.accept()
                # print("Accepted. {0}, {1}".format(con, str(addr)))
                if con:
                    self._signal.emit("Accepted. {0}, {1}".format(con, str(addr)))
                    with WebsocketServer(con) as ws:
                        while True:
                            time.sleep(1)
                            try:
                                d = {'data': z_response, 'type': 'pm'}
                                # d = {'data': np.random.permutation([1, 2, 3, 4, 5, 6, 9, 7, 8, 10]).tolist(),
                                #      'type': 'pm'}
                                ws.send(json.dumps(d))
                            except Exception as e:
                                # print("pingpong 错误：", e)
                                self._signal.emit("pingpong 错误：%s" % e)
                                break
            except Exception as e:
                # print(e)
                self._signal.emit("pingpong 错误：%s" % e)
                break


def tcp_signal_accept(msg):
    print()
    ui.textBrowser_net_data.append(msg)


class UdpThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(UdpThead, self).__init__()
        self.run_flg = True

    def run(self) -> None:
        global action_area
        global con_data
        while True:
            try:
                # 3. 等待接收对方发送的数据
                recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
                if self.run_flg:
                    res = recv_data[0].decode('utf8')
                    data_res = eval(res)  # str转换list
                    self._signal.emit(data_res)
                    array_data = []
                    for i_ in range(1, len(data_res)):  # data_res[0] 是时间戳差值 ms
                        array_data.append(data_res[i_])
                    # print(array_data)
                    array_data = deal_area(array_data, array_data[0][6])  # 收集统计区域内的球
                    if not array_data:
                        continue
                    array_data = filter_max_value(array_data)
                    deal_rank(array_data)
                    for rank_num in range(0, len(ranking_array)):
                        if (int(ranking_array[rank_num][6]) > action_area + 3
                                or (6 - max_area_count < int(  # 跨圈
                                    ranking_array[rank_num][6]) < action_area)):
                            continue
                        action_area = int(ranking_array[rank_num][6])  # 排第一位的球所在区域
                        break
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
    _signal = pyqtSignal(object)

    def __init__(self):
        super(ResetThead, self).__init__()

    def run(self) -> None:
        while True:
            time.sleep(5)
            if ranking_array[0][8] == max_lap_count - 1 and ranking_array[0][6] == max_area_count:
                time.sleep(reset_time)
                reset_ranking_array()
                self._signal.emit('提示:球排名数据已自动重置！')


def reset_signal_accept(msg):
    ui.textBrowser_background_data.clear()
    init_ranking_table()


def load_area():  # 载入位置文件初始化区域列表
    global area_Code
    for key in area_Code.keys():
        # track_file = f"./txts/{key}.txt"
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
        if ball[4] < 0.45:  # 置信度小于 0.45 的数据不处理
            continue
        x = (ball[0] + ball[2]) / 2
        y = (ball[1] + ball[3]) / 2
        point = (x, y)
        if cap_num in area_Code.keys():
            for area in area_Code[cap_num]:
                pts = np.array(area['coordinates'], np.int32)
                Result = cv2.pointPolygonTest(pts, point, False)  # -1=在外部,0=在线上，1=在内部
                if Result > -1.0:
                    ball[6] = area['area_code']
                    ball.append(area['direction'])
                    ball_area_array.append(ball)  # ball结构：x1,y1,x2,y2,置信度,球名,区域号,方向
    return ball_area_array  # ball_area_array = [[x1,y1,x2,y2,置信度,球名,区域号,方向]]


# 33 17 25 29
def filter_max_value(lists):  # 在区域范围内如果出现两个相同的球，则取置信度最高的球为准
    max_values = {}
    for sublist in lists:
        value, key = sublist[4], sublist[5]
        if key not in max_values or max_values[key] < value:
            max_values[key] = value
    filtered_list = []
    for sublist in lists:
        if sublist[4] == max_values[sublist[5]]:  # 选取置信度最大的球添加到修正后的队列
            filtered_list.append(sublist)
    # print(filtered_list)
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

        tb_Step = self.tableWidget_Step
        tb_Step.horizontalHeader().resizeSection(0, 10)
        tb_Step.horizontalHeader().resizeSection(1, 50)
        tb_Step.horizontalHeader().resizeSection(7, 50)
        tb_Step.horizontalHeader().resizeSection(8, 50)
        tb_Step.horizontalHeader().resizeSection(9, 50)
        tb_Step.horizontalHeader().resizeSection(10, 60)
        tb_Step.horizontalHeader().resizeSection(11, 60)
        tb_Step.horizontalHeader().resizeSection(12, 60)
        tb_Step.horizontalHeader().resizeSection(13, 60)
        tb_Step.horizontalHeader().resizeSection(14, 60)
        # tb_Step.setColumnHidden(3, True)
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
            rownum = tb_step.rowCount()
            print(rownum)
            if rownum != 0:
                p = tb_step.currentRow()
                for row in range(p, rownum - 1):
                    print('%d' % row)
                    for col in range(0, tb_step.columnCount() - 1):
                        if col == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet('QCheckBox{margin:6px};')
                            cb.setChecked(tb_step.cellWidget(row + 1, col).isChecked())
                            tb_step.setCellWidget(row, col, cb)
                        elif col == 14:
                            if tb_step.cellWidget(row + 1, col):
                                cb = QCheckBox()
                                cb.setStyleSheet('QCheckBox{margin:6px};')
                                cb.setText(tb_step.cellWidget(row + 1, col).text())
                                cb.setChecked(tb_step.cellWidget(row + 1, col).isChecked())
                                tb_step.setCellWidget(row, col, cb)
                            else:
                                if tb_step.cellWidget(row, col):
                                    tb_step.removeCellWidget(row, col)
                        else:
                            item = QTableWidgetItem(tb_step.item(row + 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb_step.setItem(row, col, item)
                tb_step.setRowCount(rownum - 1)
        if action == item3:
            table = self.tableWidget_Step
            rownum = table.rowCount()
            table.setRowCount(rownum + 1)
            row = table.currentRow()
            if rownum > 0:  # 下移表格
                for r in range(rownum, row, -1):
                    cb = QCheckBox()
                    cb.setStyleSheet('QCheckBox{margin:6px};')
                    table.setCellWidget(r, 0, cb)
                    table.cellWidget(r, 0).setChecked(table.cellWidget(r - 1, 0).isChecked())
                    for col in range(1, table.columnCount() - 1):
                        if col == 14:
                            if tb_step.cellWidget(r - 1, col):
                                cb = QCheckBox()
                                cb.setStyleSheet('QCheckBox{margin:6px};')
                                cb.setText(tb_step.cellWidget(r - 1, col).text())
                                cb.setChecked(tb_step.cellWidget(r - 1, col).isChecked())
                                tb_step.setCellWidget(r, col, cb)
                            else:
                                if tb_step.cellWidget(r, col):
                                    tb_step.removeCellWidget(r, col)
                        else:
                            item = QTableWidgetItem(table.item(r - 1, col).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                            table.setItem(r, col, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                table.setCellWidget(0, 0, cb)

                for r in range(1, table.columnCount() - 1):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(0, r, item)


'''
    ReStartThead(QThread) 重启动作
'''


class ReStartThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(ReStartThead, self).__init__()
        self.run_flg = False

    def run(self) -> None:
        while True:
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
                PlanCmd_Thead.run_flg = True
            # print("循环启动！")
            self.run_flg = False


def time_signal_accept(msg):
    print(msg)
    if int(msg) == 1:
        plan_refresh()
        ui.lineEdit_ball_num.setText('0')
    ui.lineEdit_time.setText(str(msg))


'''
    PosThead(QThread) 检测各轴位置
'''


class PosThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(PosThead, self).__init__()
        self.run_flg = False

    def run(self) -> None:
        global pValue
        while True:
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
    _signal = pyqtSignal(object)

    def __init__(self):
        super(CamThead, self).__init__()
        self.camitem = [5, 5]  # [运行挡位,持续时间]
        self.run_flg = False

    def run(self) -> None:
        while True:
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
    _signal = pyqtSignal(object)

    def __init__(self):
        super(PlanBallNumThead, self).__init__()
        self.run_flg = False

    def run(self) -> None:
        global flg_start
        while True:
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
                                self._signal.emit(num)
                                num_old = num
                            if num >= 10:
                                break
                            elif time.time() - time_now > 30:
                                sc.GASetDiReverseCount()  # 输入次数归0
                                # self._signal.emit(0)
                                break
                        else:
                            flg_start['card'] = False
                            self._signal.emit(fail("运动板x输入通信出错！"))
                            break
                        time.sleep(0.01)
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
    PlanObsThead(QThread) 摄像头运动方案线程
'''


class PlanObsThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(PlanObsThead, self).__init__()
        self.plan_obs = '0'  # [运行挡位,持续时间]
        self.run_flg = False

    def run(self) -> None:
        while True:
            time.sleep(0.01)
            if (not self.run_flg) or (not flg_start['obs']):
                continue
            print('OBS运行')
            try:
                if '_' in self.plan_obs:  # 切换场景
                    obs_msg = str.split(self.plan_obs, '_')
                    # print(obs_msg)
                    if int(obs_msg[0]) == 1:
                        cl_requst.set_current_program_scene(obs_msg[1])
                        self._signal.emit(succeed("OBS 场景切换完成！"))
                    get_picture(obs_msg[1])
                    self._signal.emit(succeed("OBS 截图完成！"))
                else:
                    print('没有切换的场景！')
            except:
                print("OBS 链接中断！")
                flg_start['obs'] = False
                self._signal.emit(fail("OBS 场景切换中断！"))
            self.run_flg = False


'''
    AxisThead(QThread) 轴复位线程
'''


class AxisThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(AxisThead, self).__init__()
        self.run_flg = False

    def run(self) -> None:
        global flg_start
        while True:
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
    _signal = pyqtSignal(object)

    def __init__(self):
        super(PlanCmdThead, self).__init__()
        self.run_flg = False
        self.card_next = False

    def run(self) -> None:
        global action_area
        while True:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            if flg_start['card']:
                self._signal.emit(succeed("运动流程：开始！"))
                self.card_next = False  # 初始化快速动作标志
                reset_ranking_array()  # 初始化排名，位置变量
                for plan_num in range(0, len(plan_list)):
                    # print('第 %s 个动作，识别在第 %s 区！' % (plan_num + 1, action_area))
                    if (not self.run_flg) or (not flg_start['card']):
                        print('动作未开始！')
                        break
                    if plan_list[plan_num][0] == '1':  # 是否勾选
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
                        except:
                            print("运动板运行出错！")
                            flg_start['card'] = False
                            self._signal.emit(fail("运动板通信出错！"))

                        if ui.checkBox_test.isChecked() or int(plan_list[plan_num][13]) == 0:
                            time.sleep(2)  # 测试期间停两秒切换下一个动作
                        elif int(plan_list[plan_num][13]) < 0:
                            pass  # 负数则直接下一个动作
                        else:
                            t_over = 0
                            while True:  # 正式运行，等待球进入触发区域再进行下一个动作
                                if not self.run_flg:
                                    print('动作等待中！')
                                    break
                                if int(plan_list[plan_num][13]) in [action_area, action_area - 1, action_area + 1]:
                                    break
                                t_over += 1
                                if t_over == 60:
                                    print('等待超时！')
                                    break
                                if self.card_next:
                                    break
                                time.sleep(0.1)
                        if self.card_next:  # 快速执行下一个动作
                            self.card_next = False
                            continue
                        if self.run_flg:
                            if action_area >= max_area_count - 3:
                                PlanBallNum_Thead.run_flg = True  # 终点计数器线程

                            if int(plan_list[plan_num][11]) != 0:  # 摄像头延时，也可以用作动作延时
                                if int(plan_list[plan_num][10]) != 0:  # 摄像头缩放
                                    PlanCam_Thead.camitem = [int(plan_list[plan_num][10]),
                                                             int(plan_list[plan_num][11])]
                                    PlanCam_Thead.run_flg = True  # 摄像头线程
                                time.sleep(int(plan_list[plan_num][11]))

                            if '_' in plan_list[plan_num][14]:
                                PlanObs_Thead.plan_obs = plan_list[plan_num][14]
                                PlanObs_Thead.run_flg = True  # 切换场景线程

                if not ui.checkBox_test.isChecked():  # 非测试模式才关闭
                    # 流程完成则打开终点开关，关闭闸门，关闭弹射
                    sc.GASetExtDoBit(3, 1)  # 打开终点开关
                    sc.GASetExtDoBit(1, 0)  # 关闭闸门
                    sc.GASetExtDoBit(0, 0)  # 关闭弹射

                if self.run_flg and ui.checkBox_restart.isChecked():
                    ReStart_Thead.run_flg = True  # 1分钟后重启动作
                    print('1分钟后重启动作!')
                self.run_flg = False
                self._signal.emit(succeed("运动流程：完成！"))
                print('动作已完成！')
            else:
                self._signal.emit(fail("运动卡未链接！"))
                self.run_flg = False


def signal_accept(message):
    global p_now
    print(message)
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
    _signal = pyqtSignal(object)

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
                print('头下')
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
def save_plan():
    global plan_list
    global plan_all
    table = ui.tableWidget_Step
    row_num = table.rowCount()
    # col_num = table.columnCount()
    if row_num == 0:
        return
    plan_list = []
    local_list = []
    for row in range(0, row_num):
        if table.cellWidget(row, 0):
            if table.cellWidget(row, 0).isChecked():
                local_list.append("1")
            else:
                local_list.append("0")
        for col in range(1, 14):
            local_list.append(
                "0" if (not table.item(row, col) or table.item(row, col).text() == '') else table.item(row, col).text())
        if table.cellWidget(row, 14):
            if table.cellWidget(row, 14).isChecked():
                local_list.append(str("1_%s" % table.cellWidget(row, 14).text()))
            else:
                local_list.append(str("0_%s" % table.cellWidget(row, 14).text()))
        else:
            local_list.append(
                "0" if (not table.item(row, 14) or table.item(row, 14).text() == '') else table.item(row, 14).text())
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
    file = "Plan_config.yml"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            plan_all = yaml.safe_load(f)
            f.close()
            for plan in plan_all['plans']:
                plan_names.append(plan_all['plans'][plan]['plan_name'])

            s485.s485_Cam_No = plan_all['s485_Cam_No']
            s485.s485_Axis_No = plan_all['s485_Axis_No']

            comb = ui.comboBox_plan
            comb.addItems(plan_names)
            plan_refresh()
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
    table = ui.tableWidget_Step
    num = table.rowCount()
    for i in range(0, num):
        if ui.checkBox_selectall.isChecked():
            table.cellWidget(i, 0).setChecked(True)
        else:
            table.cellWidget(i, 0).setChecked(False)


def plan_refresh():  # 刷新方案列表
    global plan_list
    comb = ui.comboBox_plan
    _index = comb.currentIndex()
    plan_list = plan_all['plans']['plan%d' % (_index + 1)]['plan_list']

    table = ui.tableWidget_Step
    for num, plan in enumerate(plan_list):
        table.setRowCount(num + 1)
        cb = QCheckBox()
        cb.setStyleSheet('QCheckBox{margin:6px};')
        table.setCellWidget(num, 0, cb)
        if plan[0] == '1':
            table.cellWidget(num, 0).setChecked(True)
        for col in range(1, len(plan)):
            if col == 14:
                if table.item(num, col):
                    table.item(num, col).setText('')
                if table.cellWidget(num, col):
                    table.removeCellWidget(num, col)
                s_num = str(plan[col]).find('_')
                if s_num != -1:
                    obs_check = str(plan[col])[0]
                    obs_name = str(plan[col])[s_num + 1:]
                    # print(obs_check, obs_name)
                    cb = QCheckBox()
                    cb.setStyleSheet('QCheckBox{margin:6px};')
                    cb.setText(obs_name)
                    if int(obs_check) == 1:
                        cb.setChecked(True)
                    table.setCellWidget(num, 14, cb)
                else:
                    item = QTableWidgetItem(
                        "0" if not plan[col] else plan[col])
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(num, col, item)
            else:
                item = QTableWidgetItem(str(plan[col]))
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                table.setItem(num, col, item)


# 进入下一步动作
def card_next():
    PlanCmd_Thead.card_next = True


# 关闭运动卡
def card_stop():
    PlanCmd_Thead.run_flg = False
    print(flg_start)
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
            Axis_Thead.run_flg = True
        ui.textBrowser.append(succeed('串口链接：%s' % flg_start['s485']))
    else:
        ui.textBrowser.append(fail('串口链接：%s' % flg_start['s485']))
    if not flg_start['obs']:
        if not Obs_Thead.isRunning():
            Obs_Thead.start()


def cmd_run():
    global p_now
    save_plan()
    p_now = 0
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
        row_num = tb_step.currentRow()
        if row_num > -1:
            if tb_step.item(row_num, 14):
                tb_step.item(row_num, 14).setText('')
            if tb_step.cellWidget(row_num, 14):
                tb_step.removeCellWidget(row_num, 14)
            cb = QCheckBox()
            cb.setText(scene)
            cb.setStyleSheet('QCheckBox{margin:6px};')
            tb_step.setCellWidget(row_num, 14, cb)
            # print(tb_step.cellWidget(row_num, 14).text())


def obs_remove_table():
    tb_step = ui.tableWidget_Step
    row_num = tb_step.currentRow()
    if row_num > -1 and tb_step.cellWidget(row_num, 14):
        tb_step.removeCellWidget(row_num, 14)


# 禁止输入非数字
def table_change():
    global plan_list
    tb_step = ui.tableWidget_Step
    row = tb_step.currentRow()
    col = tb_step.currentColumn()
    # print("%s %s" % (row, col))
    if col in [0, 14] or row < 0 or col < 0:
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
        'saveImgNum': '0,1,2,3,4,5,6,7,8',
        # 'saveImgPath': 'D:/saidao',
    }
    try:
        r = requests.post(url=wakeup_addr, data=form_data)
        print(r.text)
    except:
        print('图像识别主机通信失败！')


def ballnum2zero():
    ui.lineEdit_ball_num.setText('0')


def test():
    for i in range(0, 10):
        if i < 9:
            continue
        print("ok~")
    # message = 1
    # if type(message) == int:
    #     print('数字')
    # else:
    #     print(type(message))
    # get_picture('终点')
    # res, value = sc.GAGetDiReverseCount()
    # print(res, value)
    # res = sc.GASetDiReverseCount()
    # print(res)
    # res, value = sc.GAGetDiReverseCount()
    # print(res, value)
    # data = b'\x01\x03\x04\x06\x13\xff\xfcJ\xcf'
    # for index, byte in enumerate(data):
    #     # print(byte)
    #     if index == 3:
    #         high1 = (hex(byte)[2:]).zfill(2)
    #         print(high1)
    #     if index == 4:
    #         high2 = (hex(byte)[2:]).zfill(2)
    #         print(high2)
    #     if index == 5:
    #         lowPos1 = (hex(byte)[2:]).zfill(2)
    #         print(lowPos1)
    #     if index == 6:
    #         print(byte)
    #         lowPos2 = (hex(byte)[2:]).zfill(2)
    #         print(lowPos2)


class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.aboutToQuit.connect(self.onAboutToQuit)

    @pyqtSlot()
    def onAboutToQuit(self):
        print("Exiting the application.")
        try:
            # 当准备退出时，关闭所有服务
            tcp_socket.shutdown(socket.SHUT_RDWR)
            tcp_socket.close()

            tcp_thread.close()
            tcp_thread.join()

            udp_socket.shutdown(socket.SHUT_RDWR)
            udp_socket.close()
            udp_thread.join()

            httpd.shutdown()
            httpd.server_close()

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

    plan_list = []  # 当前方案列表 [0.选中,1.圈数,2.左右,3.前后,4.上下,5.头旋转,6.头上下,7.速度,8.加速,9.减速,10.镜头缩放,11.缩放时长,12.机关,13.运动位置,14.运动延时]
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料
    pValue = [0, 0, 0, 0, 0]  # 各轴位置
    p_now = 0  # 保存方案运行位置
    flg_key_run = True  # 键盘控制标志
    flg_start = {'card': False, 's485': False, 'obs': False, 'ai': False, 'ai_end': False, 'server1': False,
                 'server2': False}  # 各硬件启动标志

    load_plan_yaml()
    ui.lineEdit_CarNo.setText(str(plan_all['cardNo']))

    KeyListener_Thead = KeyListenerThead()  # 启用键盘监听
    KeyListener_Thead.start()

    PlanCmd_Thead = PlanCmdThead()  # 总运行方案
    PlanCmd_Thead._signal.connect(signal_accept)
    PlanCmd_Thead.start()

    PlanObs_Thead = PlanObsThead()  # OBS场景切换方案
    PlanObs_Thead._signal.connect(signal_accept)
    PlanObs_Thead.start()

    PlanCam_Thead = CamThead()  # 摄像头运行方案
    PlanCam_Thead._signal.connect(signal_accept)
    PlanCam_Thead.start()

    PlanBallNum_Thead = PlanBallNumThead()  # 统计过终点的球数
    PlanBallNum_Thead._signal.connect(PlanBallNum_signal_accept)
    PlanBallNum_Thead.start()

    Axis_Thead = AxisThead()  # 轴复位
    Axis_Thead._signal.connect(signal_accept)
    Axis_Thead.start()

    Pos_Thead = PosThead()  # 实时监控各轴位置
    Pos_Thead._signal.connect(pos_signal_accept)
    Pos_Thead.start()

    ReStart_Thead = ReStartThead()  # 重启动作
    ReStart_Thead._signal.connect(time_signal_accept)
    ReStart_Thead.start()

    ui.pushButton_fsave.clicked.connect(save_plan)
    ui.pushButton_rename.clicked.connect(test)
    # ui.pushButton_rename.clicked.connect(plan_rename)
    ui.pushButton_CardStart.clicked.connect(card_start)
    ui.pushButton_CardStop.clicked.connect(card_stop)
    ui.pushButton_CardRun.clicked.connect(cmd_run)
    ui.pushButton_CardReset.clicked.connect(card_reset)
    ui.pushButton_ToTable.clicked.connect(p_to_table)
    ui.pushButton_Obs2Table.clicked.connect(obs_to_table)
    ui.pushButton_Obs_delete.clicked.connect(obs_remove_table)
    ui.pushButton_ball_clean.clicked.connect(ballnum2zero)
    ui.pushButton_CardNext.clicked.connect(card_next)
    # ui.pushButton_stop_saveImgs.clicked.connect(stop_save_images)

    ui.checkBox_saveImgs.clicked.connect(save_images)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.comboBox_plan.currentIndexChanged.connect(plan_refresh)
    ui.tableWidget_Step.itemChanged.connect(table_change)

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

    action_area = 0  # 触发镜头向下一个位置活动的点位
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
    tcpServer_addr = ('0.0.0.0', 2222)  # pingpong 发送网页排名
    httpServer_addr = ('0.0.0.0', 8081)  # 接收网络数据包控制
    udpClient_addr = ("192.168.0.161", 19733)  # 数据发送给其他服务器
    wakeup_addr = "http://192.168.0.110:8080"  # 唤醒服务器线程
    load_ballsort_yaml()

    # 初始化列表
    con_data = []  # 排名数组
    z_response = []  # 球号排名数组(发送给前端网页排名显示)
    for i in range(0, len(init_array)):
        con_data.append([])
        z_response.append(i + 1)  # z_response[1,2,3,4,5,6,7,8,9,10]
        for j in range(0, 5):
            if j == 0:
                con_data[i].append(init_array[i][5])  # con_data[[yellow,0,0,0,0]]
            else:
                con_data[i].append(0)
    init_ranking_table()  # 初始化排名数据表
    # 初始化球数组，位置寄存器
    reset_ranking_array()  # 重置排名数组

    # 自动重置排名线程
    reset_thread = ResetThead()
    reset_thread._signal.connect(reset_signal_accept)
    reset_thread.start()

    # 1. Udp 接收数据
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(udpServer_addr)
    print('Udp_socket Server Started.')
    udp_thread = UdpThead()
    udp_thread._signal.connect(udp_signal_accept)
    udp_thread.start()

    # pingpong 发送排名
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind(tcpServer_addr)
    tcp_socket.listen(1)
    print('Pingpong Server Started.')
    tcp_thread = TcpThead()  # 前端网页以pingpong形式发送排名数据
    tcp_thread._signal.connect(tcp_signal_accept)
    tcp_thread.start()

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
    "**************************图像识别算法_结束*****************************"

    sys.exit(app.exec_())
