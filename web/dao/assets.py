#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 9:00 AM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dto.assets import AssetsDto
import time
from utils import thumbnail


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

    img_create_sql = """CREATE TABLE IMAGES(
        ID INTEGER PRIMARY KEY, 
        CODE VARCHAR(40),
        IMAGE BLOB)
    """
    img_insert_sql = "insert into images(id, code, image) values(?,?,?)"
    img_query_sql = "select id, code, image from images"

    def __init__(self, _db: DB, _img_db: DB = None):
        self._db = _db
        if _img_db:
            self._img_db = _img_db
        else:
            self._img_db = self._db

    def create_table(self):
        self._db.create_table(AssetsDao.create_sql)
        self._img_db.create_table(AssetsDao.img_create_sql)
        self._img_db.execute("CREATE INDEX IMAGES_CODE_INDEX ON IMAGES(CODE)")

    def get_assets_by_code(self, code: str):
        sql = AssetsDao.query_sql + " where code = ?"
        para = (code,)
        row = self._db.get_one(sql=sql, para=para)
        if row:
            return AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                             category=row[4], memo=row[5], image=row[6], create_time=row[7])
        return None

    def get_assets_by_user_id(self, user_id=None, limit=20, offset=0):
        """
        获取某个用户下的资产
        :param user_id:
        :param limit:
        :param offset:
        :return:  资产，但是不包含图片字段
        """
        sql = AssetsDao.query_sql + " where user_id = ? order by create_time desc limit ? offset ?"
        paras = (user_id, limit, offset,)
        rows = self._db.get_all(sql=sql, paras=paras)
        ret_assets = list()
        for row in rows:
            ret_assets.append(AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                                        category=row[4], memo=row[5], image=row[6], create_time=row[7]))
        return ret_assets

    def get_assets_image_by_code(self, code):
        sql = AssetsDao.img_query_sql + ' where code = ?'
        paras = (code,)
        # 先只做适应一个图片的，以后有时间再做多个图像的
        rows = self._img_db.get_one(sql, paras=paras)
        if rows:
            return rows[2]
        return None

    def insert_assets(self, code=None, user_id=None, user_name=None, assets_name=None,
                      assets_category=None, assets_memo=None, image=None, _assets=None, is_commit=False):
        if _assets and isinstance(_assets, AssetsDto):
            src_image, thb_image = self.parse_image(_assets.image)
            code = _assets.code
            para = (_assets.code, _assets.user_id, _assets.user_name, _assets.name, _assets.category,
                    _assets.memo, thb_image, time.time())
        else:
            src_image, thb_image = self.parse_image(image)
            para = (code, user_id, user_name, assets_name, assets_category, assets_memo, thb_image, time.time())
        sql = AssetsDao.insert_sql
        self._db.insert_one(sql=sql, para=para, is_commit=is_commit)
        # 图片保存缩略图到数据库里面，大图保存到另外的数据库或者文件系统里面
        self._img_db.insert_one(sql=AssetsDao.img_insert_sql, para=(None, code, src_image))
        return AssetsDto(para)

    @staticmethod
    def parse_image(image):
        if image:
            tmp = image.split(b'\r\n\r\n', 1)
            if len(tmp) == 2:
                src_image = tmp[1].rstrip(b'\r\n')
                if len(src_image) > 0:
                    thb_image = thumbnail(src_image)
                    return src_image, thb_image
        return None, None
