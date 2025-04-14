# import obsws_python as obs
#
# # 连接到 OBS WebSocket
# client = obs.ReqClient()  # 请求 链接配置在 config.toml 文件中
#
# # 刷新 "浏览器来源"（Browser Source）
# client.press_input_properties_button("浏览器", "refreshnocache")
#
# # 断开连接
# client.disconnect()
#
# print("已刷新浏览器来源")

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

x = np.array([0, 1, 2, 3])
y = np.array([0, 1, 4, 9])

# f = interp1d(x, y, kind='next')  # 三次样条插值
# f = interp1d(x, y, kind='previous')  # 三次样条插值
# f = interp1d(x, y, kind='nearest')  # 三次样条插值
f = interp1d(x, y, kind='cubic')  # 三次样条插值
# f = interp1d(x, y, kind='linear')  # 线性插值
# f = interp1d(x, y, kind='quadratic')  # 二次插值

x_new = np.linspace(0, 3, 100)
y_new = f(x_new)

plt.plot(x, y, 'o', label='aaa')
plt.plot(x_new, y_new, '-', label='bbb')
plt.legend()
plt.show()

