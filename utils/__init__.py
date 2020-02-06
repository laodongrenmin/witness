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

__all__ = ['dict2header', 'generate_trace_id', 'my_print']


def dict2header(d):
    header = ''
    for k in d:
        if d[k]:
            header = header + k + ": " + d[k] + '\r\n'
    return header + '\r\n'


def generate_trace_id():
    cookie = str(decimal.Decimal(time.time() * 1000000))
    hl = hashlib.md5()
    hl.update(cookie.encode(encoding='utf-8'))
    return hl.hexdigest()


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


my_print = my_print_2
