import copy
import json
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from tkinter import messagebox

import pynput
import websocket
import random

from PySide6.QtCore import QThread, Signal, Slot, QTimer, QEvent
from PySide6.QtGui import QMouseEvent, QPen, QTextCursor, QShowEvent, QHideEvent
from PySide6.QtWidgets import QMenu, QMessageBox, QFileDialog, \
    QAbstractButton, QDialog, QSplitter

import obsws_python as obs
import pygame

from BallsNumDlg_Ui import Ui_Dialog_BallsNum
from Camera_Ui import Ui_Camera_Dialog
from Map_Ui import Ui_Dialog_Map
from OrganDlg_Ui import Ui_Dialog_Organ
from ResultDlg_Ui import Ui_Dialog_Result
from Speed_Ui import Ui_Dialog_Set_Speed
from TrapBallDlg_Ui import Ui_Dialog_TrapBall
from utils import tool_unit
from utils.SportCard_unit import *
from kaj789_table import Kaj789Ui, lottery_data2table
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
    if data.output_active:
        flg_start['live'] = True
    else:
        flg_start['live'] = False


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
    signal = Signal(object)

    def __init__(self):
        super(ObsThread, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        global cl_request
        global cl_event
        global flg_start
        try:
            if not flg_start['obs']:
                cl_request.disconnect()
                cl_event.disconnect()
                time.sleep(0.5)
                cl_request = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
                cl_event = obs.EventClient()  # 监听 链接配置在 config.toml 文件中

                cl_event.callback.register(on_current_program_scene_changed)  # 场景变化
                cl_event.callback.register(on_scene_item_enable_state_changed)  # 来源变化
                cl_event.callback.register(on_record_state_changed)  # 录制状态
                cl_event.callback.register(on_stream_state_changed)  # 直播流状态
                cl_event.callback.register(on_get_stream_status)  # 直播流状态
                self.signal.emit(succeed('OBS 启动成功！'))
                flg_start['obs'] = True
        except:
            self.signal.emit(fail('OBS 启动失败！'))
            flg_start['obs'] = False


def obssignal_accept(msg):
    print(msg)
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    if '成功' in msg:
        get_scenes_list()  # 获取所有场景
        get_source_list(ui.comboBox_Scenes.currentText())


def obs_open():
    if not Obs_Thread.isRunning():
        Obs_Thread.start()


def obs_stream():
    print(ui.status_live.styleSheet())
    try:
        if '(255, 0, 0)' in ui.status_live.styleSheet():
            cl_request.start_stream()
        else:
            cl_request.stop_stream()
    except:
        print('obs 直播 错误！')
        ui.textBrowser_msg.append(fail('obs 直播 错误！'))
        flg_start['obs'] = False


class SourceThread(QObject):
    sourcesignal = Signal(object)

    def __init__(self):
        super(SourceThread, self).__init__()


def sourcesignal_accept(msg):
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
    global cl_request
    obs_scene = obs_data['obs_scene']
    item_ranking = obs_data['source_ranking']
    item_settlement = obs_data['source_settlement']
    for i in range(5):
        try:
            # 刷新 "浏览器来源"（Browser Source）
            cl_request.press_input_properties_button("结算页", "refreshnocache")
            time.sleep(1)
            cl_request.set_scene_item_enabled(obs_scene, item_ranking, True)  # 打开排位组件
            cl_request.set_scene_item_enabled(obs_scene, item_settlement, False)  # 关闭结算页
            time.sleep(1)
            cl_request.press_input_properties_button("浏览器", "refreshnocache")
            break
        except:
            if i < 3:
                try:
                    cl_request.disconnect()
                    time.sleep(0.5)
                    cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
                    print('重连OBS~~~~~~~~~~~~')
                    time.sleep(0.5)
                except:
                    print('链接OBS失败~~~~~~~~~~~~')
                continue
            else:
                lottery_term[9] = '截图失败'
                print('OBS 切换操作失败！')
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
            Source_Thread.sourcesignal.emit('写表')
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
    global cl_request
    resp = ''
    for i in range(5):
        try:
            resp = cl_request.get_source_screenshot(scence_current, "jpg", 1920, 1080, 100)
            if len(area_Code['main']) > 0:
                Screenshot = resp.image_data
                base64_string = Screenshot.replace('data:image/jpg;base64,', '')
                image_data = base64.b64decode(base64_string)  # 1. 解码 Base64 字符串为二进制数据
                nparr = np.frombuffer(image_data, np.uint8)  # 2. 转换为 NumPy 数组
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # 3. 使用 OpenCV 读取图片

                area = area_Code['main'][0]['coordinates']  # 4. 定义裁剪区域 (y1:y2, x1:x2)
                x1, x2 = area[0][0], area[1][0]
                y1, y2 = area[1][1], area[2][1]
                cropped_image = image[y1:y2, x1:x2]

                if ui.checkBox_Main_Horizontal.isChecked():
                    cropped_image = cv2.flip(cropped_image, 1)  # 🔁 5. 水平翻转图片
                if ui.checkBox_Main_Vertica.isChecked():
                    cropped_image = cv2.flip(cropped_image, 0)  # 🔁 5. 垂直翻转图片

                _, buffer = cv2.imencode('.jpg', cropped_image)  # 5. 可选：转换裁剪后的图片回 Base64
                img = base64.b64encode(buffer).decode("utf-8")
            else:
                img = resp.image_data[22:]
            form_data = {
                'CameraType': 'obs',
                'img': img,
                'sort': ui.lineEdit_sony_sort.text(),  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
            }
            try:
                res = requests.post(url=recognition_addr, data=form_data, timeout=8)
                r_list = eval(res.text)  # 返回 [图片字节码，排名列表，截图标志]
                # r_img = r_list[0]
                # if os.path.exists(ui.lineEdit_upload_Path.text()):
                #     image_json = open('%s/obs_%s_end.jpg' % (ui.lineEdit_upload_Path.text(), lottery_term[0]), 'wb')
                #     image_json.write(r_img)  # 将图片存到当前文件的fileimage文件中
                #     image_json.close()
                flg_start['ai_end'] = True
                return r_list
            except:
                flg_start['ai_end'] = False
                image_byte = base64.b64decode(img.encode('ascii'))
                print('终点识别服务没有开启！')
                return [image_byte, '[1]', 'obs']
        except:
            if i < 3:
                try:
                    cl_request.disconnect()
                    time.sleep(0.5)
                    cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
                    print('重连OBS~~~~~~~~~~~~')
                    time.sleep(0.5)
                except:
                    print('链接OBS失败~~~~~~~~~~~~')
                continue
            else:
                flg_start['obs'] = False
                return ['', '[1]', 'obs']
    # if os.path.exists(ui.lineEdit_upload_Path.text()):
    #     img_file = '%s/obs_%s_%s.jpg' % (ui.lineEdit_upload_Path.text(), lottery_term[0], int(time.time()))
    #     str2image_file(img, img_file)  # 保存图片


def obs_save_image():
    save_path = ui.lineEdit_end1_Path.text()
    if os.path.exists(save_path):
        if not ui.checkBox_saveImgs_auto.isChecked():
            res = sc.GASetDiReverseCount()  # 输入次数归0
            if res != 0:
                print('无法读取计球器！')
                return
        while ui.checkBox_saveImgs_main.isChecked():
            res, value = sc.GAGetDiReverseCount()
            if res == 0:
                num = int(value[0] / 2)
                if num >= balls_count:
                    cl_request.save_source_screenshot(ui.lineEdit_source_end.text(), "jpg",
                                                      '%s/%s.jpg' % (save_path, time.time()), 1920,
                                                      1080, 100)
                    if not ui.checkBox_saveImgs_auto.isChecked():
                        sc.GASetDiReverseCount()  # 输入次数归0
            if ui.checkBox_saveImgs_auto.isChecked():
                break
            time.sleep(1)


def obs_save_thread():
    global obs_save_t
    if not obs_save_t.is_alive():
        obs_save_t = threading.Thread(target=obs_save_image, daemon=True)
        obs_save_t.start()


# obs 脚本 obs_script_time.py 请求
def obs_script_request():
    res = requests.get(url="%s/start" % obs_script_addr)
    #  res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
    # res = requests.get(url="http://127.0.0.1:8899/period?term=开始")
    print(res)


"******************************OBS结束*************************************"

"******************************网络摄像头*************************************"


# 获取网络摄像头图片
def get_rtsp(rt_url):
    # try:
    #     ip_address = 'http://%s' % re.search(r'(\d+\.\d+\.\d+\.\d+)', rtsp_url).group(0)
    #     requests.get(ip_address)
    # except:
    #     return ['', '[1]', 'monitor']
    cap = cv2.VideoCapture(rt_url)
    if cap.isOpened():
        for i in range(3):
            ret, frame = cap.read()
            if ret:
                try:
                    if len(area_Code['net']) > 0:
                        # 获取裁剪区域坐标
                        area = area_Code['net'][0]['coordinates']
                        x1, x2 = area[0][0], area[1][0]
                        y1, y2 = area[1][1], area[2][1]
                        frame = frame[y1:y2, x1:x2]  # OpenCV 采用 (height, width) 方式裁剪
                        if ui.checkBox_Monitor_Horizontal.isChecked():
                            frame = cv2.flip(frame, 1)  # 水平翻转图片
                        if ui.checkBox_Monitor_Vertica.isChecked():
                            frame = cv2.flip(frame, 0)  # 垂直翻转图片
                    success, jpeg_data = cv2.imencode('.jpg', frame)
                    if success:
                        # 将 JPEG 数据转换为 Base64 字符串
                        jpg_base64 = base64.b64encode(jpeg_data).decode('ascii')
                        form_data = {
                            'CameraType': 'monitor',
                            'img': jpg_base64,
                            'sort': ui.lineEdit_monitor_sort.text(),  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
                        }
                        res = requests.post(url=recognition_addr, data=form_data, timeout=8)
                        r_list = eval(res.text)  # 返回 [图片字节码，排名列表，截图标志]
                        # r_img = r_list[0]
                        # if os.path.exists(ui.lineEdit_upload_Path.text()):
                        #     image_json = open('%s/rtsp_%s_end.jpg' % (ui.lineEdit_upload_Path.text(), lottery_term[0]), 'wb')
                        #     image_json.write(r_img)  # 将图片存到当前文件的fileimage文件中
                        #     image_json.close()
                        flg_start['ai_end'] = True
                        cap.release()
                        return r_list
                    else:
                        print("jpg_base64 转换错误！")
                        continue
                except:
                    print("图片错误或识别服务器未开启！")
                    continue
            else:
                print("无法读取视频帧")
                continue
    else:
        print(f'无法打开摄像头')
    cap.release()
    return ['', '[1]', 'monitor']


def rtsp_save_image():
    save_path = ui.lineEdit_end2_Path.text()
    if os.path.exists(save_path):
        try:
            ip_address = 'http://%s' % re.search(r'(\d+\.\d+\.\d+\.\d+)', rtsp_url).group(0)
            requests.get(ip_address)
        except:
            print("网络摄像头不能打开！")
            return
        if not ui.checkBox_saveImgs_auto.isChecked():
            res = sc.GASetDiReverseCount()  # 输入次数归0
            if res != 0:
                print('无法读取计球器！')
                return
        while ui.checkBox_saveImgs_monitor.isChecked():
            res, value = sc.GAGetDiReverseCount()
            if res == 0:
                num = int(value[0] / 2)
                if num >= balls_count + 1:
                    cap = cv2.VideoCapture(rtsp_url)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        cap.release()
                        if ret:
                            f = '%s/%s.jpg' % (save_path, int(time.time()))
                            cv2.imwrite(f, frame)
                        else:
                            print("无法读取视频帧")
                            return
                    else:
                        cap.release()
                        print(f'无法打开摄像头')
                        return
                    if not ui.checkBox_saveImgs_auto.isChecked():
                        sc.GASetDiReverseCount()  # 输入次数归0
            if ui.checkBox_saveImgs_auto.isChecked():
                break
            time.sleep(1)


def rtsp_save_thread():
    global rtsp_save_t
    if not rtsp_save_t.is_alive():
        rtsp_save_t = threading.Thread(target=rtsp_save_image, daemon=True)
        rtsp_save_t.start()


"************************************图像识别_开始****************************************"


# 处理触发点位
def deal_action():
    global action_area
    if ranking_array:
        action_area[0] = int(ranking_array[0][6])  # 触发区域


# 处理排名
def deal_rank(integration_qiu_array):
    global ranking_array
    area_limit = max_area_count / int(ui.lineEdit_area_limit.text())
    for r_index in range(0, len(ranking_array)):
        replaced = False
        for q_item in integration_qiu_array:
            if ranking_array[r_index][5] == q_item[5]:  # 更新 ranking_array
                if (ranking_array[0][6] >= max_area_count - balls_count
                        and ranking_array[0][8] >= max_lap_count - 1):
                    for i in range(len(ranking_array)):
                        ranking_array[i][8] = max_lap_count - 1

                if (q_item[6] < ranking_array[r_index][6] < max_area_count + 1
                        and ranking_array[r_index][8] < max_lap_count - 1):  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                    result_count = ranking_array[r_index][6] - q_item[6]
                    if result_count >= max_area_count - area_limit - balls_count:
                        ranking_array[r_index][8] += 1
                        ranking_array[r_index][6] = 0  # 每增加一圈，重置区域
                        if ranking_array[r_index][8] > max_lap_count - 1:
                            ranking_array[r_index][8] = max_lap_count - 1

                if ((ranking_array[r_index][6] == 0 and q_item[6] < area_limit)  # 等于0 刚初始化，未检测区域
                    or (max_area_count - balls_count >= q_item[6] >= ranking_array[r_index][6]  # 新位置要大于旧位置
                        and 0 < q_item[6] - ranking_array[r_index][6] <= area_limit  # 新位置相差旧位置三个区域以内
                    )  # 处理除终点排名位置的条件
                    or (q_item[6] >= ranking_array[r_index][6] >= max_area_count - area_limit - balls_count
                        and 0< q_item[6] - ranking_array[r_index][6] <= area_limit + balls_count
                        and ranking_array[r_index][8] == max_lap_count - 1  # 处理最后一圈终点附近的条件
                    )) and q_item[6] <= max_area_count:
                    write_ok = True
                    for i in range(len(ranking_array)):
                        if ((abs(q_item[0] - ranking_array[i][0]) < 5)  # 不能和前一个球的位置重叠
                                and (abs(q_item[1] - ranking_array[i][1]) < 5)):  # 避免误判两种颜色
                            write_ok = False
                            break
                    if write_ok:
                        for r_i in range(0, len(q_item)):
                            ranking_array[r_index][r_i] = copy.deepcopy(q_item[r_i])  # 更新 ranking_array
                        ranking_array[r_index][9] = 1

                if (r_index > 0
                        # and ranking_array[r_index][8] < ranking_array[0][8]
                        and q_item[6] <= (max_area_count - balls_count)):
                    if abs(q_item[6] - ranking_array[0][6]) < area_limit / 2:
                        for r_i in range(0, len(q_item)):
                            ranking_array[r_index][r_i] = copy.deepcopy(q_item[r_i])  # 更新 ranking_array
                        ranking_array[r_index][9] = 1
                        ranking_array[r_index][8] = ranking_array[0][8]
                replaced = True
                break
        if not replaced:
            if map_label_big.map_action >= len(map_label_big.path_points) - 20:
                ranking_array[r_index][9] = 1
            else:
                ranking_array[r_index][9] = 0

    sort_ranking()


def sort_ranking():
    global ranking_array
    global ball_sort
    # 1.排序区域
    # for i in range(0, len(ranking_array)):  # 冒泡排序
    #     for j in range(0, len(ranking_array) - i - 1):
    #         if ranking_array[j][6] < ranking_array[j + 1][6]:
    #             ranking_array[j], ranking_array[j + 1] = ranking_array[j + 1], ranking_array[j]
    ranking_array.sort(key=lambda x: x[6], reverse=True)

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
        if len(ball_sort) - 1 < ranking_array[i][6]:
            continue
        if not (ranking_array[i][5] in ball_sort[ranking_array[i][6]][ranking_array[i][8]]):
            ball_sort[ranking_array[i][6]][ranking_array[i][8]].append(copy.deepcopy(ranking_array[i][5]))  # 添加寄存器球排序
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


def color_to_num(res):  # 按最新排名排列数组
    global z_ranking_res
    arr_res = []
    if not z_ranking_res:
        return
    for r in res:
        for i in range(0, balls_count):
            if r[5] == init_array[i][5]:
                arr_res.append(i + 1)
    for i in range(0, len(arr_res)):
        for j in range(0, balls_count):
            if arr_res[i] == z_ranking_res[j]:
                z_ranking_res[i], z_ranking_res[j] = z_ranking_res[j], z_ranking_res[i]


def camera_to_num(res):  # 按最新排名排列数组
    camera_response = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    camera_response = camera_response[:balls_count]
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
        reset_ranking_Thread.run_flg = True
        while reset_ranking_Thread.run_flg:
            time.sleep(1)
        print('执行开始')

    def handle_stop_command(self):
        print('执行停止')


def load_ballsort_json():
    global max_lap_count
    global max_area_count
    file = "./ballsort_config.json"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        ballsort_all = json.load(f)
        max_area_count = int(ballsort_all['max_area_count'])
        max_lap_count = int(ballsort_all['max_lap_count'])

        ui.lineEdit_lap_Ranking.setText(str(max_lap_count))
        ui.lineEdit_area_Ranking.setText(str(max_area_count))
        ui.lineEdit_Time_Restart_Ranking.setText(str(ballsort_all['reset_time']))
        ui.lineEdit_start_count_ball.setText(str(ballsort_all['lineEdit_start_count_ball']))
        ui.lineEdit_end_count_ball.setText(str(ballsort_all['time_count_ball']))

        f.close()
    else:
        print("文件不存在")


def save_ballsort_json():
    global max_lap_count
    global max_area_count
    global ball_sort
    ballsort_all = {}
    file = "./ballsort_config.json"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        ballsort_all = json.load(f)
        f.close()
        if (ui.lineEdit_lap_Ranking.text().isdigit()
                and ui.lineEdit_area_Ranking.text().isdigit()
                and ui.lineEdit_Time_Restart_Ranking.text().isdigit()):
            ballsort_all['max_lap_count'] = int(ui.lineEdit_lap_Ranking.text())
            ballsort_all['max_area_count'] = int(ui.lineEdit_area_Ranking.text())
            ballsort_all['reset_time'] = int(ui.lineEdit_Time_Restart_Ranking.text())
            ballsort_all['lineEdit_start_count_ball'] = int(ui.lineEdit_start_count_ball.text())
            ballsort_all['time_count_ball'] = int(ui.lineEdit_end_count_ball.text())
            max_lap_count = int(ui.lineEdit_lap_Ranking.text())
            max_area_count = int(ui.lineEdit_area_Ranking.text())
            ball_sort = []  # 位置寄存器
            for row in range(0, max_area_count + 1):
                ball_sort.append([])
                for col in range(0, max_lap_count):
                    ball_sort[row].append([])
            # print(ballsort_conf)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(ballsort_all, f, indent=4, ensure_ascii=False)
            f.close()
            ui.textBrowser_background_data.setText(
                succeed("%s,%s,%s 保存服务器完成" % (ballsort_all['max_lap_count'],
                                                     ballsort_all['max_area_count'],
                                                     ballsort_all['reset_time'])))
        else:
            ui.textBrowser_background_data.setText(fail("错误，只能输入数字！"))


def init_ranking_table():
    global con_data
    for i in range(0, len(init_array)):
        con_data.append([])
        for j in range(0, 5):
            if j == 0:
                con_data[i].append(init_array[i][5])  # con_data[[yellow,0,0,0,0]]
            else:
                con_data[i].append(0)

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
    signal = Signal(object)

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
            if not con_data:
                continue
            for i in range(0, balls_count):
                for j in range(0, len(con_data[i])):
                    if con_data[i][0] in color_ch.keys():
                        if j == 0 and tb_ranking.item(i, j).text() != color_ch[con_data[i][j]]:
                            self.signal.emit([i, j, color_ch[con_data[i][j]]])
                        elif j != 0 and tb_ranking.item(i, j).text() != con_data[i][j]:
                            self.signal.emit([i, j, con_data[i][j]])


def rankingsignal_accept(msg):
    tb_ranking = ui.tableWidget_Ranking
    tb_ranking.item(msg[0], msg[1]).setText(str(msg[2]))


class TcpRankingThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(TcpRankingThread, self).__init__()
        self.running = True
        self.run_flg = False
        self.time_list = [''] * balls_count
        self.sleep_time = 0.5

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        tcp_ranking_socket.close()  # 关闭套接字
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global tcp_ranking_socket
        tcp_ranking_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_ranking_socket.bind(tcpServer_addr)
        tcp_ranking_socket.listen(1)
        while self.running:
            try:
                con, addr = tcp_ranking_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if con:
                    with WebsocketServer(con) as ws:
                        try:
                            while self.run_flg:
                                time.sleep(self.sleep_time)
                                if z_ranking_time != self.time_list:
                                    for i in range(balls_count):
                                        if self.time_list[i] != z_ranking_time[i]:
                                            if is_natural_num(z_ranking_time[i]):
                                                d = {"mc": i + 1, 'data': '%s"' % z_ranking_time[i],
                                                     'type': 'time'}
                                            else:
                                                d = {"mc": i + 1, 'data': z_ranking_time[i],
                                                     'type': 'time'}
                                            ws.send(json.dumps(d))
                                            self.time_list[i] = copy.deepcopy(z_ranking_time[i])
                                            if i == 0:
                                                Script_Thread.param = '%s"' % self.time_list[i]
                                                Script_Thread.run_type = 'period'
                                                Script_Thread.run_flg = True
                                else:
                                    d = {'data': z_ranking_res, 'type': 'pm'}
                                    ws.send(json.dumps(d))
                        except Exception as e:
                            print("pingpong_rank_1 错误：", e)
                            # self.signal.emit("pingpong 错误：%s" % e)
            except Exception as e:
                print("pingpong_rank_2 错误：", e)


class TcpResultThread(QThread):
    signal = Signal(object)

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
        tcp_result_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_result_socket.bind(result_tcpServer_addr)
        tcp_result_socket.listen(5)
        while self.running:
            try:
                con, addr = tcp_result_socket.accept()
                print("Accepted. {0}, {1}".format(con, str(addr)))
                if not con:
                    continue
                with WebsocketServer(con) as ws:
                    try:
                        while self.run_flg:
                            time.sleep(1)
                            if self.send_type == 'updata':
                                self.signal.emit(succeed('第%s期 结算！%s' % (term, str(z_ranking_end[:balls_count]))))
                                data_list = {'type': 'updata',
                                             'data': {'qh': str(term), 'rank': []}}
                                for index in range(balls_count):
                                    if is_natural_num(z_ranking_time[index]):
                                        data_list["data"]['rank'].append(
                                            {"mc": z_ranking_end[index], "time": ('%s"' % z_ranking_time[index])})
                                    else:
                                        data_list["data"]['rank'].append(
                                            {"mc": z_ranking_end[index], "time": ('%s' % z_ranking_time[index])})
                                # print(datalist)
                                ws.send(json.dumps(data_list))
                                self.send_type = ''

                            elif self.send_type == 'time':
                                data_list = {'type': 'time',
                                             'data': str(term)}
                                ws.send(json.dumps(data_list))
                                self.send_type = ''
                                self.run_flg = False
                            else:
                                data_list = {'type': 'pong',
                                             'data': str(term)}
                                ws.send(json.dumps(data_list))
                    except Exception as e:
                        print("pingpong_result_1 错误：%s" % e)
                        # self.signal.emit("pingpong 错误：%s" % e)
            except Exception as e:
                print("pingpong_result_2 错误：%s" % e)


def tcpsignal_accept(msg):
    # print(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)
    ui.textBrowser_background_data.append(msg)
    scroll_to_bottom(ui.textBrowser_background_data)


class DealUdpThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(DealUdpThread, self).__init__()
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
        data_res = []
        while self.running:
            if data_res == udp_thread.data_res:
                time.sleep(0.01)
                continue
            data_res = copy.deepcopy(udp_thread.data_res)  # str转换list
            self.signal.emit(data_res)
            array_data = []
            for i_ in range(0, len(data_res)):  # data_res[0] 是时间戳差值 ms
                if isinstance(data_res[i_], list):
                    array_data.append(copy.deepcopy(data_res[i_]))
            if len(array_data) < 1:
                continue
            # print(array_data)
            if len(array_data[0]) < 7:
                self.signal.emit(fail('array_data:%s < 7数据错误！' % array_data[0]))
                print('array_data < 7数据错误！', array_data[0])
                continue
            if action_area[0] > max_area_count - balls_count - 2:
                array_data = filter_max_value(array_data)  # 结束时，以置信度为准
            else:
                array_data = filter_max_value(array_data)  # 在平时球位置追踪，前面为准
            if array_data is None or len(array_data) < 1:
                continue
            array_data = deal_area(array_data, array_data[0][6])  # 收集统计区域内的球
            if array_data is None or len(array_data) < 1:
                continue
            if len(array_data[0]) < 8:
                self.signal.emit(fail('array_data:%s < 8数据错误！' % array_data[0]))
                print('array_data < 8数据错误！', array_data[0])
                continue
            if array_data is None or len(array_data) < 1:
                continue
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~2', array_data)
            deal_rank(array_data)
            if ball_sort and balls_start != len(ball_sort[1][0]):
                balls_start = len(ball_sort[1][0])  # 更新起点球数
                self.signal.emit(balls_start)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~3', ranking_array)
            deal_action()
            con_data = []
            if ranking_array:
                for k in range(0, balls_count):
                    con_item = dict(zip(keys, ranking_array[k]))  # 把数组打包成字典
                    con_data.append(
                        [con_item['name'], con_item['position'], con_item['lapCount'], con_item['x1'],
                         con_item['y1']])
                if ranking_array[0][9] != 0:
                    color_to_num(ranking_array)


class UdpThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(UdpThread, self).__init__()
        self.run_flg = True
        self.running = True
        self.data_res = []

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        udp_socket.close()
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        udp_socket.bind(udpServer_addr)
        while self.running:
            try:
                # 3. 等待接收对方发送的数据
                recv_data = udp_socket.recvfrom(10240)  # 1024表示本次接收的最大字节数
                if len(recv_data) < 1:
                    print('UDP无数据！')
                    continue
                res = recv_data[0].decode('utf8')
                if res == '':
                    # print('UDP_res无数据！', udp_thread.res)
                    continue
                data_res = eval(res)  # str转换list
                if not isinstance(data_res, list):
                    continue
                self.data_res = data_res
            except Exception as e:
                print("UDP数据接收出错:%s" % e)
                self.signal.emit("UDP数据接收出错:%s" % e)
        # 5. 关闭套接字
        udp_socket.close()


def udpsignal_accept(msg):
    global flg_start
    # print(msg)
    if isinstance(msg, int):
        if int(ui.lineEdit_ball_start.text()) < balls_start or balls_start == 0:  # 更新起点球数
            ui.lineEdit_balls_start.setText(str(balls_start))
            ui.lineEdit_ball_start.setText(str(balls_start))
            # if (ui.checkBox_saveImgs_start.isChecked()
            #         and balls_start < balls_count
            #         and balls_start != 0):
            #     save_start_images(1)
            # else:
            #     save_start_images(0)
    else:
        if '错误' in msg:
            ui.textBrowser_msg.append(msg)
        if ui.checkBox_ShowUdp.isChecked():
            ui.textBrowser_background_data.append(str(msg))


def load_area():  # 载入位置文件初始化区域列表
    global area_Code
    road_num = ui.lineEdit_map_picture.text()
    match = re.search(r"\d+(?=_)", road_num)
    if match:
        road_num = match.group()
    for key in area_Code.keys():
        track_file = "./txts/%s_%s.txt" % (road_num, key)
        print(track_file)
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
    print(area_Code)


def deal_area(ball_array, cap_num):  # 找出该摄像头内所有球的区域
    ball_area_array = []
    if len(ball_array) < 1 or cap_num == '':
        return
    for ball in ball_array:
        # print(ball)
        if ball[4] < 0.05:  # 置信度小于 0.45 的数据不处理
            continue
        if len(ball) == 7:
            ball.append(0)
        # x = (ball[0] + ball[2]) / 2
        # y = (ball[1] + ball[3]) / 2
        x = ball[0]
        y = ball[1]
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

        # 创建一个 QSplitter
        splitter = QSplitter(Qt.Horizontal)
        # splitter = QSplitter(Qt.Vertical)

        # 将已有的 QGroupBox 添加到 QSplitter 中
        splitter.addWidget(self.groupBox_main_camera)
        splitter.addWidget(self.groupBox_monitor_cam)
        # 可选：设置初始大小比例
        splitter.setSizes([300, 300])  # 左边 150 像素，右边 250 像素
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)
        self.widget_camera.setLayout(main_layout)

        tb_result = self.tableWidget_Results
        tb_result.horizontalHeader().resizeSection(0, 100)
        tb_result.horizontalHeader().resizeSection(1, 150)
        tb_result.horizontalHeader().resizeSection(2, 40)
        tb_result.horizontalHeader().resizeSection(3, 50)
        tb_result.horizontalHeader().resizeSection(4, 170)
        tb_result.horizontalHeader().resizeSection(5, 170)
        tb_result.horizontalHeader().resizeSection(6, 80)
        tb_result.horizontalHeader().resizeSection(7, 80)
        tb_result.horizontalHeader().resizeSection(8, 80)
        tb_result.horizontalHeader().resizeSection(9, 150)
        tb_result.horizontalHeader().resizeSection(10, 150)
        tb_result.horizontalHeader().resizeSection(11, 150)
        tb_result.horizontalHeader().resizeSection(12, 80)
        tb_result.horizontalHeader().resizeSection(13, 80)

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
        tb_audio.horizontalHeader().resizeSection(0, 100)
        tb_audio.horizontalHeader().resizeSection(1, 50)
        tb_audio.horizontalHeader().resizeSection(2, 80)
        tb_audio.horizontalHeader().resizeSection(3, 80)
        tb_audio.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_audio.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_audio.setColumnHidden(0, True)

        tb_ai = self.tableWidget_Ai
        tb_ai.horizontalHeader().resizeSection(0, 100)
        tb_ai.horizontalHeader().resizeSection(1, 50)
        tb_ai.horizontalHeader().resizeSection(2, 80)
        tb_ai.horizontalHeader().resizeSection(3, 80)
        tb_ai.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_ai.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb_ai.setColumnHidden(0, True)

        tb_step = self.tableWidget_Step
        tb_step.horizontalHeader().resizeSection(0, 30)
        tb_step.horizontalHeader().resizeSection(1, 40)
        tb_step.horizontalHeader().resizeSection(7, 80)
        tb_step.horizontalHeader().resizeSection(8, 50)
        tb_step.horizontalHeader().resizeSection(9, 50)
        tb_step.horizontalHeader().resizeSection(10, 70)
        tb_step.horizontalHeader().resizeSection(11, 60)
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
            exe_path = tb_result.item(row_num, 9).text()
            os.startfile(exe_path)
        if action == item1:
            exe_path = tb_result.item(row_num, 10).text()
            os.startfile(exe_path)
        if action == item2:
            send_end()
        if action == item3:
            cancel_end()
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
    signal = Signal(object)

    def __init__(self):
        super(ReStartThread, self).__init__()
        self.run_flg = False
        self.running = True
        self.start_flg = False  # 比赛进行中的标志
        self.countdown = '30'

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global term
        global betting_start_time
        global betting_end_time
        global action_area
        global ball_sort
        global ball_stop
        global ranking_time_start
        global cl_request
        global pos_stop
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            action_area = [0, 0, 0]  # 初始化触发区域
            ready_flg = True  # 准备动作开启信号
            ball_stop = False  # 保留卡珠信号
            TrapBall_ui.trap_flg = False  # 卡珠标记
            pos_stop = []  # 重置停留位置
            try:
                cl_request.disconnect()  # 断开重连 OBS
                time.sleep(0.5)
                cl_request = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
                print('断开重连OBS~~~~~~')
            except:
                self.signal.emit(fail('OBS链接失败！'))
            while PlanCmd_Thread.run_flg:
                print('PlanCmd_Thread.run_flg', '~~~~~~~~~~~')
                time.sleep(1)
            PlanCmd_Thread.background_state = True  # 运行背景
            PlanCmd_Thread.run_flg = True
            self.signal.emit('过场动画')
            if ui.checkBox_shoot_0.isChecked():
                Shoot_Thread.run_flg = True
                while Shoot_Thread.run_flg:
                    print('等待上珠结束~~~~~~~')
                    time.sleep(1)
                    # if (balls_start >= balls_count
                    #         or balls_start >= int(ui.lineEdit_balls_auto.text())):
                    #     break
                    if not ui.checkBox_shoot_0.isChecked():
                        break
            while PlanCmd_Thread.run_flg:
                print('等待背景结束~~~~~~~')
                time.sleep(1)
            if not self.run_flg:
                continue
            ball_sort[1][0] = []
            time.sleep(1)  # 有充足时间重新排名
            if ui.radioButton_start_betting.isChecked():  # 开盘模式
                response = get_term(Track_number)
                if len(response) > 2:  # 开盘模式，获取期号正常
                    self.start_flg = True
                    term = response['term']
                    betting_start_time = response['scheduledGameStartTime']
                    betting_end_time = response['scheduledResultOpeningTime']
                    self.countdown = int(betting_start_time) - int(time.time())
                    self.signal.emit('term_ok')
                    res_start = post_start(term=term, betting_start_time=betting_start_time,
                                           starting_Position=str(z_ranking_res[:balls_count])[1:-1],
                                           Track_number=Track_number)  # 发送开始信号给服务器
                    if str(res_start) != 'OK':
                        self.signal.emit(fail('比赛开始失败:%s' % res_start))
                        self.run_flg = False
                        continue
                    if self.countdown < 0:  # 时间错误，30秒后开赛
                        betting_start_time = int(time.time())
                        betting_end_time = int(time.time()) + 30
                        self.countdown = str(30)
                    else:
                        self.countdown = str(self.countdown)
                else:  # 封盘模式，退出循环
                    tcp_result_thread.send_type = 'time'
                    self.signal.emit('error')
                    self.run_flg = False
                    continue
            else:
                term = str(int(term) + 1)
                self.signal.emit('测试期号')
                self.countdown = ui.lineEdit_Time_Restart_Ranking.text()

            print('tcp_result_thread.send_type~~~~~', tcp_result_thread.send_type)
            tcp_result_thread.send_type = ''  # 退出结果页面循环
            while tcp_result_thread.send_type != '':
                time.sleep(1)
            tcp_result_thread.send_type = 'time'  # 发送新期号,结束TCP_RESULT线程
            Script_Thread.run_type = 'term'
            Script_Thread.run_flg = True  # 发送期号到OBS的python脚本

            lottery = get_lottery_term()  # 获取了开盘时间后开盘写表
            if lottery:
                self.signal.emit(lottery)

            if self.countdown.isdigit():
                self.countdown = int(self.countdown)
            else:
                self.countdown = 60
            for t in range(self.countdown, -1, -1):
                if not betting_loop_flg:
                    self.run_flg = False
                    break
                if t <= self.countdown - 5:
                    if not PlanCmd_Thread.background_state and ready_flg:
                        PlanCmd_Thread.ready_state = True  # 运行背景
                        PlanCmd_Thread.run_flg = True
                        if not reset_ranking_Thread.run_flg:
                            reset_ranking_Thread.run_flg = True  # 初始化排名，位置变量
                        ready_flg = False
                    ball_sort[1][0] = []
                ranking_time_start = time.time()
                time.sleep(1)
                self.signal.emit(t)
            if self.run_flg:
                # reset_ranking_Thread.run_flg = True  # 初始化排名，位置变量
                # while reset_ranking_Thread.run_flg:
                #     print('reset_ranking_Thread.run_flg', '~~~~~~~~~~~')
                #     time.sleep(1)
                for index in range(0, 16):
                    if index not in [
                        int(ui.lineEdit_start.text()) - 1,
                        int(ui.lineEdit_shake.text()) - 1,
                        int(ui.lineEdit_end.text()) - 1,
                        int(ui.lineEdit_alarm.text()) - 1,
                        int(ui.lineEdit_start_count.text()) - 1,
                    ]:
                        sc.GASetExtDoBit(index, 1)
                OrganCycle_Thread.run_flg = True
                while PlanCmd_Thread.run_flg:
                    print('PlanCmd_Thread.run_flg', '~~~~~~~~~~~')
                    time.sleep(1)
                PlanCmd_Thread.run_flg = True

            print("循环启动！")
            self.run_flg = False


