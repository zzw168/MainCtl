"""串口 处理库
    pip install serial
    pip install pyserial
"""
import binascii
import ctypes
import time

import serial


class Serial485:
    def __init__(self):
        self.ser = ''
        try:
            self.ser = serial.Serial('COM1', 9600, timeout=5)
        except:
            print('s485 启动失败')

    def cam_open(self, com='COM1'):
        try:
            if not self.ser.is_open:
                self.ser = serial.Serial(com, 9600, timeout=5)
            return self.ser.is_open
        except:
            return '%s 端口链接失败！' % com

    # 发送镜头缩放指令
    def cam_zoom_move(self, in_out: int = 5):
        speed = abs(in_out)
        if self.ser.is_open:
            if in_out > 0:
                hexCmd = "81 01 04 07 2%d FF" % speed  # 放大总共 7 挡 81代表 1号镜头
            elif in_out < 0:
                hexCmd = "81 01 04 07 3%d FF" % speed  # 缩小总共 7 挡 81代表 1号镜头
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')

    # 镜头缩放开关
    def cam_zoom_on_off(self):
        if self.ser.is_open:
            hexCmd = "81 01 04 07 00 FF"  # 停止运动
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')

    # 五轴校正
    def get_axis_pos(self):
        nAxisList = [bytes.fromhex('01030B07000277EE'),
                     bytes.fromhex('02030B07000277DD'),
                     bytes.fromhex('03030B070002760C'),
                     bytes.fromhex('04030B07000277BB'),
                     bytes.fromhex('05030B070002766A')]
        try:
            sercol = serial.Serial(port='COM23', baudrate=57600, stopbits=2, timeout=1)
            datas = []
            if sercol.is_open:
                print('端口已经打开')
                for nAxis in nAxisList:
                    sercol.write(nAxis)
                    data = sercol.read(10)
                    print("读取数据 %s" % data)
                    if data:
                        (nAxisNum, highPos) = self.analysisData(data)
                        if nAxisNum != 0:
                            datas.append({'nAxisNum': nAxisNum, 'highPos': highPos})
            sercol.close()
            return datas
        except BaseException as e:
            print('轴伺服器复位出错 %s' % e)
            return 0

    def analysisData(self, data: bytes):
        # CRC 校验
        if self.calculate_crc16(data[0:-2], data[-2:]):
            lowPos1 = ""
            lowPos2 = ""
            high1 = ""
            high2 = ""
            nAxisNum = 0
            for index, byte in enumerate(data):
                nAxisNum = (byte if index == 0 else nAxisNum)
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
                    lowPos2 = (hex(byte)[2:]).zfill(2)
                    print(lowPos2)
            highPos = lowPos1 + lowPos2 + high1 + high2
            if highPos == "":
                return (nAxisNum, 0)
            else:
                return (nAxisNum, int(highPos, 16))
        else:
            print('no~~~~~~')

    def calculate_crc16(self, data: bytes, value: bytes) -> bool:
        crc16 = 0XFFFF
        poly = 0xA001
        for item in data:
            crc16 = item ^ crc16
            for i in range(8):
                # 对于每-个data，帮器要右移8次，可以
                if 1 & crc16 == 1:
                    crc16 = crc16 >> 1
                    # >>表示右移，即从高位向低位移出，最高位补0
                    crc16 = crc16 ^ poly
                else:
                    crc16 = crc16 >> 1
        crc16 = hex(int(crc16))  # 将10进制特换成16进制
        crc16 = crc16[2:].upper()
        length = len(crc16)
        high = crc16[0:length - 2].zfill(2)
        high = str(high)
        low = crc16[length - 2:length].zfill(2)
        low = str(low)
        print("校验码:" + low.upper() + high.upper())
        print("准确码:" + value.hex().upper())
        if value.hex().upper() == (low.upper() + high.upper()):
            return True
        else:
            return False

    def cam_close(self):
        self.ser.close()
