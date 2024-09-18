def succeed(msg: str):
    return "<font color='green'> %s </font>" % (msg,)


def fail(msg: str):
    return "<font color='red'> %s </font>" % (msg,)


# 检测正负数
def is_natural_num(z):
    try:
        z = int(z)
        return isinstance(z, int)
    except ValueError:
        return False
