#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 10:54 AM
@Desc   ：
=================================================="""
from web.biz.constant import Const
from request import HttpRequest
import web.dto as dto
import json


__all__ = ['get_post_data', 'package_body']


def get_post_data(req: HttpRequest):
    paras = req.parameters
    # 前端或者前序流程中（比如测试案例）没有上送跟踪号，就使用后台跟踪号
    trace_id = paras.get('trace_id', req.trace_id)
    reason = paras.get("reason", None)
    user_info = paras.get('userInfo', None)
    if user_info:
        pid = user_info.get('id', None)
        login_name = user_info.get('login_name', None)
        name = user_info.get('name', None)
        mobile = user_info.get('mobile', None)
        status = user_info.get('status', None)
        depart = user_info.get('dept_name', None)
        org = user_info.get('org', None)
        memo = user_info.get('dept_name', None)
    else:
        pid = paras.get('userInfo.id', None)
        login_name = paras.get('userInfo.login_name', None)
        name = paras.get('userInfo.name', None)
        mobile = paras.get('userInfo.mobile', None)
        status = paras.get('userInfo.status', None)
        depart = paras.get('userInfo.dept_name', None)
        org = paras.get('userInfo.org', None)
        memo = paras.get('userInfo.dept_name', None)

    _user = dto.UserDto(pid=pid, login_name=login_name, name=name, mobile=mobile,
                        status=status, depart=depart, org=org, memo=memo)

    code = paras.get("code", None)
    name = paras.get("name", None)
    memo = paras.get("memo", None)
    image = paras.get("image", None)
    category = paras.get('category', None)
    _assets = dto.AssetsDto(code=code, name=name, memo=memo, image=image, category=category)

    return _user, _assets, reason, trace_id


def package_body(req=None, status: Const.OpStatus = None, op_type: Const.OpType = None, message=None, assets=None):
    body = dict()
    body['status'] = status.value
    body['op_type'] = op_type.value
    body['message'] = message
    body['assets'] = assets
    req.res_body = json.dumps(body, ensure_ascii=False).encode('UTF-8')


