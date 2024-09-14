# coding: utf-8
import ctypes
from PySide6.QtCore import QObject

class GasCall(QObject):

    def __init__(self):
        super().__init__()
        self.dll = ctypes.WinDLL("modules/dll_gas/GAS.dll")

    ''' 打开板卡
        cName 当 iType=0（网口方式打开）时，该参数代表 PC 端 IP 地址
        当 iType=1（串口方式打开）时，该参数代表默认串口号
        iType 打开方式，0 网口，1 串口
    '''
    def GAopen(self,cName:str,iType = 0):
        # 设置参数类型
        self.dll.GA_Open.argtypes = [ctypes.c_int, ctypes.c_char_p] 
        # 设置返回值类型
        self.dll.GA_Open.restype = ctypes.c_int
        # 转换为c_char_p类型
        cName_c = ctypes.c_char_p(cName.encode('utf-8'))
        iType_c  = ctypes.c_int(iType)
        # 调用方法
        return self.dll.GA_Open(iType_c,cName_c)
    
    ''' 关闭板卡 '''
    def GAclose(self):
        self.dll.GA_Close.restype = ctypes.c_int
        return self.dll.GA_Close()

    ''' 指定位 输出
      nValue IO 输出值(0/1)
      nBitIndex IO 位索引号(0~15)
      nCardIndex 0 是主模块，扩展模块从 1 默认主模块
    '''
    def GASetExtDoBit(self,nBitIndex:int,nValue:int,nCardIndex=0):
        self.dll.GA_SetExtDoBit.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.dll.GA_SetExtDoBit.restype = ctypes.c_int
        nCardIndex_c  = ctypes.c_int(nCardIndex)
        nBitIndex_c  = ctypes.c_int(nBitIndex)
        nValue_c  = ctypes.c_int(nValue)
        return self.dll.GA_SetExtDoBit(nCardIndex_c,nBitIndex_c,nValue_c)

    ''' 指定位 输入
     nBitIndex IO 位索引号(0~15)
     pValue IO 输入值存放指针
     nCardIndex 0 是主模块，扩展模块从 1 默认主模块
    '''
    def GAGetExtDiBit(self,nBitIndex:int,pValue:int,nCardIndex=0):
        self.dll.GA_GetExtDiBit.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_ushort)]
        self.dll.GA_GetExtDiBit.restype = ctypes.c_int
        nCardIndex_c  = ctypes.c_int(nCardIndex)
        nBitIndex_c  = ctypes.c_int(nBitIndex)
        nValue_c  = ctypes.c_ushort(pValue)
        return self.dll.GA_GetExtDiBit(nCardIndex_c,nBitIndex_c,nValue_c)

    ''' 获取 IO 输入（包含主卡 IO、限位、零位）
     ditType
      MC_LIMIT_POSITIVE(该宏定义为 0) 正限位
      MC_LIMIT_NEGATIVE(该宏定义为 1) 负限位
      MC_ALARM(该宏定义为 2) 驱动报警
      MC_HOME(该宏定义为 3) 原点开关
      MC_GPI(该宏定义为 4) 通用输入
      MC_MPG(该宏定义为 7) 手轮 IO 输入
      pValue IO 输入值存放指
    '''
    def GAGetDiRaw(self,nDiType:int,pValue:int):
        self.dll.GA_GetDiRaw.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_long)]
        self.dll.GA_GetDiRaw.restype = ctypes.c_int
        nDiType_c  = ctypes.c_int(nDiType)
        pValue_c  =ctypes.c_long(pValue)
        return (self.dll.GA_GetDiRaw(nDiType_c,ctypes.byref(pValue_c)),int(pValue_c.value))

    ''' 获取 IO 输入（包含主模块和扩展模块)
     nCardIndex 起始板卡索引(0~63),0 是主模块，扩展模块从 1 开始
     pValue IO 输入值存放指针
     nCount 本次获取的模块数量(1~64)
    '''
    def GAGetExtDiValue(self,value:int,nCount=1,nCardIndex=0):
        self.dll.GA_GetExtDiValue.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulong),ctypes.c_short]
        self.dll.GA_GetExtDiValue.restype = ctypes.c_int
        nCardIndex_c  = ctypes.c_int(nCardIndex)
        value_c  = ctypes.c_ulong(value)
        nCount_c  = ctypes.c_short(nCount)
        return (self.dll.GA_GetExtDiValue(nCardIndex_c,value_c,nCount_c),int(value_c.value))

    '''设置指定轴为点位模式
      iAxis 规划轴号
    '''
    def GAPrfTrap(self,nAxisNum:int):
        self.dll.GA_PrfTrap.argtypes = [ctypes.c_short]
        self.dll.GA_PrfTrap.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        return self.dll.GA_PrfTrap(nAxisNum_c)

    ''' 设置数字量输入信号的变化次数的初值
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
    def GASetDiReverseCount(self, nDiType:int, diIndex:int, ReserveCount:int,nCount=1):
        self.dll.GA_SetDiReverseCount.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_ulong,ctypes.c_int]
        self.dll.GA_SetDiReverseCount.restype = ctypes.c_int
        nDiType_c = ctypes.c_int(nDiType)
        diIndex_c = ctypes.c_int(diIndex)
        reserveCount_c = ctypes.c_ulong(ReserveCount)
        nCount_c = ctypes.c_int(nCount)
        return self.dll.GA_SetDiReverseCount(nDiType_c,diIndex_c,reserveCount_c,nCount_c)

    '''读取数字量输入信号的变化次数
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
         nDiType= MC_ALARM 时：[0,0]
         nDiType= MC_HOME 时：[0,7]
         nDiType= MC_GPI 时：[0,15]
         nDiType= MC_ARRIVE 时：[0,7]
         pReserveCount 读取的数字量输入的变化次数
         nCount 读取变化次数的数字量输入的个数，默认为 1
    '''
    def GAGetDiReverseCount(self, nDiType:int, diIndex:int,pReserveCount:int,nCount=1):
        self.dll.GA_GetDiReverseCount.argtypes = [ctypes.c_short,ctypes.c_short,ctypes.POINTER(ctypes.c_ulong),ctypes.c_short]
        self.dll.GA_GetDiReverseCount.restype = ctypes.c_int
        nDiType_c = ctypes.c_short(nDiType)
        diIndex_c = ctypes.c_short(diIndex)
        pReserveCount_c = ctypes.c_ulong(pReserveCount)
        nCount_c = ctypes.c_short(nCount)
        return (self.dll.GA_GetDiReverseCount(nDiType_c,diIndex_c,pReserveCount_c,nCount_c), int(pReserveCount_c.value))

    ''' 设置点位模式运动参数（可替代 MC_SetTrapPrm）
         nAxisNum 规划轴号
         dAcc 加速度
         dDec 减速度
         dVelStart 启动速度
         dSmoothTime 平滑时间
    '''
    def GASetTrapPrmSingle(self, nAxisNum:int, dAcc, dDec, dVelStart, dSmoothTime = 0):
        self.dll.GA_SetTrapPrmSingle.argtypes =  [ctypes.c_short,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_int]
        self.dll.GA_SetTrapPrmSingle.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        dAcc_c = ctypes.c_double(dAcc)
        dDec_c = ctypes.c_double(dDec)
        dVelStart_c = ctypes.c_double(dVelStart)
        dSmoothTime_c = ctypes.c_int(dSmoothTime)
        return  self.dll.GA_SetTrapPrmSingle(nAxisNum_c,dAcc_c,dDec_c,dVelStart_c,dSmoothTime_c)

    ''' 设置目标速度
     nAxisNum 规划轴号  
     vel 设置目标速度，单位是“脉冲/毫秒"  
    '''
    def GASetVel(self, nAxisNum:int, vel):
        self.dll.GA_SetVel.argtypes =  [ctypes.c_short,ctypes.c_double]
        self.dll.GA_SetVel.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        vel_c  = ctypes.c_double(vel)
        return self.dll.GA_SetVel(nAxisNum_c,vel_c)
    
    ''' 切换当前运动控制器卡号
      iCardNum 将被设置为当前运动控制器的卡号，取值范围：[1,255]
    '''
    def GASetCardNo(self, iCardNum):
        self.dll.GA_SetCardNo.argtypes = [ctypes.c_short]
        self.dll.GA_SetCardNo.restype = ctypes.c_int
        iCardNum_c = ctypes.c_short(iCardNum)
        return   self.dll.GA_SetCardNo(iCardNum_c)

    ''' 设置目标位置
      iAxis 规划轴号
      pos 设置目标位置，单位是脉冲
    '''
    def GASetPos(self, nAxisNum:int, pos:int):
        self.dll.GA_SetPos.argtypes =  [ctypes.c_short,ctypes.c_long]
        self.dll.GA_SetPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pos_c  = ctypes.c_long(pos)
        return self.dll.GA_SetPos(nAxisNum_c,pos_c)

    ''' 启动点位运动
        mask  按位指示需要启动点位运动的轴号  bit0 表示轴，bit1 表示 2 轴，
    '''
    def GAUpdate(self,mask:int):
        self.dll.GA_Update.argtypes = [ctypes.c_long]
        self.dll.GA_Update.restype = ctypes.c_int
        mask = 2 **(mask - 1)
        mask_c = ctypes.c_long(mask)
        return self.dll.GA_Update(mask_c)

    ''' 设置回零参数（非结构体方式，可以代替 MC_HomeSetPrm）
     nAxisNum 需要设置回零参数的轴号,取值范围：[1,AXIS_MAX_COUNT]
     nHomeMode 1:HOME 回原点,此回零方式最常用   2:HOME 加 Index 回原点（仅支持带 Index 的驱动）  3:Index 回原点（仅支持带 Index 的驱动）
     nHomeDir 回零方向，1:正向回零，0:负向回零
     lOffset 回零偏移，回到零位后再走一个 Offset 作为零位,通常该参数为 0
     dHomeRapidVel 回零快移速度，单位：Pluse/ms
     dHomeLocatVel 回零定位速度，单位：Pluse/ms
     dHomeIndexVel  回零寻找 INDEX 速度，单位：Pluse/ms
     dHomeAcc 回零使用的加速度，单位 Pluse/ms/ms
    '''
    def GAHomeSetPrmSingle(self, iAxisNum:int, nHomeMode:int, nHomeDir:int, lOffset:int, dHomeRapidVel,dHomeLocatVel,
                           dHomeIndexVel, dHomeAcc):
         self.dll.GA_HomeSetPrmSingle.argtypes = [ctypes.c_short,ctypes.c_short,ctypes.c_short,ctypes.c_long,
                                                  ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
         self.dll.GA_HomeSetPrmSingle.restype =  ctypes.c_int
         iAxisNum_c = ctypes.c_short(iAxisNum)
         nHomeMode_c = ctypes.c_short(nHomeMode)
         nHomeDir_c = ctypes.c_short(nHomeDir)
         lOffset_c =ctypes.c_long(lOffset)
         dHomeRapidVel_c = ctypes.c_double(dHomeRapidVel)
         dHomeLocatVel_c = ctypes.c_double(dHomeLocatVel)
         dHomeIndexVel_c = ctypes.c_double(dHomeIndexVel)
         dHomeAcc_c = ctypes.c_double(dHomeAcc)
         return self.dll.GA_HomeSetPrmSingle(iAxisNum_c,nHomeMode_c,nHomeDir_c,lOffset_c,dHomeRapidVel_c,dHomeLocatVel_c,dHomeIndexVel_c,dHomeAcc_c)

    ''' 启动轴回零
      iAxisNum 需要回零的轴号,取值范围：[1,AXIS_MAX_COUNT
    '''
    def GAHomeStart(self,iAxisNum:int):
        self.dll.GA_HomeStart.argtypes = [ctypes.c_int]
        self.dll.GA_HomeStart.restype  = ctypes.c_int
        iAxisNum_c = ctypes.c_int(iAxisNum)
        return self.dll.GA_HomeStart(iAxisNum_c)


    ''' 读取编码器位值
      nAxisNum 起始轴号，取值范围：[1,AXIS_MAX_COUNT]
      pValue 轴的编码器位置
      nCount 读取的轴数，默认为,1次最多可以读取多个轴的编码器位置
      pClock 读取控制器时钟，默认为：NULL，即不用读取控制器时钟
    '''
    def GAGetAxisEncPos(self, nAxisNum:int, pValue, nCount=1, pClock=None):
        self.dll.GA_GetAxisEncPos.argtypes = [ctypes.c_short,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_ulong)]
        self.dll.GA_GetAxisEncPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pValue_c = ctypes.c_double(pValue)
        nCount_c = ctypes.c_int(nCount)
        pClock_c = ctypes.c_ulong(pClock)
        return (self.dll.GA_GetAxisEncPos(nAxisNum_c,pValue_c,nCount_c,pClock_c),float(pValue_c.value),int(pClock_c.value))

    ''' 停止一个或多个轴的规划运动，停止坐标系运动
     lMask 按位指示需要停止运动的轴号或者坐标系号 bit0表示轴1，bit1表示轴2，„，bit7表示轴8   bit8表示坐标系1，bit9表示坐标系2 当 bit 位为 1 时表示停止对应的轴或者坐标系
     lOption  按位指示停止方式 bit0表示轴1，bit1表示轴2，„，bit7表示轴8 bit8表示坐标系1，bit9表示坐标系2  当bit位为0时表示平滑停止对应的轴或坐标系  当bit位为1时表示紧急停止对应的轴或坐标系
    '''
    def GAStop(self,  lMask:int, lOption:int):
        self.dll.GA_Stop.argtypes = [ctypes.c_long,ctypes.c_long]
        self.dll.GA_Stop.restype = ctypes.c_int
        lMask =   2 ** (lMask - 1)
        lMask_c  = ctypes.c_long(lMask)
        lOption_c = ctypes.c_long(lOption)
        return self.dll.GA_Stop(lMask_c,lOption_c)

    '''用于代替 MC_SetCrdPrm 函数，方便不擅长结构体的客户使用。
      1.nCrdNum :坐标系号，取值范围：[1,CRDSYS_MAX_COUNT]  !         2.dimension：坐标系的维数，取值范围：[1,5]
      3.profile0 :坐标系 X 轴号，取值范围：[1,8]  .                  4.profile1  坐标系 Y 轴号，取值范围：[1,8]，用不到可以设置为 0
      5.profile2 坐标系 Z 轴号，取值范围：[1,8]，用不到可以设置为 0    6.profile3  坐标系 A 轴号，取值范围：[1,8]，用不到可以设置为 0
      7.profile4 坐标系 B 轴号，取值范围：[1,8]，用不到可以设置为 0    8.profile5  保留，固定为 0
      9.profile6 保留，固定为 0                                     10.profile7 保留，固定为 0
      11.synVelMax：该坐标系的最大合成速度。取值范围：(0,32767)，单位：pulse/ms   12.synAccMax 该坐标系的最大合成加速度。取值范围：(0,32767)，单位：pulse/(ms*ms)
      13.evenTime 每个插补段的最小匀速段时间。取值范围：[0,32767)，单位：ms
      14.setOriginFlag表示是否需要指定坐标系的原点坐标的规划位置。 0：不需要指定原点坐标值，则坐标系的原点在当前规划位置上  1：需要指定原点坐标值，按照后面的 originPos 设定原点坐标值
      15.originPos0  X 轴的原点坐标位置，单位脉冲           16.originPos1  Y 轴的原点坐标位置，单位脉冲
      17.originPos2  Z 轴的原点坐标位置，单位脉冲    18.originPos3  A 轴的原点坐标位置，单位脉冲
      19.originPos4  B 轴的原点坐标位置，单位脉冲    20.originPos5 保留，固定为 0
      21.originPos6 保留，固定为 0                  22.originPos7 保留，固定为 0
    '''
    def GASetCrdPrmSingleEX(self, nCrdNum:int, dimension:int, profile0:int,profile1:int, profile2:int, profile3:int, profile4:int,
                             profile5:int,profile6:int, profile7:int,synVelMax:float, synAccMax:float, evenTime:int, setOriginFlag:int,
                             originPos0:int, originPos1:int, originPos2:int, originPos3:int, originPos4:int, originPos5=0,
                             originPos6=0, originPos7=0):
        self.dll.GA_SetCrdPrmSingleEX.argtypes = [ ctypes.c_short, ctypes.c_short,ctypes.c_short,ctypes.c_short,  ctypes.c_short,
            ctypes.c_short,ctypes.c_short, ctypes.c_short,ctypes.c_short,ctypes.c_short,
            ctypes.c_double,ctypes.c_double, ctypes.c_short, ctypes.c_short,
            ctypes.c_long,ctypes.c_long,ctypes.c_long, ctypes.c_long, ctypes.c_long,
            ctypes.c_long,ctypes.c_long,ctypes.c_long]
        self.dll.GA_SetCrdPrmSingleEX.restype = ctypes.c_int
        nCrdNum_c = ctypes.c_int16(nCrdNum)
        dimension_c = ctypes.c_int16(dimension)
        profile0_c = ctypes.c_int16(profile0)
        profile1_c = ctypes.c_int16(profile1)
        profile2_c = ctypes.c_int16(profile2)
        profile3_c = ctypes.c_int16(profile3)
        profile4_c = ctypes.c_int16(profile4)
        profile5_c = ctypes.c_int16(profile5)
        profile6_c = ctypes.c_int16(profile6)
        profile7_c = ctypes.c_int16(profile7)
        synVelMax_c = ctypes.c_double(synVelMax)
        synAccMax_c = ctypes.c_double(synAccMax)
        evenTime_c = ctypes.c_short(evenTime)
        setOriginFlag_c = ctypes.c_short(setOriginFlag)
        originPos0_c = ctypes.c_int32(originPos0)
        originPos1_c = ctypes.c_int32(originPos1)
        originPos2_c = ctypes.c_int32(originPos2)
        originPos3_c = ctypes.c_int32(originPos3)
        originPos4_c = ctypes.c_int32(originPos4)
        originPos5_c = ctypes.c_int32(originPos5)
        originPos6_c = ctypes.c_int32(originPos6)
        originPos7_c = ctypes.c_int32(originPos7)
        return self.dll.GA_SetCrdPrmSingleEX(nCrdNum_c,dimension_c,profile0_c,profile1_c,profile2_c,profile3_c,profile4_c,profile5_c,profile6_c,profile7_c,
                                      synVelMax_c,synAccMax_c,evenTime_c,setOriginFlag_c,originPos0_c,originPos1_c,originPos2_c,originPos3_c,
                                      originPos4_c, originPos5_c,originPos6_c,originPos7_c)

    ''' 缓存区指令，五维直线插补
      nCrdNum 坐标系号，取值范围：[1,CRDSYS_MAX_COUNT]
      x 插补段 x 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
      y 插补段 y 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
      z 插补段 z 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
      a 插补段 a 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
      b 插补段 b 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
      synVel 插补段的目标合成速度。取值范围：(0,32767)，单位：pulse/ms。
      synAcc 插补段的合成加速度。取值范围：(0,32767)，单位：pulse/(ms*ms)。
      velEnd 插补段的终点速度。取值范围：[0,32767)，单位：pulse/ms。该值只有在没有
      使用前瞻预处理功能时才有意义，否则该值无效。默认为：0
      FifoIndex 插补缓存区号，取值范围：[0,1]，默认为：0
      segNum 用户自定义行号
    '''
    def GALnXYZAB(self, nCrdNum:int, x:int, y:int, z:int, a:int, b:int, synVel:float, synAcc:float,
                  velEnd=0, FifoIndex=0, segNum = 0):
        self.dll.GA_LnXYZAB.argtypes=[ctypes.c_int,ctypes.c_long,ctypes.c_long,ctypes.c_long,ctypes.c_long,ctypes.c_long,
                                      ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_long]
        self.dll.GA_LnXYZAB.restype = ctypes.c_int
        nCrdNum_c = ctypes.c_int(nCrdNum)
        x_c =ctypes.c_long(x)
        y_c=ctypes.c_long(y)
        z_c=ctypes.c_long(z)
        a_c=ctypes.c_long(a)
        b_c=ctypes.c_long(b)
        synVel_c =ctypes.c_double(synVel)
        synAcc_c =ctypes.c_double(synAcc)
        velEnd_c =ctypes.c_double(velEnd)
        FifoIndex_c =ctypes.c_int(FifoIndex)
        segNum_c = ctypes.c_long(segNum)
        return self.dll.GA_LnXYZAB(nCrdNum_c,x_c,y_c,z_c,a_c,b_c,synVel_c,synAcc_c,velEnd_c,FifoIndex_c,segNum_c)

    ''' 清除插补缓存区内的插补数据
        nCrdNum     坐标系编号
        FifoIndex    索引
    '''
    def GACrdClear(self, nCrdNum = 1, fifoIndex = 0):
        self.dll.GA_CrdClear.argtypes = [ctypes.c_short,ctypes.c_short]
        self.dll.GA_CrdClear.restype = ctypes.c_short
        nCrdNum_c = ctypes.c_short(nCrdNum)
        fifoIndex_c = ctypes.c_short(fifoIndex)
        return self.dll.GA_CrdClear(nCrdNum,fifoIndex)

    '''缓存区指令，XY 平面圆弧插补（以终点坐标和圆心位置为输入参数）
        nCrdNum 坐标系号，取值范围：[1,CRDSYS_MAX_COUNT]
        x 圆弧插补 x 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
        y 圆弧插补 y 轴终点坐标值。取值范围：[-1073741823, 1073741823]，单位：pulse。
        xCenter 圆弧插补的圆心 x 方向相对于起点位置的偏移量
        yCenter 圆弧插补的圆心 Y 方向相对于起点位置的偏移量
        circleDir 圆弧的旋转方向 0 顺时针圆弧 1 逆时针圆弧
        synVel 插补段的目标合成速度。取值范围：(0,32767)，单位：pulse/ms。
        synAcc 插补段的合成加速度。取值范围：(0,32767)，单位：pulse/(ms*ms)。
        velEnd 插补段的终点速度。取值范围：[0,32767)，单位：pulse/ms。该值只有在没有
        使用前瞻预处理功能时才有意义，否则该值无效。默认为：0
        FifoIndex 插补缓存区号，取值范围：[0,1]，默认为：0
        segNum 用户自定义行号
    '''
    def GAArcXYC(self, nCrdNum:int, x:int, y:int, xCenter, yCenter,circleDir:int, synVel, synAcc, velEnd=0, FifoIndex=0, segNum = 0):
        self.dll.GA_ArcXYC.argtypes = [ctypes.c_short,ctypes.c_long,ctypes.c_long,ctypes.c_double,ctypes.c_double,ctypes.c_short,
                                       ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_short,ctypes.c_long]
        self.dll.GA_ArcXYC.restype = ctypes.c_int
        nCrdNum_c = ctypes.c_short(nCrdNum)
        x_c = ctypes.c_long(x)
        y_c  = ctypes.c_long(y)
        xCenter_c = ctypes.c_double(xCenter)
        yCenter_c =ctypes.c_double(yCenter)
        circleDir_c = ctypes.c_short(circleDir)
        synVel_c  = ctypes.c_double(synVel)
        synAcc_c = ctypes.c_double(synAcc)
        velEnd_c = ctypes.c_double(velEnd)
        FifoIndex_c = ctypes.c_short(FifoIndex)
        segNum_c = ctypes.c_long(segNum)
        self.dll.GA_ArcXYC(nCrdNum_c,x_c,y_c,xCenter_c,yCenter_c,circleDir_c,synVel_c,synAcc_c,velEnd_c,FifoIndex_c,segNum_c)

    '''启动插补运动
      mask 从 bit0~bit1 按位表示需要启动的坐标系，其中，bit0 对应坐标系 1，bit1 对应坐标系 2；0：不启动该坐标系，1：启动该坐标系。
      option 从 bit0~bit1 按位表示坐标系需要启动的缓存区的编号，其中，bit0 对应坐标系 1，bit1 对应坐标系 2；0：启动坐标系中 FIFO0 的运动，1：启动坐标系中 FIFO1的运动。
      函数返回值含义如下：
         MN，M 代表返回值十位，N 代表返回值个位
         M 代表轴号
         N 代表失败类型
         N=1:轴 M 不在插补模式，无法启动，原因是未建立坐标系或者中途进入其他模式
         N=2:轴 M 报警，无法启动坐标系
         N=3:轴 M 急停，无法启动坐标系
         N=4:轴 M 正软限位触发，无法启动坐标系
         N=5:轴 M 正硬限位触发，无法启动坐标系
         N=6:轴 M 负软限位触发，无法启动坐标系
         N=7:轴 M 负硬限位触发，无法启动坐标系
         N=8:轴 M 跟随误差超限，无法启动坐标系
    '''
    def GACrdStart(self, mask=1, option = 1):
        self.dll.GA_CrdStart.argtypes = [ctypes.c_int,ctypes.c_int]
        self.dll.GA_CrdStart.restype = ctypes.c_int
        mask_c = ctypes.c_int(mask)
        option_c = ctypes.c_int(option)
        return self.dll.GA_CrdStart(mask_c,option_c)

    ''' 读取未完成的插补段段数
      nCrdNum 坐标系号，取值范围：[1,CRDSYS_MAX_COUNT]
      pSegment 读取的剩余插补段的段数
      FifoIndex 插补缓存区号，取值范围：[0,1]，默认为：0
    '''
    def GAGetRemainderSegNum(self, nCrdNum:int, pSegment:int, FifoIndex=0):
        self.dll.GA_GetRemainderSegNum.argtypes= [ctypes.c_int,ctypes.POINTER(ctypes.c_long),ctypes.c_int]
        self.dll.GA_GetRemainderSegNum.restype = ctypes.c_int
        nCrdNum_c = ctypes.c_int(nCrdNum)
        pSegment_c =ctypes.c_long(pSegment)
        FifoIndex_c = ctypes.c_int(FifoIndex)
        return (self.dll.GA_GetRemainderSegNum(nCrdNum_c,pSegment_c,FifoIndex_c),int(pSegment_c.value))

    ''' 修改规划（脉冲）位置，修改时，轴不能处于运动状态
      nAxisNum 轴编号
      lPrfPos 规划(脉冲)位置
    '''
    def GASetPrfPos(self, nAxisNum:int, lPrfPos):
        self.dll.GA_SetPrfPos.argtypes = [ctypes.c_short,ctypes.c_long]
        self.dll.GA_SetPrfPos.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        lPrfPos_c = ctypes.c_long(lPrfPos)
        return self.dll.GA_SetPrfPos(nAxisNum_c,lPrfPos_c)

    ''' 指定轴开始手轮模式
      nAxisNum 轴编号
      nMasterAxisNum 跟随轴号，通常为 9
      lMasterEven 跟随比例系数，可以先设定为 1，然后逐渐调整到合适比例。
      lSlaveEven 跟随比例系数，可以先设定为 1，然后逐渐调整到合适比例。
      nIntervalTime 固定为 0
      dAcc 固定为 0.1
      dDec 固定为 0.1
      dVel 固定为 50
      nStopWaitTime 固定为 0
    '''
    def GAStartHandwheel(self, nAxisNum:int, nMasterAxisNum:int, lMasterEven:int, lSlaveEven:int,nIntervalTime:int,
                          dAcc=0.1, dDec=0.1, dVel=50, nStopWaitTime=0):
        self.dll.GA_StartHandwheel.argtypes = [ctypes.c_short,ctypes.c_int,ctypes.c_long,ctypes.c_long,ctypes.c_int,
                                               ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_int]
        self.dll.GA_StartHandwheel.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        nMasterAxisNum_c= ctypes.c_int(nMasterAxisNum)
        lMasterEven_c= ctypes.c_long(lMasterEven)
        lSlaveEven_c= ctypes.c_long(lSlaveEven)
        nIntervalTime_c= ctypes.c_int(nIntervalTime)
        dAcc_c = ctypes.c_double(dAcc)
        dDec_c = ctypes.c_double(dDec)
        dVel_c = ctypes.c_double(dVel)
        nStopWaitTime_c = ctypes.c_int(nStopWaitTime)
        return self.dll.GA_StartHandwheel(nAxisNum_c,nMasterAxisNum_c,lMasterEven_c,lSlaveEven_c,nIntervalTime_c,dAcc_c,dDec_c,dVel_c,nStopWaitTime_c)

    ''' 指定轴结束手轮模式
      nAxisNum 轴编号
    '''
    def GAEndHandwheel(self,nAxisNum:int):
        self.dll.GA_EndHandwheel.argtypes = [ctypes.c_short]
        self.dll.GA_EndHandwheel.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        return self.dll.GA_EndHandwheel(nAxisNum_c)

    ''' 读取自定义插补段段号
      nCrdNum 坐标系号，取值范围：[1,CRDSYS_MAX_COUNT]
      pSegment 读取的用户自定义的插补段段号
      FifoIndex 插补缓存区号，取值范围：[0,1]，默认为：0
    '''
    def GAGetUserSegNum(self, nCrdNum:int, pSegment:int, FifoIndex=0):
        self.dll.GA_GetUserSegNum.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_long),ctypes.c_int]
        self.dll.GA_GetUserSegNum.restype =ctypes.c_int
        nCrdNum_c = ctypes.c_int(nCrdNum)
        pSegment_c = ctypes.c_long(pSegment)
        FifoIndex_c = ctypes.c_int(FifoIndex)
        return (self.dll.GA_GetUserSegNum(nCrdNum_c,pSegment_c,FifoIndex_c),int(pSegment_c.value))

    ''' 读取轴状态
      nAxisNum 起始轴号
      pSts 32位轴状态字，详细定义参见光盘头文件GAS_N.h的轴状态位定义部分
          轴状态位定义
        define AXIS_STATUS_ESTOP (0x00000001) //急停
        define AXIS_STATUS_SV_ALARM (0x00000002) //驱动器报警标志
        define AXIS_STATUS_POS_SOFT_LIMIT (0x00000004) //正软限位触发标志
        define AXIS_STATUS_NEG_SOFT_LIMIT (0x00000008) //负软位触发标志
        define AXIS_STATUS_FOLLOW_ERR (0x00000010) //规划位置和实际位置的误差过大时置 1
        define AXIS_STATUS_POS_HARD_LIMIT (0x00000020) //正硬限位触发标志
        define AXIS_STATUS_NEG_HARD_LIMIT (0x00000040) //负硬限位触发标志
        define AXIS_STATUS_IO_SMS_STOP (0x00000080) //保留
        define AXIS_STATUS_IO_EMG_STOP (0x00000100) //保留
        define AXIS_STATUS_ENABLE (0x00000200) //电机使能标志
        define AXIS_STATUS_RUNNING (0x00000400) //规划运动标志，规划器运动时置 1
        define AXIS_STATUS_ARRIVE (0x00000800) //电机到位
        define AXIS_STATUS_HOME_RUNNING (0x00001000) //正在回零
        define AXIS_STATUS_HOME_SUCESS (0x00002000) //回零成功
        define AXIS_STATUS_HOME_SWITCH (0x00004000) //零位信号
        define AXIS_STATUS_INDEX (0x00008000) //z 索引信号
        define AXIS_STATUS_GEAR_START (0x00010000) //电子齿轮开始啮合
        define AXIS_STATUS_GEAR_FINISH (0x00020000) //电子齿轮完成啮合
      nCount 读取的轴数，默认为 1次最多可以读取多个轴的状态
      pClock 读取控制器时钟，默认为：NULL，即不用读取控制器时钟
    '''
    def GAGetSts(self , nAxisNum:int, pSts:int, nCount=1, pClock=0):
        self.dll.GA_GetSts.argtypes = [ctypes.c_short,ctypes.POINTER(ctypes.c_long),ctypes.c_int,ctypes.POINTER(ctypes.c_ulong)]
        self.dll.GA_GetSts.restype = ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pSts_c = ctypes.c_long(pSts)
        nCount_c = ctypes.c_int(nCount)
        pClock_c = ctypes.c_ulong(pClock)
        return (self.dll.GA_GetSts(nAxisNum_c,pSts_c,nCount_c,pClock_c),int(pSts_c.value))

    ''' 读取规划位置
        nAxisNum 起始轴号，取值范围：[1,AXIS_MAX_COUNT]
        pValue 规划位置
        nCount 读取的规划轴数，默认为,1次最多可以读取多个轴的运动模式
        pClock 读取控制器时钟，默认为：NULL，即不用读取控制器时钟
    '''
    def GAGetPrfPos(self, nAxisNum:int, pValue, nCount=1,pClock=None):
        self.dll.GA_GetPrfPos.argtypes= [ctypes.c_short,ctypes.POINTER(ctypes.c_double),ctypes.c_short,ctypes.POINTER(ctypes.c_ulong)]
        self.dll.GA_GetPrfPos.restype =  ctypes.c_int
        nAxisNum_c = ctypes.c_short(nAxisNum)
        pValue_c = ctypes.c_double(pValue)
        nCount_c = ctypes.c_short(nCount)
        pClock_c = ctypes.c_ulong(pClock)
        return (self.dll.GA_GetPrfPos(nAxisNum_c, pValue_c, nCount_c, pClock_c), int(pValue_c.value),int(pClock_c.value))




