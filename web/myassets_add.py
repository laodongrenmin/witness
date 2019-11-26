#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/11/20 10:42'


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
        if not login_name:
            login_name = req.parameters.get('userInfo')
            if login_name:
                login_name = login_name.get('login_name')
        assets_code = req.parameters.get('code','')
        _assets = dbMng.get_assets_bycode(assets_code)
        _user = dbMng.get_user_by_logname(login_name)
        if _user and _assets:
            body['assets'] = dbMng.insert_myassets(_user, _assets)
            body['status'] = 0
            body['message'] = 'insert my assets success.'
        else:
            body['status'] = 1
            body['message'] = 'user and assets can not be found.'
    else:
        raise Exception('para req is not HttpRequest')
    ymp = json.dumps(body, ensure_ascii=False)
    req.res_body = ymp.encode('UTF-8')
    return True


def do_get(req: HttpRequest):
    return do_post(req)


if __name__ == '__main__':
    exit(0)