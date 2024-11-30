import time
import requests

url = 'http://127.0.0.1:8080'

run_toggle = 1

while True:

    # 进行打开关闭图像识别操作
    form_data = {
        'requestType': 'set_run_toggle',  #设置是否打开图像识别
        'run_toggle': 1, #设置1 打开图像识别 0关闭图像识别
    }


    form_data = {
        'requestType': 'get_run_toggle',  #获取现在图像识别是否打开操作   返回1 代表打开 0代表关闭
    }




    if run_toggle == 1:
        run_toggle = 0
    else:
        run_toggle = 1

    # 发送 POST 请求并传递表单数据
    print(run_toggle)



    form_data = {
        'requestType': 'saveImg',  #类型是保存图片
        'saveImgNum': '1,2,3,4,5,6,7,8,9,11,12',# 摄像头编号
        'saveImgPath': './testimg3',#图片保存位置
        'saveImgRun': '1',# 1开始保存图片  0停止保存
        'saveBackground': '0',# 1开始保存背景图不判断是否有球  0停止保存
        'save_ball_num': '1,2', # 需要只保存某一类球  英文逗号分割球索引数字
    }

    response = requests.post(url, data=form_data, timeout=5)

    # 检查响应状态码
    if response.status_code == 200:
        print('请求成功！')
        print('响应内容：', response.text)
    else:
        print('请求失败，状态码：', response.status_code)


    time.sleep(3)














