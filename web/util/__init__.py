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


__all__ = ['generate_trace_id']


def generate_trace_id():
    cookie = str(decimal.Decimal(time.time() * 1000000))
    hl = hashlib.md5()
    hl.update(cookie.encode(encoding='utf-8'))
    return hl.hexdigest()