def restartsignal_accept(msg):
    global labels
    if isinstance(msg, bool):
        lottery_data2table(ui.tableWidget_Results, lottery_term, labels)
        ui.lineEdit_Main_Camera.setText('')
        ui.lineEdit_Backup_Camera.setText('')
        ui.lineEdit_Send_Result.setText('')
    elif isinstance(msg, int):
        if int(msg) == 1:
            plan_refresh()
            ui.lineEdit_ball_end.setText('0')
            ui.lineEdit_balls_end.setText('0')
        ui.lineEdit_time.setText(str(msg))
        ui.lineEdit_times_count.setText(str(msg))
        tb_result = ui.tableWidget_Results
        row_count = tb_result.rowCount()
        if row_count > 0:
            tb_result.item(0, 2).setText(str(msg))
    elif '比赛开始失败' in msg:
        ui.radioButton_stop_betting.click()
        ui.textBrowser_msg.append(msg)
        scroll_to_bottom(ui.textBrowser_msg)
    elif msg == '过场动画':
        ui.textBrowser_msg.append(succeed('过场动画'))
        scroll_to_bottom(ui.textBrowser_msg)
    elif msg == '测试期号':
        ui.groupBox_term.setStyleSheet("QGroupBox { background-color: yellow; }")  # 让 GroupBox 变黄
        ui.pushButton_term.setText(str(term))
    elif msg == 'term_ok':
        ui.groupBox_term.setStyleSheet("QGroupBox { background-color: red; }")  # 让 GroupBox 变红
        ui.pushButton_term.setText(str(term))
    elif msg == 'error':
        ui.radioButton_stop_betting.click()
        ui.textBrowser_msg.append(fail('分机服务器没有响应，可能在封盘状态！'))
        scroll_to_bottom(ui.textBrowser_msg)
    else:
        ui.textBrowser.append(msg)
        ui.textBrowser_msg.append(msg)
        scroll_to_bottom(ui.textBrowser)
        scroll_to_bottom(ui.textBrowser_msg)


'''
    PosThread(QThread) 检测各轴位置
'''


class PosThread(QThread):
    signal = Signal(object)

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
                    self.signal.emit(pValue)

                except:
                    pass
            self.run_flg = False


def possignal_accept(message):
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
    signal = Signal(object)

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
            if str(self.camitem[0]).isdigit() and self.camitem[0] != 0:
                try:
                    print(self.camitem)
                    res = s485.cam_zoom_step(self.camitem[0] - 1)
                    if not res:
                        flg_start['s485'] = False
                        self.signal.emit(fail("s485运行通信出错！"))
                        self.run_flg = False
                        continue
                    # time.sleep(self.camitem[1])
                    # s485.cam_zoom_off()
                except:
                    print("485 运行出错！")
                    flg_start['s485'] = False
                    self.signal.emit(fail("s485通信出错！"))
            self.run_flg = False


def cam_signal_accept(msg):
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser)
    scroll_to_bottom(ui.textBrowser_msg)


'''
    PlanBallNumThread(QThread) 摄像头运动方案线程
'''


class PlanBallNumThread(QThread):
    signal = Signal(object)

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
        global term_status
        global term_comment
        global ball_sort
        global betting_end_time
        global lottery_term
        while self.running:
            time.sleep(0.1)
            if (not self.run_flg) or (not flg_start['card']):
                continue
            print('正在接收运动卡输入信息！')
            # try:
            res = sc.GASetDiReverseCount()  # 输入次数归0
            tcp_ranking_thread.sleep_time = 0.05  # 终点前端排名时间发送设置
            time_now = time.time()
            time_old = time.time()
            sec_ = 0
            num_old = 0
            term_status = 1
            screen_sort = True
            ObsEnd_Thread.ball_flg = False  # 结算页标志2
            if res == 0:
                while self.run_flg:
                    res, value = sc.GAGetDiReverseCount()
                    print(res, value)
                    if res == 0:
                        num = int(value[0] / 2) - 1
                        if num > len(z_ranking_time):
                            num = len(z_ranking_time)
                        if num > num_old:
                            for i in range(num):
                                if z_ranking_time[i] in ['TRAP', 'OUT', '']:
                                    t = time.time()
                                    z_ranking_time[i] = '%.2f' % (t - ranking_time_start)
                            if num == 1:
                                betting_end_time = int(time.time())
                                lottery_term[11] = str(betting_end_time)
                                map_label_big.bet_running = False
                            if num == balls_count:
                                self.signal.emit('录终点图')
                            self.signal.emit(num)
                            num_old = num
                        if num > balls_count - 2 and screen_sort:
                            ScreenShot_Thread.run_flg = True  # 终点截图识别线程
                            screen_sort = False
                        if num >= balls_count:
                            break
                        # elif num >= balls_start and not ui.checkBox_Pass_Recognition_Start.isChecked():
                        #     break
                        elif time.time() - time_now > int(ui.lineEdit_end_count_ball.text()):
                            # 超时则跳出循环计球
                            if (ui.checkBox_Pass_Ranking_Twice.isChecked()
                                    or ui.radioButton_stop_betting.isChecked()):
                                self.run_flg = False
                            self.signal.emit('人工检查')
                            time.sleep(1)
                            if not self.run_flg:
                                break
                        else:
                            time_num = time.time() - time_old
                            if time_num > 1:
                                time_old = time.time()
                                sec_ += 1
                                for i in range(max_area_count, max_area_count - balls_count, -1):
                                    for j in range(balls_count):
                                        if ranking_array[j][6] == i:
                                            ball_sort[i][max_lap_count - 1] = []
                                            break
                                self.signal.emit(
                                    succeed('计球倒计时：%s' %
                                            str(int(ui.lineEdit_end_count_ball.text()) - sec_)))
                    else:
                        flg_start['card'] = False
                        self.signal.emit(fail("运动板x输入通信出错！"))
                    time.sleep(0.01)
                try:
                    index = int(ui.lineEdit_alarm.text()) - 1
                    sc.GASetExtDoBit(index, 0)
                except:
                    print('警报电压输出错误！')
                    flg_start['card'] = False
                self.signal.emit('检查结束')
                for index in range(balls_count):
                    if z_ranking_time[index] == '':
                        t = time.time()
                        z_ranking_time[index] = '%.2f' % (t - ranking_time_start)
                    if z_ranking_time[index] in ['TRAP', 'OUT']:
                        s = z_ranking_time[index]
                        term_comment = s
                        term_status = 0
                    time.sleep(0.5)
            else:
                print("次数归0 失败！")
                flg_start['card'] = False
                self.signal.emit(fail("运动板x输入通信出错！"))

            tcp_ranking_thread.sleep_time = 0.1  # 恢复正常前端排名数据包发送频率
            if screen_sort:
                term_comment = term_comments[1]
                ScreenShot_Thread.run_flg = True  # 终点截图识别线程
            ObsEnd_Thread.ball_flg = True  # 结算页标志2
            print('ObsEnd_Thread.ball_flg:%s' % ObsEnd_Thread.ball_flg, '~~~~~~~~~~~~~~~~~~~~~~')
            Audio_Thread.run_flg = False  # 停止卫星图音效播放线程
            Ai_Thread.run_flg = False  # 停止卫星图AI播放线程
            # main_music_worker.toggle_enablesignal.emit(False)
            # except:
            #     print("接收运动卡输入 运行出错！")
            #     flg_start['card'] = False
            #     self.signal.emit(fail("运动板x输入通信出错！"))
            self.run_flg = False


def PlanBallNumsignal_accept(msg):
    if isinstance(msg, int):
        ui.lineEdit_ball_end.setText(str(msg))
        ui.lineEdit_balls_end.setText(str(msg))
    elif '录终点图' in msg:
        if (not ui.checkBox_test.isChecked()) and ui.checkBox_saveImgs_auto.isChecked():  # 非测试模式:
            ui.checkBox_saveImgs_main.setChecked(True)
            ui.checkBox_saveImgs_monitor.setChecked(True)
    elif '检查结束' in msg:
        if term_comment in ['TRAP', 'OUT']:
            ui.checkBox_end_stop.setChecked(True)
        TrapBall_ui.label_state.setText('确认成功！')
        TrapBall_ui.label_state.setStyleSheet('color: rgb(0, 255, 0)')
        TrapBall_ui.hide()
    elif '人工检查' in msg:
        if not TrapBall_ui.isVisible() and PlanBallNum_Thread.run_flg:
            TrapBall_ui.label_state.setText('请确认卡珠情况')
            TrapBall_ui.label_state.setStyleSheet('color: rgb(255, 0, 0)')
            TrapBall_ui.show()
            play_alarm()
    elif '计球倒计时' in msg:
        text_lines = ui.textBrowser_msg.toHtml().splitlines()
        if len(text_lines) >= 1:
            if '计球倒计时' in text_lines[-1]:
                text_lines[-1] = msg
                new_text = "\n".join(text_lines)
                ui.textBrowser_msg.setHtml(new_text)
                scroll_to_bottom(ui.textBrowser_msg)
            else:
                ui.textBrowser_msg.append(msg)
                scroll_to_bottom(ui.textBrowser_msg)
    else:
        ui.textBrowser.append(msg)
        ui.textBrowser_msg.append(msg)
        scroll_to_bottom(ui.textBrowser)
        scroll_to_bottom(ui.textBrowser_msg)


