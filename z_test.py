import time

import requests

import websocket
import json
import time

# WebSocket 连接配置
OBS_WEBSOCKET_URL = "ws://localhost:4455"  # 根据你的设置调整
PASSWORD = "D9AQaWOH0b8Tu0Xn"  # 如果未设置密码，可以留空


# 重新加载浏览器源的函数
def reload_browser_source(source_name):
    # 创建 WebSocket 连接
    ws = websocket.create_connection(OBS_WEBSOCKET_URL)

    # 认证请求
    auth_request = json.dumps({
        "op": 1,
        "d": {"rpcVersion": 1, "authentication": PASSWORD}
    })
    ws.send(auth_request)
    time.sleep(1)  # 等待认证完成

    # 重载浏览器源
    reload_request = json.dumps({
        "op": 6,
        "d": {
            "requestType": "BroadcastCustomEvent",
            "requestId": "reload-source",
            "requestData": {
                "sourceName": source_name
            }
        }
    })
    ws.send(reload_request)
    ws.close()


if __name__ == "__main__":
    # 你在 OBS 中的浏览器源名称
    reload_browser_source("浏览器")


def test1():
    # res = requests.get(url="http://127.0.0.1:8899/start")
    res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
    # res = requests.get(url="http://127.0.0.1:8899/period?term=开始")
    print(res)


def test2():
    t = time.time()
    ranking_time_start = t - 386
    minute = int((t - ranking_time_start) / 60)
    Second = int((t - ranking_time_start) % 60)
    print('%s"%s' % (minute, Second))

#
# if __name__ == '__main__':
#     test2()
