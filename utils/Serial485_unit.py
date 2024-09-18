"""串口 处理库
    pip install serial
    pip install pyserial
"""
import binascii
import serial


class Serial485:
    def __init__(self):
        self.ser = serial.Serial('COM1', 9600, timeout=5)

    def cam_open(self, com='COM1'):
        try:
            self.ser = serial.Serial(com, 9600, timeout=5)
            print(self.ser.is_open)
        except:
            print('%s 端口链接失败！' % com)

    # 发送镜头缩放指令
    def cam_zoom_move(self, in_out=0, speed=5):
        if self.ser.is_open:
            if in_out == 0:
                hexCmd = "81 01 04 07 2%d FF" % speed  # 拉远总共 7 挡 81代表 1号镜头
            else:
                hexCmd = "81 01 04 07 3%d FF" % speed  # 拉近总共 7 挡 81代表 1号镜头
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')

    # 镜头缩放开关
    def cam_zoom_on_off(self, on_off=0):
        if self.ser.is_open:
            if on_off == 0:
                hexCmd = "81 01 04 06 03 FF"  # 停止运动
            else:
                hexCmd = "81 01 04 06 02 FF"  # 开启运动
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')

    def cam_close(self):
        self.ser.close()
