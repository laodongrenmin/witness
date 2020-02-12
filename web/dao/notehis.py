#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> notehis
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 5:02 PM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dto.user import UserDto
from web.dto.note import NoteDto
from web.dto.assets import AssetsDto
import time


class NoteHisDao(object):
    create_sql = """CREATE TABLE NOTE_HIS (       -- 把所有的与统计相关的字段值都保存到历史登记簿中
            ID INTEGER PRIMARY KEY,
            ASSETS_CODE VARCHAR(40),
            ASSETS_NAME VARCHAR(40),
            CATEGORY VARCHAR (40),
            MNG_USER_ID INT,         -- 归还的管理员, 统计归还工作量, 按用户、机构、部门
            MNG_USER_ORG VARCHAR(40),
            MNG_USER_DEPT VARCHAR(256),
            MNG_USER_NAME VARCHAR(40),
            MGN_USER_MOBILE VARCHAR(40),
            SRC_USER_ID INT,        -- 资产的拥有者, 按用户、机构、部门
            SRC_USER_ORG VARCHAR(40),
            SRC_USER_DEPT VARCHAR(256),
            SRC_USER_NAME VARCHAR(40) NOT NULL,
            SRC_USER_MOBILE VARCHAR(40) NOT NULL,
            DST_USER_ID INT,        -- 资产的借用者, 统计借出工作量, 按用户、机构、部门
            DST_USER_ORG VARCHAR(40),
            DST_USER_DEPT VARCHAR(256),
            DST_USER_NAME VARCHAR(40) NOT NULL,
            DST_MOBILE VARCHAR(40) NOT NULL,
            WITNESS_ID INT,
            BORROW_REASON VARCHAR(256),  --保存用途, 比如餐卡的加班或者招待
            RETURN_REASON VARCHAR(256),  --保存归还原因, 比如超期, 催还, 一般用于借出未规划时候
            BORROW_TIME TIMESTAMP,
            LIMIT_TIME TIMESTAMP,   -- 保存操作时间, 比如中间有催还, 记录催还时间, 预计归还时间, 提醒时间
            RETURN_TIME TIMESTAMP,
            LOG VARCHAR(256),
            FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE),
            FOREIGN KEY(MNG_USER_ID) REFERENCES USER(ID),
            FOREIGN KEY(SRC_USER_ID) REFERENCES USER(ID),
            FOREIGN KEY(DST_USER_ID) REFERENCES USER(ID)
             )"""

    insert_sql = "insert into NOTE_HIS(ID, ASSETS_CODE, ASSETS_NAME, CATEGORY, " \
                 "MNG_USER_ID, MNG_USER_ORG, MNG_USER_DEPT, MNG_USER_NAME, MGN_USER_MOBILE," \
                 "SRC_USER_ID, SRC_USER_ORG, SRC_USER_DEPT, SRC_USER_NAME, SRC_USER_MOBILE," \
                 "DST_USER_ID, DST_USER_ORG, DST_USER_DEPT, DST_USER_NAME, DST_MOBILE, " \
                 "WITNESS_ID, BORROW_REASON, RETURN_REASON, BORROW_TIME, LIMIT_TIME, " \
                 "RETURN_TIME, LOG) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    query_sql = "select ID, ASSETS_CODE, ASSETS_NAME, CATEGORY, " \
                "MNG_USER_ID, MNG_USER_ORG, MNG_USER_DEPT, MNG_USER_NAME, MGN_USER_MOBILE, " \
                "SRC_USER_ID, SRC_USER_ORG, SRC_USER_DEPT, SRC_USER_NAME, SRC_USER_MOBILE, " \
                "DST_USER_ID, DST_USER_ORG, DST_USER_DEPT, DST_USER_NAME, DST_MOBILE, " \
                "WITNESS_ID, BORROW_REASON, RETURN_REASON, BORROW_TIME, LIMIT_TIME, " \
                "RETURN_TIME, LOG from NOTE_HIS"

    def __init__(self, _db: DB):
        self._db = _db

    def create_table(self):
        self._db.create_table(NoteHisDao.create_sql)

    def insert_note_his(self, _assets: AssetsDto, mng_user: UserDto = None,
                        src_user=None, dst_user=None, _note: NoteDto = None,
                        _log=None, is_commit=False):
        sql = NoteHisDao.insert_sql
        para = (None, _assets.code, _assets.name, _assets.category,
                mng_user.id, mng_user.org, mng_user.depart, mng_user.name, mng_user.mobile,
                src_user.id, src_user.org, src_user.depart, src_user.name, src_user.mobile,
                dst_user.id, dst_user.org, dst_user.depart, dst_user.name, dst_user.mobile,
                _note.witness_id, _note.borrow_reason, _note.return_reason, _note.borrow_time, _note.limit_time,
                time.time(), _log)
        self._db.execute(sql=sql, para=para, is_commit=is_commit)
