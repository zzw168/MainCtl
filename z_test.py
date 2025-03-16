import obsws_python as obs

# 连接到 OBS WebSocket
client = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中

# 刷新 "浏览器来源"（Browser Source）
client.press_input_properties_button("浏览器", "refreshnocache")

# 断开连接
client.disconnect()

print("已刷新浏览器来源")
