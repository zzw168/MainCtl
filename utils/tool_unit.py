import base64
import time


# 图片处理
def str2image_file(img, filename):
    image_str = img[22:]  # 截掉图片无效部分"data:image/jpg;base64,"
    image_str = image_str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open(filename, 'wb')
    image_json.write(image_byte)  # 将图片存到当前文件的fileimage文件中
    image_json.close()


def str2image(img):
    image_str = img[22:]  # 截掉图片无效部分"data:image/jpg;base64,"
    image_str = image_str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    return image_byte


def succeed(msg: str):
    return "<font color='green'>[%s] %s </font>" % (time.strftime("%H:%M:%S", time.localtime()), msg)


def fail(msg: str):
    return "<font color='red'>[%s] %s </font>" % (time.strftime("%H:%M:%S", time.localtime()), msg)


# 检测正负数
def is_natural_num(z):
    try:
        z = float(z)
        return isinstance(z, float)
    except ValueError:
        return False
