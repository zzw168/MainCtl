import re

import requests

# 给定的 RTSP URL
rtsp_url = "rtsp://admin:123456@192.168.0.29:554/Streaming/Channels/101"

# 使用正则表达式匹配 IP 地址
ip_address = 'http://%s'%re.search(r'(\d+\.\d+\.\d+\.\d+)', rtsp_url).group(0)
res = requests.get(ip_address)

print(res.status_code)  # 输出: 192.168.0.2
