#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest, ResponseCode, AttachFile
# from web.DBMng import dbMng, AssetsDto, UserDto
from web.biz.assets import AssetsImpl


__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/7/23 17:51'


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 2
    req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
    if isinstance(req, HttpRequest):
        # code, user_id, user_name, name, memo, image, create_time
        paras = req.parameters
        code = paras.get('code', None)
        reason = paras.get('reason', None)
        login_name = paras['userInfo'].get('login_name', None)
        name = paras['userInfo'].get('name', None)
        memo = paras['userInfo'].get('dept_name', '建信金科/武汉事业群')
        mobile = paras['userInfo'].get('mobile', None)
        if code:
            assets_impl = AssetsImpl()
            _assets, op_type = assets_impl.do_biz(code=code, login_name=login_name, name=name, memo=memo, mobile=mobile)
            if _assets:
                if op_type:
                    body['status'] = 0
                    body['op_type'] = op_type.name
                    body['message'] = '已经成功实现了 ' + op_type.name + ' 动作'
                    body['assets'] = _assets.to_dict()
                else:
                    body['message'] = '出现了未知错误'
                    body['assets'] = _assets.to_dict()
            else:
                body['status'] = 1
                body["message"] = "没有找到资产编码为: %s 的资产" % code
        else:
            body['status'] = 1
            body["message"] = "没有上送资产编码"
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
                assets_impl = AssetsImpl()
                content_type, content = assets_impl.get_image(code=code)
                if content_type and content:
                    req.res_head['Content-Type'] = content_type
                    req.res_body = content
                else:
                    req.res_command = ResponseCode.NOT_FOUND
                    req.res_head['Content-Type'] = 'text/html; charset=utf-8'
                    req.res_body = "没有图像记录或者图像类型".encode('utf-8')
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
    # return True