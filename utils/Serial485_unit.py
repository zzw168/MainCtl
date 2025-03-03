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
        self.s485_Cam_No = 'COM1'
        self.s485_Axis_No = 'COM23'
        self.cam_Visca = {'Flip_Horizontal': ['81 01 04 61 02 FF', '81 01 04 61 03 FF'],  # 水平翻转
                          'Flip_Vertica': ['81 01 04 66 02 FF', '81 01 04 66 03 FF'],  # 对角翻转
                          'Shutter': ['81 01 04 0A 00 FF', '81 01 04 0A 02 FF', '81 01 04 0A 03 FF'],  # 快门
                          'Iris': ['81 01 04 0B 00 FF', '81 01 04 0B 02 FF',
                                   '81 01 04 0B 03 FF', '81 01 04 4B 00 00 0%s 0%s FF'],  # 光圈
                          'WDR_Level': ['81 01 04 21 00 FF', '81 01 04 21 02 FF', '81 01 04 21 03 FF'],  # 对比度
                          'Low_Light': ['81 01 04 22 00 FF', '81 01 04 22 02 FF', '81 01 04 22 03 FF'],  # 低光
                          'R_Gain': ['81 01 04 03 00 FF', '81 01 04 03 02 FF', '81 01 04 03 03 FF'],  # R 红色增益
                          'B_Gain': ['81 01 04 04 00 FF', '81 01 04 04 02 FF', '81 01 04 04 03 FF'],  # B 蓝色增益
                          'Aperture': ['81 01 04 02 00 FF', '81 01 04 02 02 FF', '81 01 04 02 03 FF'],  # 光圈控制
                          'Exposure_Compensation': ['81 01 04 3E 02 FF', '81 01 04 3E 03 FF',
                                                    '81 01 04 0E 00 FF',
                                                    '81 01 04 0E 02 FF', '81 01 04 0E 03 FF'],  # 曝光补偿
                          }

    def cam_open(self):
        try:
            self.ser = serial.Serial(self.s485_Cam_No, 9600, timeout=5)
            print('摄像头端口:%s' % self.s485_Cam_No)
            return self.ser.is_open
        except:
            return False

    # B 蓝色增益
    def cam_b_gain(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['B_Gain'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # R 红色增益
    def cam_r_gain(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['R_Gain'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 曝光补偿
    def cam_exposure_compensation(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Exposure_Compensation'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
            print("曝光补偿~~~~")
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 低光
    def cam_low_light(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Low_Light'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 对比度
    def cam_wdr(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['WDR_Level'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 光圈
    def cam_aperture(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Aperture'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 光圈
    def cam_iris(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Iris'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 快门
    def cam_shutter(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Shutter'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 垂直翻转指令
    def cam_flip_vertica(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Flip_Vertica'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 水平翻转指令
    def cam_flip_horizontal(self, opt: int = 0):
        if self.ser.is_open:
            hexCmd = self.cam_Visca['Flip_Horizontal'][opt]
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 发送镜头缩放指令
    def cam_zoom_step(self, in_out: int = 1):
        if in_out < 16:
            speed = [0, abs(in_out)]  # 总共（0） 16档调整
        elif 16 <= in_out < 32:
            speed = [1, abs(in_out) - 16]  # 总共（1） 16档调整
        elif 32 <= in_out < 48:
            speed = [2, abs(in_out) - 32]  # 总共（1） 16档调整
        elif 48 <= in_out < 64:
            speed = [3, abs(in_out) - 48]  # 总共（1） 16档调整
        elif 64 <= in_out < 80:
            speed = [4, abs(in_out) - 64]  # 总共（1） 16档调整
        else:
            speed = [0, 0]
        if self.ser.is_open:
            hexCmd = "81 01 04 47 0%d 0%s 00 00 FF" % (speed[0], hex(speed[1])[2:])
            print(hexCmd)
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

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
        return self.ser.is_open

    # 镜头缩放开关
    def cam_zoom_off(self):
        if self.ser.is_open:
            hexCmd = "81 01 04 07 00 FF"  # 停止运动
            hexCmd = hexCmd.replace(' ', '')  # 去除空格
            cmd = binascii.a2b_hex(hexCmd)  # 转换为16进制串
            self.ser.write(cmd)  # 4. Hex发送
        else:
            print('端口未链接！')
        return self.ser.is_open

    # 五轴校正
    def get_axis_pos(self, nAxis):
        """
                    nAxisList = [bytes.fromhex('01030B07000277EE'),
                                         bytes.fromhex('02030B07000277DD'),
                                         bytes.fromhex('03030B070002760C'),
                                         bytes.fromhex('04030B07000277BB'),
                                         bytes.fromhex('05030B070002766A')]
                """
        try:
            axis_data = {}
            ser_axis = serial.Serial(port=self.s485_Axis_No, baudrate=57600, stopbits=2, timeout=1)
            if ser_axis.is_open:
                print('端口已经打开')
                ser_axis.write(nAxis)
                data = ser_axis.read(10)
                print("读取数据 %s" % data)
                if data:
                    (nAxisNum, highPos) = self.analysisData(data)
                    if nAxisNum != 0:
                        axis_data = {'nAxisNum': nAxisNum, 'highPos': highPos}
            ser_axis.close()
            return axis_data
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

    " CRC16 校验"

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
