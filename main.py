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
from PyQt5.QtGui import QBrush, QColor
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
        try:
            cl_requst = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
            cl_event = obs.EventClient()  # 监听 链接配置在 config.toml 文件中

            cl_event.callback.register(on_current_program_scene_changed)  # 场景变化
            cl_event.callback.register(on_scene_item_enable_state_changed)  # 来源变化
            cl_event.callback.register(on_record_state_changed)  # 录制状态
            cl_event.callback.register(on_stream_state_changed)  # 直播流状态
            cl_event.callback.register(on_get_stream_status)  # 直播流状态
            self._signal.emit(succeed('OBS 启动成功！'))
        except:
            self._signal.emit(fail('OBS 启动失败！'))


def obs_signal_accept(msg):
    print(msg)
    ui.textBrowser.append(msg)
    if '成功' in msg:
        get_scenes_list()  # 获取所有场景
        get_source_list(ui.comboBox_Scenes.currentText())


def obs_open():
    Obs_Thead.start()


class SourceThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(SourceThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        self._signal.emit('写表')


def source_signal_accept(msg):
    print(msg)
    source2table()


def source2table():
    global source_list
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
    res = cl_requst.get_scene_item_list(scene_name)
    source_list = []
    for item in res.scene_items:
        source_list.append([item['sceneItemEnabled'], item['sourceName'], item['sceneItemId']])
        # print(item)
    Source_Thead.start()


def scenes_change():  # 变换场景
    scene_name = ui.comboBox_Scenes.currentText()
    try:
        cl_requst.set_current_program_scene(scene_name)
    except:
        ui.textBrowser.append(fail("OBS 链接中断！"))


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
        if (ui.lineEdit_lap.text().isdigit()
                and ui.lineEdit_region.text().isdigit()
                and ui.lineEdit_time.text().isdigit()):
            ballsort_conf['max_lap_count'] = int(ui.lineEdit_lap.text())
            ballsort_conf['max_area_count'] = int(ui.lineEdit_region.text())
            ballsort_conf['reset_time'] = int(ui.lineEdit_time.text())
            max_lap_count = int(ui.lineEdit_lap.text())
            max_area_count = int(ui.lineEdit_region.text())
            reset_time = int(ui.lineEdit_time.text())
            # print(ballsort_conf)
            with open(file, "w", encoding="utf-8") as f:
                yaml.dump(ballsort_conf, f, allow_unicode=True)
                ui.textBrowser_msg.setText(
                    "%s,%s,%s 保存服务器完成" % (ballsort_conf['max_lap_count'],
                                                 ballsort_conf['max_area_count'],
                                                 ballsort_conf['reset_time']))
        else:
            ui.textBrowser_msg.setText("错误，只能输入数字！")


def init_table():
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

    def run(self) -> None:
        global action_location
        global con_data
        con_data_temp = []
        while True:
            try:
                # 3. 等待接收对方发送的数据
                recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
                res = recv_data[0].decode('utf8')
                # res = json.loads(res)
                data_res = eval(res)  # str转换list
                array_data = []
                for i_ in range(1, len(data_res)):
                    array_data.append(data_res[i_])
                # print(array_data)
                array_data = deal_area(array_data, array_data[0][6])
                if not array_data:
                    continue
                action_location = int(array_data[0][6])
                array_data = filter_max_value(array_data)
                deal_rank(array_data)
                con_data = []
                con_data1 = []
                for k in range(0, len(ranking_array)):
                    con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                    con_data.append(
                        [con_item['name'], con_item['position'], con_item['lapCount'], con_item['x1'],
                         con_item['y1']])
                    con_data1.append(
                        [con_item['name'], con_item['position'], con_item['lapCount']])
                # print(con_data)
                to_num(con_data)
                if con_data_temp != con_data1:
                    con_data_temp = con_data1
                    self._signal.emit(con_data1)

            except Exception as e:
                print("UDP数据接收出错:%s" % e)
                self._signal.emit("UDP数据接收出错:%s" % e)
        # 5. 关闭套接字
        # udp_socket.close()


def udp_signal_accept(msg):
    # print(msg)
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
    init_table()


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
        tb_Step.horizontalHeader().resizeSection(1, 30)
        tb_Step.horizontalHeader().resizeSection(7, 50)
        tb_Step.horizontalHeader().resizeSection(8, 50)
        tb_Step.horizontalHeader().resizeSection(9, 50)
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
                for i in range(p, rownum - 1):
                    print('%d' % i)
                    for j in range(0, tb_step.columnCount() - 1):
                        if j == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet('QCheckBox{margin:6px};')
                            cb.setChecked(tb_step.cellWidget(i + 1, j).isChecked())
                            tb_step.setCellWidget(i, j, cb)
                        else:
                            item = QTableWidgetItem(tb_step.item(i + 1, j).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb_step.setItem(i, j, item)
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
                    for i in range(1, table.columnCount() - 1):
                        item = QTableWidgetItem(table.item(r - 1, i).text())
                        item.setTextAlignment(Qt.AlignCenter)
                        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                        table.setItem(r, i, item)

                # table.cellWidget(row, 0).setChecked(False)
                # for i in range(1, table.columnCount() - 1):
                #     item = QTableWidgetItem('0')
                #     item.setTextAlignment(Qt.AlignCenter)
                #     # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                #     table.setItem(row, i, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                table.setCellWidget(0, 0, cb)

                for i in range(1, table.columnCount() - 1):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(0, i, item)


'''
    PosThead(QThread) 检测各轴位置
'''


class PosThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(PosThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        global pValue
        if flag_card_start:
            try:
                while True:
                    for i in range(0, 5):
                        (res, pValue[i], pClock) = sc.get_pos(i + 1)
                    self._signal.emit(pValue)
                    time.sleep(0.01)
            except:
                pass


def pos_signal_accept(message):
    if len(message) == 5:
        for i in range(0, len(message)):
            getattr(ui, 'lineEdit_axis%s' % i).setText(str(message[i]))
    else:
        pass


'''
    CamThead(QThread) 摄像头运动方案线程
'''


class CamThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(CamThead, self).__init__()
        self.camitem = [5, 5]  # [运行挡位,持续时间]

    def run(self) -> None:
        print('串口运行')
        try:
            s485.cam_zoom_move(self.camitem[0])
            time.sleep(self.camitem[1])
            s485.cam_zoom_on_off()
        except:
            print("485 运行出错！")


'''
    AxisThead(QThread) 轴复位线程
'''


class AxisThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(AxisThead, self).__init__()

    def run(self) -> None:
        print('串口运行')
        try:
            self._signal.emit(succeed('轴复位开始！'))
            datas = s485.get_axis_pos()
            print(datas)
            if datas:
                for data in datas:
                    if data['nAxisNum'] in [1, 5]:  # 轴一，轴五，方向反过来，所以要设置负数
                        data['highPos'] = -data['highPos']
                    res = sc.GASetPrfPos(data['nAxisNum'], data['highPos'])
                    if res == 0:
                        sc.card_move(int(data['nAxisNum']), 0)
                res = sc.card_update()
                if res == 0:
                    self._signal.emit(succeed('轴复位完成！'))
                else:
                    self._signal.emit(fail('运动卡链接出错！'))
        except:
            print("轴复位出错！")
            self._signal.emit(fail('轴复位出错！'))


'''
    CmdThead(QThread) 执行运动方案线程
'''


class CmdThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(CmdThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        if flag_card_start:
            try:
                self._signal.emit(succeed("运动流程：开始！"))
                for i in range(0, len(plan_list)):
                    # print(plan_list)
                    if plan_list[i][0] == '1':  # 是否勾选
                        self._signal.emit(i)
                        try:
                            sc.card_move(1, int(plan_list[i][2]), vel=int(plan_list[i][7]), dAcc=float(plan_list[i][8]),
                                         dDec=float(plan_list[i][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(2, int(plan_list[i][3]), vel=int(plan_list[i][7]), dAcc=float(plan_list[i][8]),
                                         dDec=float(plan_list[i][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(3, int(plan_list[i][4]), vel=int(plan_list[i][7]), dAcc=float(plan_list[i][8]),
                                         dDec=float(plan_list[i][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(4, int(plan_list[i][5]), vel=int(plan_list[i][7]), dAcc=float(plan_list[i][8]),
                                         dDec=float(plan_list[i][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_move(5, int(plan_list[i][6]), vel=int(plan_list[i][7]), dAcc=float(plan_list[i][8]),
                                         dDec=float(plan_list[i][9]),
                                         dVelStart=0.1, dSmoothTime=0)
                            sc.card_update()

                            print("开启机关")
                            if int(plan_list[i][12]) != 0:
                                if '-' in plan_list[i][12]:
                                    sc.GASetExtDoBit(abs(int(plan_list[i][12])) - 1, 0)
                                else:
                                    sc.GASetExtDoBit(abs(int(plan_list[i][12])) - 1, 1)
                        except:
                            print("运动板运行出错！")

                        while True:  # 等待动作完成
                            k = 0
                            if int(plan_list[i][11]) != 0:
                                for j in range(0, len(pValue)):
                                    if pValue[j] == int(plan_list[i][j + 2]):
                                        k += 1
                                if k == 5:
                                    # 摄像头缩放
                                    if int(plan_list[i][10]) != 0 and int(plan_list[i][10]) != 0:
                                        if Cam_Thead.isRunning():
                                            Cam_Thead.terminate()
                                        Cam_Thead.camitem = [int(plan_list[i][10]), int(plan_list[i][11])]
                                        Cam_Thead.start()
                                    time.sleep(int(plan_list[i][11]))
                                    if (int(plan_list[i][13]) == action_location or ui.checkBox_test.isChecked()
                                            or int(plan_list[i][13]) == -1):
                                        break
                            else:
                                time.sleep(float(plan_list[i][14]))
                                if ui.checkBox_test.isChecked() or int(plan_list[i][13]) <= 0:
                                    break
                                else:
                                    while True:
                                        if int(plan_list[i][13]) in [action_location, action_location + 1]:
                                            break
                                    break

                self._signal.emit(succeed("运动流程：完成！"))
            except:
                self._signal.emit(fail("运动卡运行：出错！"))
        else:
            self._signal.emit(fail("运动卡未链接！"))


def signal_accept(message):
    global p_now
    print(message)
    if is_natural_num(message):
        if ui.checkBox_follow.isChecked():
            print(message)
            tb_step = ui.tableWidget_Step
            col_num = tb_step.columnCount()
            # print(col_num)
            for i in range(1, col_num - 1):
                tb_step.item(p_now, i).setBackground(QBrush(QColor(255, 255, 255)))
                tb_step.item(message, i).setBackground(QBrush(QColor(255, 0, 255)))
        p_now = message
    else:
        if not is_natural_num(message):
            ui.textBrowser.append(str(message))


class KeyListenerThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(KeyListenerThead, self).__init__()

    def run(self) -> None:
        with pynput.keyboard.Listener(on_press=keyboard_press, on_release=keyboard_release) as lsn:
            lsn.join()


def keyboard_release(key):
    global flag_key_run
    if ui.checkBox_key.isChecked() and flag_card_start:
        try:
            if key == key.up:
                print('前')
                # sc.card_stop(2)
                flag_key_run = True
                sc.card_setpos(2, pValue[1] + 30000)
                sc.card_update()

            if key == key.down:
                print('后')
                # sc.card_stop(2)
                flag_key_run = True
                sc.card_setpos(2, pValue[1] - 30000)
                sc.card_update()

            if key == key.left:
                print('左')
                # sc.card_stop(1)
                flag_key_run = True
                sc.card_setpos(1, pValue[0] + 30000)
                sc.card_update()

            if key == key.right:
                print('右')
                # sc.card_stop(1)
                flag_key_run = True
                sc.card_setpos(1, pValue[0] - 30000)
                sc.card_update()

            if key == key.insert:
                print('上')
                flag_key_run = True
                sc.card_setpos(3, pValue[2] - 30000)
                sc.card_update()

            if key == key.delete:
                print('下')
                flag_key_run = True
                sc.card_setpos(3, pValue[2] + 30000)
                sc.card_update()

            if key == key.home:
                print('头左')
                flag_key_run = True
                sc.card_setpos(4, pValue[3] + 30000)
                sc.card_update()

            if key == key.end:
                print('头右')
                flag_key_run = True
                sc.card_setpos(4, pValue[3] - 30000)
                sc.card_update()

            if key == key.page_up:
                print('头下')
                flag_key_run = True
                sc.card_setpos(5, pValue[4] - 30000)
                sc.card_update()

            if key == key.page_down:
                print('头下')
                flag_key_run = True
                sc.card_setpos(5, pValue[4] + 30000)
                sc.card_update()

        except AttributeError:
            print(key)
        try:
            if key.char == '-':
                s485.cam_zoom_on_off()
            elif key.char == '+':
                s485.cam_zoom_on_off()
        except:
            print(key)


def keyboard_press(key):
    global flag_key_run
    if ui.checkBox_key.isChecked() and flag_card_start:
        try:
            if key == key.up:
                print('前')
                if flag_key_run:
                    sc.card_move(2, pos=2000000)
                    sc.card_update()
                    flag_key_run = False

            elif key == key.down:
                print('后')
                if flag_key_run:
                    sc.card_move(2, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.left:
                print('左')
                if flag_key_run:
                    sc.card_move(1, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.right:
                print('右')
                if flag_key_run:
                    sc.card_move(1, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.insert:
                print('上')
                if flag_key_run:
                    sc.card_move(3, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.delete:
                print('下')
                if flag_key_run:
                    sc.card_move(3, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.home:
                print('头左')
                if flag_key_run:
                    sc.card_move(4, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.end:
                print('头右')
                if flag_key_run:
                    sc.card_move(4, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.page_up:
                print('头下')
                if flag_key_run:
                    sc.card_move(5, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            elif key == key.page_down:
                print('头上')
                if flag_key_run:
                    sc.card_move(5, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
        except AttributeError:
            print(key)
        try:
            if key.char == '+':
                s485.cam_zoom_move(5)
            elif key.char == '-':
                s485.cam_zoom_move(-5)
        except:
            print(key)


# 保存方案
def save_plan():
    global plan_list
    global plan_all
    table = ui.tableWidget_Step
    row_num = table.rowCount()
    col_num = table.columnCount()
    if row_num == 0:
        return
    plan_list = []
    local_list = []
    for i in range(0, row_num):
        if table.cellWidget(i, 0).isChecked():
            local_list.append("1")
        else:
            local_list.append("0")
        for j in range(1, col_num - 1):
            # host.append(table.item(i, j).text())
            local_list.append(
                "0" if (table.item(i, j) == None or table.item(i, j).text() == '') else table.item(i, j).text())
        plan_list.append(local_list)
        local_list = []
    # print(plan_list)

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
    num = 0
    for task in plan_list:
        table.setRowCount(num + 1)
        cb = QCheckBox()
        cb.setStyleSheet('QCheckBox{margin:6px};')
        table.setCellWidget(num, 0, cb)
        if task[0] == '1':
            table.cellWidget(num, 0).setChecked(True)

        for i in range(1, len(task)):
            item = QTableWidgetItem(str(task[i]))
            item.setTextAlignment(Qt.AlignCenter)
            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
            table.setItem(num, i, item)
        num += 1


# 打开运动卡
def card_start():
    global flag_card_start
    cardnum = ui.lineEdit_CarNo.text()
    if cardnum.isdigit():
        res = sc.card_open(int(cardnum))
        print(res)
        if res == 0:
            flag_card_start = True
            ui.textBrowser.append(succeed('启动板卡：%s' % card_res[res]))
            Pos_Thead.start()
        else:
            ui.textBrowser.append(res)
    else:
        ui.textBrowser.append(fail('请输入正确的卡号~！'))
    s485_flag = s485.cam_open()
    if s485_flag == True:
        ui.textBrowser.append(succeed('串口链接：%s' % s485_flag))
    else:
        ui.textBrowser.append(fail('串口链接：%s' % s485_flag))


def cmd_run():
    global p_now
    save_plan()
    p_now = 0
    if Cmd_Thead.isRunning():
        Cmd_Thead.terminate()
    Cmd_Thead.start()


def card_reset():
    Axis_Thead.start()


# 实时轴位置入表
def p_to_table():
    tb_step = ui.tableWidget_Step
    for i in range(0, len(pValue)):
        row_num = tb_step.currentRow()
        tb_step.item(row_num, i + 2).setText(str(pValue[i]))


# 禁止输入非数字
def table_change():
    global plan_list
    tb_step = ui.tableWidget_Step
    row = tb_step.currentRow()
    col = tb_step.currentColumn()
    # print("%s %s" % (row, col))
    if row < 0 or col < 0:
        return
    try:
        if not is_natural_num(tb_step.item(row, col).text()):
            if col > len(plan_list[row]) - 1:
                tb_step.item(row, col).setText('0')
            else:
                comb = ui.comboBox_plan
                _index = comb.currentIndex()
                tb_step.item(row, col).setText(plan_list[row][col])
    except:
        print("数据表操作出错！")


def cmd_stop():
    Cmd_Thead.terminate()


def wakeup_server():
    form_data = {
        'requestType': 'set_run_toggle',
        'run_toggle': '1',
    }
    while True:
        try:
            r = requests.post(url=wakeup_addr, data=form_data)
            print(r.text)
        except:
            print('图像识别主机通信失败！')
        time.sleep(60)


def test():
    data = b'\x01\x03\x04\x06\x13\xff\xfcJ\xcf'
    for index, byte in enumerate(data):
        # print(byte)
        if index == 3:
            high1 = (hex(byte)[2:]).zfill(2)
            print(high1)
        if index == 4:
            high2 = (hex(byte)[2:]).zfill(2)
            print(high2)
        if index == 5:
            lowPos1 = (hex(byte)[2:]).zfill(2)
            print(lowPos1)
        if index == 6:
            print(byte)
            lowPos2 = (hex(byte)[2:]).zfill(2)
            print(lowPos2)
    # if res == 0:
    #     ui.textBrowser.append(succeed('复位：%s' % card_res[res]))
    # else:
    #     ui.textBrowser.append(res)


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
    flag_key_run = True  # 键盘控制标志
    flag_card_start = False  # 运动板卡启动标志

    load_plan_yaml()
    ui.lineEdit_CarNo.setText(str(plan_all['cardNo']))

    KeyListener_Thead = KeyListenerThead()  # 启用键盘监听
    KeyListener_Thead.start()

    Cmd_Thead = CmdThead()  # 运行方案
    Cmd_Thead._signal.connect(signal_accept)

    Axis_Thead = AxisThead()  # 轴复位
    Axis_Thead._signal.connect(signal_accept)

    Cam_Thead = CamThead()  # 摄像头运行方案
    Cam_Thead._signal.connect(signal_accept)

    Pos_Thead = PosThead()  # 实时监控各轴位置
    Pos_Thead._signal.connect(pos_signal_accept)

    ui.pushButton_fsave.clicked.connect(save_plan)
    ui.pushButton_rename.clicked.connect(test)
    # ui.pushButton_rename.clicked.connect(plan_rename)
    ui.pushButton_CardStart.clicked.connect(card_start)
    ui.pushButton_CardRun.clicked.connect(cmd_run)
    ui.pushButton_CardReset.clicked.connect(card_reset)
    ui.pushButton_ToTable.clicked.connect(p_to_table)
    # ui.pushButton_cmd_stop.clicked.connect(cmd_stop)

    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.comboBox_plan.currentIndexChanged.connect(plan_refresh)
    ui.tableWidget_Step.itemChanged.connect(table_change)

    """
        OBS 处理
    """
    source_list = []  # OBS来源列表
    cl_requst = ''  # 请求
    cl_event = ''  # 监听

    Obs_Thead = ObsThead()  # OBS启动线程
    Obs_Thead._signal.connect(obs_signal_accept)

    Source_Thead = SourceThead()  # OBS来源入表线程
    Source_Thead._signal.connect(source_signal_accept)

    ui.pushButton_ObsConnect.clicked.connect(obs_open)
    ui.comboBox_Scenes.currentTextChanged.connect(scenes_change)

    "**************************OBS*****************************"

    "**************************图像识别算法_开始*****************************"
    # set_run_toggle 发送请求运行数据
    camera_num = 8  # 摄像头数量
    area_Code = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}  # 摄像头代码列表
    load_area()  # 初始化区域划分

    action_location = 0  # 触发镜头向下一个位置活动的点位

    ranking_array = []  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]

    # 初始化数据
    max_lap_count = 2  # 最大圈
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
    init_table()  # 初始化排名数据表

    # 初始化球数组，位置寄存器
    ball_sort = []  # 位置寄存器
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
