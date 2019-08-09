#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest, ResponseCode, AttachFile
from web.DBMng import dbMng, AssetsDto
import re

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/7/23 17:51'


def do(req):
    pass


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body["result"] = "failed"
    req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
    if isinstance(req, HttpRequest):
        # code, user_id, user_name, name, memo, image, create_time
        paras = req.parameters
        code = paras.get('code', None)
        login_name = paras['userInfo'].get('login_name', None)
        # print('dbMng id:%d' % id(dbMng))
        if code:
            _assets = dbMng.get_assets_bycode(code=code)
            if _assets:
                _user = dbMng.get_user_by_logname(login_name)
                _assets = AssetsDto(code=code)
                op_type = dbMng.do_biz(_user, _assets)
                _assets = dbMng.get_assets_bycode(code)
                if _assets:
                    body["result"] = "success"
                    body['op_type'] = op_type.name
                    body['reason'] = '已经成功实现了 ' + op_type.name + ' 动作'
                    body['assets'] = _assets.to_dict()
            body["code"] = code
        else:
            body["reason"] = "没有上送资产编码"
        req.res_body = json.dumps(body, ensure_ascii=False).encode('UTF-8')
    else:
        raise Exception('para req is not HttpRequest')
    return True


def do_get(req: HttpRequest):
    paras = req.parameters
    action = paras.get('action', None)
    code = paras.get('code', None)
    if isinstance(req, HttpRequest):
        if action == 'get_image':
            if code:
                _assets = dbMng.get_assets_bycode(code=code)
                if _assets and _assets.image:
                    head, content = _assets.image.split(b'\r\n\r\n', 2)
                    file = AttachFile(head.decode('utf-8'), content)
                    req.res_head['Content-Type'] = file.content_type
                    req.res_body = file.content
                else:
                    req.res_command = ResponseCode.NOT_FOUND
                    req.res_head['Content-Type'] = 'text/html; charset=utf-8'
                    req.res_body = "没有图像记录".encode('utf-8')
            else:
                req.res_command = ResponseCode.BAD_REQUEST
                req.res_head['Content-Type'] = 'text/html; charset=utf-8'
                req.res_body = "没有上送资产编码".encode('utf-8')
        else:
            req.res_command = ResponseCode.NOT_IMPLEMENTED
            req.res_head['Content-Type'] = 'text/html; charset=utf-8'
            req.res_body = "不支持的动作".encode('utf-8')
    else:
        raise Exception('para req is not HttpRequest')
    return True


    # req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
    # req.res_body = '{"result":"failed","reason":"get method is developing"}'.encode('UTF-8')
    return True


if __name__ == '__main__':
    exit(0)