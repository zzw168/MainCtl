import ctypes
import socket
from utils.tool_unit import *

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
    def card_move(self, nAxisNum, pos=0, vel=100, dAcc=0.3, dDec=0.2, dVelStart=0.1, dSmoothTime=0):
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

    # 设置位置
    def card_setpos(self, nAxisNum, pos=0):
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pos_c = ctypes.c_long(pos)
        res = self.card_dll.GA_SetPos(nAxisNum_c, pos_c)
        if res == 0:
            return res
        else:
            return fail(("设置位置: %s" % (card_res[res])))

    # 更新位置
    def card_update(self, axis_bit: int = 255):
        nAxis_bit = ctypes.c_long(axis_bit)
        res = self.card_dll.GA_Update(nAxis_bit)
        if res == 0:
            return res
        else:
            return fail(("更新位置: %s" % (card_res[res])))

    # 停止轴运动
    def card_stop(self, nAxisNum: int = 255, lOption: int = 255):
        self.card_dll.GA_Stop.argtypes = [ctypes.c_long, ctypes.c_long]
        self.card_dll.GA_Stop.restype = ctypes.c_int
        # nAxisNum = 2 ** (nAxisNum - 1)
        # nAxisNum = 0xff
        lMask_c = ctypes.c_long(nAxisNum)
        lOption_c = ctypes.c_long(lOption)
        return self.card_dll.GA_Stop(lMask_c, lOption_c)

    # 获取轴位置
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
            self.card_move(i, 0)
        return self.card_update()

    ''' 指定位 输出
    nValue IO 输出值(0/1)
    nBitIndex IO 位索引号(Y0~Y15)
    nCardIndex 0 是主模块，扩展模块从 1 默认主模块
    '''

    def GASetExtDoBit(self, nBitIndex: int = 0, nValue: int = 1, nCardIndex: int = 0):
        self.card_dll.GA_SetExtDoBit.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.card_dll.GA_SetExtDoBit.restype = ctypes.c_int
        nCardIndex_c = ctypes.c_int(nCardIndex)
        nBitIndex_c = ctypes.c_int(nBitIndex)
        nValue_c = ctypes.c_int(nValue)
        return self.card_dll.GA_SetExtDoBit(nCardIndex_c, nBitIndex_c, nValue_c)

    ''' 读取规划位置
        nAxisNum 起始轴号，取值范围：[1,AXIS_MAX_COUNT]
        pValue 规划位置
        nCount 读取的规划轴数，默认为,1次最多可以读取多个轴的运动模式
        pClock 读取控制器时钟，默认为：NULL，即不用读取控制器时钟
    '''

    def GAGetPrfPos(self, nAxisNum: int = 1, pValue=0, nCount=1, pClock=0):
        self.card_dll.GA_GetPrfPos.argtypes = [ctypes.c_short, ctypes.POINTER(ctypes.c_double), ctypes.c_short,
                                               ctypes.POINTER(ctypes.c_ulong)]
        self.card_dll.GA_GetPrfPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pValue_c = ctypes.c_double(pValue)
        nCount_c = ctypes.c_short(nCount)
        pClock_c = ctypes.c_ulong(pClock)
        return (
            self.card_dll.GA_GetPrfPos(nAxisNum_c, pValue_c, nCount_c, pClock_c), pValue_c, pClock_c)

    ''' 修改规划（脉冲）位置，修改时，轴不能处于运动状态
      nAxisNum 轴编号
      lPrfPos 规划(脉冲)位置
    '''

    def GASetPrfPos(self, nAxisNum: int, lPrfPos):

        self.card_dll.GA_SetPrfPos.argtypes = [ctypes.c_short, ctypes.c_long]
        self.card_dll.GA_SetPrfPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        lPrfPos_c = ctypes.c_long(lPrfPos)
        return self.card_dll.GA_SetPrfPos(nAxisNum_c, lPrfPos_c)

    """
    GA_GetDiRaw 读取数字 IO 输入状态的原始值
    GA_GetDiReverseCount 读取数字量输入信号的变化次数
    GA_SetDiReverseCount 设置数字量输入信号的变化次数的初值
    MC_GetExtDiValue 获取 IO 输入（包含主模块和扩展模块）
    MC_GetExtDiBit 获取指定 IO 模块的指定位输入（包含主模块和扩展模块）
    """

    ''' GA_SetDiReverseCount 设置数字量输入信号的变化次数的初值
    int GA_SetDiReverseCount(short nDiType,short diIndex,unsigned long ReserveCount,short
        nCount)
         nDiType 指定数字 IO 类型
            MC_LIMIT_POSITIVE(该宏定义为 0) 正限位
            MC_LIMIT_NEGATIVE(该宏定义为 1) 负限位
            MC_ALARM(该宏定义为 2) 驱动报警
            MC_HOME(该宏定义为 3) 原点开关
            MC_GPI(该宏定义为 4) 通用输入
            MC_ARRIVE(该宏定义为 5) 电机到位信号
        diIndex 数字量输入的索引,取值范围：
            nDiType= MC_LIMIT_POSITIVE 时：[0,7]
            nDiType= MC_LIMIT_NEGATIVE 时：[0,7]
            nDiType= MC_ALARM 时：[0,7]
            nDiType= MC_HOME 时：[0,7]
            nDiType= MC_GPI 时：[0,15]
            nDiType= MC_ARRIVE 时：[0,7]
        ReserveCount 设置的数字量输入的变化次数
        nCount 设置变化次数的数字量输入的个数，默认为 1
    '''

    def GASetDiReverseCount(self, nDiType=4, diIndex=0, nReserveCount=0, nCount=1):
        self.card_dll.GA_SetDiReverseCount.argtypes = [ctypes.c_short, ctypes.c_short, ctypes.c_ulong,
                                                       ctypes.c_short]
        self.card_dll.GA_SetDiReverseCount.restype = ctypes.c_int
        nDiType_c = ctypes.c_short(nDiType)
        diIndex_c = ctypes.c_short(diIndex)
        nReserveCount_c = ctypes.c_ulong(nReserveCount)
        nCount_c = ctypes.c_short(nCount)
        return self.card_dll.GA_SetDiReverseCount(nDiType_c, diIndex_c, nReserveCount_c, nCount_c)

    ''' GA_GetDiReverseCount 读取数字量输入信号的变化次数
    int GA_GetDiReverseCount(short nDiType,short diIndex,unsigned long*pReserveCount,short
        nCount=1)
     diType 指定数字 IO 类型
            MC_LIMIT_POSITIVE(该宏定义为 0) 正限位
            MC_LIMIT_NEGATIVE(该宏定义为 1) 负限位
            MC_ALARM(该宏定义为 2) 驱动报警
            MC_HOME(该宏定义为 3) 原点开关
            MC_GPI(该宏定义为 4) 通用输入
            MC_ARRIVE(该宏定义为 5) 电机到位信号
     diIndex 数字量输入的索引,取值范围：
            nDiType= MC_LIMIT_POSITIVE 时：[0,7]
            nDiType= MC_LIMIT_NEGATIVE 时：[0,7]
            nDiType= MC_ALARM 时：[0,0]
            nDiType= MC_HOME 时：[0,7]
            nDiType= MC_GPI 时：[0,15]
            nDiType= MC_ARRIVE 时：[0,7]
    pReserveCount 读取的数字量输入的变化次数
    nCount 读取变化次数的数字量输入的个数，默认为 1
    '''

    def GAGetDiReverseCount(self, nDiType=4, diIndex=0, nCount=1):
        self.card_dll.GA_GetDiReverseCount.argtypes = [ctypes.c_short, ctypes.c_short, ctypes.POINTER(ctypes.c_ulong),
                                                       ctypes.c_short]
        self.card_dll.GA_GetDiReverseCount.restype = ctypes.c_int
        nDiType_c = ctypes.c_short(nDiType)
        diIndex_c = ctypes.c_short(diIndex)
        pReserveCount_c = (ctypes.c_ulong * nCount)()
        nCount_c = ctypes.c_short(nCount)
        return self.card_dll.GA_GetDiReverseCount(nDiType_c, diIndex_c, pReserveCount_c, nCount_c), list(
            pReserveCount_c)
