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
                IMAGE BLOB,         -- 缩略图
                CREATE_TIME TIMESTAMP,
                LIMIT_TIME INT,         -- 限制借出时间， 提醒时间
                
                DST_USER_ID INT,              -- 借物品的人的用户ID
                DST_USER_NAME VARCHAR (40),   -- 借物品的人的名字，用于我的物品
                DST_USER_MOBILE VARCHAR (40), -- 借物品的人的电话
                STATUS INT,  --enum,  0 此物品未借出 1 此物品已借出 2 此物品已归还
                OP_TIME TIMESTAMP,   -- 操作时间 
                
                PRIMARY KEY(CODE),
                FOREIGN KEY(USER_ID) REFERENCES USER(ID))
    """
    insert_sql = "insert into assets(code, user_id, user_name, name, " \
                 "category, memo, image, create_time, limit_time, dst_user_id, dst_user_name, dst_user_mobile," \
                 "status, op_time) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    query_sql = "select t.code, t.user_id, t.user_name, t.name, t.category, t.memo, t.image, t.create_time," \
                "t.limit_time, t.dst_user_id, t.dst_user_name, t.dst_user_mobile, t.status, t.op_time from assets t"

    img_create_sql = """CREATE TABLE IMAGES(
        ID INTEGER PRIMARY KEY, 
        CODE VARCHAR(40),
        HEADER VARCHAR(256),
        IMAGE BLOB)
    """
    img_insert_sql = "insert into images(id, code, header, image) values(?,?,?,?)"
    img_query_sql = "select id, code, header, image from images"

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

    @staticmethod
    def row2asserts(row):
        if row:
            return AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                             category=row[4], memo=row[5], image=row[6], create_time=row[7], limit_time=row[8],
                             dst_user_id=row[9], dst_user_name=row[10], dst_user_mobile=row[11],
                             status=row[12], op_time=row[13])
        return None

    def get_assets_by_code(self, code: str):
        sql = AssetsDao.query_sql + " where code = ?"
        para = (code,)
        row = self._db.get_one(sql=sql, para=para)
        return self.row2asserts(row=row)

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
        rows = self._db.get_all(sql=sql, para=paras)
        ret_assets = list()
        for row in rows:
            ret_assets.append(self.row2asserts(row=row))
        if len(ret_assets) > 0:
            sql = 'select count(*) from assets where user_id = ?'
            paras = (user_id, )
            row = self._db.get_one(sql, paras)
            if row:
                count = row[0]
        return ret_assets, count

    def get_assets_image_by_code(self, code):
        sql = AssetsDao.img_query_sql + ' where code = ?'
        paras = (code,)
        # 先只做适应一个图片的，以后有时间再做多个图像的
        rows = self._img_db.get_one(sql, para=paras)
        if rows:
            return rows[1], rows[2], rows[3]  # code, header, image
        return None, None, None

    def insert_assets(self, code=None, user_id=None, user_name=None, user_mobile=None, assets_name=None,
                      assets_category=None, assets_memo=None, image=None, limit_time=31536000,
                      _assets=None, is_commit=False):
        if _assets and isinstance(_assets, AssetsDto):
            src_image, thb_image, header = self.parse_image(_assets.image)
            code = _assets.code
            para = (_assets.code, _assets.user_id, _assets.user_name, _assets.name, _assets.category,
                    _assets.memo, thb_image, time.time(), _assets.limit_time, _assets.dst_user_id,
                    _assets.dst_user_name,
                    _assets.dst_user_mobile, _assets.status, time.time())
        else:
            src_image, thb_image, header = self.parse_image(image)
            para = (code, user_id, user_name, assets_name, assets_category, assets_memo, thb_image, time.time(),
                    limit_time, user_id, user_name, user_mobile, 0, time.time())
        sql = AssetsDao.insert_sql
        self._db.insert_one(sql=sql, para=para, is_commit=is_commit)
        if src_image:
            # 图片保存缩略图到数据库里面，大图保存到另外的数据库或者文件系统里面
            self._img_db.insert_one(sql=AssetsDao.img_insert_sql, para=(None, code, header, src_image), is_commit=is_commit)
        return AssetsDto(para)

    def update_assert_status(self, code=None, user_id=None, user_name=None, user_mobile=None,
                             src_status=None, dst_status=None, is_commit=None):
        sql = 'update assets set dst_user_id=?, dst_user_name=?, dst_user_mobile = ?, op_time=?, status=? ' \
              'where code=? and status=?'
        if code is None or user_id is None or user_name is None or src_status is None or dst_status is None:
            return False, '资产代码，用户名称等不能为None'
        paras = (user_id, user_name, user_mobile, time.time(), dst_status, code, src_status,)
        self._db.execute(sql, para=paras, is_commit=is_commit)
        sql = 'select code, name, user_name from assets ' \
              'where code = ? and dst_user_id=? and dst_user_name = ? and status = ?'
        paras = (code, user_id, user_name, dst_status,)
        _assets = self._db.get_one(sql, paras)
        if _assets:
            message = '{0}({1})成功借出{2}的{3}({4})'.format(user_name, user_mobile, _assets[2], _assets[1], _assets[0])
            return True, message
        return False, '{0}({1})借资产{2}失败，可能已被被人借走'.format(user_name, user_mobile, code)

    @staticmethod
    def parse_image(image):
        if image:
            tmp = image.split(b'\r\n\r\n', 1)
            if len(tmp) == 2:
                src_image = tmp[1].rstrip(b'\r\n')
                if len(src_image) > 0:
                    thb_image = thumbnail(src_image)
                    return src_image, thb_image, tmp[0].decode('utf-8')
        return None, None, None
