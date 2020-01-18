#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 10:54 AM
@Desc   ：
=================================================="""
from web.biz.constant import Const
import json


__all__ = ['package_body']


def package_body(req=None, status: Const.OpStatus=None, op_type: Const.OpType=None, message=None, assets=None):
    body = dict()
    body['status'] = status.value
    body['op_type'] = op_type.value
    body['message'] = message
    body['assets'] = assets
    req.res_body = json.dumps(body, ensure_ascii=False).encode('UTF-8')