class ObsEndThread(QThread):
    """
    ObsEndThread(QThread) 实时结果截图线程
    """
    signal = Signal(object)

    def __init__(self):
        super(ObsEndThread, self).__init__()
        self.screen_flg = False
        self.ball_flg = False
        self.run_flg = True
        self.running = True

    def stop(self):
        self.screen_flg = False
        self.ball_flg = False
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global lottery_term, cl_request
        global tcp_result_socket
        global action_area
        global term_comment
        global result_data
        global betting_loop_flg
        global balls_start
        while self.running:
            time.sleep(1)
            if not (self.screen_flg and self.ball_flg):
                self.signal.emit('比赛计时')
                continue
            print('结算页面运行！')
            self.signal.emit('录图结束')
            send_flg = True  # 发送赛果成功标志
            save_path = '%s' % ui.lineEdit_upload_Path.text()
            if os.path.exists(save_path):
                lottery_term[9] = '%s/%s.jpg' % (save_path, term)
                for i in range(5):
                    try:
                        cl_request.save_source_screenshot(ui.lineEdit_scene_name.text(), "jpg",
                                                          lottery_term[9], 1920,
                                                          1080, 100)
                        break
                    except:
                        if i < 3:
                            try:
                                cl_request.disconnect()
                                time.sleep(0.5)
                                cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
                                print('重连OBS~~~~~~~~~~~~')
                                time.sleep(0.5)
                            except:
                                print('链接OBS失败~~~~~~~~~~~~')
                            continue
                        else:
                            lottery_term[9] = '截图失败'
                            print('OBS 截图操作失败！')
                            self.signal.emit(fail('OBS 截图操作失败！'))
                            flg_start['obs'] = False
            for i in range(5):
                try:
                    tcp_result_thread.send_type = 'updata'
                    tcp_result_thread.run_flg = True

                    cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_ranking'],
                                                      False)  # 关闭排名来源
                    cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_settlement'],
                                                      True)  # 打开结果来源
                    break
                except:
                    if i < 3:
                        try:
                            cl_request.disconnect()
                            time.sleep(0.5)
                            cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
                            print('重连OBS~~~~~~~~~~~~')
                            time.sleep(0.5)
                        except:
                            print('链接OBS失败~~~~~~~~~~~~')
                        continue
                    else:
                        print('OBS 切换操作失败！')
                        self.signal.emit(fail('OBS 切换操作失败！'))
                        flg_start['obs'] = False
            for i in range(5):
                try:
                    # 获取录屏状态
                    recording_status = cl_request.get_record_status()
                    # 检查是否正在录屏
                    if recording_status.output_active:  # 确保键名正确
                        time.sleep(3)
                        video_name = cl_request.stop_record()  # 关闭录像
                        lottery_term[10] = video_name.output_path  # 视频保存路径
                    break
                except:
                    if i < 3:
                        try:
                            cl_request.disconnect()
                            time.sleep(0.5)
                            cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
                            print('重连OBS~~~~~~~~~~~~')
                            time.sleep(0.5)
                        except:
                            print('链接OBS失败~~~~~~~~~~~~')
                        continue
                    else:
                        print('OBS 关闭录像失败！')
                        self.signal.emit(fail('OBS 关闭录像失败！'))
                        flg_start['obs'] = False

            lottery_term[3] = '已结束'  # 新一期比赛的状态（0.已结束）
            if ui.radioButton_start_betting.isChecked():  # 开盘模式
                result_data = {"raceTrackID": Track_number, "term": str(term),
                               "actualResultOpeningTime": betting_end_time,
                               "result": z_ranking_end[0:balls_count],
                               "timings": "[]"}
                data_temp = []
                for index in range(balls_count):
                    if is_natural_num(z_ranking_time[index]):
                        data_temp.append(
                            {"pm": index + 1, "id": z_ranking_end[index],
                             "time": float(z_ranking_time[index])})
                    else:
                        data_temp.append(
                            {"pm": index + 1, "id": z_ranking_end[index],
                             "time": z_ranking_time[index]})
                result_data["timings"] = json.dumps(data_temp)
                lottery_term[12] = json.dumps(result_data)
                print(lottery_term[12])
                try:
                    res_end = post_end(term=term, betting_end_time=betting_end_time,
                                       status=term_status,
                                       Track_number=Track_number)  # 发送游戏结束信号给服务器
                    if res_end == 'OK':
                        res_result = post_result(term=term, betting_end_time=betting_end_time,
                                                 result_data=result_data,
                                                 Track_number=Track_number)  # 发送最终排名给服务器
                        if res_result == 'OK':
                            lottery_term[6] = "发送成功"
                        else:
                            lottery_term[6] = "发送失败"
                        if os.path.exists(lottery_term[9]):
                            res_upload = post_upload(term=term, img_path=lottery_term[9],
                                                     Track_number=Track_number)  # 上传结果图片
                            if res_upload == 'OK':
                                lottery_term[7] = "上传成功"
                            else:
                                lottery_term[7] = "上传失败"
                        if term_comment != '':
                            res_marble_results = post_marble_results(term=term,
                                                                     comments=term_comment,
                                                                     Track_number=Track_number)  # 上传备注信息
                            if str(term) in res_marble_results:
                                lottery_term[8] = term_comment
                            else:
                                lottery_term[8] = "备注失败"
                            term_comment = ''
                    else:
                        send_flg = False
                except:
                    send_flg = False
                    self.signal.emit(fail('上传结果错误！'))
                    print('上传结果错误！')
                ReStart_Thread.start_flg = False  # 比赛结束标志
                lottery_term[2] = str(int(time.time() - ranking_time_start))
            if send_flg:
                lottery_term[3] = '已结束'  # 新一期比赛的状态（0.已结束）
            else:
                lottery_term[3] = '未结束'
                betting_loop_flg = False
            lottery2json()  # 保存数据
            self.signal.emit(succeed('第%s期 结束！' % term))

            if ui.checkBox_end_stop.isChecked():  # 本局结束自动封盘
                betting_loop_flg = False

            if ui.checkBox_end_BlackScreen.isChecked():  # 本局结束自动封盘黑屏
                betting_loop_flg = False

            if betting_loop_flg:
                while PlanCmd_Thread.run_flg:
                    time.sleep(1)
                ReStart_Thread.run_flg = True  # 重启动作
            else:
                while PlanCmd_Thread.run_flg:
                    time.sleep(1)
                action_area = [0, 0, 0]  # 初始化触发区域
                PlanCmd_Thread.end_state = True  # 运行背景
                PlanCmd_Thread.run_flg = True
                auto_shoot()  # 自动上珠
                self.run_flg = False

            self.screen_flg = False
            self.ball_flg = False


def ObsEndsignal_accept(msg):
    # print(msg)
    if '录图结束' in msg:
        # if term_comment in ['TRAP', 'OUT']:
        #     Map_ui.show()
        if not ui.checkBox_test.isChecked() and ui.checkBox_saveImgs_auto.isChecked():
            ui.checkBox_saveImgs_main.setChecked(False)
            ui.checkBox_saveImgs_monitor.setChecked(False)
    elif '比赛计时' in msg:
        if ReStart_Thread.start_flg:
            t = int(time.time() - ranking_time_start)
            ui.label_time_count.setText(str(t))
    elif '期 结束！' in msg:
        tb_result = ui.tableWidget_Results
        row_count = tb_result.rowCount()
        col_count = tb_result.columnCount()
        if row_count > 0:
            for i in range(2, col_count):
                item = tb_result.item(0, i)
                if item is None:
                    item = QTableWidgetItem()
                    tb_result.setItem(0, i, item)
                item.setText(str(lottery_term[i]))
                item.setTextAlignment(Qt.AlignCenter)
                if i == 3:
                    item.setForeground(QColor("red") if lottery_term[i] == "未结束" else QColor("green"))
            tb_result.viewport().update()
        if not betting_loop_flg:
            ui.radioButton_stop_betting.click()  # 封盘
            if ui.checkBox_end_BlackScreen.isChecked():
                ui.checkBox_black_screen.click()
        ui.checkBox_main_music.setChecked(False)
        ui.lineEdit_balls_start.setText('0')
        ui.lineEdit_ball_start.setText('0')
        ui.groupBox_term.setStyleSheet("")
    else:
        ui.textBrowser.append(str(msg))
        ui.textBrowser_msg.append(str(msg))
        scroll_to_bottom(ui.textBrowser)
        scroll_to_bottom(ui.textBrowser_msg)


'''
    ScreenShotThread(QThread) 结果截图线程
'''


class ScreenShotThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(ScreenShotThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global ball_sort
        global lottery_term
        global betting_end_time
        global Send_Result_End
        global z_ranking_end
        global z_ranking_res
        global ranking_array
        global term_status
        global term_comment
        global main_Camera, monitor_Camera, fit_Camera
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('截图结果识别运行！')
            self.signal.emit(succeed('截图结果识别运行！'))
            ObsEnd_Thread.screen_flg = False  # 结算页标志1
            obs_res = get_picture(ui.lineEdit_source_end.text())  # 拍摄来源
            if obs_res:
                obs_list = eval(obs_res[1])
                main_Camera = camera_to_num(obs_list)
                if len(obs_list) > 2 and ui.checkBox_main_camera_set.isChecked():
                    # print(obs_list)
                    for i in range(0, len(obs_list)):
                        for j in range(0, len(ranking_array)):
                            if ranking_array[j][5] == obs_list[i]:
                                ranking_array[j][6] = max_area_count
                                ranking_array[j][8] = max_lap_count - 1
                                ranking_array[j], ranking_array[i] = ranking_array[i], ranking_array[j]
                        ball_sort[max_area_count][max_lap_count - 1].append('')
                        ball_sort[max_area_count][max_lap_count - 1][i] = obs_list[i]
                    color_to_num(ranking_array)
                self.signal.emit(obs_res)

            monitor_res = get_rtsp(rtsp_url)  # 网络摄像头拍摄
            if monitor_res:
                rtsp_list = eval(monitor_res[1])
                monitor_Camera = camera_to_num(rtsp_list)
                self.signal.emit(monitor_res)

            if obs_res[1] != '[1]' and main_Camera == monitor_Camera:
                term_status = 1
                print('主镜头识别正确:', main_Camera)
                z_ranking_end = copy.deepcopy(main_Camera)
                lottery_term[4] = str(z_ranking_end[0:balls_count])  # 排名
            # elif z_ranking_res == monitor_Camera:
            #     term_status = 1
            #     print('网络识别正确:', monitor_Camera)
            #     z_ranking_end = copy.deepcopy(monitor_Camera)
            #     lottery_term[4] = str(z_ranking_end[0:balls_count])  # 排名
            # elif z_ranking_res == main_Camera and not ui.checkBox_main_camera_set.isChecked():
            #     term_status = 1
            #     print('赛道识别正确:', main_Camera)
            #     z_ranking_end = copy.deepcopy(main_Camera)
            #     lottery_term[4] = str(z_ranking_end[0:balls_count])  # 排名
            else:
                term_status = 0
                term_comment = term_comments[3]
                z_ranking_end = copy.deepcopy(z_ranking_res)
                send_list = []
                if not ui.checkBox_Pass_Ranking_Twice.isChecked():
                    ui.lineEdit_Send_Result.setText('')
                    Send_Result_End = False
                    while self.run_flg:
                        self.signal.emit('显示结果对话框')
                        if Send_Result_End:
                            send_list = []
                            for i in range(len(z_ranking_res)):
                                if getattr(ui, 'lineEdit_result_%s' % i).text().isdigit():
                                    num = int(getattr(ui, 'lineEdit_result_%s' % i).text())
                                    if num not in send_list:
                                        send_list.append(num)
                            if len(send_list) >= balls_count:
                                self.signal.emit('send_ok')
                                Send_Result_End = False
                                break
                            else:
                                Send_Result_End = False
                                self.signal.emit(fail('发送数据错误！'))
                        if ui.checkBox_Pass_Ranking_Twice.isChecked():
                            break
                        time.sleep(1)
                    Send_Result_End = False
                    for i in range(0, len(send_list)):
                        for j in range(0, len(z_ranking_end)):
                            if send_list[i] == z_ranking_end[j]:
                                z_ranking_end[i], z_ranking_end[j] = z_ranking_end[j], z_ranking_end[i]
                lottery_term[5] = str(z_ranking_end[0:balls_count])  # 排名
            camera_list = []
            for i in range(balls_count):
                camera_list.append(init_array[z_ranking_end[i] - 1][5])
            ball_sort[max_area_count][max_lap_count - 1] = []
            temp_lap = []
            for i in range(max_lap_count):
                temp_lap.append([])
            ball_sort.append(temp_lap)
            for i in range(0, len(camera_list)):
                for j in range(0, len(ranking_array)):
                    if ranking_array[j][5] == camera_list[i]:
                        if i < balls_count - 1:
                            ranking_array[j][6] = max_area_count + 1
                        ranking_array[j][8] = max_lap_count - 1
                        ranking_array[j], ranking_array[i] = ranking_array[i], ranking_array[j]
                if len(ball_sort[max_area_count + 1][max_lap_count - 1]) - 1 < i:
                    ball_sort[max_area_count + 1][max_lap_count - 1].append('')
                ball_sort[max_area_count + 1][max_lap_count - 1][i] = camera_list[i]
            color_to_num(ranking_array)
            betting_end_time = int(time.time())
            lottery_term[11] = str(betting_end_time)
            self.signal.emit('核对完成')
            time.sleep(3)
            ObsEnd_Thread.screen_flg = True  # 结算页标志1
            print('ObsEnd_Thread.screen_flg:%s' % ObsEnd_Thread.screen_flg, '~~~~~~~~~~~~~~~~~~~~~~')

            self.run_flg = False


def ScreenShotsignal_accept(msg):
    # try:
    if isinstance(msg, list):
        if len(msg) < 2 or msg[0] == '':
            return
        img = msg[0]
        pixmap = QPixmap()
        pixmap.loadFromData(img)
        pixmap = pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2, Qt.KeepAspectRatio, Qt.SmoothTransformation);

        if msg[2] == 'obs':
            painter = QPainter(pixmap)
            painter.setFont(QFont("Arial", 50, QFont.Bold))  # 设置字体
            painter.setPen(QColor(255, 0, 0))  # 设定颜色（红色）
            painter.drawText(10, 60, "1")  # (x, y, "文本")
            painter.end()  # 结束绘制
            ui.lineEdit_Main_Camera.setText(str(main_Camera[:balls_count]))
            # if ui.checkBox_main_camera.isChecked():
            main_camera_ui.label_picture.setPixmap(pixmap)
            ui.label_main_picture.setPixmap(pixmap)
        elif msg[2] == 'monitor':
            painter = QPainter(pixmap)
            painter.setFont(QFont("Arial", 50, QFont.Bold))  # 设置字体
            painter.setPen(QColor(0, 255, 0))  # 设定颜色（红色）
            painter.drawText(10, 60, "2")  # (x, y, "文本")
            painter.end()  # 结束绘制
            ui.lineEdit_Backup_Camera.setText(str(monitor_Camera[:balls_count]))
            # if ui.checkBox_monitor_cam.isChecked():
            monitor_camera_ui.label_picture.setPixmap(pixmap)
            ui.label_monitor_picture.setPixmap(pixmap)
        for index in range(len(main_Camera)):
            fit_Camera[index] = (main_Camera[index] == monitor_Camera[index])
            if fit_Camera[index]:
                getattr(ui, 'lineEdit_result_%s' % index).setText(str(main_Camera[index]))
                getattr(result_ui, 'lineEdit_result_%s' % index).setText(str(main_Camera[index]))
            else:
                getattr(ui, 'lineEdit_result_%s' % index).setText('')
                getattr(result_ui, 'lineEdit_result_%s' % index).setText('')
    elif msg == '显示结果对话框':
        if not result_ui.isVisible():
            result_ui.show()
            play_alarm()  # 警报声
    elif msg == 'send_res':
        ui.lineEdit_Send_Result.setText('')
    elif '核对完成' in msg:
        set_result(z_ranking_end)
    elif msg == 'send_ok':
        result_ui.hide()
        ui.checkBox_alarm.click()
    else:
        ui.textBrowser.append(str(msg))
        ui.textBrowser_msg.append(str(msg))
        scroll_to_bottom(ui.textBrowser)
        scroll_to_bottom(ui.textBrowser_msg)


# except:
#     print('OBS 操作失败！')


'''
    PlanObsThread(QThread) 摄像头运动方案线程
'''


class PlanObsThread(QThread):
    signal = Signal(object)

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
                        self.signal.emit(succeed("OBS 场景切换完成！"))
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
                        self.signal.emit(succeed("OBS 来源切换完成！"))
                else:
                    print('没有切换的场景！')
            except:
                print("OBS 切换中断！")
                flg_start['obs'] = False
                self.signal.emit(fail("OBS 场景切换中断！"))
            self.run_flg = False


def PlanObssignal_accept(msg):
    ui.textBrowser.append(str(msg))


'''
    ShootThread(QThread) 弹射上珠线程
'''


class ShootThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(ShootThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global ranking_array
        global ball_sort
        global balls_start
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('弹射上珠线程！')
            self.signal.emit(succeed("正在弹射上珠。。。"))
            try:
                ranking_array = []  # 排名数组
                for row in range(0, len(init_array)):
                    ranking_array.append([])
                    for col in range(0, len(init_array[row])):
                        ranking_array[row].append(init_array[row][col])
                ball_sort = []  # 位置寄存器
                for row in range(0, max_area_count + 1):
                    ball_sort.append([])
                    for col in range(0, max_lap_count):
                        ball_sort[row].append([])
                balls_start = 0  # 起点球数
                sc.GASetExtDoBit(int(ui.lineEdit_start.text()) - 1, 0)  # 关闭闸门
                shoot_index = int(ui.lineEdit_shoot.text()) - 1
                sc.GASetExtDoBit(shoot_index, 1)
                time.sleep(2)
                end_index = int(ui.lineEdit_end.text()) - 1
                sc.GASetExtDoBit(end_index, 0)
                time_count = 0
                while self.run_flg:
                    time.sleep(1)
                    ball_sort[1][0] = []  # 持续刷新起点排名
                    if (BallsNum_ui.go_flg
                            or (ui.lineEdit_balls_auto.text().isdigit()
                                and ((not BallsNum_ui.isVisible())
                                     and balls_start >= int(ui.lineEdit_balls_auto.text())))
                            or ui.checkBox_Pass_Recognition_Start.isChecked()):
                        self.signal.emit(succeed("隐藏提示"))
                        if BallsNum_ui.go_flg:
                            BallsNum_ui.go_flg = False
                        break

                    time_count += 1
                    if time_count > int(ui.lineEdit_start_count_ball.text()):
                        if int(time_count % 3) == 0:
                            if ui.radioButton_stop_betting.isChecked():
                                self.signal.emit(succeed("隐藏提示"))
                                break  # 封盘时不持续弹窗
                            self.signal.emit(fail("弹射上珠不够"))
                for index in range(0, 16):
                    if index not in [
                        int(ui.lineEdit_start.text()) - 1,
                        int(ui.lineEdit_shake.text()) - 1,
                        int(ui.lineEdit_end.text()) - 1,
                        int(ui.lineEdit_alarm.text()) - 1,
                        int(ui.lineEdit_start_count.text()) - 1,
                    ]:
                        sc.GASetExtDoBit(index, 0)
                OrganCycle_Thread.run_flg = False
                ranking_array = []  # 排名数组
                for row in range(0, len(init_array)):
                    ranking_array.append([])
                    for col in range(0, len(init_array[row])):
                        ranking_array[row].append(init_array[row][col])
                ball_sort = []  # 位置寄存器
                for row in range(0, max_area_count + 1):
                    ball_sort.append([])
                    for col in range(0, max_lap_count):
                        ball_sort[row].append([])
                balls_start = 0  # 起点球数
            except:
                print("弹射上珠参数出错！")
                self.signal.emit(fail("弹射上珠参数出错！"))
            self.run_flg = False


def shootsignal_accept(msg):
    global betting_loop_flg
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)
    if "正在弹射上珠" in msg:
        ui.lineEdit_balls_start.setText('0')
        ui.lineEdit_ball_start.setText('0')
    elif "隐藏提示" in msg:
        BallsNum_ui.hide()
    elif "弹射上珠不够" in msg:
        if Shoot_Thread.run_flg and (not BallsNum_ui.isVisible()):
            BallsNum_ui.show()
            play_alarm()


'''
    AxisThread(QThread) 轴复位线程
'''


class AxisThread(QThread):
    signal = Signal(object)

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
        global axis_reset
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            print('串口运行')
            try:
                self.signal.emit(succeed('轴复位开始...'))
                nAxisList = [bytes.fromhex('01030B07000277EE'),
                             bytes.fromhex('02030B07000277DD'),
                             bytes.fromhex('03030B070002760C'),
                             bytes.fromhex('04030B07000277BB'),
                             bytes.fromhex('05030B070002766A')]
                for nAxis in nAxisList:
                    s485_data = s485.get_axis_pos(nAxis)
                    # print(s485_data)
                    if s485_data != 0:
                        s485_data['highPos'] = s485_data['highPos'] * five_axis[s485_data['nAxisNum'] - 1]
                        res = sc.GASetPrfPos(s485_data['nAxisNum'], s485_data['highPos'])
                        if res == 0:
                            self.signal.emit(succeed('%s 轴复位完成！' % s485_data['nAxisNum']))
                            Pos_Thread.run_flg = True

                            flg_start['card'] = True
                        flg_start['s485'] = True
                    else:
                        flg_start['s485'] = False
                        flg_start['card'] = False
                        self.signal.emit(fail('复位串口未连接！'))
                if axis_reset:
                    for index in range(1, 6):
                        sc.card_move(index, 0)
                    sc.card_update()
                    axis_reset = False
                    self.signal.emit(succeed('轴复位完成！'))
                    for index in range(0, 16):
                        sc.GASetExtDoBit(index, 0)
                    self.signal.emit(succeed('所有机关已关闭！'))
            except:
                print("轴复位出错！")
                flg_start['s485'] = False
                self.signal.emit(fail('轴复位出错！'))
            self.run_flg = False


def axis_signal_accept(msg):
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)


'''
    CmdThread(QThread) 执行运动方案线程
'''


class PlanCmdThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(PlanCmdThread, self).__init__()
        self.run_flg = False
        self.cmd_next = False
        self.running = True
        self.background_state = False
        self.end_state = False
        self.ready_state = False

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global action_area, previous_channel
        global ranking_time_start
        global lottery_term
        global ranking_array
        global ball_sort

        axis_list = [1, 2, 4, 8, 16]
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            if flg_start['card'] and action_area[1] < max_lap_count:
                Audio_Thread.run_flg = True  # 开启音频播放线程
                Ai_Thread.run_flg = True  # 开启AI播放线程
                self.signal.emit(succeed("运动流程：开始！"))
                self.cmd_next = False  # 初始化手动快速跳过下一步动作标志
                cb_index = ui.comboBox_plan.currentIndex()
                time_old = int(time.time())
                for plan_index in range(0, len(plan_list)):
                    self.signal.emit(succeed(
                        '第%s个动作，识别在第%s区%s圈 %s秒！' %
                        (plan_index + 1, action_area[0], action_area[1], int(time.time()) - time_old)))
                    time_old = int(time.time())
                    if (not self.run_flg) or (not flg_start['card']):  # 强制停止线程
                        print('动作未开始！')
                        break
                    if plan_list[plan_index][0] != '1':  # 是否勾选,且在圈数范围内
                        continue
                    if (((((action_area[1] < int(float(plan_list[plan_index][1][0]))  # 循环运行圈数在设定圈数范围内
                            and (float(plan_list[plan_index][1][0]) > 0) and cb_index == 0)  # 或者设定圈数的值为 0 时，最后一圈执行
                           or (action_area[1] == int(float(plan_list[plan_index][1][0])) - 1  # 顺序运行圈数在设定圈数范围内
                               and (float(plan_list[plan_index][1][0]) > 0) and cb_index == 1)  # 或者设定圈数的值为 0 时，最后一圈执行
                           or float(plan_list[plan_index][1][0]) == 0)
                          and not self.background_state
                          and not self.ready_state
                          and not self.end_state))
                            or (float(plan_list[plan_index][1][0]) == -1 and self.background_state)  # 背景动作
                            or (float(plan_list[plan_index][1][0]) == -3 and self.ready_state)  # 准备动作
                            or (float(plan_list[plan_index][1][0]) == -2 and self.end_state)):  # 结束动作动作
                        self.signal.emit(plan_index)  # 控制列表跟踪变色的信号
                        if (int(float(plan_list[plan_index][1][0])) == 0
                                and action_area[1] < max_lap_count - 1):
                            continue
                        try:
                            # print("开启机关")
                            if int(float(plan_list[plan_index][12][0])) != 0:
                                if '-' in plan_list[plan_index][12][0]:  # 带负号即关闭机关
                                    sc.GASetExtDoBit(abs(int(float(plan_list[plan_index][12][0]))) - 1, 0)
                                else:  # 不带负号即开启机关
                                    sc.GASetExtDoBit(abs(int(float(plan_list[plan_index][12][0]))) - 1, 1)
                                if (plan_list[plan_index][12][0] == ui.lineEdit_start_count.text()
                                        and not self.background_state):  # '9'倒数机关打开
                                    ranking_array = []  # 排名数组
                                    for row in range(balls_count):
                                        ranking_array.append([])
                                        for col in range(0, len(init_array[row])):
                                            ranking_array[row].append(init_array[row][col])
                                    ball_sort = []  # 位置寄存器
                                    for row in range(0, max_area_count + 1):
                                        ball_sort.append([])
                                        for col in range(0, max_lap_count):
                                            ball_sort[row].append([])
                                    lottery_term[3] = '进行中'  # 新一期比赛的状态（1.进行中）
                                    self.signal.emit('进行中')  # 修改结果列表中的赛事状态
                                    if flg_start['obs'] and not ui.checkBox_test.isChecked():  # 非测试模式:
                                        try:
                                            # 获取录屏状态
                                            recording_status = cl_request.get_record_status()
                                            if not recording_status.output_active:  # 确保键名正确
                                                cl_request.start_record()  # 开启OBS录像
                                        except:
                                            print('OBS脚本开始错误！')
                                if plan_list[plan_index][12][0] == ui.lineEdit_start.text():  # '2'闸门机关打开
                                    if flg_start['obs'] and not ui.checkBox_test.isChecked():  # 非测试模式:
                                        self.signal.emit('音乐')
                                        Script_Thread.run_type = 'start'
                                        Script_Thread.run_flg = True  # 开始OBS的python脚本计时
                                        map_label_big.bet_running = True
                                        ranking_time_start = time.time()  # 每个球的起跑时间

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
                                    sound_volume = float(tb_audio.item(int(plan_list[plan_index][15][0]) - 1, 3).text())
                                    print(sound_file, sound_times, sound_delay)
                                    # 加载音效
                                    try:
                                        sound_effect = pygame.mixer.Sound(sound_file)
                                        sound_effect.set_volume(sound_volume)  # 设置音量（范围：0.0 到 1.0）
                                        # sound_effect.play(loops=sound_times, maxtime=sound_delay)  # 播放音效
                                        # 如果上一次有播放音效，淡出它（例如在 1000ms 内逐渐停止）
                                        if previous_channel is not None and previous_channel.get_busy():
                                            previous_channel.fadeout(1000)
                                        # 播放新的音效，并保存通道
                                        previous_channel = sound_effect.play(loops=sound_times, maxtime=sound_delay)
                                    except:
                                        print('音效加载失败！~~~~~')

                            if (not ui.checkBox_test.isChecked()
                                    and not self.end_state
                                    and not self.ready_state
                                    and not self.background_state
                                    and (map_label_big.map_action >=
                                         len(map_label_big.path_points) / 10 * int(ui.lineEdit_Map_Action.text()))
                                    and (action_area[1] >= max_lap_count - 1)):  # 到达最后一圈终点前区域，则打开终点及相应机关
                                # 计球器
                                # if len(plan_list) / 10 * 8 <= plan_index:  # 到达最后两个动作时，触发球计数器启动
                                if not ui.radioButton_stop_betting.isChecked():
                                    PlanBallNum_Thread.run_flg = True  # 终点计数器线程

                                # 最后几个动作内，打开终点开关，关闭闸门，关闭弹射
                                sc.GASetExtDoBit(int(ui.lineEdit_end.text()) - 1, 1)  # 打开终点开关
                                # sc.GASetExtDoBit(int(ui.lineEdit_start.text()) - 1, 0)  # 关闭闸门
                                # sc.GASetExtDoBit(int(ui.lineEdit_shoot.text()) - 1, 0)  # 关闭弹射
                            # 轴运动
                            axis_bit = 0  # 非延迟轴统计
                            max_delay_time = 0  # 记录最大延迟时间
                            delay_list = []  # 延迟的轴列表
                            for index, speed_item in enumerate(plan_list[plan_index][7]):
                                sc.card_move(index + 1, int(float(plan_list[plan_index][index + 2][0])),
                                             vel=abs(int(float(speed_item[0]))),
                                             dAcc=float(speed_item[1]),
                                             dDec=float(speed_item[2]),
                                             dVelStart=float(speed_item[4]),
                                             dSmoothTime=int(float(speed_item[5])))
                                if float(speed_item[3]) == 0:
                                    axis_bit += axis_list[index]
                                else:
                                    delay_list.append([axis_list[index], float(format(float(speed_item[3]), ".3f"))])
                                if max_delay_time < float(format(float(speed_item[3]), ".3f")):
                                    max_delay_time = float(format(float(speed_item[3]), ".3f"))
                            list_equal = {}
                            for index in range(len(delay_list)):
                                if not (delay_list[index][1] in list_equal.keys()):
                                    list_equal[delay_list[index][1]] = delay_list[index][0]
                                else:
                                    list_equal[delay_list[index][1]] += delay_list[index][0]
                            delay_list = []
                            for key in list_equal.keys():
                                delay_list.append([list_equal[key], key])
                            if axis_bit != 0:  # 非延迟轴
                                res = sc.card_update(axis_bit)
                                if res != 0:
                                    print("运动板通信出错！")
                                    flg_start['card'] = False
                                    self.signal.emit(fail("运动板通信出错！"))
                            old_time = 0
                            for t in range(0, int(max_delay_time * 100) + 1):  # 延迟轴
                                for index in range(len(delay_list)):
                                    if t >= delay_list[index][1] * 100 > old_time:
                                        sc.card_update(delay_list[index][0])
                                        old_time = t
                                time.sleep(0.01)
                        except:
                            print("运动板运行出错！")
                            self.signal.emit(fail("运动板通信出错！"))

                        if self.run_flg:
                            try:
                                if float(plan_list[plan_index][11][0]) > 0:
                                    time.sleep(float(plan_list[plan_index][11][0]))  # 延时，等待镜头缩放完成
                                # 摄像头缩放
                                if 0 < int(float(plan_list[plan_index][10][0])) <= 80:  # 摄像头缩放
                                    PlanCam_Thread.camitem = [int(float(plan_list[plan_index][10][0])),
                                                              float(plan_list[plan_index][11][0])]
                                    PlanCam_Thread.run_flg = True  # 摄像头线程
                            except:
                                print("摄像头数据出错！")
                                self.signal.emit(fail("摄像头数据出错！"))
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
                                        self.signal.emit(fail("%s 卫星图号出错！" % plan_list[plan_index][14][0]))
                                        break
                                    if len(camera_points) - 1 < abs(int(float(plan_list[plan_index][14][0]))):
                                        self.signal.emit(fail("%s 卫星图号出错！" % plan_list[plan_index][14][0]))
                                        break
                                    # 判断镜头点位在运行区域内则进入下一个动作循环
                                    self.signal.emit({'map_action': map_label_big.map_action})
                                    if (len(camera_points) > abs(int(float(plan_list[plan_index][14][0])))
                                            and (int(camera_points[abs(int(float(plan_list[plan_index][14][0])))]
                                                     [cb_index + 1][0][0]) - 100
                                                 < map_label_big.map_action)):
                                        break
                                    t_over += 1
                                    if plan_list[plan_index][16][0] != '0':
                                        if t_over >= abs(float(plan_list[plan_index][16][0])) * 10:  # 每个动作超时时间
                                            self.signal.emit(fail('第 %s 个动作 等待超时！' % str(plan_index + 1)))
                                            print('等待超时！')
                                            break
                                    else:
                                        if t_over >= 200:
                                            self.signal.emit(fail('第 %s 个动作 等待超过15秒！' % str(plan_index + 1)))
                                            print('等待超过20秒！')
                                            break
                                    if self.cmd_next:  # 手动进入下一个动作
                                        break
                                    time.sleep(0.1)
                        except:
                            print("动作等待数据出错！")
                            self.signal.emit(fail("动作等待数据出错！"))
                        if self.cmd_next:  # 快速执行下一个动作
                            self.signal.emit(succeed("跳过动作 %s！" % (plan_index + 1)))
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
                                self.signal.emit(fail("场景数据出错！"))

                # 背景模式不循环
                if self.background_state or self.ready_state or self.end_state:
                    self.background_state = False
                    self.ready_state = False
                    self.run_flg = False
                    # 结束模式不循环
                    if self.end_state:
                        self.end_state = False
                        self.signal.emit('end_state')
                        if flg_start['card']:
                            for index in range(0, 16):  # 关闭所有机关
                                if index not in [int(ui.lineEdit_shoot.text()) - 1,
                                                 int(ui.lineEdit_start.text()) - 1,
                                                 int(ui.lineEdit_shake.text()) - 1,
                                                 int(ui.lineEdit_end.text()) - 1,
                                                 int(ui.lineEdit_alarm.text()) - 1,
                                                 int(ui.lineEdit_start_count.text()) - 1,
                                                 ]:
                                    sc.GASetExtDoBit(index, 0)
                        self.signal.emit(succeed("辅助模式完成！"))
                    continue
                # 强制中断情况处理
                if not ui.checkBox_test.isChecked() and not self.run_flg:  # 强制中断情况下的动作
                    # 强制中断则打开终点开关，关闭闸门，关闭弹射
                    print('另外开关~~~~~~~~~')
                    sc.GASetExtDoBit(int(ui.lineEdit_end.text()) - 1, 1)  # 打开终点开关
                    # sc.GASetExtDoBit(int(ui.lineEdit_start.text()) - 1, 0)  # 关闭闸门
                    # sc.GASetExtDoBit(int(ui.lineEdit_shoot.text()) - 1, 0)  # 关闭弹射
                    # main_music_worker.toggle_enablesignal.emit(False)
                    self.signal.emit(succeed("运动流程：中断！"))
                if ui.checkBox_test.isChecked():
                    self.signal.emit(succeed("测试流程：完成！"))
                    self.run_flg = False  # 测试模式，不自动关闭任何机关
                else:  # 每次循环增加一圈，初始化动作位置为0，初始化地图位置为0
                    action_area[2] = 1  # 写入标志 1 为独占写入
                    action_area[0] = 0
                    if action_area[1] < max_lap_count:
                        action_area[1] += 1
                    action_area[2] = 0  # 写入标志 0 为任意写入
                    if action_area[1] < max_lap_count:
                        map_label_big.map_action = 0
            else:  # 运行出错，或者超出圈数，流程完成时执行
                if not ui.checkBox_test.isChecked():  # 非测试模式，流程结束始终关闭闸门
                    sc.GASetExtDoBit(int(ui.lineEdit_end.text()) - 1, 1)  # 打开终点开关
                    # sc.GASetExtDoBit(int(ui.lineEdit_start.text()) - 1, 0)  # 关闭闸门
                    # sc.GASetExtDoBit(int(ui.lineEdit_shoot.text()) - 1, 0)  # 关闭弹射
                self.signal.emit(succeed("运动流程：完成！"))
                print('动作已完成！')
                if not flg_start['card']:
                    self.signal.emit(fail("运动卡未链接！"))
                self.run_flg = False


def cmd_signal_accept(msg):
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
                ui.lineEdit_area_2.setText(str(msg['map_action']))
        else:
            if msg == 'end_state':
                ui.checkBox_end_stop.setChecked(False)
                ui.checkBox_end_BlackScreen.setChecked(False)
            if msg == '音乐':
                if not ui.checkBox_test.isChecked():  # 如果是测试模式，不播放主题音乐
                    num = random.randint(1, 3)
                    getattr(ui, 'radioButton_music_%s' % num).click()
                    ui.checkBox_main_music.setChecked(True)
            if msg == '进行中':
                tb_result = ui.tableWidget_Results
                tb_result.item(0, 3).setText(lottery_term[3])  # 新一期比赛的状态（1.进行中）
                ui.label_time_count.setText('0')
            ui.textBrowser_msg.append(msg)
            scroll_to_bottom(ui.textBrowser_msg)
    except:
        print("运行数据处理出错！")


"""
    ui工作线程
"""


class UiWorker(QObject):
    toggle_enablesignal = Signal(object)

    def __init__(self, z_object):
        super().__init__()
        self.z_object = z_object
        self.toggle_enablesignal.connect(self.toggle_enable)

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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[3] = pValue[3] - 30000 * int(five_key[3])
                ui.lineEdit_axis3.setText(str(pValue[3]))
                sc.card_setpos(4, pValue[3])
                sc.card_update()

            if key == key.end:
                print('头右')
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[3] = pValue[3] + 30000 * int(five_key[3])
                ui.lineEdit_axis3.setText(str(pValue[3]))
                sc.card_setpos(4, pValue[3])
                sc.card_update()

            if key == key.page_up:
                print('头上')
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
                flg_key_run = True
                Pos_Thread.run_flg = False
                pValue[4] = pValue[4] + 30000 * int(five_key[4])
                ui.lineEdit_axis4.setText(str(pValue[4]))
                sc.card_setpos(5, pValue[4])
                sc.card_update()

            if key == key.page_down:
                print('头下')
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
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
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
                s485.cam_zoom_off()
            elif key.char == '*':
                tb_step_worker.toggle_enablesignal.emit(ui.checkBox_test.isChecked())
                s485.cam_zoom_off()
        except:
            pass
            # print(key)
        Pos_Thread.run_flg = False


