import os
import sys
import time

import pynput
import yaml

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu

import obsws_python as obs

from utils.SportCard_unit import *
from utils.tool_unit import *
from utils.Serial485_unit import *
from MainCtl_Ui import *

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

"************************************OBS****************************************"


class ObsThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(ObsThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        global cl_requst
        global cl_event
        try:
            cl_requst = obs.ReqClient()  # 请求
            cl_event = obs.EventClient()  # 监听

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
        global source_list
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
        print('操作OBS来源失败！')


def get_scenes_list():  # 刷新所有列表
    try:
        res = cl_requst.get_scene_list()  # 获取场景列表
        res_name = cl_requst.get_current_program_scene()  # 获取激活的场景
    except:
        print('获取场景失败！')
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
    cl_requst.set_current_program_scene(scene_name)


"******************************OBS结束*************************************"


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

                table.cellWidget(row, 0).setChecked(False)
                for i in range(1, table.columnCount() - 1):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(row, i, item)
            else:
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                table.setCellWidget(0, 0, cb)

                for i in range(1, table.columnCount() - 1):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(0, i, item)


class ColorThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(ColorThead, self).__init__()

    def run(self) -> None:
        while True:
            if z_status:
                status_color = 'background:rgb(255, 0, 0)'
            else:
                status_color = 'background:rgb(0, 255, 0)'
                pass
            self._signal.emit(status_color)
            time.sleep(1)


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
        self.camitem = [5, 5]

    def run(self) -> None:
        s485.cam_zoom_move(self.camitem[0])
        time.sleep(self.camitem[1])
        s485.cam_zoom_on_off()


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
                for i, item in enumerate(plan_list):
                    print(plan_list)
                    if item[0] == '1':  # 是否勾选
                        self._signal.emit(i)
                        sc.card_move(1, int(item[2]), vel=int(item[7]), dAcc=float(item[8]), dDec=float(item[9]),
                                     dVelStart=0.1, dSmoothTime=0)
                        sc.card_move(2, int(item[3]), vel=int(item[7]), dAcc=float(item[8]), dDec=float(item[9]),
                                     dVelStart=0.1, dSmoothTime=0)
                        sc.card_move(3, int(item[4]), vel=int(item[7]), dAcc=float(item[8]), dDec=float(item[9]),
                                     dVelStart=0.1, dSmoothTime=0)
                        sc.card_move(4, int(item[5]), vel=int(item[7]), dAcc=float(item[8]), dDec=float(item[9]),
                                     dVelStart=0.1, dSmoothTime=0)
                        sc.card_move(5, int(item[6]), vel=int(item[7]), dAcc=float(item[8]), dDec=float(item[9]),
                                     dVelStart=0.1, dSmoothTime=0)
                        sc.card_update()

                        # time.sleep(2)
                        while True:
                            k = 0
                            for i in range(0, len(pValue)):
                                if pValue[i] == int(item[i + 2]):
                                    k += 1
                            if k == 5:
                                break

                        if int(item[10]) != 0 and int(item[10]) != 0:
                            Cam_Thead.camitem = [int(item[10]), int(item[11])]
                            Cam_Thead.start()

                self._signal.emit(succeed("运动流程：完成！"))
            except:
                self._signal.emit(fail("运动卡运行：出错！"))
        else:
            self._signal.emit(fail("运动卡未链接！"))


def signal_accept(message):
    global p_now
    print(message)
    if isinstance(message, int):
        print(message)
        tb_step = ui.tableWidget_Step
        col_num = tb_step.columnCount()
        print(col_num)
        for i in range(1, col_num - 1):
            tb_step.item(p_now, i).setBackground(QBrush(QColor(255, 255, 255)))
            tb_step.item(message, i).setBackground(QBrush(QColor(255, 0, 255)))
        p_now = message
    else:
        ui.textBrowser.append(message)


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
            if key.char == '-':
                s485.cam_zoom_on_off()

            if key.char == '+':
                s485.cam_zoom_on_off()

            if key == key.up:
                print('前')
                # sc.card_stop(2)
                flag_key_run = True
                sc.card_setpos(2, pValue[1] + 30000)

            if key == key.down:
                print('后')
                # sc.card_stop(2)
                flag_key_run = True
                sc.card_setpos(2, pValue[1] - 30000)

            if key == key.left:
                print('左')
                # sc.card_stop(1)
                flag_key_run = True
                sc.card_setpos(1, pValue[0] + 30000)

            if key == key.right:
                print('右')
                # sc.card_stop(1)
                flag_key_run = True
                sc.card_setpos(1, pValue[0] - 30000)

            if key == key.insert:
                print('上')
                flag_key_run = True
                sc.card_setpos(3, pValue[2] - 30000)

            if key == key.delete:
                print('下')
                flag_key_run = True
                sc.card_setpos(3, pValue[2] + 30000)

            if key == key.home:
                print('头左')
                flag_key_run = True
                sc.card_setpos(4, pValue[3] + 30000)

            if key == key.end:
                print('头右')
                flag_key_run = True
                sc.card_setpos(4, pValue[3] - 30000)

            if key == key.page_up:
                print('头下')
                flag_key_run = True
                sc.card_setpos(5, pValue[4] - 30000)

            if key == key.page_down:
                print('头下')
                flag_key_run = True
                sc.card_setpos(5, pValue[4] + 30000)
            sc.card_update()
        except AttributeError:
            print(key)


def keyboard_press(key):
    global flag_key_run
    if ui.checkBox_key.isChecked() and flag_card_start:
        try:
            if key.char == '+':
                s485.cam_zoom_move(5)

            if key.char == '-':
                s485.cam_zoom_move(-5)

            if key == key.up:
                print('前')
                if flag_key_run:
                    sc.card_move(2, pos=2000000)
                    sc.card_update()
                    flag_key_run = False

            if key == key.down:
                print('后')
                if flag_key_run:
                    sc.card_move(2, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.left:
                print('左')
                if flag_key_run:
                    sc.card_move(1, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.right:
                print('右')
                if flag_key_run:
                    sc.card_move(1, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.insert:
                print('上')
                if flag_key_run:
                    sc.card_move(3, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.delete:
                print('下')
                if flag_key_run:
                    sc.card_move(3, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.home:
                print('头左')
                if flag_key_run:
                    sc.card_move(4, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.end:
                print('头右')
                if flag_key_run:
                    sc.card_move(4, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.page_up:
                print('头下')
                if flag_key_run:
                    sc.card_move(5, pos=-2000000)
                    sc.card_update()
                    flag_key_run = False
            if key == key.page_down:
                print('头上')
                if flag_key_run:
                    sc.card_move(5, pos=2000000)
                    sc.card_update()
                    flag_key_run = False
        except AttributeError:
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
    print(plan_list)

    comb = ui.comboBox_plan
    plan_num = comb.currentIndex()
    plan_name = comb.currentText()

    file = "./Robot.yml"
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


# 载入方案
def deal_yaml():
    global plan_names
    global plan_all
    file = "./Robot.yml"
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


def plan_refresh():
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


def flashsignal_accept(status_color):  # 更改颜色
    ui.status_server1.setStyleSheet(status_color)
    ui.status_obs.setStyleSheet(status_color)
    ui.status_server2.setStyleSheet(status_color)
    ui.status_live.setStyleSheet(status_color)
    ui.status_road.setStyleSheet(status_color)
    ui.status_lenses.setStyleSheet(status_color)
    ui.status_Extension.setStyleSheet(status_color)
    ui.status_mainlenses.setStyleSheet(status_color)
    ui.status_Recognition.setStyleSheet(status_color)
    ui.status_track.setStyleSheet(status_color)
    ui.status_sportsCards.setStyleSheet(status_color)


def bt_start():
    global z_status
    # ui.widget_9.setVisible(not (ui.widget_9.isVisible()))
    z_status = not (z_status)


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
    s485_flag = s485.cam_open(plan_all['s485No'])
    if s485_flag == True:
        ui.textBrowser.append(succeed('串口链接：%s' % s485_flag))
    else:
        ui.textBrowser.append(fail('串口链接：%s' % s485_flag))


def cmd_run():
    save_plan()
    if Cmd_Thead.isRunning():
        Cmd_Thead.terminate()
    Cmd_Thead.start()
    # ui.textBrowser.append(succeed('串口链接：%s' % s485.cam_open(plan_all['s485No'])))


def card_reset():
    (res, pValue, pClock) = sc.get_pos()
    print("%s %s %s" % (res, pValue, pClock))
    res = sc.card_reset()
    if res == 0:
        ui.textBrowser.append(succeed('复位：%s' % card_res[res]))
    else:
        ui.textBrowser.append(res)
    # (res, pValue, pClock) = sc.get_pos()
    # print("%s %s %s" % (res, pValue, pClock))


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
    print("%s %s" % (row, col))
    if row < 0 or col < 0:
        return
    if not is_natural_num(tb_step.item(row, col).text()):
        try:
            if col > len(plan_list[row]) - 1:
                tb_step.item(row, col).setText('0')
            else:
                comb = ui.comboBox_plan
                _index = comb.currentIndex()
                tb_step.item(row, col).setText(plan_list[row][col])
        except:
            pass


def cmd_stop():
    Cmd_Thead.terminate()


def test():
    # ui.textBrowser.append("<font color='green'> okok </font>")
    for item in enumerate(plan_list):
        print(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()

    z_status = True
    sc = SportCard()  # 运动卡
    s485 = Serial485()  # 摄像头

    plan_list = []  # 当前方案列表
    plan_names = []  # 当前方案名称
    plan_all = {}  # 所有方案资料
    pValue = [0, 0, 0, 0, 0]  # 各轴位置
    p_now = 0  # 保存方案运行位置
    flag_key_run = True  # 键盘控制标志
    flag_card_start = False  # 运动板卡启动标志

    deal_yaml()
    ui.lineEdit_CarNo.setText(str(plan_all['cardNo']))

    KeyListener_Thead = KeyListenerThead()  # 启用键盘监听
    KeyListener_Thead.start()

    Cmd_Thead = CmdThead()  # 运行方案
    Cmd_Thead._signal.connect(signal_accept)

    Cam_Thead = CamThead()  # 摄像头运行方案
    Cam_Thead._signal.connect(signal_accept)

    Pos_Thead = PosThead()  # 实时监控摄像头位置
    Pos_Thead._signal.connect(pos_signal_accept)

    Color_Thead = ColorThead()  # 更新状态信息线程
    Color_Thead._signal.connect(flashsignal_accept)
    Color_Thead.start()

    ui.pushButton_fsave.clicked.connect(save_plan)
    # ui.pushButton_rename.clicked.connect(test)
    ui.pushButton_rename.clicked.connect(plan_rename)
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

    sys.exit(app.exec_())
