#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng, AssetsDto
import os

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/9/5 15:08'


def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 1
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
        # 从Ｓｅｓｓｉｏｎ里面取出用户ＩＤ
        login_name = req.parameters.get('userInfo.login_name', '')
        limit = int(req.parameters.get('limit', '1000'))
        offset = int(req.parameters.get('offset', '0'))
        body['status'] = 0
        body['message'] = 'query success'
        body['logs'] = dbMng.get_note_by_login_name(login_name, limit, offset)
    else:
        raise Exception('para req is not HttpRequest')
    ymp = json.dumps(body, ensure_ascii=False)
    req.res_body = ymp.encode('UTF-8')
    return True


def do_get(req: HttpRequest):
    return do_post(req)