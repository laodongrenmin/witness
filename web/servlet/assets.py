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
import utils
import web.dto as dto


def get_image(req, code):
    b_ret = False
    op_type = Const.OpType.查询
    if code:
        assets_impl = AssetsImpl()
        content_type, content = assets_impl.get_image(code=code)
        if content_type and content:
            req.res_head['Content-Type'] = content_type
            req.res_body = content
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


def get_assets(req=None, code=None):
    assets_impl = AssetsImpl()
    assets = assets_impl.get_assets_by_code(code=code)
    req.res_command = ResponseCode.OK
    op_type = Const.OpType.查询
    if assets:
        status = Const.OpStatus.成功
        message = "找到 %s 的记录" % assets.code
        package_body(req=req, status=status, op_type=op_type, message=message, assets=assets.to_html_dict())
        return True
    else:
        status = Const.OpStatus.失败
        message = "没有找到 %s 的记录" % code
        package_body(req=req, status=status, op_type=op_type, message=message)
    return False


def do_get(req: HttpRequest):
    paras = req.parameters
    action = paras.get('action', None)
    code = paras.get('code', None)
    b_ret = False
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
        if action == 'get_image':
            b_ret = get_image(req=req, code=code)
        elif action == 'get_assets':
            b_ret = get_assets(req=req, code=code)
        else:
            req.res_command = ResponseCode.NOT_IMPLEMENTED
            package_body(req=req, status=Const.OpStatus.失败, op_type=Const.OpType.查询, message="不支持的动作")
    else:
        raise Exception('para req is not HttpRequest')
    return b_ret


def get_post_data(req: HttpRequest):
    paras = req.parameters
    # 前端或者前序流程中（比如测试案例）没有上送跟踪号，就生成跟踪号
    trace_id = paras.get('trace_id', utils.generate_trace_id())
    reason = paras.get("reason", None)
    login_name = paras['userInfo'].get('login_name', None)
    name = paras['userInfo'].get('name', None)
    memo = paras['userInfo'].get('dept_name', '建信金科/武汉事业群')
    mobile = paras['userInfo'].get('mobile', None)
    _user = dto.UserDto(login_name=login_name, name=name, memo=memo, mobile=mobile)

    code = paras.get("code", None)
    name = paras.get("name", None)
    memo = paras.get("memo", None)
    image = paras.get("image", None)
    category = paras.get('category', None)
    _assets = dto.AssetsDto(code=code, name=name, memo=memo, image=image, category=category)
    return _user, _assets, reason, trace_id


def do_post(req: HttpRequest):
    assets_impl = AssetsImpl()
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
        _user, _assets, reason, trace_id = get_post_data(req)
        status, _assets, op_type, message = assets_impl.do_biz(_assets=_assets, _user=_user,
                                                               assets_reason=reason, trace_id=trace_id)
        package_body(req=req, status=status, op_type=op_type, message=message)
    else:
        raise Exception('para req is not HttpRequest')
    return True
