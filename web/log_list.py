#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng, AssetsDto
import os

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/8/23 15:00'


def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 1
    body['message'] = 'unknown error.'
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
        action = req.parameters.get('action','all')

        # 从Ｓｅｓｓｉｏｎ里面取出用户ＩＤ
        login_name = req.parameters.get('userInfo.login_name', '')
        limit = int(req.parameters.get('limit', '1000'))
        offset = int(req.parameters.get('offset', '0'))

        if action == '4':   # OpType.归还
            body['reback'] = dbMng.get_my_reback(login_name, limit, offset)
            body['status'] = 0
            body['message'] = 'query success'
        elif action == '2':  # OpType.借出
            body['borrow'] = dbMng.get_my_borrow(login_name, limit, offset)
            body['status'] = 0
            body['message'] = 'query success'
        elif action == 'all':  # 全部
            body['borrow'] = dbMng.get_my_log(login_name, limit, offset)
            body['status'] = 0
            body['message'] = 'query success'
        else:
            body['message'] = 'action not found.'
    else:
        raise Exception('para req is not HttpRequest')
    ymp = json.dumps(body, ensure_ascii=False)
    req.res_body = ymp.encode('UTF-8')
    return True


def do_get(req: HttpRequest):
    return do_post(req)