def keyboard_press(key):
    global flg_key_run
    try:
        if key == key.enter:
            if ui.checkBox_key_stop.isChecked():
                cmd_stop()
    except:
        pass
    try:
        if key.char == '-':
            stop_alarm()
    except:
        pass
    if ui.checkBox_key.isChecked() and flg_start['card']:
        try:
            Pos_Thread.run_flg = True
            if key == key.up:
                if flg_key_run:
                    print('前')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = 2000000 * int(five_key[1])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(2, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.down:
                if flg_key_run:
                    print('后')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = -2000000 * int(five_key[1])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(2, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.left:
                if flg_key_run:
                    print('左')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = -2000000 * int(five_key[0])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(1, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.right:
                if flg_key_run:
                    print('右')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = 2000000 * int(five_key[0])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(1, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.insert:
                if flg_key_run:
                    print('上')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = -2000000 * int(five_key[2])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(3, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.delete:
                if flg_key_run:
                    print('下')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    pos = 2000000 * int(five_key[2])
                    if pos <= 0:
                        pos = 0
                    sc.card_move(3, pos=pos)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.home:
                if flg_key_run:
                    print('头左')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    sc.card_move(4, pos=-2000000 * int(five_key[3]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.end:
                if flg_key_run:
                    print('头右')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    sc.card_move(4, pos=2000000 * int(five_key[3]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_up:
                if flg_key_run:
                    print('头下')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    sc.card_move(5, pos=2000000 * int(five_key[4]), vel=50)
                    sc.card_update()
                    flg_key_run = False
            elif key == key.page_down:
                if flg_key_run:
                    print('头上')
                    tb_step_worker.toggle_enablesignal.emit(False)
                    sc.card_move(5, pos=-2000000 * int(five_key[4]), vel=50)
                    sc.card_update()
                    flg_key_run = False
        except AttributeError:
            # print(key)
            pass
        try:
            if key.char == '/':
                tb_step_worker.toggle_enablesignal.emit(False)
                s485.cam_zoom_move(5)
            elif key.char == '*':
                tb_step_worker.toggle_enablesignal.emit(False)
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
def save_plan_json():
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

    file = "Plan_config.json"
    plan_all['plans']['plan%d' % (plan_num + 1)]['plan_name'] = plan_name
    plan_all['plans']['plan%d' % (plan_num + 1)]['plan_list'] = plan_list_temp
    try:
        # 写入 JSON 文件
        with open(file, "w", encoding="utf-8") as file:
            json.dump(plan_all, file, indent=4, ensure_ascii=False)
        ui.textBrowser.append(succeed('方案保存：成功'))
    except:
        ui.textBrowser.append(fail('方案保存：失败'))
    print("保存成功~！")


# 载入方案
def load_plan_json():
    global plan_names
    global plan_all
    global camera_points
    file = "Plan_config.json"
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            plan_all = json.load(f)
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
        # camera_points[index][0].show()
    for index in range(len(audio_points)):  # 卫星图刷新
        num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
        audio_points[index][0].move(*audio_points[index][num][1])  # 设置初始位置
        # audio_points[index][0].show()
    for index in range(len(ai_points)):  # 卫星图刷新
        num = ui.comboBox_plan.currentIndex() + 1  # 方案索引+1
        ai_points[index][0].move(*ai_points[index][num][1])  # 设置初始位置
        # ai_points[index][0].show()
    save_main_json()


def save_main_json():
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

    file = "main_config.json"
    if not os.path.exists(file):
        return
    try:
        with (open(file, "r", encoding="utf-8") as f):
            main_all = json.load(f)
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
            main_all['lineEdit_upload_Path'] = ui.lineEdit_upload_Path.text()
            main_all['lineEdit_saidao_Path'] = ui.lineEdit_saidao_Path.text()
            main_all['lineEdit_end1_Path'] = ui.lineEdit_end1_Path.text()
            main_all['lineEdit_end2_Path'] = ui.lineEdit_end2_Path.text()
            main_all['scene_name'] = ui.lineEdit_scene_name.text()
            main_all['source_ranking'] = ui.lineEdit_source_ranking.text()
            main_all['source_picture'] = ui.lineEdit_source_picture.text()
            main_all['source_settlement'] = ui.lineEdit_source_settlement.text()
            main_all['source_end'] = ui.lineEdit_source_end.text()
            main_all['monitor_sort'] = ui.lineEdit_monitor_sort.text()
            main_all['sony_sort'] = ui.lineEdit_sony_sort.text()
            main_all['lineEdit_start'] = ui.lineEdit_start.text()
            main_all['lineEdit_shoot'] = ui.lineEdit_shoot.text()
            main_all['lineEdit_shake'] = ui.lineEdit_shake.text()
            main_all['lineEdit_end'] = ui.lineEdit_end.text()
            main_all['lineEdit_start_count'] = ui.lineEdit_start_count.text()
            main_all['lineEdit_alarm'] = ui.lineEdit_alarm.text()
            main_all['lineEdit_shoot_2'] = ui.lineEdit_shoot_2.text()
            main_all['lineEdit_shoot_3'] = ui.lineEdit_shoot_3.text()
            main_all['lineEdit_Cycle'] = ui.lineEdit_Cycle.text()
            main_all['lineEdit_Cycle_Time'] = ui.lineEdit_Cycle_Time.text()
            main_all['lineEdit_area_limit'] = ui.lineEdit_area_limit.text()
            main_all['lineEdit_volume_1'] = ui.lineEdit_volume_1.text()
            main_all['lineEdit_volume_2'] = ui.lineEdit_volume_2.text()
            main_all['lineEdit_volume_3'] = ui.lineEdit_volume_3.text()
            main_all['lineEdit_background_Path'] = ui.lineEdit_background_Path.text()
            main_all['lineEdit_Start_Path'] = ui.lineEdit_Start_Path.text()
            main_all['lineEdit_Map_Action'] = ui.lineEdit_Map_Action.text()
            main_all['lineEdit_GPS_Num'] = ui.lineEdit_GPS_Num.text()
            main_all['lineEdit_End_Num'] = ui.lineEdit_End_Num.text()
            main_all['lineEdit_lost'] = ui.lineEdit_lost.text()
            main_all['checkBox_Cycle'] = ui.checkBox_Cycle.isChecked()
            main_all['checkBox_Monitor_Horizontal'] = ui.checkBox_Monitor_Horizontal.isChecked()
            main_all['checkBox_Monitor_Vertica'] = ui.checkBox_Monitor_Vertica.isChecked()
            main_all['checkBox_Main_Horizontal'] = ui.checkBox_Main_Horizontal.isChecked()
            main_all['checkBox_Main_Vertica'] = ui.checkBox_Main_Vertica.isChecked()
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
            json.dump(main_all, f, indent=4, ensure_ascii=False)
        f.close()
        ui.textBrowser_save_msg.append(succeed('方案保存：成功'))
        ui.textBrowser_background_data.append(succeed('方案保存：成功'))
    except:
        ui.textBrowser_save_msg.append(fail('方案保存：失败'))
        ui.textBrowser_background_data.append(fail('方案保存：失败'))
    print("保存成功~！")


def load_main_json():
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
    file = "main_config.json"
    if os.path.exists(file):
        # try:
        f = open(file, 'r', encoding='utf-8')
        main_all = json.load(f)
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
        ui.lineEdit_monitor_sort.setText(main_all['monitor_sort'])
        ui.lineEdit_sony_sort.setText(main_all['sony_sort'])
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
        ui.lineEdit_upload_Path.setText(main_all['lineEdit_upload_Path'])
        ui.lineEdit_saidao_Path.setText(main_all['lineEdit_saidao_Path'])
        ui.lineEdit_end1_Path.setText(main_all['lineEdit_end1_Path'])
        ui.lineEdit_end2_Path.setText(main_all['lineEdit_end2_Path'])
        ui.lineEdit_scene_name.setText(main_all['scene_name'])
        ui.lineEdit_source_ranking.setText(main_all['source_ranking'])
        ui.lineEdit_source_picture.setText(main_all['source_picture'])
        ui.lineEdit_source_settlement.setText(main_all['source_settlement'])
        ui.lineEdit_source_end.setText(main_all['source_end'])
        ui.lineEdit_shoot.setText(main_all['lineEdit_shoot'])
        ui.lineEdit_start.setText(main_all['lineEdit_start'])
        ui.lineEdit_shake.setText(main_all['lineEdit_shake'])
        ui.lineEdit_end.setText(main_all['lineEdit_end'])
        ui.lineEdit_start_count.setText(main_all['lineEdit_start_count'])
        ui.lineEdit_alarm.setText(main_all['lineEdit_alarm'])
        ui.lineEdit_shoot_2.setText(main_all['lineEdit_shoot_2'])
        ui.lineEdit_shoot_3.setText(main_all['lineEdit_shoot_3'])
        ui.lineEdit_Cycle.setText(main_all['lineEdit_Cycle'])
        ui.lineEdit_Cycle_Time.setText(main_all['lineEdit_Cycle_Time'])
        ui.lineEdit_Track_number.setText(main_all['Track_number'])
        ui.pushButton_start_game.setEnabled(main_all['pushButton_start_game'])
        ui.lineEdit_area_limit.setText(main_all['lineEdit_area_limit'])
        ui.lineEdit_volume_1.setText(main_all['lineEdit_volume_1'])
        ui.lineEdit_volume_2.setText(main_all['lineEdit_volume_2'])
        ui.lineEdit_volume_3.setText(main_all['lineEdit_volume_3'])
        ui.lineEdit_Map_Action.setText(str(main_all['lineEdit_Map_Action']))
        ui.lineEdit_GPS_Num.setText(main_all['lineEdit_GPS_Num'])
        ui.lineEdit_End_Num.setText(main_all['lineEdit_End_Num'])
        ui.lineEdit_background_Path.setText(main_all['lineEdit_background_Path'])
        ui.lineEdit_Start_Path.setText(main_all['lineEdit_Start_Path'])
        ui.lineEdit_lost.setText(main_all['lineEdit_lost'])
        ui.comboBox_plan.setCurrentIndex(int(main_all['comboBox_plan']))
        ui.checkBox_Cycle.setChecked(main_all['checkBox_Cycle'])
        ui.checkBox_Monitor_Horizontal.setChecked(main_all['checkBox_Monitor_Horizontal'])
        ui.checkBox_Monitor_Vertica.setChecked(main_all['checkBox_Monitor_Vertica'])
        ui.checkBox_Main_Horizontal.setChecked(main_all['checkBox_Main_Horizontal'])
        ui.checkBox_Main_Vertica.setChecked(main_all['checkBox_Main_Vertica'])
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
        for i in range(balls_count, 10):
            getattr(ui, 'lineEdit_result_%s' % i).hide()
            getattr(result_ui, 'lineEdit_result_%s' % i).hide()
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


def net_camera():
    r_url = ui.lineEdit_rtsp_url.text()
    parsed_url = r_url.split('@')[-1]
    ip_address = parsed_url.split(':')[0]
    webbrowser.open(ip_address)


def cmd_run():
    if not ui.checkBox_test.isChecked():
        if not ReStart_Thread.run_flg:
            ReStart_Thread.run_flg = True
        # ui.checkBox_saveImgs_auto.setChecked(True)
    else:
        save_plan_json()
        plan_refresh()
        PlanCmd_Thread.run_flg = True


def cmd_loop():
    global betting_loop_flg
    if ui.radioButton_stop_betting.isChecked():
        return
    betting_loop_flg = True
    ui.checkBox_test.setChecked(False)
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
    tcp_result_thread.send_type = ''  # 退出结果页面循环
    sc.card_stop()  # 立即停止


def card_start():
    if not CardStart_Thread.isRunning():
        CardStart_Thread.start()


def card_reset():
    global axis_reset
    axis_reset = True
    Axis_Thread.run_flg = True


def card_close_all():
    if not flg_start['card']:
        return
    for index in range(0, 16):
        if index not in [
            # int(ui.lineEdit_shoot.text()) - 1,
            int(ui.lineEdit_start.text()) - 1,
            int(ui.lineEdit_shake.text()) - 1,
            int(ui.lineEdit_end.text()) - 1,
            int(ui.lineEdit_alarm.text()) - 1,
            int(ui.lineEdit_start_count.text()) - 1,
        ]:
            sc.GASetExtDoBit(index, 0)
    ui.textBrowser.append(succeed('已经关闭所有机关！'))
    ui.textBrowser_msg.append(succeed('已经关闭所有机关！'))
    ui.textBrowser_background_data.append(succeed('已经关闭所有机关！'))


def end_all():
    res = QMessageBox.warning(z_window, '提示', '是否关闭直播，和所有机关！',
                              QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    print(res)
    if res == QMessageBox.Yes:
        card_reset()
        card_close_all()
        if flg_start['live']:
            cl_request.stop_stream()


def card_on_off_all():
    if not flg_start['card']:
        return
    for index in range(0, 16):
        if index not in [int(ui.lineEdit_shoot.text()) - 1,
                         int(ui.lineEdit_start.text()) - 1,
                         int(ui.lineEdit_shake.text()) - 1,
                         int(ui.lineEdit_end.text()) - 1,
                         int(ui.lineEdit_alarm.text()) - 1,
                         int(ui.lineEdit_start_count.text()) - 1,
                         ]:
            if ui.checkBox_all.isChecked():
                sc.GASetExtDoBit(index, 1)
            else:
                sc.GASetExtDoBit(index, 0)
    ui.textBrowser.append(succeed('已经关闭所有机关！'))
    ui.textBrowser_msg.append(succeed('已经关闭所有机关！'))
    ui.textBrowser_background_data.append(succeed('已经关闭所有机关！'))


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
        elif tb_step.item(row, col) and not is_natural_num(tb_step.item(row, col).text()):
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
        save_path = ui.lineEdit_saidao_Path.text()
    else:
        saveBackground = 1  # 0 无球录图标志
        save_path = ui.lineEdit_background_Path.text()
    form_data = {
        'saveImgRun': saveImgRun,
        'requestType': 'saveImg',
        'saveBackground': saveBackground,
        'saveImgNum': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
        # 'saveImgNum': '1',
        # 'saveImgPath': r'\\%s\%s' % (local_ip[2], ui.lineEdit_saidao_Path.text()),
        'saveImgPath': r'%s' % save_path,
    }
    try:
        for index in range(len(wakeup_addr)):
            r = requests.post(url=wakeup_addr[index], data=form_data)
            print(r.text)
    except:
        print('图像识别主机通信失败！')


def save_start_images(saveImgRun):
    saveBackground = 0  # 0 有球录图标志
    save_path = ui.lineEdit_Start_Path.text()
    form_data = {
        'saveImgRun': saveImgRun,
        'requestType': 'saveImg',
        'saveBackground': saveBackground,
        'saveImgNum': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
        # 'saveImgNum': '1',
        # 'saveImgPath': r'\\%s\%s' % (local_ip[2], ui.lineEdit_saidao_Path.text()),
        'saveImgPath': r'%s' % save_path,
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


class PositionsLiveThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(PositionsLiveThread, self).__init__()
        self.running = True
        self.run_flg = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        def on_open(z_ws):
            """连接成功后，持续发送数据"""
            data = {"message": "Hello, server!"}
            while True:  # 监测是否需要退出
                if not self.run_flg:
                    z_ws.close()
                    break
                try:
                    if (data != positions_live
                            and lottery_term[3] == '进行中'
                            and ui.radioButton_start_betting.isChecked()):
                        data = positions_live
                        z_ws.send(json.dumps(data))
                        # print(f"已发送数据: {data}")
                    time.sleep(0.05)  # 每 2 秒发送一次
                except Exception as e:
                    print(f"发送数据时出错: {e}")
                    self.signal.emit(fail(f"发送数据时出错: {e}"))
                    break  # 退出循环，触发 on_close

        while self.running:
            try:
                ws = websocket.WebSocketApp(WS_URL)
                print("实时数据服务:链接成功！")
                self.signal.emit(succeed("实时数据服务:链接成功！"))
                ws.on_open = on_open
                if self.run_flg:
                    ws.run_forever()  # 运行 WebSocket 连接
                else:
                    ws.close()
            except Exception as e:
                print(f"WebSocket 连接失败: {e}")
                self.signal.emit(fail(f"WebSocket 连接失败: {e}"))
            time.sleep(0.01)


def livesignal_accept(msg):
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser_msg)


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
    def __init__(self, picture_size=860, ball_radius=10, step_length=2.0, ball_space=11, flash_time=30, parent=None):
        """
        picture_size 地图像素
        ball_radius 球半径（像素）
        step_length 步长（每个轨迹点之间的像素）
        ball_space  两个球之间的距离（单位:步数）
        flash_time  画图刷新频率时间
        """
        super().__init__(parent)
        global map_orbit
        self.map_action = 0  # 地图触发点位
        img = map_data[0]
        pixmap = QPixmap(img)
        self.picture_size = picture_size  # 像素
        self.step_length = step_length  # 步长
        self.ball_space = ball_space  # 球之间的距离（步数）
        self.ball_radius = ball_radius  # 像素
        self.bet_running = False
        # 设置label的尺寸
        self.setMaximumSize(picture_size, picture_size)
        self.setPixmap(pixmap)
        self.setScaledContents(True)

        self.color_names = {'red': QColor(255, 0, 0), 'green': QColor(0, 255, 0), 'blue': QColor(0, 0, 255),
                            'pink': QColor(255, 0, 255), 'yellow': QColor(255, 255, 0), 'black': QColor(0, 0, 0),
                            'purple': QColor(128, 0, 128), 'orange': QColor(255, 165, 0),
                            'White': QColor(248, 248, 255),
                            'Brown': QColor(139, 69, 19)}

        self.path_points = []
        if os.path.exists(map_data[1]):
            with open(map_data[1], 'r', encoding='utf-8') as fcc_file:
                fcc_data = json.load(fcc_file)
            if picture_size == 860:
                map_scale = 1
            else:
                map_scale = picture_size / int(map_data[2])  # 缩放比例
            for p in fcc_data[0]["content"]:
                self.path_points.append((p['x'] * map_scale, p['y'] * map_scale))
            self.path_points = divide_path(self.path_points, self.step_length)
            print('地图长度:%s' % len(self.path_points))
            if map_scale == 1:
                map_orbit = self.path_points

        # self.num_balls = 8  # 8个小球
        self.speed = 1  # 小球每次前进的步数（可以根据需要调整）
        self.flash_time = flash_time
        self.positions = []  # 每个球的当前位置索引
        for num in range(balls_count):
            self.positions.append([num * self.ball_space, init_array[num][5], 0, 0, 0, 0])
            # [位置索引, 顔色, 號碼, 圈數, 实际位置, 停留时间]
        # 创建定时器，用于定时更新球的位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)  # 定时触发更新
        self.timer.start(self.flash_time)  # 每1秒更新一次

    def update_positions(self):
        global positions_live, ranking_time
        global z_ranking_res
        global ball_stop
        global pos_stop
        # 更新每个小球的位置
        if len(self.positions) != balls_count:
            self.positions = []  # 每个球的当前位置索引[位置索引，球颜色，球号码, 圈數, 实际位置, 停留时间]
            for num in range(balls_count):
                self.positions.append([num * self.ball_space, init_array[num][5], 0, 0, 0, 0])
        for num in range(0, balls_count):
            if len(ranking_array) >= balls_count and ranking_array[num][5] in self.color_names.keys():
                area_num = max_area_count - balls_count  # 跟踪区域数量
                if ((ranking_array[num][6] <= max_area_count
                     and not ObsEnd_Thread.ball_flg)
                        or (ranking_array[num][6] >= max_area_count + 1
                            and ObsEnd_Thread.ball_flg)):
                    p = int(len(self.path_points) * (ranking_array[num][6] / area_num))
                    if p >= len(self.path_points):
                        p = len(self.path_points) - 1
                    for i in range(len(self.positions)):  # 排序
                        if self.positions[i][1] == ranking_array[num][5]:
                            self.positions[i], self.positions[num] = self.positions[num], self.positions[i]
                            self.positions[num][3] = ranking_array[num][8]
                            if self.positions[num][4] != p:
                                self.positions[num][4] = p
                                self.positions[num][5] = int(time.time())
                    if ranking_array[num][6] <= 1:  # 起点
                        if num == 0:
                            index = len(ranking_array) * self.ball_space
                        else:
                            index = len(ranking_array) * self.ball_space - num * self.ball_space
                    elif (ranking_array[num][8] >= max_lap_count - 1  # 最后一圈处理
                          and ranking_array[num][6] >= max_area_count / 3 * 2
                          and self.positions[num][0] > len(self.path_points) - num * self.ball_space - 20):
                        if num == 0:
                            index = len(self.path_points) - 1
                        else:
                            index = len(self.path_points) - 1 - num * self.ball_space
                    else:
                        if p - self.positions[num][0] > 50:
                            self.speed = 3
                        elif 50 >= p - self.positions[num][0] >= 25:
                            self.speed = 2
                        elif p < self.positions[num][0] and ranking_array[num][9] == 1:
                            self.positions[num][0] = p  # 跨圈情况
                        elif (int(time.time()) - self.positions[num][5] > int(ui.lineEdit_lost.text())
                              and self.map_action <= len(self.path_points) / 10 * int(ui.lineEdit_Map_Action.text())):
                            self.positions[num][0] = p  # 盲跑时间
                        elif (int(time.time()) - self.positions[num][5] >= 0    # 最后路段不盲跑
                              and self.map_action > len(self.path_points) / 10):
                            self.positions[num][0] = p  # 最后路段，盲跑时间为1秒
                        elif (int(time.time()) - self.positions[num][5] > 1
                              and self.map_action > len(self.path_points) / 10 * int(ui.lineEdit_Map_Action.text())):
                            self.positions[num][0] = p  # 最后路段，盲跑时间为1秒
                        else:
                            self.speed = 1
                        index = self.positions[num][0] + self.speed
                    if index < len(self.path_points) and ranking_array[num][8] < max_lap_count:
                        self.positions[num][0] = index
                        for color_index in range(len(init_array)):
                            if init_array[color_index][5] == ranking_array[num][5]:
                                self.positions[num][2] = color_index + 1
        # 模拟排名
        if ranking_array[0][6] < max_area_count - 2 and ranking_array[0][9] == 0:
            self.positions.sort(key=lambda x: (-x[3], -x[0]))
            z_ranking_res = [ball[2] for ball in self.positions]

        # 更新实时触发位置
        for i in range(len(self.positions)):
            if ((self.positions[i][0] - self.map_action < len(self.path_points) / 3)
                    and (self.positions[i][3]) == action_area[1]):  # 圈数重置后，重新位置更新范围限制300个点位以内
                if self.picture_size == 860:
                    if self.map_action < self.positions[i][0]:
                        self.map_action = self.positions[i][0]  # 赋值实时位置
                        break

        # 实时位置数据包处理
        res = []
        if self.picture_size == 860:
            for i in range(balls_count):
                x, y = self.path_points[self.positions[i][0]]
                b = round(self.positions[i][0] / len(self.path_points), 4)
                if self.bet_running:
                    ranking_time = int((time.time() - ranking_time_start) * 1000)
                res.append(
                    {"pm": i + 1, "id": self.positions[i][2], "x": int(x), "y": int(y), "bFloat": b,
                     "b": b * 100, "t": ranking_time})
            positions_live = {
                "raceTrackID": Track_number,
                "term": term,
                "timestampMs": int(time.time() * 1000),
                "result": res
            }

        # 保留卡珠位置
        if ObsEnd_Thread.ball_flg and ObsEnd_Thread.screen_flg:
            ball_stop = True
        if TrapBall_ui.trap_flg:
            pos_stop = copy.deepcopy(self.positions)
            for num in range(0, balls_count):
                for i in range(len(pos_stop)):  # 排序
                    if pos_stop[i][1] == ranking_array[num][5]:
                        pos_stop[i], pos_stop[num] = pos_stop[num], pos_stop[i]
                        area_num = max_area_count - balls_count  # 跟踪区域数量
                        p = int(len(self.path_points) * (ranking_array[num][6] / area_num))
                        if p < len(self.path_points):
                            pos_stop[num][0] = p
            TrapBall_ui.trap_flg = False
        if ball_stop:
            if len(pos_stop) == len(self.positions):
                self.positions = copy.deepcopy(pos_stop)

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
                part = len(self.path_points) / (max_area_count - balls_count)
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
                painter.setBrush(QBrush(self.color_names[self.positions[index_position][1]], Qt.SolidPattern))
                # 绘制球
                painter.drawEllipse(int(x - self.ball_radius), int(y - self.ball_radius),
                                    self.ball_radius * 2, self.ball_radius * 2)
                if self.picture_size == 860:
                    if str(self.positions[index_position][2]) == '7':
                        font = QFont("Arial", 12, QFont.Bold)  # 字体：Arial，大小：16，加粗
                        painter.setFont(font)
                        painter.setPen('black')
                        painter.drawText(int(x - self.ball_radius / 2), int(y + self.ball_radius / 2),
                                         str(self.positions[index_position][2]))
                    elif str(self.positions[index_position][2]) == '1':
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
        file = "camera_points.json"
        for index in range(len(camera_points)):
            points_save.append([index, [(camera_points[index][1][0]), (camera_points[index][1][1])],
                                [(camera_points[index][2][0]), (camera_points[index][2][1])],
                                [(camera_points[index][3][0]), (camera_points[index][3][1])]])
    elif color == 'blue':
        file = "audio_points.json"
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
        file = "ai_points.json"
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
    try:
        with open(file, "w", encoding="utf-8") as f:
            if color == 'red':
                json.dump({'camera_points': points_save}, f, indent=4, ensure_ascii=False)
            elif color == 'blue':
                json.dump({'audio_points': points_save, 'audio_table': table_save}, f, indent=4, ensure_ascii=False)
            elif color == 'green':
                json.dump({'ai_points': points_save, 'ai_table': table_save}, f, indent=4, ensure_ascii=False)
        f.close()
        ui.textBrowser.append(succeed('%s点位保存：成功' % color))
    except:
        ui.textBrowser.append(fail('%s点位保存：失败' % color))
    print("保存成功~！")


def load_points_json(color):
    global camera_points
    global audio_points
    global ai_points
    if color == 'red':
        file = "camera_points.json"
    elif color == 'blue':
        file = "audio_points.json"
    elif color == 'green':
        file = "ai_points.json"
    else:
        return
    if os.path.exists(file):
        try:
            f = open(file, 'r', encoding='utf-8')
            points_all = json.load(f)
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
                    for col in range(col_count):
                        if col == col_count - 1:
                            text = str(audio_table[row][0])
                            pattern = r"(?<=\/)[^\/]+(?=\.)"
                            try:
                                match = re.search(pattern, text).group()
                            except:
                                match = '选择文件'
                            btn = QPushButton(str(match))
                            btn.clicked.connect(lambda _, r=row: open_file_dialog(tb_audio, r))  # 传递行号
                            tb_audio.setCellWidget(row, col_count - 1, btn)
                        else:
                            audio_item = QTableWidgetItem(str(audio_table[row][col]))
                            audio_item.setTextAlignment(Qt.AlignCenter)
                            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                            tb_audio.setItem(row, col, audio_item)

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
                    for col in range(col_count):
                        if col == col_count - 1:
                            text = str(ai_table[row][0])
                            pattern = r"(?<=\/)[^\/]+(?=\.)"
                            try:
                                match = re.search(pattern, text).group()
                            except:
                                match = '选择文件'
                            btn = QPushButton(str(match))
                            btn.clicked.connect(lambda _, r=row: open_file_dialog(tb_ai, r))  # 传递行号
                            tb_ai.setCellWidget(row, col_count - 1, btn)
                        else:
                            ai_item = QTableWidgetItem(str(ai_table[row][col]))
                            ai_item.setTextAlignment(Qt.AlignCenter)
                            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                            tb_ai.setItem(row, col, ai_item)
        except:
            print("提取点位错误！")
    else:
        print("文件不存在")


def open_file_dialog(tb, r):
    # 打开文件选择对话框
    file_path, _ = QFileDialog.getOpenFileName(tb, "选择文件")
    if file_path:
        try:
            # 更新对应行的文件路径
            tb.item(r, 0).setText(file_path)
            col_count = tb.columnCount()
            text = str(file_path)
            pattern = r"(?<=\/)[^\/]+(?=\.)"
            match = re.search(pattern, text).group()
            tb.cellWidget(r, col_count - 1).setText(match)
        except:
            print('打开声音文件错误！')


def add_camera_points():
    global camera_points
    # 加载图标并放置在窗口中心
    camera_points_count = len(camera_points)
    num = ui.comboBox_plan.currentIndex() + 1
    if num == 1:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [[0], [camera_points_count * 20, 0]], [[0], [0, 0]], [[0], [0, 0]]])
    if num == 2:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [[0], [0, 0]], [[0], [camera_points_count * 20, 0]], [[0], [0, 0]]])
    if num == 3:
        camera_points.append(
            [DraggableLabel(str(camera_points_count), 'red', map_label_big),
             [[0], [0, 0]], [[0], [0, 0]], [[0], [camera_points_count * 20, 0]]])
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
             [[0], [audio_points_count * 20, 0]], [[0], [0, 0]], [[0], [0, 0]]])
    if num == 2:
        audio_points.append(
            [DraggableLabel(str(audio_points_count), 'blue', map_label_big),
             [[0], [0, 0]], [[0], [audio_points_count * 20, 0]], [[0], [0, 0]]])
    if num == 3:
        audio_points.append(
            [DraggableLabel(str(audio_points_count), 'blue', map_label_big),
             [[0], [0, 0]], [[0], [0, 0]], [[0], [audio_points_count * 20, 0]]])
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
             [[0], [ai_points_count * 20, 0]], [[0], [0, 0]], [[0], [0, 0]]])
    if num == 2:
        ai_points.append(
            [DraggableLabel(str(ai_points_count), 'green', map_label_big),
             [[0], [0, 0]], [[0], [ai_points_count * 20, 0]], [[0], [0, 0]]])
    if num == 3:
        ai_points.append(
            [DraggableLabel(str(ai_points_count), 'green', map_label_big),
             [[0], [0, 0]], [[0], [0, 0]], [[0], [ai_points_count * 20, 0]]])
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
    signal = Signal(object)

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
                    sound_volume = float(tb_audio.item(index - 1, 3).text())
                    print(sound_file, sound_times, sound_delay)
                    # 加载音效
                    sound_effect = pygame.mixer.Sound(sound_file)
                    sound_effect.play(loops=sound_times, maxtime=sound_delay * 1000)  # 播放音效
                    sound_effect.set_volume(sound_volume)
                    area_old = copy.deepcopy(action_area)
                    print('Audio~~~~~~~~~~~~~', area_old, audio_points[index][plan_index][0][0], action_area[0])
                    break


def audiosignal_accept(msg):
    try:
        print(msg)
    except:
        print("轴数据显示错误！")


class AiThread(QThread):
    signal = Signal(object)

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
                    sound_volume = float(tb_ai.item(index - 1, 3).text())
                    print(sound_file, sound_times, sound_delay)
                    # 加载音效
                    sound_effect = pygame.mixer.Sound(sound_file)
                    sound_effect.play(loops=sound_times, maxtime=sound_delay * 1000)  # 播放音效
                    sound_effect.set_volume(sound_volume)
                    area_old = copy.deepcopy(action_area)
                    print('Ai~~~~~~~~~~~~~', area_old, ai_points[index][plan_index][0][0], action_area[0])
                    break


def aisignal_accept(msg):
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
                pygame.mixer.music.set_volume(float(getattr(ui, 'lineEdit_volume_%s' % index).text()))
                pygame.mixer.music.play(-1)  # 循环播放背景音乐
                break
    else:
        pygame.mixer.music.stop()


def play_alarm():  # 报警音
    try:
        ui.checkBox_alarm.setChecked(True)
        index = int(ui.lineEdit_alarm.text()) - 1
        sc.GASetExtDoBit(index, 1)
    except:
        print('警报电压输出错误！')
        ui.textBrowser_msg.append(fail('警报电压输出错误！'))
        flg_start['card'] = False


def stop_alarm():
    try:
        index = int(ui.lineEdit_alarm.text()) - 1
        sc.GASetExtDoBit(index, 0)
    except:
        print('警报电压输出错误！')
        ui.textBrowser_msg.append(fail('警报电压输出错误！'))
        flg_start['card'] = False


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
        for index in range(balls_count):
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
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("QLabel 被左键点击")
            if self.Camera_index == 'main_Camera':
                set_result(main_Camera)
            elif self.Camera_index == 'monitor_Camera':
                set_result(monitor_Camera)
        elif event.button() == Qt.RightButton:
            print("QLabel 被右键点击")


class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print(self.text(), event.key())
            if self.text().isdigit() and (int(self.text()) > 10 or int(self.text()) <= 0):
                self.setText('')
            else:
                name = self.objectName()[0:-1]
                for index in range(10):
                    if (getattr(result_ui, '%s%s' % (name, index), None).objectName() != self.objectName() and
                            getattr(result_ui, '%s%s' % (name, index), None).text() == self.text()):
                        getattr(result_ui, '%s%s' % (name, index), None).setText('')
                getattr(result_ui, '%s' % self.objectName(), None).setText(self.text())
                for index in range(10):
                    if (getattr(ui, '%s%s' % (name, index), None).objectName() != self.objectName() and
                            getattr(ui, '%s%s' % (name, index), None).text() == self.text()):
                        getattr(ui, '%s%s' % (name, index), None).setText('')
                getattr(ui, '%s' % self.objectName(), None).setText(self.text())
                i = int(self.objectName()[-1:]) + 1
                print(name, i)
                if i < 10:
                    target_line_edit = getattr(result_ui, '%s%s' % (name, i), None)
                    if target_line_edit:
                        target_line_edit.setFocus()
                        target_line_edit.selectAll()
                    target_line_edit = getattr(ui, '%s%s' % (name, i), None)
                    if target_line_edit:
                        target_line_edit.setFocus()
                        target_line_edit.selectAll()
        elif event.text().isdigit() or event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            super().keyPressEvent(event)
        else:
            print("仅允许输入数字！")


def set_result_class():
    for i in range(10):
        getattr(ui, 'lineEdit_result_%s' % i, None).__class__ = CustomLineEdit
        getattr(result_ui, 'lineEdit_result_%s' % i, None).__class__ = CustomLineEdit


def set_result(msg):
    print(msg)
    balls = msg[:balls_count]
    for index, item in enumerate(balls):
        getattr(ui, 'lineEdit_result_%s' % index, None).setText(str(item))
        getattr(result_ui, 'lineEdit_result_%s' % index, None).setText(str(item))
    res = ''
    for index, item in enumerate(balls):
        if index == 0:
            res = item
        else:
            res = '%s_%s' % (res, item)
    ui.lineEdit_Send_Result.setText(res)


"****************************************摄像头识别结果_结束***********************************************"

"****************************************直播大厅_开始****************************************************"


def lottery_sql_init():
    global lottery_term
    global labels
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
                lottery_data2table(ui.tableWidget_Results, lottery_term, labels)
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def lottery_json_init():
    global lottery_term
    global labels
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    file = "./terms/%s.json" % current_date
    print(file)
    if os.path.exists(file):
        lottery_list = []
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                print(json.loads(line))  # 逐行解析 JSON
                lottery_list.append(json.loads(line))
        for row in range(len(lottery_list)):
            for col in range(len(lottery_list[row])):
                lottery_term[col] = lottery_list[row][col]
            lottery_data2table(ui.tableWidget_Results, lottery_term, labels)


def lottery2json():
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    file = "./terms/%s.json" % current_date
    with open(file, "a", encoding="utf-8") as f:
        f.write(json.dumps(lottery_term) + "\n")

    limit_folder_size("./terms/", max_files=7)  # 删除超过7天的记录


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
        lottery_term[2] = '0'  # 倒数
        lottery_term[3] = '未开始'  # 新一期比赛的状态（2.未开始）
        lottery_term[4] = ''  # 自动赛果
        lottery_term[5] = ''  # 手动赛果
        lottery_term[6] = ''  # 发送赛果
        lottery_term[7] = ''  # 上传图片
        lottery_term[8] = ''  # 备注
        lottery_term[9] = ''  # 图片
        lottery_term[10] = ''  # 录像
        lottery_term[11] = ''  # 结束时间戳
        lottery_term[12] = ''  # 赛果数据包
        lottery_term[13] = ''  # 补发状态
        lottery_term[14] = ''  # 补传状态
        flg_start['server'] = True
        return True
    except:
        print('分机链接错误！')
        flg_start['server'] = False
        return False


"""
    运动卡开启线程
"""


class CardStartThread(QThread):
    signal = Signal(object)

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
                self.signal.emit(succeed('启动板卡：%s' % card_res[res]))
            else:
                self.signal.emit(fail('板卡链接失败：%s' % card_res[res]))
        else:
            self.signal.emit(fail('运动卡已链接~！'))

        if not flg_start['s485']:
            flg_start['s485'] = s485.cam_open()
            if flg_start['s485']:
                Axis_Thread.run_flg = True  # 轴复位
            self.signal.emit(succeed('串口链接：%s' % flg_start['s485']))
        else:
            self.signal.emit(fail('串口链接：%s' % flg_start['s485']))
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


def CardStartsignal_accept(msg):
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser)
    scroll_to_bottom(ui.textBrowser_msg)


"""
    OBS脚本线程
"""


class ScriptThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(ScriptThread, self).__init__()
        self.run_flg = False
        self.running = True
        self.run_type = ''
        self.param = ''

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            time.sleep(0.1)
            if not self.run_flg:
                continue
            try:
                if self.run_type == 'start':
                    requests.get(url="%s/start" % obs_script_addr)  # 开始OBS的python脚本计时
                if self.run_type == 'reset':
                    requests.get(url="%s/reset" % obs_script_addr)
                elif self.run_type == 'period':
                    requests.get(url='%s/period?period=%s' % (obs_script_addr, self.param))
                elif self.run_type == 'term':
                    requests.get(url="%s/term?term=%s" % (obs_script_addr, term))  # 开始OBS的python脚本期号显示
            except:
                print('OBS脚本链接错误！')
                flg_start['obs'] = False

            self.run_flg = False


def script_signal_accept(msg):
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser)
    scroll_to_bottom(ui.textBrowser_msg)


class OrganCycleThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(OrganCycleThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        while self.running:
            time.sleep(1)
            organ_list = ui.lineEdit_Cycle.text().split(',')
            cycle_list = ui.lineEdit_Cycle_Time.text().split(',')
            if len(organ_list) < 1 or len(organ_list) != len(cycle_list):
                self.signal.emit(fail('循环机关设置错误！'))
                continue
            cycle_time = 0
            while self.run_flg and ui.checkBox_Cycle.isChecked():
                time.sleep(1)
                try:
                    for i in range(len(organ_list)):
                        if (organ_list[i].isdigit()
                                and cycle_list[i].isdigit()
                                and cycle_time % int(cycle_list[i]) == 0):
                            index = int(organ_list[i]) - 1
                            on_off = int(cycle_time / int(cycle_list[i])) % 2
                            sc.GASetExtDoBit(index, on_off)
                except:
                    print('循环机关错误！')
                    ui.textBrowser_msg.append(fail('循环机关错误！'))
                    flg_start['card'] = False
                cycle_time += 1
            self.run_flg = False


def OrganCycle_signal_accept(msg):
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser)
    scroll_to_bottom(ui.textBrowser_msg)


class Kaj789Thread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(Kaj789Thread, self).__init__()
        self.run_flg = False
        self.running = True
        self.run_type = ''

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global term_comment
        global lottery_term
        global betting_loop_flg
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            for i in range(5):
                if self.run_type == 'post_start':
                    res_status = post_status(True, Track_number)
                    if 'OK' in res_status:
                        self.signal.emit({'post_start': res_status})
                        break
                    else:
                        continue
                if self.run_type == 'post_stop':
                    betting_loop_flg = False  # 关闭循环标志
                    ReStart_Thread.run_flg = False  # 停止重启循环
                    res_status = post_status(False, Track_number)
                    if 'OK' in res_status:
                        self.signal.emit({'post_stop': res_status})
                        break
                    else:
                        continue
                if self.run_type == 'post_end':
                    res_end = post_end(term=term, betting_end_time=betting_end_time,
                                       status=term_status,
                                       Track_number=Track_number)  # 发送游戏结束信号给服务器
                    if res_end == 'OK':
                        if term_status == 2:
                            lottery_term[3] = '已取消'
                            self.signal.emit({'post_end': res_end})
                        elif lottery_term[12] != '':
                            self.run_type = 'post_result'
                            lottery_term[3] = '已结束'
                            self.signal.emit({'post_end': res_end})
                        else:
                            break
                    else:
                        continue
                if self.run_type == 'post_result':
                    res_result = post_result(term=term, betting_end_time=betting_end_time,
                                             result_data=lottery_term[12],
                                             Track_number=Track_number)  # 发送最终排名给服务器
                    if res_result == 'OK':
                        lottery_term[6] = "发送成功"
                        self.run_type = 'post_upload'
                        self.signal.emit({'post_result': res_result})
                    else:
                        continue
                if self.run_type == 'post_upload' and os.path.exists(lottery_term[9]):
                    res_upload = post_upload(term=term, img_path=lottery_term[9],
                                             Track_number=Track_number)  # 上传结果图片
                    if res_upload != 'OK':
                        continue
                    else:
                        lottery_term[7] = "上传成功"
                        self.signal.emit({'post_upload': res_upload})
                        if term_comment == '':
                            lottery2json()  # 保存数据
                            break
                if term_comment != '':
                    res_marble_results = post_marble_results(term=term,
                                                             comments=term_comment,
                                                             Track_number=Track_number)  # 上传备注信息
                    lottery_term[8] = term_comment
                    self.signal.emit({'post_marble_results': res_marble_results})
                    if str(term) in res_marble_results:
                        lottery2json()  # 保存数据
                    term_comment = ''
                    break

            self.run_flg = False


def kaj789_signal_accept(msg):
    message = msg
    if isinstance(msg, dict):
        if 'post_start' in msg.keys():
            if msg['post_start'] == 'OK':
                ui.textBrowser_msg.append(succeed('开盘成功！'))
            else:
                ui.textBrowser_msg.append(succeed('开盘失败！服务器链接错误！'))
            ui.groupBox_term.setStyleSheet('')
        if 'post_stop' in msg.keys():
            if msg['post_stop'] == 'OK':
                ui.textBrowser_msg.append(succeed('封盘成功！'))
            else:
                ui.textBrowser_msg.append(succeed('封盘失败！服务器链接错误！'))
            ui.groupBox_term.setStyleSheet('')
        if 'post_end' in msg.keys():
            if msg['post_end'] == 'OK':
                message = succeed('发送结束标志成功！')
                tb_result = ui.tableWidget_Results
                if tb_result.rowCount() > 0:
                    item = QTableWidgetItem(lottery_term[3])
                    item.setTextAlignment(Qt.AlignCenter)
                    if term_status == 1:
                        item.setForeground(QColor("green"))  # 设置字体颜色为红色
                    else:
                        item.setForeground(QColor("red"))  # 设置字体颜色为红色
                    tb_result.setItem(0, 3, item)
            else:
                message = fail('发送结束标志失败:%s' % msg['post_end'])
        if 'post_result' in msg.keys():
            if msg['post_result'] == 'OK':
                message = succeed(lottery_term[6])
                tb_result = ui.tableWidget_Results
                if tb_result.rowCount() > 0:
                    item = QTableWidgetItem(lottery_term[6])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("green"))  # 设置字体颜色为红色
                    tb_result.setItem(0, 6, item)
            else:
                message = fail('发送结果失败:%s' % msg['post_result'])
        if 'post_upload' in msg.keys():
            if msg['post_upload'] == 'OK':
                message = succeed(lottery_term[7])
                tb_result = ui.tableWidget_Results
                if tb_result.rowCount() > 0:
                    item = QTableWidgetItem(lottery_term[7])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("green"))  # 设置字体颜色为红色
                    tb_result.setItem(0, 7, item)
            else:
                message = fail('发送图片失败:%s' % msg['post_upload'])
        if 'post_marble_results' in msg.keys():
            if str(term) in msg['post_marble_results']:
                message = succeed('发送备注成功！')
                tb_result = ui.tableWidget_Results
                row_count = tb_result.rowCount()
                if row_count > 0:
                    item = QTableWidgetItem(lottery_term[8])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("green"))  # 设置字体颜色为红色
                    tb_result.setItem(0, 8, item)
            else:
                message = fail('发送备注失败:%s' % msg['post_marble_results'])
    else:
        ui.textBrowser.append(message)
        ui.textBrowser_msg.append(message)
        scroll_to_bottom(ui.textBrowser)
        scroll_to_bottom(ui.textBrowser_msg)


def send_end():
    global term_status
    if ReStart_Thread.start_flg:
        messagebox.showinfo("敬告", "比赛未结束，进行补发！")
        return
    Kaj789_Thread.run_type = 'post_end'
    Kaj789_Thread.run_flg = True


def cancel_end():
    global term_status
    global term_comment
    global betting_loop_flg
    if ReStart_Thread.start_flg:
        messagebox.showinfo("取消当局", "当前开盘中，不能直接取消比赛，如需强制取消，请点击封盘！")
        return
    response = messagebox.askquestion("取消当局", "取消当局，你确定吗？")
    print(response)  # "yes" / "no"
    if "yes" in response:
        term_status = 2
        term_comment = term_comments[0]
        Kaj789_Thread.run_type = 'post_end'
        Kaj789_Thread.run_flg = True
        betting_loop_flg = False
        ui.radioButton_stop_betting.click()
    # res = post_marble_results(term, 'Invalid Term', Track_number)
    # if 'Invalid Term' in res:
    #     lottery_term[5] = '取消比赛'


class ResetRankingThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(ResetRankingThread, self).__init__()
        self.run_flg = False
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global ranking_array
        global ball_sort
        global con_data
        global action_area
        global z_ranking_res
        global z_ranking_end
        global z_ranking_time
        global balls_start
        global term_comment
        global init_array
        # global previous_position
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            init_array = init_array[:balls_count]
            ranking_array = []  # 排名数组
            for row in range(balls_count):
                ranking_array.append([])
                for col in range(0, len(init_array[row])):
                    ranking_array[row].append(init_array[row][col])
            ball_sort = []  # 位置寄存器
            for row in range(0, max_area_count + 1):
                ball_sort.append([])
                for col in range(0, max_lap_count):
                    ball_sort[row].append([])
            balls_start = 0  # 起点球数
            if con_data:
                for row in range(0, len(init_array)):
                    for col in range(0, 5):
                        if col == 0:
                            con_data[row][col] = init_array[row][5]  # con_data 数据表数组
                        else:
                            con_data[row][col] = 0
            action_area = [0, 0, 0]  # 初始化触发区域
            z_ranking_res = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 初始化网页排名
            z_ranking_res = z_ranking_res[:balls_count]
            z_ranking_end = z_ranking_res[:balls_count]
            z_ranking_time = [''] * balls_count  # 初始化网页排名时间
            tcp_ranking_thread.sleep_time = 0.1  # 重置排名数据包发送时间
            tcp_ranking_thread.run_flg = True  # 打开排名线程
            print('tcp_ranking_thread.run_flg = True~~~~~~~~~~~~')
            map_label_big.map_action = 0
            term_comment = ''
            alarm_worker.toggle_enablesignal.emit(False)
            if not ui.checkBox_test.isChecked():
                activate_browser()  # 刷新OBS中排名浏览器
                try:
                    while Script_Thread.run_flg:
                        time.sleep(1)
                    Script_Thread.run_type = 'reset'
                    Script_Thread.run_flg = True
                except:
                    print('OBS脚本链接错误！')
                    flg_start['obs'] = False
            self.signal.emit(succeed('初始化完成！'))
            self.run_flg = False


def reset_ranking_signal_accept(msg):
    # Map_ui.hide()
    ui.textBrowser.append(msg)
    ui.textBrowser_msg.append(msg)
    scroll_to_bottom(ui.textBrowser)
    scroll_to_bottom(ui.textBrowser_msg)


class CheckFileThread(QThread):
    signal = Signal(object)

    def __init__(self):
        super(CheckFileThread, self).__init__()
        self.run_flg = True
        self.running = True

    def stop(self):
        self.run_flg = False
        self.running = False  # 修改标志位，线程优雅退出
        self.quit()  # 退出线程事件循环

    def run(self) -> None:
        global flg_start
        while self.running:
            time.sleep(3)
            if not self.run_flg:
                continue
            path1 = ui.lineEdit_saidao_Path.text()
            path2 = ui.lineEdit_upload_Path.text()
            path3 = ui.lineEdit_end1_Path.text()
            path4 = ui.lineEdit_end2_Path.text()
            folder_name = os.path.basename(path1)
            folder_path = os.path.join(os.path.dirname(path2), folder_name).replace("\\", "/")
            gps_num = 5000
            end_num = 5000
            if os.path.exists(folder_path):
                files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                         os.path.isfile(os.path.join(folder_path, f))]
                if ui.lineEdit_GPS_Num.text().isdigit():
                    gps_num = int(ui.lineEdit_GPS_Num.text())
                if ui.lineEdit_End_Num.text().isdigit():
                    end_num = int(ui.lineEdit_End_Num.text())
                if len(files) >= gps_num:
                    self.signal.emit('停止录图')
                limit_folder_size(folder_path, max_files=gps_num)  # 限制GPS文件夹数量
            if os.path.exists(path2):
                limit_folder_size(path2, max_files=gps_num)  # 限制上报文件夹数量
            if os.path.exists(path3):
                limit_folder_size(path3, max_files=end_num)  # 限制终点1文件夹数量
            if os.path.exists(path4):
                limit_folder_size(path4, max_files=end_num)  # 限制终点2文件夹数量
            video_part = os.path.join(os.path.dirname(path2), '录像').replace("\\", "/")
            if os.path.exists(video_part):
                limit_folder_size(video_part, max_files=800)  # 限制文件夹数量
            if os.path.exists('D:/ApowerREC'):
                limit_folder_size('D:/ApowerREC', max_files=30)  # 限制文件夹数量

            if ui.lineEdit_login.text() == 'zzw':
                if not ui.frame_zzw_1.isEnabled():
                    ui.frame_zzw_1.setEnabled(True)
                    ui.frame_zzw_2.setEnabled(True)
                    ui.groupBox_ranking.setEnabled(True)
                    ui.checkBox_shoot_0.setEnabled(True)
                    ui.checkBox_Pass_Recognition_Start.setEnabled(True)
                    ui.checkBox_Pass_Ranking_Twice.setEnabled(True)
                    ui.lineEdit_balls_auto.setEnabled(True)
            else:
                if ui.frame_zzw_1.isEnabled():
                    ui.frame_zzw_1.setEnabled(False)
                    ui.frame_zzw_2.setEnabled(False)
                    ui.groupBox_ranking.setEnabled(False)
                    ui.checkBox_shoot_0.setEnabled(False)
                    ui.checkBox_Pass_Recognition_Start.setEnabled(False)
                    ui.checkBox_Pass_Ranking_Twice.setEnabled(False)
                    ui.lineEdit_balls_auto.setEnabled(False)


def CheckFile_signal_accept(msg):
    if '停止录图' in msg:
        ui.checkBox_saveImgs.setChecked(False)


class TestStatusThread(QThread):
    signal = Signal(object)

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
        while self.running:
            time.sleep(1)
            if not self.run_flg:
                continue
            cardnum = ui.lineEdit_CardNo.text()
            if cardnum.isdigit() and not (flg_start['card']):
                res = sc.card_open(int(cardnum))
                print(res)
                if res == 0:
                    flg_start['card'] = True
                    if flg_start['card']:  # 轴复位一次
                        Axis_Thread.run_flg = True
                        res_sql = query_sql()  # 加载网络设置 一次
                        self.signal.emit(res_sql)

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
                try:
                    res = s485.cam_zoom_step()
                    if not res:
                        flg_start['s485'] = False
                        print("485 驱动出错！~~~~~")
                        continue
                except:
                    print("485 运行出错！!!!!!")
                    flg_start['s485'] = False

            if not flg_start['obs']:
                if not Obs_Thread.isRunning():
                    Obs_Thread.start()
            else:
                try:
                    res = cl_request.get_stream_status()
                    if res.output_active:
                        flg_start['live'] = True
                    else:
                        flg_start['live'] = False
                except:
                    flg_start['obs'] = False
                    print('OBS脚本开始错误！')

            if not flg_start['ai']:  # 识别服务器
                try:
                    for index in range(len(wakeup_addr)):
                        res = requests.get(wakeup_addr[index])
                        if res.text == 'ok':
                            flg_start['ai'] = True
                except:
                    flg_start['ai'] = False

            self.signal.emit('标志')


def test_statussignal_accept(msg):
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


def maintain_screen():  # OBS维护
    if ui.checkBox_maintain.isChecked() and flg_start['obs']:
        try:
            cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_picture'],
                                              True)  # 打开维护来源
            cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_settlement'],
                                              False)  # 关闭结算页来源
        except:
            print('obs 维护 错误！')
            ui.textBrowser_msg.append(fail('obs 维护 错误！'))
            flg_start['obs'] = False
    else:
        try:
            cl_request.set_scene_item_enabled(obs_data['obs_scene'], obs_data['source_picture'],
                                              False)  # 关闭维护来源
        except:
            print('obs %s 错误！' % obs_data['obs_scene'])
            ui.textBrowser_msg.append(fail('obs %s 错误！' % obs_data['obs_scene']))
            flg_start['obs'] = False


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
        if (ui.checkBox_shoot.isChecked()
                or ui.checkBox_shoot1.isChecked()
                or ui.checkBox_shoot_1.isChecked()):
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_shoot2():  # 弹射开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_shoot_2.text()) - 1
        if ui.checkBox_shoot2.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_shoot3():  # 弹射开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_shoot_3.text()) - 1
        if ui.checkBox_shoot3.isChecked():
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
        if ui.checkBox_start.isChecked() or ui.checkBox_start_2.isChecked():
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
        if ui.checkBox_end.isChecked() or ui.checkBox_end_2.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_shake():  # 震动开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_shake.text()) - 1
        if ui.checkBox_shake.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_start_count():  # 震动开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_start_count.text()) - 1
        if ui.checkBox_start_count.isChecked():
            sc.GASetExtDoBit(index, 1)
        else:
            sc.GASetExtDoBit(index, 0)
    except:
        print('运动卡电压输出错误！')
        ui.textBrowser_msg.append(fail('运动卡电压输出错误！'))
        flg_start['card'] = False


