#!/user/bin/python3
# -*- codeing:utf-8 -*-
# Time : 2018/8/6 17:13
# Author : LiuShiHua
# Desc : 时间转换工具

import time

formatstr_ymdHMS = "%Y-%m-%d %H:%M:%S"
formatstr_ymdHM = "%Y-%m-%d %H:%M"
formatstr_ymd = "%Y-%m-%d"


# 返回样式 2018-05-06
# 传入样式 2018-05-06 12:22:23 或者 151512443.5656 或者 151512443
# time.localtime(timeRes) 获取float时间元祖
# time.strptime(timeRes, formatstr_ymdHMS) 获取“指定时间格式”的时间元祖
# time.strftime(formatstr_ymdHMS, 时间元祖) 时间元祖转“指定格式”的字符串
# 转换失败则返回原始值
def getDateStr_ymd(timeRes):
    try:
        if isinstance(timeRes, str):  # 传入的是str
            return time.strftime(formatstr_ymd, time.strptime(timeRes, formatstr_ymdHMS))
        elif isinstance(timeRes, float):  # 传入的是float
            return time.strftime(formatstr_ymd, time.localtime(timeRes))
        elif isinstance(timeRes, int):  # 传入的是float
            return time.strftime(formatstr_ymd, time.localtime(float(timeRes)))
        else:
            return timeRes;
    except ValueError:
        return timeRes;


# 返回样式 2018-05-06 12:22
# 传入样式 2018-05-06 12:22:23 或者 151512443.5656 或者 151512443
# 转换失败则返回原始值
def getDateStr_ymdHM(timeRes):
    try:
        if isinstance(timeRes, str):  # 传入的是str
            return time.strftime(formatstr_ymdHM, time.strptime(timeRes, formatstr_ymdHMS))
        elif isinstance(timeRes, float):  # 传入的是float
            return time.strftime(formatstr_ymdHM, time.localtime(timeRes))
        elif isinstance(timeRes, int):  # 传入的是float
            return time.strftime(formatstr_ymdHM, time.localtime(float(timeRes)))
        else:
            return timeRes;
    except ValueError:
        return timeRes;


# 返回样式 2018-05-06 12:22
# 传入样式 2018-05-06 或者 151512443.5656 或者 151512443
# 转换失败则返回原始值
def getDateStr_ymdHMS(timeRes):
    try:
        if isinstance(timeRes, str):  # 传入的是str
            return time.strftime(formatstr_ymdHMS, time.strptime(timeRes, formatstr_ymd))
        elif isinstance(timeRes, float):  # 传入的是float
            return time.strftime(formatstr_ymdHMS, time.localtime(timeRes))
        elif isinstance(timeRes, int):  # 传入的是float
            return time.strftime(formatstr_ymdHMS, time.localtime(float(timeRes)))
        else:
            return timeRes;
    except ValueError:
        return timeRes;


# 返回 时间戳 1512356413.0012
# 输入 2012-12-22 13:20:11
# 输入 2012-12-22
# 输入其他格式数据 返回0
def getDateMillis(timeRes):
    try:
        if ":" in timeRes:
            return time.mktime(time.strptime(timeRes, formatstr_ymdHMS))
        else:
            return time.mktime(time.strptime(timeRes, formatstr_ymd))
    except (ValueError,TypeError):
        return timeRes

import Image
from io import BytesIO

def thumbnail(filePath):
    im = Image.open(filePath)
    im.thumbnail((40,40))
    print(im.format,im.size,im.mode)
    fp = BytesIO()
    im.save(fp, 'JPEG')
    buf = fp.getvalue()  #87505553
    print(buf)

thumbnail('test.jpg')



