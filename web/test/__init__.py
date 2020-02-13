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
import time
from web.conf import Conf
from utils import *
import sqlite3

__all__ = [
           'get_test_db', 'get_test_img_db', 'get_trace_id',
           'get_test_user_dto', 'get_test_book_assets_dto',
           'get_test_request',
           'get_borrow_reason', 'get_return_reason', 'show_db', 'show_table_content', 'show_table_desc']


def get_test_user_dto():
    return dto.UserDto(pid=1, login_name='login_name_0001', name='admin', mobile="18995533533",
                       status=0, depart='建信金科/武汉事业群/架构服务团队', org='0000100001', memo='测试用户admin')


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

    return dto.AssetsDto(code='A8888', user_id=1, user_name='admin',
                         name='图书', category='类别一', memo='很牛的书', image=image,
                         dst_user_id=1, dst_user_name='admin', dst_user_mobile='18995533533',
                         status=0, op_time=time.time(), limit_time=3*24*60*60)


def get_test_db():
    _db = DB(Conf.db_file_path_rw)
    _db.IS_PRINT_SQL = True
    return _db


def get_test_img_db():
    _db = DB(Conf.db_file_path_img)
    _db.IS_PRINT_SQL = True
    return _db


def get_test_request():
    req = HttpRequest()
    req.my_db = get_test_db()
    req.my_img_db = get_test_img_db()
    paras = req.parameters
    _user = get_test_user_dto()
    # 前端或者前序流程中（比如测试案例）没有上送跟踪号，就生成跟踪号
    paras['trace_id'] = get_trace_id()
    paras['reason'] = 'overtime'
    paras['userInfo'] = dict()
    user_info = paras['userInfo']
    user_info['login_name'] = _user.login_name
    user_info['name'] = _user.name
    user_info['dept_name'] = _user.depart
    user_info['mobile'] = _user.mobile
    user_info['memo'] = _user.memo
    user_info['org'] = _user.org
    user_info['id'] = _user.id

    _assets = get_test_book_assets_dto()

    paras["code"] = _assets.code
    paras["name"] = _assets.name
    paras["memo"] = _assets.memo
    paras["image"] = _assets.image
    paras['category'] = _assets.category
    paras['limit_time'] = _assets.limit_time
    return req


def get_borrow_reason():
    return 'overtime'


def get_return_reason():
    return 'return reason delay because NCP'


def get_trace_id():
    return 'generate_trace_id_999999'


def show_table_desc(conn, table_name, limit_len=4096):
    sql = 'PRAGMA table_info({})'.format(table_name)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    while rows:
        rows_print = get_print_string(rows, limit_len, True)
        my_print(rows_print)
        rows = cur.fetchone()
    cur.close()


def show_table_content(conn, table_name, limit_len=4096):
    cur = conn.cursor()
    cur.execute("select * from %s" % table_name)
    rows = cur.fetchone()
    while rows:
        rows_print = get_print_string(rows, limit_len, True)
        my_print(rows_print)
        rows = cur.fetchone()
    cur.close()


def show_db(file_path, limit_len=4096):
    with sqlite3.connect(database=file_path) as conn:
        query_table_sql = "select name from sqlite_master where type='table'"
        t_cur = conn.cursor()
        t_cur.execute(query_table_sql)
        t_rows = t_cur.fetchone()
        while t_rows:
            table_name = t_rows[0]
            my_print('-' * 15 + file_path + '(' + table_name + ')' + '-' * 15)
            show_table_desc(conn, table_name, limit_len)
            show_table_content(conn, table_name, limit_len)
            t_rows = t_cur.fetchone()