def organ_alarm():  # 震动开关
    if not flg_start['card']:
        return
    try:
        index = int(ui.lineEdit_alarm.text()) - 1
        if ui.checkBox_alarm_2.isChecked():
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
        res = ''
        for index, item in enumerate(eval(ui.lineEdit_Main_Camera.text())):
            if index == 0:
                res = item
            else:
                res = '%s_%s' % (res, item)
        ui.lineEdit_Send_Result.setText(res)


def backup2result():
    if ui.lineEdit_Backup_Camera.text() != '':
        res = ''
        for index, item in enumerate(eval(ui.lineEdit_Backup_Camera.text())):
            if index == 0:
                res = item
            else:
                res = '%s_%s' % (res, item)
        ui.lineEdit_Send_Result.setText(res)


def res2end():
    global Send_Result_End
    s = ui.lineEdit_Send_Result.text().split('_')
    if len(s) == balls_count:
        for index, item in enumerate(s):
            getattr(ui, 'lineEdit_result_%s' % index).setText(item)
        Send_Result_End = True
        ui.checkBox_alarm.setChecked(False)


def result2end():
    global Send_Result_End
    for index in range(balls_count):
        item = getattr(result_ui, 'lineEdit_result_%s' % index).text()
        getattr(ui, 'lineEdit_result_%s' % index).setText(item)
    Send_Result_End = True
    ui.checkBox_alarm.setChecked(False)


def send_result():
    global Send_Result_End
    Send_Result_End = True
    ui.checkBox_alarm.setChecked(False)


def start_betting():
    if not Kaj789_Thread.run_flg:
        Kaj789_Thread.run_type = 'post_start'
        Kaj789_Thread.run_flg = True


def stop_betting():
    global betting_loop_flg
    global term_status
    global term_comment
    if ReStart_Thread.start_flg:
        response = messagebox.askquestion("取消当局", "比赛进行中，是否取消当局？")
        print(response)  # "yes" / "no"
        if "yes" in response:
            term_status = 2
            term_comment = term_comments[0]
            ReStart_Thread.start_flg = False
            while Kaj789_Thread.run_flg:
                time.sleep(1)
            Kaj789_Thread.run_type = 'post_end'
            Kaj789_Thread.run_flg = True
            betting_loop_flg = False
        else:
            ui.radioButton_start_betting.setChecked(True)
            return
    while Kaj789_Thread.run_flg:
        time.sleep(1)
    betting_loop_flg = False
    Kaj789_Thread.run_type = 'post_stop'
    Kaj789_Thread.run_flg = True


def test_betting():
    if ReStart_Thread.start_flg:
        messagebox.showinfo("敬告", "当前开盘中，不能更改比赛状态！")
        ui.radioButton_start_betting.setChecked(True)
        return
    ui.textBrowser_msg.append(succeed('模拟开盘！'))
    ui.groupBox_term.setStyleSheet('')


def auto_shoot():  # 自动上珠
    global balls_start
    global ball_sort
    global ranking_array
    if ui.checkBox_shoot_0.isChecked():
        ranking_array = []  # 排名数组
        for row in range(0, len(init_array)):
            ranking_array.append([])
            for col in range(0, len(init_array[row])):
                ranking_array[row].append(init_array[row][col])
        ball_sort = []  # 位置寄存器
        for row in range(0, max_area_count + 1):
            ball_sort.append([])
            for col in range(0, max_lap_count):
                ball_sort[row].append([])
        balls_start = 0
        Shoot_Thread.run_flg = True
    else:
        Shoot_Thread.run_flg = False


def ready_btn():
    while PlanCmd_Thread.run_flg:
        print('等待动作结束~~~~~~~~')
        time.sleep(1)
    PlanCmd_Thread.ready_state = True  # 运行准备
    PlanCmd_Thread.run_flg = True


def kaj789_table():
    if ui.radioButton_start_betting.isChecked():
        QMessageBox.information(z_window, "开盘中", "正在开盘中，请在封盘后再处理赛事数据！")
    else:
        Kaj789_ui.show()


"****************************************直播大厅_结束****************************************************"
"****************************************参数设置_开始****************************************************"


def query_sql():
    global local_ip
    # 创建数据库连接
    try:
        conn = create_connection("192.168.0.80", "root", "root", "dataini")

        if conn:
            local_ip = tool_unit.check_network_with_ip()
            print(local_ip)
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


def flip_horizontal():  # 主镜头水平翻转
    if ui.checkBox_Flip_Horizontal.isChecked():
        s485.cam_flip_horizontal(0)
    else:
        s485.cam_flip_horizontal(1)


def flip_vertica():  # 主镜头垂直翻转
    if ui.checkBox_Flip_Vertica.isChecked():
        s485.cam_flip_vertica(0)
    else:
        s485.cam_flip_vertica(1)


"****************************************参数设置_结束****************************************************"


def red_line():
    if flg_start['card']:
        res, value = sc.GAGetDiReverseCount()
        print(res, value)


def my_test():
    global term
    global z_ranking_res
    cl_request.stop_stream()
    # cl_request.press_input_properties_button("结算页", "refreshnocache")
    # OrganCycle_Thread.run_flg = not OrganCycle_Thread.run_flg
    # play_alarm()
    # PlanCmd_Thread.background_state = True
    # PlanCmd_Thread.run_flg = True
    # for i in range(98):
    #     ui.textBrowser_msg.append('这是第%s行' % i)
    # ScreenShot_Thread.run_flg = True
    # z_ranking_res = [1,4,5,3,2,6,7,8,9,10]
    # tcp_ranking_thread.run_flg = True
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

    # resp = cl_requst.get_source_screenshot('终点2', "jpg", 1920, 1080, 100)
    # resp = cl_requst.save_source_screenshot('终点1', "jpg", 'd:/img/%s.jpg' % (time.time()), 1920, 1080, 100)
    # resp = cl_requst.save_source_screenshot('终点2', "jpg", 'd:/img/%s.jpg' % (time.time()), 1920, 1080, 100)


def clean_browser(textBrowser):
    # 获取所有行
    lines = textBrowser.toPlainText().split("\n")
    if len(lines) > 100:
        # 只保留最后 max_lines 行
        textBrowser.clear()
        textBrowser.setPlainText("\n".join(lines[-50:]))


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
            stop_server()
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
            listener.stop()
            ScreenShot_Thread.stop()
            ObsEnd_Thread.stop()
            Shoot_Thread.stop()
            positions_live_thread.stop()
            Script_Thread.stop()
            Kaj789_Thread.stop()
            reset_ranking_Thread.stop()
            OrganCycle_Thread.stop()
            deal_udp_thread.stop()
            CheckFile_Thread.stop()
            pygame.quit()
        except Exception as e:
            print(f"Error stopping threads: {e}")

    def join_all_threads(self):
        """等待所有线程退出。"""
        try:
            PlanCmd_Thread.wait()  # 运动方案线程
            PlanObs_Thread.wait()  # OBS切换线程
            PlanCam_Thread.wait()  # 镜头切换线程
            PlanBallNum_Thread.wait()  # 计球器线程
            tcp_ranking_thread.wait()  # 前端排名线程
            tcp_result_thread.wait()  # 前端结果线程
            udp_thread.wait()  # 处理udp数据线程
            Update_Thread.wait()  # 更新排名数据表线程
            TestStatus_Thread.wait()  # 测试各功能状态线程
            Axis_Thread.wait()  # 五轴复位线程
            Pos_Thread.wait()  # 龙门架坐标线程
            ReStart_Thread.wait()  # 重启方案线程
            Audio_Thread.wait()  # 音效方案线程
            Ai_Thread.wait()  # AI方案线程
            listener.join()  # 键盘监听线程
            ScreenShot_Thread.wait()  # 摄像头排名识别线程
            ObsEnd_Thread.wait()  # 推送结果到前端线程
            Shoot_Thread.wait()  # 弹射上珠线程
            positions_live_thread.wait()  # 发送实时位置到服务器线程
            Script_Thread.wait()  # OBS计时脚本线程
            Kaj789_Thread.wait()  # 开奖王线程（补发结果数据）
            reset_ranking_Thread.wait()  # 初始化数据线程
            CheckFile_Thread.wait()  # 检查文件线程
            OrganCycle_Thread.wait()  # 机关循环
            deal_udp_thread.wait()  # 机关循环
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
    tb_step = ui.tableWidget_Step
    row_index = tb_step.currentRow()

    tb_speed = speed_ui.tableWidget_Set_Speed
    row = tb_speed.currentRow()
    col = tb_speed.currentColumn()
    if tb_speed.item(row, col):
        if (not is_natural_num(tb_speed.item(row, col).text())
                or '-' in tb_speed.item(row, col).text()):
            tb_speed.item(row, col).setText(plan_list[row_index][7][row][col])

    x_0 = 0
    y_0 = 0
    if row_index > 0:
        x_0 = int(tb_step.item(row_index - 1, 2).text())
        y_0 = int(tb_step.item(row_index - 1, 3).text())
    x_distance = abs(int(tb_step.item(row_index, 2).text()) - x_0)
    y_distance = abs(int(tb_step.item(row_index, 3).text()) - y_0)
    x_speed = int(tb_speed.item(0, 0).text())
    y_speed = int(tb_speed.item(1, 0).text())
    # 计算直线速度
    if speed_ui.checkBox_auto_line.isChecked() and x_distance != 0:
        y_speed = int(x_speed * (y_distance / x_distance))
        tb_speed.item(1, 0).setText(str(y_speed))
    # 计算动作运行时间
    time_x = int(x_distance / x_speed) / 1000 + float(tb_speed.item(0, 3).text())
    time_y = int(y_distance / y_speed) / 1000 + float(tb_speed.item(1, 3).text())
    if time_x > time_y:
        speed_ui.lineEdit_time.setText('%.3f' % time_x)
    else:
        speed_ui.lineEdit_time.setText('%.3f' % time_y)


def auto_time():  # 相对上一个动作按时间设置速度
    if (not is_natural_num(speed_ui.lineEdit_time_set.text())
            or '-' in speed_ui.lineEdit_time_set.text()):
        speed_ui.lineEdit_time_set.setText('0')
    now_time = abs(float(speed_ui.lineEdit_time.text()))
    set_time = abs(float(speed_ui.lineEdit_time_set.text()))
    if now_time > 0 and set_time > 0:
        tb_speed = speed_ui.tableWidget_Set_Speed
        x_speed = float(tb_speed.item(0, 0).text())
        y_speed = float(tb_speed.item(1, 0).text())
        z_speed = float(tb_speed.item(2, 0).text())
        rx_speed = float(tb_speed.item(3, 0).text())
        ry_speed = float(tb_speed.item(4, 0).text())
        x_delay = float(tb_speed.item(0, 3).text())
        y_delay = float(tb_speed.item(1, 3).text())
        z_delay = float(tb_speed.item(2, 3).text())
        rx_delay = float(tb_speed.item(3, 3).text())
        ry_delay = float(tb_speed.item(4, 3).text())
        ratio = set_time / now_time
        tb_speed.item(0, 0).setText(str(int(x_speed / ratio)))
        tb_speed.item(1, 0).setText(str(int(y_speed / ratio)))
        tb_speed.item(2, 0).setText(str(int(z_speed / ratio)))
        tb_speed.item(3, 0).setText(str(int(rx_speed / ratio)))
        tb_speed.item(4, 0).setText(str(int(ry_speed / ratio)))
        tb_speed.item(0, 3).setText('%.3f' % float(x_delay * ratio))
        tb_speed.item(1, 3).setText('%.3f' % float(y_delay * ratio))
        tb_speed.item(2, 3).setText('%.3f' % float(z_delay * ratio))
        tb_speed.item(3, 3).setText('%.3f' % float(rx_delay * ratio))
        tb_speed.item(4, 3).setText('%.3f' % float(ry_delay * ratio))


"************************************Camera_UI*********************************************"


class CameraUi(QDialog, Ui_Camera_Dialog):
    def __init__(self):
        super().__init__()

    def setupUi(self, z_dialog):
        super(CameraUi, self).setupUi(z_dialog)


def main_hide_event(event):
    ui.checkBox_main_camera.setChecked(False)
    event.accept()


def main_doubleclick_event(event):
    if event.button() == Qt.LeftButton:
        set_result(main_Camera)


def monitor_doubleclick_event(event):
    if event.button() == Qt.LeftButton:
        set_result(monitor_Camera)


def monitor_hide_event(event):
    ui.checkBox_monitor_cam.setChecked(False)
    event.accept()


def map_hide_event(event):
    ui.checkBox_map.setChecked(False)
    event.accept()


def main_cam_change():
    if ui.checkBox_main_camera.isChecked():
        MainCameraDialog.show()
    else:
        MainCameraDialog.hide()


def monitor_cam_change():
    if ui.checkBox_monitor_cam.isChecked():
        MonitorCameraDialog.show()
    else:
        MonitorCameraDialog.hide()


def map_change():
    if ui.checkBox_map.isChecked():
        Map_ui.show()
    else:
        Map_ui.hide()


"************************************ResultDlg_Ui*********************************************"


class OrganUi(QDialog, Ui_Dialog_Organ):
    def __init__(self):
        super().__init__()

    def setupUi(self, z_dialog):
        super(OrganUi, self).setupUi(z_dialog)

        for i in range(16):
            getattr(self, 'checkBox_organ_%s' % (i + 1)).__class__ = OrganCheckBox


class OrganCheckBox(QCheckBox):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        organ_num = self.objectName().split('_')[2]
        if not flg_start['card']:
            return
        try:
            index = int(organ_num) - 1
            if not self.isChecked():
                sc.GASetExtDoBit(index, 1)
            else:
                sc.GASetExtDoBit(index, 0)
        except:
            print('机关%s输出错误！' % organ_num)
            ui.textBrowser_msg.append(fail('机关%s输出错误！' % organ_num))
            flg_start['card'] = False

        super().mousePressEvent(event)  # 让父类继续处理事件（否则复选框不会切换状态）


def organ_show():
    file = "./organ_config.json"
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)  # 读取 JSON 并转换为 Python 字典
        for i in range(len(data)):
            # organ_ui.lineEdit_organ_1.setText(data[i])
            getattr(organ_ui, 'lineEdit_organ_%s' % (i + 1)).setText(data[i])
    OrganDialog.show()


def organ_ok():
    file = "./organ_config.json"
    data = []
    with open(file, "w", encoding="utf-8") as f:
        for i in range(16):
            data.append(getattr(organ_ui, 'lineEdit_organ_%s' % (i + 1)).text())
        json.dump(data, f, ensure_ascii=False, indent=4)  # `ensure_ascii=False` 支持中文
    # OrganDialog.hide()


class ResultUi(QDialog, Ui_Dialog_Result):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setupUi(self, z_dialog):
        super(ResultUi, self).setupUi(z_dialog)


class BallsNumUi(QDialog, Ui_Dialog_BallsNum):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.go_flg = False

    def setupUi(self, z_dialog):
        super(BallsNumUi, self).setupUi(z_dialog)


def balls_close_btn():
    ReStart_Thread.run_flg = False
    Shoot_Thread.run_flg = False
    ui.radioButton_stop_betting.click()
    BallsNum_ui.hide()


def balls_continue_btn():
    BallsNum_ui.go_flg = True
    BallsNum_ui.hide()


class MapUi(QDialog, Ui_Dialog_Map):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setupUi(self, z_dialog):
        super().setupUi(z_dialog)


class TrapBallUi(QDialog, Ui_Dialog_TrapBall):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.trap_flg = False  # 卡珠记录时间标记

    def setupUi(self, z_dialog):
        super(TrapBallUi, self).setupUi(z_dialog)


class TrapPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName(text)

    def mousePressEvent(self, event):
        global z_ranking_time
        global term_comment
        items = self.objectName().split('_')
        print(items)
        if items[2].isdigit():
            num = int(items[2])
            if z_ranking_time[num - 1] in ['TRAP', 'OUT', '']:
                z_ranking_time[num - 1] = items[1]
                term_comment = items[1]

        super().mousePressEvent(event)  # 确保按钮仍然触发默认的点击事件


def set_trap_btn():
    for index in range(10):
        if index < balls_count:
            getattr(TrapBall_ui, 'pushButton_TRAP_%s' % (index + 1), None).__class__ = TrapPushButton
            getattr(TrapBall_ui, 'pushButton_OUT_%s' % (index + 1), None).__class__ = TrapPushButton
            getattr(ui, 'pushButton_TRAP_%s' % (index + 1), None).__class__ = TrapPushButton
            getattr(ui, 'pushButton_OUT_%s' % (index + 1), None).__class__ = TrapPushButton
        else:
            getattr(TrapBall_ui, 'pushButton_TRAP_%s' % (index + 1), None).hide()
            getattr(TrapBall_ui, 'pushButton_OUT_%s' % (index + 1), None).hide()
            getattr(ui, 'pushButton_TRAP_%s' % (index + 1), None).hide()
            getattr(ui, 'pushButton_OUT_%s' % (index + 1), None).hide()


def trap_ok():
    PlanBallNum_Thread.run_flg = False
    TrapBall_ui.trap_flg = True
    TrapBall_ui.hide()


def trap_cancel():
    PlanBallNum_Thread.run_flg = False
    TrapBall_ui.hide()


"************************************ResultDlg_Ui*********************************************"

