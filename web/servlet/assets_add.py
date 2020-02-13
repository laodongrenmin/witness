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
import time


def do_get(req: HttpRequest):
    b_ret = False
    if isinstance(req, HttpRequest):
        pass
    else:
        raise Exception('para req is not HttpRequest')
    return b_ret


def do_post(req: HttpRequest):
    assets_impl = AssetsImpl(_db=req.my_db, _img_db=req.my_img_db)
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
        _user, _assets, reason, trace_id = get_post_data(req)
        _user = assets_impl.get_or_create_user(_user, trace_id)  # 如果session有了，应该先从session里面获取

        _assets.create_time, _assets.op_time = time.time(), time.time()
        _assets.status = Const.AssetsStatus.未借出.value

        _assets.user_id, _assets.user_name = _user.id, _user.name
        _assets.dst_user_id, _assets.dst_user_name, _assets.dst_user_mobile = _user.id, _user.name, _user.mobile

        status, _assets, op_type, message = assets_impl.create_assets(_assets=_assets, _user=_user, trace_id=trace_id)
        package_body(req=req, status=status, op_type=op_type, message=message, assets=_assets.to_html_dict())
    else:
        raise Exception('para req is not HttpRequest')
    return True



