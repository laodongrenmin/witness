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
        code = req.parameters.get('code', '')
        limit = int(req.parameters.get('limit', '1000'))
        offset = int(req.parameters.get('offset', '0'))

        body['status'] = 0
        body['message'] = 'query success'
        if action == '16':    # 根据物品编码获取归还的历史信息
            body['data'] = dbMng.get_reback_by_code(code, limit, offset)
        elif action == '8':    # 根据物品编码获取当前借出的信息
            body['data'] = dbMng.get_borrow_by_code(code)
        elif action == '4':   # OpType.归还
            body['data'] = dbMng.get_my_reback(login_name, limit, offset)
        elif action == '2':  # OpType.借出
            body['data'] = dbMng.get_my_borrow(login_name, limit, offset)
        elif action == 'all':  # 全部
            body['data'] = dbMng.get_my_log(login_name, limit, offset)
        else:
            body['status'] = 1
            body['message'] = 'action not found.'
    else:
        raise Exception('para req is not HttpRequest')
    ymp = json.dumps(body, ensure_ascii=False)
    req.res_body = ymp.encode('UTF-8')
    return True


def do_get(req: HttpRequest):
    return do_post(req)