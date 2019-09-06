#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng, AssetsDto
import os

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/7/24 07:51'


def do(req):
    pass


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 1
    if isinstance(req, HttpRequest):
        # print('[%d] dbMng id:%d' % (os.getpid(), id(dbMng)))
        # Resource interpreted as Document but transferred with MIME type application/json
        # req.res_head['Content-Type'] = 'application/json; charset=UTF-8'

        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'

        # str_body = '''
        #        <!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><title>资产列表页面</title></head><body><table>%s</table></body></html>
        #        '''

        # 从Ｓｅｓｓｉｏｎ里面取出用户ＩＤ
        # user_id = int(req.parameters.get('user_id','2'))
        login_name = req.parameters.get('userInfo.login_name', '')
        _user = dbMng.get_user_by_logname(login_name)
        if _user:
            limit = int(req.parameters.get('limit', '1000'))
            offset = int(req.parameters.get('offset', '0'))
            body['status'] = 0
            body['message'] = 'query success'
            body['assets'] = dbMng.get_assets_by_user_id(_user.id, limit, offset)
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