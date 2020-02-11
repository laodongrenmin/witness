#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 4:18 PM
@Desc   ：
=================================================="""
import time, hashlib, decimal, random
import os
import sys
# 如果没有把路径添加到系统中，就需要在导入库之前把搜索路径添加上
# vips_home = r'D:\software\vips-dev-8.7\bin'
# os.environ['PATH'] = vips_home + ';' + os.environ['PATH']
import pyvips

__all__ = ['dict2header', 'generate_trace_id', 'get_print_string',
           'read_bytes_from_file', 'write_bytes_to_file', 'write_to_file',
           'thumbnail',
           'my_print']


def dict2header(d):
    """
    封装字典为Head头
    :param d:
    :return:
    """
    header = ''
    for k in d:
        if d[k]:
            header = header + k + ": " + d[k] + '\r\n'
    return header + '\r\n'


def generate_trace_id():
    """
    生成跟踪号，也用于sessionID
    :return:
    """
    cookie = str(decimal.Decimal(time.time() * 1000000 + random.randint(1, 10000)))
    hl = hashlib.md5()
    hl.update(cookie.encode(encoding='utf-8'))
    return hl.hexdigest()


def thumbnail(buf, size=128, q=75):
    thumb = pyvips.Image.thumbnail_buffer(buf, size)
    data = thumb.write_to_buffer('.jpg[optimize_coding,strip]', Q=q)
    return data


def read_bytes_from_file(file_path):
    """
    小文件读
    :param file_path:
    :return:
    """
    f = open(file_path, 'rb')
    try:
        b = f.read()
    finally:
        f.close()
    return b


def write_bytes_to_file(file_path, buf):
    """
    小文件写
    :param file_path:
    :param buf:
    :return:
    """
    f = open(file_path, 'wb')
    try:
        f.write(buf)
    finally:
        f.close()


def write_to_file(file_path, *args):
    with open(file_path, "a+b") as f:
        for arg in args:
            for a in arg:
                if type(a) == bytearray or type(a) == bytes:
                    f.write(a)
                else:
                    f.write("{}".format(a).encode("utf-8"))


def my_print_1(str_log):
    pid = os.getpid()
    record_time = time.strftime("%m-%d %H:%M:%S", time.localtime())
    sz_log = "[{0}] {1} {2}".format(pid, record_time, str_log)
    print(sz_log)


def my_print_2(str_log):
    pid = os.getpid()
    record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    frame = sys._getframe()
    file_name = os.path.basename(frame.f_back.f_code.co_filename)
    fun_name = frame.f_back.f_code.co_name
    line_no = frame.f_back.f_lineno
    sz_log = "[{0}] {1} [{2},{3},{4}] {5}".format(pid, record_time, file_name, fun_name, line_no, str_log)
    print(sz_log)


LIMIT_LEN = 2048


def get_print_string(msgs, limit_len=256):
    """
    截取打印字符，避免太长输出打印console太多内容，看不起其他的内容
    :param msgs: 想输出打印的变量
    :param limit_len: 最大想截取的长度，最大不会超过2048
    :return: 截取后的可打印内容
    """

    if limit_len < LIMIT_LEN:
        limit_len = LIMIT_LEN
    if msgs is None:
        ret = None
    elif (type(msgs) == bytes or type(msgs) == bytearray) and len(msgs) > limit_len:
        ret = ['too long, len is {}'.format(len(msgs),), msgs[:LIMIT_LEN/2], msgs[-LIMIT_LEN/2:]]
    elif isinstance(msgs, tuple):
        lst = list()
        for msg in msgs:
            if (type(msg) == bytes or type(msg) == bytearray) and len(msg) > limit_len:
                lst.append(['too long, len is {}' .format(len(msg),), msg[:128], msg[-128:]])
            else:
                lst.append(msg)
        ret = tuple(lst)
    elif isinstance(msgs, dict):
        d = dict()
        for key, value in msgs.items():
            if (type(value) == bytes or type(value) == bytearray) and len(value) > limit_len:
                value = ['too long, len is {}' .format(len(value),), value[:128], value[-128:]]
            d[key] = value
        ret = d
    else:
        ret = msgs
    return ret


my_print = my_print_2