if __name__ == '__main__':
    app = ZApp(sys.argv)

    z_window = ZMainwindow()
    ui = ZUi()
    ui.setupUi(z_window)
    z_window.show()

    Map_ui = MapUi(z_window)
    Map_ui.setupUi(Map_ui)
    Map_ui.hideEvent = map_hide_event

    TrapBall_ui = TrapBallUi(z_window)
    TrapBall_ui.setupUi(TrapBall_ui)
    TrapBall_ui.pushButton_ok.clicked.connect(trap_ok)
    TrapBall_ui.pushButton_cancel.clicked.connect(trap_cancel)

    result_ui = ResultUi(parent=z_window)
    result_ui.setupUi(result_ui)
    result_ui.pushButton_Send_Res.clicked.connect(result2end)
    result_ui.checkBox_stop.checkStateChanged.connect(stop_alarm)

    BallsNum_ui = BallsNumUi(z_window)
    BallsNum_ui.setupUi(BallsNum_ui)
    BallsNum_ui.pushButton_close.clicked.connect(balls_close_btn)
    BallsNum_ui.pushButton_continue.clicked.connect(balls_continue_btn)

    OrganDialog = QDialog(z_window)
    organ_ui = OrganUi()
    organ_ui.setupUi(OrganDialog)
    organ_ui.pushButton_ok.clicked.connect(organ_ok)

    SpeedDialog = QDialog(z_window)
    speed_ui = SpeedUi()
    speed_ui.setupUi(SpeedDialog)

    speed_ui.buttonBox.accepted.connect(accept_speed)
    speed_ui.buttonBox.rejected.connect(reject_speed)
    speed_ui.checkBox_auto_line.checkStateChanged.connect(auto_line)
    speed_ui.tableWidget_Set_Speed.itemChanged.connect(auto_line)
    speed_ui.lineEdit_time_set.editingFinished.connect(auto_time)

    MainCameraDialog = QDialog(z_window)
    MainCameraDialog.hideEvent = main_hide_event
    main_camera_ui = CameraUi()
    main_camera_ui.setupUi(MainCameraDialog)
    main_camera_ui.groupBox_main_camera.setTitle('主摄像头')
    main_camera_ui.label_picture.mouseDoubleClickEvent = main_doubleclick_event
    ui.label_main_picture.mouseDoubleClickEvent = main_doubleclick_event
    main_camera_ui.pushButton_net.hide()

    MonitorCameraDialog = QDialog(z_window)
    MonitorCameraDialog.hideEvent = monitor_hide_event
    monitor_camera_ui = CameraUi()
    monitor_camera_ui.setupUi(MonitorCameraDialog)
    monitor_camera_ui.groupBox_main_camera.setTitle('网络摄像头')
    monitor_camera_ui.label_picture.mouseDoubleClickEvent = monitor_doubleclick_event
    ui.label_monitor_picture.mouseDoubleClickEvent = monitor_doubleclick_event
    monitor_camera_ui.pushButton_net.clicked.connect(net_camera)

    sc = SportCard()  # 运动卡
    s485 = Serial485()  # 摄像头

    plan_list = []  # 当前方案列表 [0.选中,1.圈数,2.左右,3.前后,4.上下,5.头旋转,6.头上下,7.速度,8.加速,9.减速,10.镜头缩放,11.缩放时长,12.机关,13.运动位置,14.卫星图位置,col_count - 2.OBS画面]
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料
    pValue = [0, 0, 0, 0, 0]  # 各轴位置
    flg_key_run = True  # 键盘控制标志
    axis_reset = False  # 轴复位标志
    flg_start = {'card': False, 's485': False, 'obs': False, 'live': False,
                 'ai': False, 'ai_end': False, 'server': False}  # 各硬件启动标志

    load_plan_json()

    tb_step_worker = UiWorker(ui.tableWidget_Step)
    # main_music_worker = UiWorker(ui.checkBox_main_music)
    alarm_worker = UiWorker(ui.checkBox_alarm)

    listener = pynput.keyboard.Listener(on_press=keyboard_press, on_release=keyboard_release)
    listener.start()  # 键盘监听线程 1

    PlanCmd_Thread = PlanCmdThread()  # 总运行方案 2
    PlanCmd_Thread.signal.connect(cmd_signal_accept)
    PlanCmd_Thread.start()

    PlanObs_Thread = PlanObsThread()  # OBS场景切换方案 3
    PlanObs_Thread.signal.connect(PlanObssignal_accept)
    PlanObs_Thread.start()

    Shoot_Thread = ShootThread()  # 自动上球 3
    Shoot_Thread.signal.connect(shootsignal_accept)
    Shoot_Thread.start()

    PlanCam_Thread = CamThread()  # 摄像头运行方案 4
    PlanCam_Thread.signal.connect(cam_signal_accept)
    PlanCam_Thread.start()

    PlanBallNum_Thread = PlanBallNumThread()  # 统计过终点的球数 5
    PlanBallNum_Thread.signal.connect(PlanBallNumsignal_accept)
    PlanBallNum_Thread.start()

    ScreenShot_Thread = ScreenShotThread()  # 终点截图识别线程 6
    ScreenShot_Thread.signal.connect(ScreenShotsignal_accept)
    ScreenShot_Thread.start()

    ObsEnd_Thread = ObsEndThread()  # 终点截图识别线程 6
    ObsEnd_Thread.signal.connect(ObsEndsignal_accept)
    ObsEnd_Thread.start()

    Axis_Thread = AxisThread()  # 轴复位 7
    Axis_Thread.signal.connect(axis_signal_accept)
    Axis_Thread.start()

    Pos_Thread = PosThread()  # 实时监控各轴位置 8
    Pos_Thread.signal.connect(possignal_accept)
    Pos_Thread.start()

    ReStart_Thread = ReStartThread()  # 循环模式 9
    ReStart_Thread.signal.connect(restartsignal_accept)
    ReStart_Thread.start()

    Audio_Thread = AudioThread()  # 音频线程 10
    Audio_Thread.signal.connect(audiosignal_accept)
    Audio_Thread.start()

    Ai_Thread = AiThread()  # Ai语言线程 11
    Ai_Thread.signal.connect(aisignal_accept)
    Ai_Thread.start()

    CardStart_Thread = CardStartThread()  # 运动卡开启线程 12
    CardStart_Thread.signal.connect(CardStartsignal_accept)

    TestStatus_Thread = TestStatusThread()  # 测试线程 13
    TestStatus_Thread.signal.connect(test_statussignal_accept)
    TestStatus_Thread.start()

    CheckFile_Thread = CheckFileThread()  # 测试线程 13
    CheckFile_Thread.signal.connect(CheckFile_signal_accept)
    CheckFile_Thread.start()

    Script_Thread = ScriptThread()  # OBS脚本线程
    Script_Thread.signal.connect(script_signal_accept)
    Script_Thread.start()

    OrganCycle_Thread = OrganCycleThread()  # OBS脚本线程
    OrganCycle_Thread.signal.connect(OrganCycle_signal_accept)
    OrganCycle_Thread.start()

    reset_ranking_Thread = ResetRankingThread()  # KAJ789发送线程
    reset_ranking_Thread.signal.connect(reset_ranking_signal_accept)
    reset_ranking_Thread.start()

    ui.pushButton_fsave.clicked.connect(save_plan_json)
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
    ui.checkBox_all.stateChanged.connect(card_on_off_all)
    ui.pushButton_CardClose.clicked.connect(card_close_all)
    ui.pushButton_end_all.clicked.connect(end_all)

    ui.pushButton_start_game.clicked.connect(cmd_loop)
    ui.pushButton_RedLine.clicked.connect(red_line)
    ui.pushButton_test1.clicked.connect(my_test)

    ui.checkBox_saveImgs.checkStateChanged.connect(save_images)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.checkBox_test.checkStateChanged.connect(edit_enable)

    ui.checkBox_shoot.checkStateChanged.connect(organ_shoot)
    ui.checkBox_shoot1.checkStateChanged.connect(organ_shoot)
    ui.checkBox_shoot_1.checkStateChanged.connect(organ_shoot)
    ui.checkBox_shoot2.checkStateChanged.connect(organ_shoot2)
    ui.checkBox_shoot3.checkStateChanged.connect(organ_shoot3)
    ui.checkBox_start.checkStateChanged.connect(organ_start)
    ui.checkBox_start_2.checkStateChanged.connect(organ_start)
    ui.checkBox_end.checkStateChanged.connect(organ_end)
    ui.checkBox_end_2.checkStateChanged.connect(organ_end)
    ui.checkBox_start_count.checkStateChanged.connect(organ_start_count)
    ui.checkBox_shake.checkStateChanged.connect(organ_shake)
    ui.checkBox_alarm_2.checkStateChanged.connect(organ_alarm)
    ui.checkBox_switch.checkStateChanged.connect(organ_number)

    ui.comboBox_plan.currentIndexChanged.connect(plan_refresh)
    ui.tableWidget_Step.itemChanged.connect(table_change)

    ui.textBrowser.textChanged.connect(lambda: clean_browser(ui.textBrowser))
    ui.textBrowser_msg.textChanged.connect(lambda: clean_browser(ui.textBrowser_msg))
    ui.textBrowser_background_data.textChanged.connect(lambda: clean_browser(ui.textBrowser_background_data))

    """
        OBS 处理
    """
    source_list = []  # OBS来源列表
    obs_data = {'obs_scene': ui.lineEdit_scene_name.text(), 'source_ranking': 36, 'source_picture': 13,
                'source_settlement': 26}  # 各来源ID号初始化{'现场', '排名时间组件', '画中画', '结算页'}
    record_data = [False, 'OBS_WEBSOCKET_OUTPUT_STARTING', None]  # OBS 录像状态数据
    scene_now = ''
    cl_request = ''  # 请求 链接配置在 config.toml 文件中
    cl_event = ''  # 监听 链接配置在 config.toml 文件中

    try:
        cl_request = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
        cl_event = obs.EventClient()  # 监听 链接配置在 config.toml 文件中

        cl_event.callback.register(on_current_program_scene_changed)  # 场景变化
        cl_event.callback.register(on_scene_item_enable_state_changed)  # 来源变化
        cl_event.callback.register(on_record_state_changed)  # 录制状态
        cl_event.callback.register(on_stream_state_changed)  # 直播流状态
        cl_event.callback.register(on_get_stream_status)  # 直播流状态
        flg_start['obs'] = True
    except:
        flg_start['obs'] = False

    Obs_Thread = ObsThread()  # OBS启动线程
    Obs_Thread.signal.connect(obssignal_accept)

    Source_Thread = SourceThread()  # OBS来源入表 13
    Source_Thread.sourcesignal.connect(sourcesignal_accept)

    ui.status_live.clicked.connect(obs_stream)
    ui.pushButton_ObsConnect.clicked.connect(obs_open)
    ui.comboBox_Scenes.activated.connect(scenes_change)

    obs_save_t = threading.Thread(target=obs_save_image, daemon=True)
    # obs_save_t.start()
    ui.checkBox_saveImgs_main.checkStateChanged.connect(obs_save_thread)

    rtsp_save_t = threading.Thread(target=rtsp_save_image, daemon=True)
    # rtsp_save_t.start()
    ui.checkBox_saveImgs_monitor.checkStateChanged.connect(rtsp_save_thread)

    "**************************OBS*****************************"

    "**************************图像识别算法_开始*****************************"
    # set_run_toggle 发送请求运行数据
    camera_num = 15  # 摄像头数量
    area_Code = {1: [], 2: [], 3: [], 4: [], 5: [],
                 6: [], 7: [], 8: [], 9: [], 10: [],
                 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 'main': [], 'net': []}  # 摄像头代码列表
    # print(area_Code)

    action_area = [0, 0, 0]  # 触发镜头向下一个位置活动的点位 action_area[区域, 圈数, 可写]
    balls_count = 8  # 运行球数
    balls_start = 0  # 起点球数量
    ranking_array = []  # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    keys = ["x1", "y1", "x2", "y2", "con", "name", "position", "direction", "lapCount", "visible", "lastItem"]
    ball_sort = []  # 位置寄存器 ball_sort[[[]*max_lap_count]*max_area_count + 1]
    ball_stop = False
    pos_stop = []  # 每个球的停止位置索引

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
    term = '8000'  # 期号
    betting_start_time = 0  # 比赛预定开始时间
    betting_end_time = int(time.time())  # 比赛预定结束时间
    stream_url = ''  # 流链接
    Send_Result_End = False  # 发送结果标志位
    betting_loop_flg = True  # 比赛循环标志位
    Track_number = "L"  # 轨道直播编号
    term_status = 1  # 赛事状态（丢球）
    term_comments = ['Invalid Term', 'TRAP', 'OUT', 'Revise']
    term_comment = ''
    result_data = {"raceTrackID": Track_number, "term": str(term), "actualResultOpeningTime": betting_end_time,
                   "result": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                   "timings": json.dumps([
                       {"pm": 1, "id": 1, "time": 120.11},
                       {"pm": 2, "id": 2, "time": 122.73},
                       {"pm": 3, "id": 3, "time": 123.24},
                       {"pm": 4, "id": 4, "time": 125.89},
                       {"pm": 5, "id": 5, "time": 126.01},
                       {"pm": 6, "id": 6, "time": 128.27},
                       {"pm": 7, "id": 7, "time": 129.35},
                       {"pm": 8, "id": 8, "time": 130.98},
                       {"pm": 9, "id": 9, "time": 130.99},
                       {"pm": 10, "id": 10, "time": 131.22}])}
    load_main_json()
    load_ballsort_json()
    load_area()  # 初始化区域划分

    s485.cam_open()

    # 初始化列表
    con_data = []  # 排名数组
    z_ranking_res = []  # 球号排名数组(发送给前端网页排名显示)
    z_ranking_end = []  # 结果排名数组(发送给前端网页排名显示)
    z_ranking_time = []  # 球号排名数组(发送给前端网页排名显示)
    ranking_time_start = time.time()  # 比赛开始时间

    init_ranking_table()  # 初始化排名数据表
    set_trap_btn()  # 初始化TRAP按钮

    # 1. Udp 接收数据 14
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_thread = UdpThread()
        udp_thread.signal.connect(udpsignal_accept)
        udp_thread.start()
    except:
        # 使用infomation信息框
        QMessageBox.information(z_window, "UDP", "UDP端口被占用")
        # sys.exit()

    deal_udp_thread = DealUdpThread()
    deal_udp_thread.signal.connect(udpsignal_accept)
    deal_udp_thread.start()

    # pingpong 发送排名 15
    tcp_ranking_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ranking_thread = TcpRankingThread()  # 前端网页以pingpong形式发送排名数据
    tcp_ranking_thread.signal.connect(tcpsignal_accept)
    tcp_ranking_thread.start()

    tcp_result_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_result_thread = TcpResultThread()  # 前端网页以pingpong形式发送结果数据 16
    tcp_result_thread.signal.connect(tcpsignal_accept)
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
    Update_Thread.signal.connect(rankingsignal_accept)
    Update_Thread.start()

    ui.pushButton_save_Ranking.clicked.connect(save_ballsort_json)

    ui.lineEdit_start_count_ball.editingFinished.connect(save_ballsort_json)
    ui.lineEdit_end_count_ball.editingFinished.connect(save_ballsort_json)

    # 初始化球数组，位置寄存器
    reset_ranking_Thread.run_flg = True  # 重置排名数组

    Kaj789_ui = Kaj789Ui(parent=z_window)
    Kaj789_ui.Track_number = Track_number
    Kaj789_ui.setupUi(Kaj789_ui)
    "**************************图像识别算法_结束*****************************"

    "**************************卫星图_开始*****************************"
    # 开奖记录 lottery_term[期号, 开跑时间, 倒数, 状态, 自动赛果, 确认赛果, 发送状态,
    #                       图片上传状态, 备注, 图片, 录像, 结束时间, 数据包, 补发状态, 补传图片]
    lottery_term = ['0'] * 15
    camera_points = []  # 摄像机移动点位 camera_points[[label内存],[区域号],[卫星图坐标]]
    audio_points = []  # 音效点位 audio_points[[label内存],[区域号],[卫星图坐标]]
    ai_points = []  # AI点位 ai_points[[label内存],[区域号],[卫星图坐标]]
    map_orbit = []  # 地图轨迹
    previous_channel = None  # 音效通道
    ranking_time = 0  # 比赛进行时间
    positions_live = {
        "raceTrackID": "D",
        "term": "5712844",
        "timestampMs": int(time.time() * 1000),
        "result": [
            {"pm": 1, "id": 8, "x": 104, "y": 645, "b": 15},
            {"pm": 2, "id": 3, "x": 101, "y": 355, "b": 13},
            {"pm": 3, "id": 5, "x": 77, "y": 642, "b": 12},
            {"pm": 4, "id": 8, "x": 54, "y": 745, "b": 10},
            {"pm": 5, "id": 7, "x": 31, "y": 891, "b": 10},
            {"pm": 6, "id": 6, "x": 128, "y": 735, "b": 10},
            {"pm": 7, "id": 2, "x": 191, "y": 444, "b": 10},
            {"pm": 8, "id": 1, "x": 124, "y": 605, "b": 9},
            {"pm": 9, "id": 9, "x": 78, "y": 695, "b": 8},
            {"pm": 10, "id": 10, "x": 79, "y": 635, "b": 7}
        ]
    }

    positions_live_thread = PositionsLiveThread()  # 发送实时位置到服务器线程
    positions_live_thread.signal.connect(livesignal_accept)
    positions_live_thread.start()

    map_label_big = MapLabel()
    # map_label_big = MapLabel(picture_size=680, ball_space=11, ball_radius=10, flash_time=30, step_length=2.0,)
    layout_big = QVBoxLayout(ui.widget_map_big)
    layout_big.setContentsMargins(0, 0, 0, 0)
    layout_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 添加自定义的 QLabel 到布局中
    layout_big.addWidget(map_label_big)

    map_label = MapLabel(picture_size=350, ball_space=11, ball_radius=5, step_length=1.03)
    map_layout = QVBoxLayout(ui.widget_map)
    map_layout.setContentsMargins(0, 0, 0, 0)
    map_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 添加自定义的 QLabel 到布局中
    map_layout.addWidget(map_label)

    map_label1 = MapLabel(picture_size=350, ball_space=11, ball_radius=5, step_length=1.03)
    map_layout1 = QVBoxLayout(Map_ui.widget_map)
    map_layout1.setContentsMargins(0, 0, 0, 0)
    map_layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 添加自定义的 QLabel 到布局中
    map_layout1.addWidget(map_label1)

    # 初始化混音器
    pygame.mixer.init()

    ui.checkBox_alarm.checkStateChanged.connect(stop_alarm)
    TrapBall_ui.checkBox_stop.checkStateChanged.connect(stop_alarm)
    ui.checkBox_main_music.checkStateChanged.connect(music_ctl)
    ui.radioButton_music_1.clicked.connect(music_ctl)
    ui.radioButton_music_2.clicked.connect(music_ctl)
    ui.radioButton_music_3.clicked.connect(music_ctl)

    load_points_json('red')
    load_points_json('blue')
    load_points_json('green')

    ui.pushButton_add_camera.clicked.connect(add_camera_points)
    ui.pushButton_del_camera.clicked.connect(del_camera_points)
    ui.pushButton_add_Audio.clicked.connect(add_audio_points)
    ui.pushButton_del_Audio.clicked.connect(del_audio_points)
    ui.pushButton_add_Ai.clicked.connect(add_ai_points)
    ui.pushButton_del_Ai.clicked.connect(del_ai_points)
    ui.pushButton_save_camera.clicked.connect(lambda: save_points('red'))
    ui.pushButton_save_Audio.clicked.connect(lambda: save_points('blue'))
    ui.pushButton_save_Ai.clicked.connect(lambda: save_points('green'))
    ui.checkBox_show_camera.checkStateChanged.connect(lambda: show_points('red'))
    ui.checkBox_show_audio.checkStateChanged.connect(lambda: show_points('blue'))
    ui.checkBox_show_ai.checkStateChanged.connect(lambda: show_points('green'))

    ui.checkBox_show_camera.setChecked(False)
    ui.checkBox_show_audio.setChecked(False)
    ui.checkBox_show_ai.setChecked(False)

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

    result_main_camera_layout = QVBoxLayout(result_ui.widget_camera_sony)
    result_main_camera_layout.setContentsMargins(0, 9, 0, 0)
    result_main_camera_label = CameraLabel()
    result_main_camera_label.Camera_index = 'main_Camera'
    result_main_camera_layout.addWidget(result_main_camera_label)

    result_monitor_camera_layout = QVBoxLayout(result_ui.widget_camera_monitor)
    result_monitor_camera_layout.setContentsMargins(0, 9, 0, 0)
    result_monitor_camera_label = CameraLabel()
    result_monitor_camera_label.Camera_index = 'monitor_Camera'
    result_monitor_camera_layout.addWidget(result_monitor_camera_label)

    fit_camera_layout = QVBoxLayout(ui.widget_camera_fit)
    fit_camera_layout.setContentsMargins(0, 5, 0, 5)
    fit_camera_label = CameraLabel()
    fit_camera_label.Camera_index = 'fit_Camera'
    fit_camera_layout.addWidget(fit_camera_label)

    result_fit_camera_layout = QVBoxLayout(result_ui.widget_camera_fit)
    result_fit_camera_layout.setContentsMargins(0, 5, 0, 5)
    result_fit_camera_label = CameraLabel()
    result_fit_camera_label.Camera_index = 'fit_Camera'
    result_fit_camera_layout.addWidget(result_fit_camera_label)

    ui.checkBox_main_camera.checkStateChanged.connect(main_cam_change)
    ui.checkBox_monitor_cam.checkStateChanged.connect(monitor_cam_change)
    ui.checkBox_map.checkStateChanged.connect(map_change)

    set_result_class()

    "**************************摄像头结果_结束*****************************"
    "**************************参数设置_开始*****************************"
    local_ip = []

    ui.lineEdit_UdpServer_Port.editingFinished.connect(save_main_json)
    ui.lineEdit_TcpServer_Port.editingFinished.connect(save_main_json)
    ui.lineEdit_result_tcpServer_port.editingFinished.connect(save_main_json)
    ui.lineEdit_wakeup_addr.editingFinished.connect(save_main_json)
    ui.lineEdit_rtsp_url.editingFinished.connect(save_main_json)
    ui.lineEdit_recognition_addr.editingFinished.connect(save_main_json)
    ui.lineEdit_obs_script_addr.editingFinished.connect(save_main_json)
    ui.lineEdit_cardNo.editingFinished.connect(save_main_json)
    ui.lineEdit_CardNo.editingFinished.connect(save_main_json)
    ui.lineEdit_s485_Axis_No.editingFinished.connect(save_main_json)
    ui.lineEdit_s485_Cam_No.editingFinished.connect(save_main_json)
    ui.lineEdit_five_axis.editingFinished.connect(save_main_json)
    ui.lineEdit_five_key.editingFinished.connect(save_main_json)
    ui.lineEdit_map_picture.editingFinished.connect(save_main_json)
    ui.lineEdit_map_size.editingFinished.connect(save_main_json)
    ui.lineEdit_map_line.editingFinished.connect(save_main_json)
    ui.lineEdit_upload_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_saidao_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_end1_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_end2_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_scene_name.editingFinished.connect(save_main_json)
    ui.lineEdit_source_ranking.editingFinished.connect(save_main_json)
    ui.lineEdit_source_picture.editingFinished.connect(save_main_json)
    ui.lineEdit_source_settlement.editingFinished.connect(save_main_json)
    ui.lineEdit_source_end.editingFinished.connect(save_main_json)
    ui.lineEdit_music_1.editingFinished.connect(save_main_json)
    ui.lineEdit_music_2.editingFinished.connect(save_main_json)
    ui.lineEdit_music_3.editingFinished.connect(save_main_json)
    ui.lineEdit_sony_sort.editingFinished.connect(save_main_json)
    ui.lineEdit_monitor_sort.editingFinished.connect(save_main_json)
    ui.lineEdit_start.editingFinished.connect(save_main_json)
    ui.lineEdit_shoot.editingFinished.connect(save_main_json)
    ui.lineEdit_shake.editingFinished.connect(save_main_json)
    ui.lineEdit_end.editingFinished.connect(save_main_json)
    ui.lineEdit_start_count.editingFinished.connect(save_main_json)
    ui.lineEdit_alarm.editingFinished.connect(save_main_json)
    ui.lineEdit_shoot_2.editingFinished.connect(save_main_json)
    ui.lineEdit_shoot_3.editingFinished.connect(save_main_json)
    ui.lineEdit_Cycle.editingFinished.connect(save_main_json)
    ui.lineEdit_Cycle_Time.editingFinished.connect(save_main_json)
    ui.lineEdit_area_limit.editingFinished.connect(save_main_json)
    ui.lineEdit_volume_1.editingFinished.connect(save_main_json)
    ui.lineEdit_volume_2.editingFinished.connect(save_main_json)
    ui.lineEdit_volume_3.editingFinished.connect(save_main_json)
    ui.lineEdit_Map_Action.editingFinished.connect(save_main_json)
    ui.lineEdit_End_Num.editingFinished.connect(save_main_json)
    ui.lineEdit_GPS_Num.editingFinished.connect(save_main_json)
    ui.lineEdit_background_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_Start_Path.editingFinished.connect(save_main_json)
    ui.lineEdit_lost.editingFinished.connect(save_main_json)

    ui.checkBox_Cycle.checkStateChanged.connect(save_main_json)
    ui.checkBox_Monitor_Horizontal.checkStateChanged.connect(save_main_json)
    ui.checkBox_Monitor_Vertica.checkStateChanged.connect(save_main_json)
    ui.checkBox_Main_Horizontal.checkStateChanged.connect(save_main_json)
    ui.checkBox_Main_Vertica.checkStateChanged.connect(save_main_json)

    ui.radioButton_music_background_1.clicked.connect(save_main_json)
    ui.radioButton_music_background_2.clicked.connect(save_main_json)
    ui.radioButton_music_background_3.clicked.connect(save_main_json)
    ui.pushButton_Save_Ball.clicked.connect(save_main_json)
    ui.pushButton_Organ.clicked.connect(organ_show)
    ui.pushButton_NetCamera.clicked.connect(net_camera)

    ui.checkBox_Flip_Horizontal.clicked.connect(flip_horizontal)
    ui.checkBox_Flip_Vertica.clicked.connect(flip_vertica)

    "**************************参数设置_结束*****************************"
    "**************************直播大厅_开始*****************************"
    # start_lottery_server_bat()  # 模拟开奖王服务器
    labels = []
    lottery_json_init()

    Kaj789_Thread = Kaj789Thread()  # KAJ789发送线程
    Kaj789_Thread.signal.connect(kaj789_signal_accept)
    Kaj789_Thread.start()

    ui.pushButton_Send_End.clicked.connect(send_end)
    ui.pushButton_Cancel_End.clicked.connect(cancel_end)
    ui.pushButton_ready.clicked.connect(ready_btn)

    ui.radioButton_start_betting.clicked.connect(start_betting)  # 开盘
    ui.radioButton_stop_betting.clicked.connect(stop_betting)  # 封盘
    ui.radioButton_test_game.clicked.connect(test_betting)  # 模拟
    ui.checkBox_black_screen.checkStateChanged.connect(black_screen)
    ui.checkBox_maintain.checkStateChanged.connect(maintain_screen)

    ui.pushButton_close_all.clicked.connect(card_close_all)
    ui.pushButton_Stop_All.clicked.connect(cmd_stop)
    # ui.pushButton_end_all.clicked.connect(stop_server)
    ui.pushButton_Main_Camera.clicked.connect(main2result)
    ui.pushButton_Backup_Camera.clicked.connect(backup2result)
    # ui.pushButton_Cancel_Result.clicked.connect(cancel_betting)
    ui.pushButton_Send_Result.clicked.connect(res2end)
    ui.pushButton_Send_Res.clicked.connect(send_result)
    ui.pushButton_kaj789.clicked.connect(kaj789_table)

    "**************************直播大厅_结束*****************************"

    sys.exit(app.exec())
