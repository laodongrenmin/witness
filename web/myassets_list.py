#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/11/19 16:28'


def do(req):
    pass


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 1
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
        # 从Ｓｅｓｓｉｏｎ里面取出用户ＩＤ
        # user_id = int(req.parameters.get('user_id','2'))
        login_name = req.parameters.get('userInfo.login_name', '')
        _user = dbMng.get_user_by_logname(login_name)
        if _user:
            limit = int(req.parameters.get('limit', '1000'))
            offset = int(req.parameters.get('offset', '0'))
            body['assets'] = dbMng.get_myassets_by_user_id(_user.id, limit, offset)
            body['status'] = 0
            body['message'] = 'query success'
        else:
            body['status'] = 1
            body['message'] = 'user ' + login_name + ' not found.'
    else:
        raise Exception('para req is not HttpRequest')
    ymp = json.dumps(body, ensure_ascii=False)
    req.res_body = ymp.encode('UTF-8')
    return True


def do_get(req: HttpRequest):
    return do_post(req)


if __name__ == '__main__':
    exit(0)