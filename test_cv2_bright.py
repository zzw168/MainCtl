import cv2

obs_cap = cv2.VideoCapture(0)  # 打开摄像头
brightness = obs_cap.get(cv2.CAP_PROP_BRIGHTNESS)  # 获取当前亮度
print(f"当前亮度: {brightness}")

success = obs_cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
print(f"设置亮度是否成功: {success}")

# for i in [0, 0.5, 0.75, 1, 100, 255]:
#     success = obs_cap.set(cv2.CAP_PROP_BRIGHTNESS, i)
#     current = obs_cap.get(cv2.CAP_PROP_BRIGHTNESS)
#     print(f"尝试设置亮度为 {i}, 实际亮度: {current}, 设置成功: {success}")