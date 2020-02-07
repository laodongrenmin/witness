#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/14/2020 2:22 PM
@Desc   ：准备测试数据
=================================================="""
import web.dto as dto
from request import HttpRequest
from web.dao.db import DB
import os
from web.conf import Conf

__all__ = [
           'get_test_db', 'get_test_img_db',
           'get_test_user_dto', 'get_test_book_assets_dto',
           'get_test_request',
           'get_borrow_reason']


def get_test_user_dto():
    return dto.UserDto(login_name='login_name_0001', name='admin', status='0',
                       memo='ccb_ft', mobile='18999999999')


def get_test_book_assets_dto():
    file_path = os.path.join(os.path.dirname(__file__), r'res\d.jpg')
    f = open(file_path, 'rb')
    try:
        b = f.read()
    finally:
        f.close()

    image = bytearray()
    image[0:] = b'\r\nContent-Disposition: form-data; name="image"; ' \
                b'filename="TT.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'
    image[len(image):] = b
    image[len(image):] = b'\r\n'

    return dto.AssetsDto(code='A8888', user_id=0, user_name='admin',
                         name='图书', category='类别一', memo='很牛的书', image=image)


def get_test_db():
    _db = DB(Conf.db_file_path_rw)
    _db.IS_PRINT_SQL = False
    return _db


def get_test_img_db():
    _db = DB(Conf.db_file_path_img)
    _db.IS_PRINT_SQL = False
    return _db


def get_test_request():
    req = HttpRequest()
    req.my_db = get_test_db()
    req.my_img_db = get_test_img_db()
    paras = req.parameters
    _user = get_test_user_dto()
    # 前端或者前序流程中（比如测试案例）没有上送跟踪号，就生成跟踪号
    paras['trace_id'] = 'generate_trace_id_999999'
    paras['reason'] = 'overtime'
    paras['userInfo'] = dict()
    user_info = paras['userInfo']
    user_info['login_name'] = _user.login_name
    user_info['name'] = _user.name
    user_info['dept_name'] = _user.memo
    user_info['mobile'] = _user.mobile

    _assets = get_test_book_assets_dto()

    paras["code"] = _assets.code
    paras["name"] = _assets.name
    paras["memo"] = _assets.memo
    paras["image"] = _assets.image
    paras['category'] = _assets.category
    return req


def get_borrow_reason():
    return 'overtime'

