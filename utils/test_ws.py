import websocket
import json
import time
import threading

# WebSocket 服务器地址
WS_URL = "wss://ws.kaj789.com/live?token=L8yUwg1wljco3j57u59XdkGKalrK0NtTMX1ok8fSCSYBVj5Vdu"

# 线程关闭标志
stop_event = threading.Event()

def on_message(ws, message):
    print(f"收到消息: {message}")

def on_error(ws, error):
    print(f"发生错误: {error}")

def on_close(ws, close_status_code, close_msg):
    print("连接已关闭")

def on_open(ws):
    """连接成功后，持续发送数据"""
    def run():
        while not stop_event.is_set():  # 监测是否需要退出
            try:
                data = {"message": "Hello, server!"}
                ws.send(json.dumps(data))
                print(f"已发送数据: {data}")
                time.sleep(2)  # 每 2 秒发送一次
            except Exception as e:
                print(f"发送数据时出错: {e}")
                break  # 退出循环，触发 on_close

    threading.Thread(target=run, daemon=True).start()

def connect_with_retries():
    """创建 WebSocket 连接，并在断线时自动重连"""
    while not stop_event.is_set():
        try:
            ws = websocket.WebSocketApp(
                WS_URL,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open

            ws.run_forever()  # 运行 WebSocket 连接
        except Exception as e:
            print(f"WebSocket 连接失败: {e}")

        if stop_event.is_set():
            break

        print("连接断开，5 秒后重试...")
        time.sleep(5)

# 启动 WebSocket 线程
thread = threading.Thread(target=connect_with_retries, daemon=True)
thread.start()

# 主线程等待用户输入 `exit` 关闭 WebSocket
while True:
    user_input = input("输入 'exit' 关闭 WebSocket: ").strip()
    if user_input.lower() == "exit":
        print("正在关闭 WebSocket 连接...")
        stop_event.set()  # 让线程退出
        break  # 退出主线程

print("WebSocket 已关闭。")
