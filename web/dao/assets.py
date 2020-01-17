#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 9:00 AM
@Desc   ：
=================================================="""
from web.dao.db import DB, g_db
from web.dto.assets import AssetsDto
import time


class AssetsDao(object):
    create_sql = """CREATE TABLE ASSETS (
                CODE VARCHAR(40),
                USER_ID INT,
                USER_NAME VARCHAR(40), 
                NAME VARCHAR(40) NOT NULL,
                CATEGORY VARCHAR (40),
                MEMO TEXT(500),
                IMAGE BLOB, 
                CREATE_TIME TIMESTAMP,
                PRIMARY KEY(CODE),
                FOREIGN KEY(USER_ID) REFERENCES USER(ID))
    """
    insert_sql = "insert into assets(code, user_id, user_name, name, " \
                 "category, memo, image, create_time) values(?,?,?,?,?,?,?,?)"
    query_sql = "select code, user_id, user_name, name, category, memo, image, create_time from assets"

    def __init__(self, _db: DB=g_db):
        self._db = _db

    def create_table(self):
        self._db.create_table(AssetsDao.create_sql)

    def get_assets_by_code(self, code: str):
        sql = AssetsDao.query_sql + " where code = ?"
        para = (code,)
        row = self._db.get_one(sql=sql, para=para)
        if row:
            return AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                             category=row[4], memo=row[5], image=row[6], create_time=row[7])
        return None

    def get_assets_by_user_id(self, user_id=None, limit=1000, offset=0):
        """
        获取某个用户下的资产
        :param user_id:
        :param limit:
        :param offset:
        :return:  资产，但是不包含图片字段
        """
        sql = "select code, user_id, user_name, name, category, memo, create_time from assets "
        sql = sql + " where user_id = ? order by create_time desc limit ? offset ?"
        paras = (user_id, limit, offset,)
        rows = self._db.get_all(sql=sql, paras=paras)
        ret_assets = list()
        for row in rows:
            ret_assets.append(AssetsDto(code=row[0], user_id=row[1], user_name=row[2],
                                        category=row[4], memo=row[5], image=None, create_time=row[6]).to_dict())
        return ret_assets

    def insert_assets(self, code=None, user_id=None, user_name=None, assets_name=None,
                      assets_category=None, assets_memo=None, image=None, _assets=None, is_commit=False):
        if _assets and isinstance(_assets, AssetsDto):
            para = (_assets.code, _assets.user_id, _assets.user_name, _assets.name, _assets.category,
                    _assets.memo, _assets.image, time.time())
        else:
            para = (code, user_id, user_name, assets_name, assets_category, assets_memo, image, time.time())
        sql = AssetsDao.insert_sql
        self._db.insert_one(sql=sql, para=para, is_commit=is_commit)
        return AssetsDto(para)


g_assetsDao = AssetsDao()
