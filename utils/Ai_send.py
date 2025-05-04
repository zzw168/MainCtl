import requests
import time
import os


# 读取比赛数据文件
def read_race_data(filename):
    if not os.path.exists(filename):
        print(f"错误：文件 {filename} 不存在")
        return []

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 移除每行末尾的换行符
    lines = [line.strip() for line in lines if line.strip()]
    return lines


# 发送数据到服务器
def send_data(data, url ="http://192.168.0.240:8082"):
    try:
        response = requests.post(url, data=data.encode('utf-8'))
        if response.status_code == 200:
            print(f"成功发送数据: {data[:50]}...")
            return response.text
        else:
            print(f"发送失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"发送异常: {e}")
        return None


# 主函数
def main():
    # 读取比赛数据
    race_data = read_race_data("race.txt")

    if not race_data:
        print("没有读取到比赛数据，程序退出")
        return

    print(f"共读取到 {len(race_data)} 条比赛数据")

    # 发送开始标记
    print("发送比赛开始标记...")
    result = send_data("START", 'http://192.168.0.240:8082')
    print(f"服务器响应: {result}")
    time.sleep(1)  # 等待服务器准备

    # 发送数据
    for i, data in enumerate(race_data):
        print(f"发送第 {i + 1}/{len(race_data)} 条数据")
        send_data(data, 'http://192.168.0.240:8082')

        # 延迟0.2秒
        time.sleep(2)

    # 发送结束标记
    print("发送比赛结束标记...")
    time.sleep(3)
    result = send_data("STOP", 'http://192.168.0.240:8082')
    print(f"服务器响应: {result}")

    print("所有数据发送完成")


if __name__ == "__main__":
    main()