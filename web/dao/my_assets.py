#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> my_assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 10:14 AM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dto.myassets import MyAssetsDto
import time


class MyAssetsDao(object):
    create_sql = """CREATE TABLE MY_ASSETS (
                ID INTEGER PRIMARY KEY, 
                ASSETS_CODE VARCHAR(40),
                USER_ID INT,
                CREATE_TIME TIMESTAMP,
                FOREIGN KEY(USER_ID) REFERENCES USER(ID),
                FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE)
                )"""

    insert_sql = "insert into MY_ASSETS(ID, ASSETS_CODE, USER_ID, CREATE_TIME) values(?,?,?,?)"
    query_sql = "select ID, ASSETS_CODE, USER_ID, CREATE_TIME from MY_ASSETS"

    def __init__(self, _db: DB):
        self._db = _db

    def create_table(self):
        self._db.create_table(MyAssetsDao.create_sql)
        self._db.execute("CREATE INDEX ID_CODE_INDEX ON MY_ASSETS(USER_ID, ASSETS_CODE)")
        self._db.execute("CREATE INDEX CODE_ID_INDEX ON MY_ASSETS(ASSETS_CODE, USER_ID)")

    def is_my_mng_assets(self, user_id=None, assets_code=None):
        row = self._db.get_one('select user_id, assets_code from my_assets where user_id=? and assets_code=?',
                               (user_id, assets_code,))
        return row is not None

    def get_my_assets(self, user_id=None, assets_code=None):
        lst = list()
        condition = None
        if user_id is not None:
            condition = "user_id=?"
            lst.append(user_id)
        if assets_code is not None:
            if condition:
                condition = condition + " and code=?"
            else:
                condition = "code=?"
            lst.append(assets_code)
        if condition:
            condition = " where " + condition
        sql = MyAssetsDao.query_sql + condition
        para = tuple(lst)
        row = self._db.get_one(sql=sql, para=para)
        if row:
            return MyAssetsDto(pid=row[0], code=row[1], user_id=row[2], user_name=row[3],
                               name=row[4], memo=row[5], status=row[6],
                               create_time=row[7], borrow_time=row[8])
        return None

    def insert_my_assets(self, assets_code=None, user_id=None, is_commit=False):
        sql = MyAssetsDao.insert_sql
        para = (None, assets_code, user_id, time.time(),)
        self._db.insert_one(sql, para, is_commit)

