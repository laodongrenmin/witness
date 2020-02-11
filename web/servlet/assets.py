#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 10:55 AM
@Desc   ：
=================================================="""
from request import HttpRequest, ResponseCode
from web.biz.assets import AssetsImpl
from web.servlet import *
from web.biz.constant import Const
import re


def get_image(req: HttpRequest, code):
    b_ret = False
    op_type = Const.OpType.查询
    if code:
        assets_impl = AssetsImpl(_db=req.my_db, _img_db=req.my_img_db)
        code, header, image = assets_impl.get_image(code=code)
        if image:
            content_type = "application/octet-stream"
            if header:
                if type(header) == bytes or type(header) == bytearray:
                    header = header.decode("utf-8")
                tmp = re.findall('Content-Type:.*', header, re.I)
                if tmp:
                    content_type = re.sub('Content-Type:', '', tmp[0], re.I)
            req.res_head['Content-Type'] = content_type
            req.res_body = image
            b_ret = True
        else:
            req.res_command = ResponseCode.NOT_FOUND
            package_body(req=req, status=Const.OpStatus.成功, op_type=op_type,
                         message='没有图像记录或者图像记录格式不对')
    else:
        req.res_command = ResponseCode.BAD_REQUEST
        package_body(req=req, status=Const.OpStatus.失败, op_type=op_type,
                     message='没有上送资产编码')
    return b_ret


def get_assets(req=None, code=None, login_name=None, limit=10, offset=0):
    assets_impl = AssetsImpl(_db=req.my_db, _img_db=req.my_img_db)
    lst, count = assets_impl.get_assets(code=code, login_name=login_name, limit=limit, offset=offset)
    req.res_command = ResponseCode.OK
    op_type = Const.OpType.查询
    d = dict()
    lst_assets = list()
    d['count'] = count
    for assets in lst:
        lst_assets.append(assets.to_html_dict())
    d['assets'] = lst_assets
    if count == 0:
        status = Const.OpStatus.失败
        message = "没有找到 code:{} 或者 login_name:{} 的记录".format(code, login_name)
    else:
        status = Const.OpStatus.成功
        message = "找到 code:{} 或者 login_name:{} 的记录".format(code, login_name)
    package_body(req=req, status=status, op_type=op_type, message=message, assets=d)
    return count != 0


def do_get(req: HttpRequest):
    paras = req.parameters
    action = paras.get('action', None)
    limit = paras.get('limit', 10)
    offset = paras.get('offset', 0)
    code = paras.get('code', None)
    login_name = paras.get('userInfo.login_name', None)
    if not login_name:
        user_info = paras.get('userInfo')
        if user_info:
            login_name = user_info.get('login_name', None)
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
        if action == 'get_image':
            b_ret = get_image(req=req, code=code)
        elif action == 'get_assets':
            b_ret = get_assets(req=req, code=code, login_name=login_name, limit=limit, offset=offset)
        else:
            req.res_command = ResponseCode.NOT_IMPLEMENTED
            package_body(req=req, status=Const.OpStatus.失败, op_type=Const.OpType.查询, message="不支持的动作")
            b_ret = False
    else:
        raise Exception('para req is not HttpRequest')
    return b_ret


def do_post(req: HttpRequest):
    assets_impl = AssetsImpl(_db=req.my_db, _img_db=req.my_img_db)
    if isinstance(req, HttpRequest):
        pass
    else:
        raise Exception('para req is not HttpRequest')
    return True



