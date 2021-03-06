#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> _log
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 2:34 PM
@Desc   ：
=================================================="""
from web.dao.db import DB
import time


class LogDao(object):
    create_sql = """CREATE TABLE LOG (
                ID INTEGER PRIMARY KEY, 
                USER_ID INT, 
                USER_NAME VARCHAR(40),
                OP_TYPE INT, 
                ASSETS_CODE VARCHAR(40), 
                ASSETS_NAME VARCHAR(40), 
                LOG TEXT(200), 
                LOG_TIME TIMESTAMP)"""
# [(None, 3, OpType.借出.value, '餐卡', '小李子借给小东子餐卡', time.time()),
#  (None, 2, OpType.借出.value, '餐卡', '小东子借给小李子餐卡', time.time()), ]],
    insert_sql = "insert into LOG(ID, USER_ID, USER_NAME, OP_TYPE,ASSETS_CODE,ASSETS_NAME,LOG,LOG_TIME) " \
                 "values(?,?,?,?,?,?,?,?)"
    query_sql = "select ID, USER_ID, USER_NAME, OP_TYPE,ASSETS_CODE, ASSETS_NAME,LOG,LOG_TIME from LOG"

    def __init__(self, _db: DB):
        self._db = _db

    def create_table(self):
        self._db.create_table(LogDao.create_sql)

    def insert_log(self, user_id=None, user_name=None, op_type=None,
                   assets_code=None, assets_name=None, _log=None, is_commit=False):
        try:
            para = (None, user_id, user_name, op_type, assets_code, assets_name, _log, time.time(),)
            self._db.insert_one(LogDao.insert_sql, para, False)
        finally:
            if is_commit:      # 日志插入失败也要保证业务事务提交
                self._db.commit()

