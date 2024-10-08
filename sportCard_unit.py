import ctypes
import socket
from utils.log_util import *

card_res = {
    0: '执行成功',
    1: '执行失败(检测命令执行条件是否满足)',
    2: '版本不支持该API(如有需要，联系厂家)',
    7: '参数错误(检测参数是否合理)',
    -1: '通讯失败(接线是否牢靠，更换板卡)',
    -6: '打开控制器失败(是否输入正确串口名，是否调用2次MC_Open)',
    -7: '运动控制器无响应(检测运动控制器是否连接，是否打开。更换板卡)'
}


class SportCard:
    def __init__(self):
        self.card_dll = ctypes.CDLL("./GAS/GAS.dll")
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        self.localip = socket.gethostbyname(hostname)

    # 打开板卡
    def card_open(self, card_num):
        res = self.card_dll.GA_SetCardNo(card_num)
        if res == 0:
            res = self.card_dll.GA_Open(0, self.localip)
            if res == 0:
                return res
                # return self.card_dll.GA_Reset()
            else:
                return fail(("打开板卡: %s" % (card_res[res])))
        else:
            return fail(("板卡设置: %s" % (card_res[res])))

    # 关闭板卡
    def card_close(self):
        return card_res[self.card_dll.GA_Close()]

    # 设置位置
    def card_pos(self, nAxisNum, pos=0, vel=100, dAcc=0.3, dDec=0.2, dVelStart=0.1, dSmoothTime=0):
        nAxisNum_c = ctypes.c_short(nAxisNum)
        dAcc_c = ctypes.c_double(dAcc)
        dDec_c = ctypes.c_double(dDec)
        dVelStart_c = ctypes.c_double(dVelStart)
        dSmoothTime_c = ctypes.c_int(dSmoothTime)
        vel_c = ctypes.c_double(vel)
        pos_c = ctypes.c_long(pos)
        self.card_dll.GA_AxisOn(nAxisNum)  # 设置轴 1 使能
        self.card_dll.GA_PrfTrap(nAxisNum)  # 设置板卡轴 1 为点位模式
        res = self.card_dll.GA_SetTrapPrmSingle(nAxisNum_c, dAcc_c, dDec_c, dVelStart_c, dSmoothTime_c)
        if res == 0:
            res = self.card_dll.GA_SetVel(nAxisNum_c, vel_c)
            if res == 0:
                return self.card_dll.GA_SetPos(nAxisNum_c, pos_c)
            else:
                return fail(("设置加速: %s" % (card_res[res])))
        else:
            return fail(("设置速度: %s" % (card_res[res])))

    # 更新位置
    def card_update(self):
        res = self.card_dll.GA_Update(0xff)
        if res == 0:
            return res
        else:
            return fail(("更新位置: %s" % (card_res[res])))

    # 停止轴运动
    def card_stop(self, nAxisNum):
        nAxisNum_c = ctypes.c_short(nAxisNum - 1)
        res = self.card_dll.GA_Stop((0x001 << (nAxisNum_c)), 0)
        if res == 0:
            return res
        else:
            return fail(("停止运动: %s" % (card_res[res])))

    def get_pos(self, nAxisNum=1, pValue=0, nCount=1, pClock=0):
        self.card_dll.GA_GetPrfPos.argtypes = [ctypes.c_short, ctypes.POINTER(ctypes.c_double), ctypes.c_short,
                                               ctypes.POINTER(ctypes.c_ulong)]
        self.card_dll.GA_GetPrfPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pValue_c = ctypes.c_double(pValue)
        nCount_c = ctypes.c_short(nCount)
        pClock_c = ctypes.c_ulong(pClock)
        return (
            self.card_dll.GA_GetPrfPos(nAxisNum_c, pValue_c, nCount_c, pClock_c), int(pValue_c.value),
            int(pClock_c.value))

    # 复位板卡
    def card_reset(self):
        for i in range(1, 6):
            (res, pValue, pClock) = self.get_pos(i, 0, 1, 0)
            self.card_pos(i, 0)
        self.card_update()
