#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> _log
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 2:41 PM
@Desc   ：
=================================================="""
import web.dao as dao
from utils import my_print


class LogImpl(object):
    def __init__(self, _dao=dao, _db=None):
        self._dao = dao
        self._db = _db

    def set_dao(self, _dao):
        self._dao = _dao

    def set_db(self, _db):
        self._db = _db

    def log(self, user_id=None, user_name=None, op_type=None, assets_code=None, assets_name=None, _log=None,
            is_commit=False, is_print=True):
        self._dao.insert_log(self._db, user_id=user_id, user_name=user_name, op_type=op_type, assets_code=assets_code,
                             assets_name=assets_name, _log=_log, is_commit=is_commit)
        if is_print:
            str_log = "user: {0} type: {1} assets: {2}({3}) _log: {4}".format(user_id, op_type, assets_name, assets_code, _log)
            my_print(str_log)
