#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 4:18 PM
@Desc   ：
=================================================="""
import time, hashlib, decimal
import os
import sys
# 如果没有把路径添加到系统中，就需要在导入库之前把搜索路径添加上
# vips_home = r'D:\software\vips-dev-8.7\bin'
# os.environ['PATH'] = vips_home + ';' + os.environ['PATH']
import pyvips

__all__ = ['dict2header', 'generate_trace_id', 'get_print_string',
           'read_bytes_from_file', 'write_bytes_to_file',
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
    cookie = str(decimal.Decimal(time.time() * 1000000))
    hl = hashlib.md5()
    hl.update(cookie.encode(encoding='utf-8'))
    return hl.hexdigest()


def thumbnail(buf, size=128, q=75):
    thumb = pyvips.Image.thumbnail_buffer(buf, 128)
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


def get_print_string(msgs, limit_len=512):
    if msgs is None:
        return None
    if limit_len < 256:
        limit_len = 256
    if isinstance(msgs, tuple):
        lst = list()
        for msg in msgs:
            if msg and (type(msg) == bytes or type(msg) == bytearray) and len(msg) > limit_len:
                lst.append(['too long, len is {}' .format(len(msg),), msg[:128], msg[-128:]])
            else:
                lst.append(msg)
        return tuple(lst)
    elif isinstance(msgs, dict):
        d = dict()
        for key, value in msgs.items():
            if value and (type(value) == bytes or type(value) == bytearray) and len(value) > limit_len:
                value = ['too long, len is {}' .format(len(value),), value[:128], value[-128:]]
            d[key] = value
        return d
    return msgs


my_print = my_print_2
