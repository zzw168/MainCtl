from PIL import Image

# 打开 PNG 图片
png_path = "diary.png"  # 替换为你的 PNG 文件路径
ico_path = "diary.ico"  # 输出 ICO 文件路径

# 读取并转换
img = Image.open(png_path)

# 保存为 ICO，支持多尺寸
# img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
img.save(ico_path, format='ICO', sizes=[(256, 256)])

print(f"转换完成：{ico_path}")
