#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> my_assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 10:14 AM
@Desc   ：
=================================================="""
from web.dao.db import DB, g_db
from web.dto.myassets import MyAssetsDto
import time


class MyAssetsDao(object):
    create_sql = """CREATE TABLE MY_ASSETS (
                ID INTEGER PRIMARY KEY, 
                CODE VARCHAR(40),
                USER_ID INT,
                USER_NAME VARCHAR(40), 
                NAME VARCHAR(40) NOT NULL,
                MEMO TEXT(500),
                DST_USER_NAME VARCHAR (40),   -- 借物品的人的名字，用于我的物品
                DST_USER_MOBILE VARCHAR (40),
                STATUS INT,  --enum,  0 此物品未借出 1 此物品已借出 2 此物品已归还
                OP_TIME TIMESTAMP, 
                CREATE_TIME TIMESTAMP,
                FOREIGN KEY(USER_ID) REFERENCES USER(ID))"""

    insert_sql = "insert into MY_ASSETS(ID, CODE, USER_ID, USER_NAME, NAME, " \
                 "MEMO, STATUS, OP_TIME, CREATE_TIME) values(?,?,?,?,?,?,?,?,?)"
    query_sql = "select ID, CODE, USER_ID, USER_NAME, NAME, MEMO, STATUS, OP_TIME, CREATE_TIME from MY_ASSETS"

    def __init__(self, _db: DB=g_db):
        self._db = _db

    def create_table(self):
        self._db.create_table(MyAssetsDao.create_sql)
        self._db.execute("CREATE INDEX CODE_INDEX ON MY_ASSETS(CODE)")

    def get_my_assets(self, assets_code=None, user_id=None):
        sql = MyAssetsDao.query_sql + " where code=? and user_id=?"
        para = (assets_code, user_id)
        row = self._db.get_one(sql=sql, para=para)
        if row:
            return MyAssetsDto(pid=row[0], code=row[1], user_id=row[2], user_name=row[3],
                               name=row[4], memo=row[5], status=row[6],
                               create_time=row[7], borrow_time=row[8])
        return None

    def insert_my_assets(self, assets_code=None, assets_name=None, assets_memo=None,
                         user_id=None, user_name=None, _user=None, _assets=None, is_commit=False):
        if _assets:
            assets_code = _assets.code
            assets_name = _assets.name
            assets_memo = _assets.memo
        if _user:
            user_name = _user.name
            user_id = _user.id
        sql = MyAssetsDao.insert_sql
        para = (None, assets_code, user_id, user_name, assets_name, assets_memo, 0, time.time(), time.time())
        self._db.insert_one(sql, para, is_commit)

    def update_my_assets_status(self, code=None, status=None):
        self._db.execute("update my_assets set status = ?, op_time = ? where code = ?", (status, time.time(), code))


g_myAssetsDao = MyAssetsDao()
