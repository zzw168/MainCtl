import base64
import os

import requests


def send_detect_picture():
    track_file = 'E:/saidao/image/rtsp_0.jpg'
    recognition_addr = "http://127.0.0.1:6066"  # 终点识别主机网址
    with open(track_file, 'rb') as file:
        img = base64.b64encode(file.read()).decode('ascii')
    form_data = {
        'CameraType': 'monitor',
        'img': str(img),
        'sort': '0',  # 排序方向: 0:→ , 1:←, 10:↑, 11:↓
    }
    try:
        res = requests.post(url=recognition_addr, data=form_data, timeout=5)
        r_list = eval(res.text)  # 返回 [图片字节码，排名列表，截图标志]
        r_img = r_list[0]
        if os.path.exists('E:/saidao/image'):
            image_json = open('%s/rtsp_%s_end.jpg' % ('E:/saidao/image', '0'), 'wb')
            image_json.write(r_img)  # 将图片存到当前文件的fileimage文件中
            image_json.close()
    except:
        print('终点识别服务没有开启！')


if __name__ == '__main__':
    send_detect_picture()
