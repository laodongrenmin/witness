#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> notehis
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/17/2020 5:02 PM
@Desc   ：
=================================================="""
from web.dao.db import DB, g_db
from web.dto.notehis import NoteHisDto
from web.dto.user import UserDto
from web.dto.note import NoteDto
from web.dto.assets import AssetsDto
import time


class NoteHisDao(object):
    create_sql = """CREATE TABLE NOTE_HIS (
            ID INTEGER PRIMARY KEY,
            ASSETS_CODE VARCHAR(40),
            ASSETS_NAME VARCHAR(40),
            CATEGORY VARCHAR (40),
            MNG_USER_ID INT,         -- 归还的管理员
            MNG_USER_NAME VARCHAR(40),
            SRC_USER_ID INT,        -- 资产的拥有者
            DST_USER_ID INT,        -- 资产的借用者
            WITNESS_ID INT,
            SRC_MOBILE VARCHAR(40) NOT NULL,
            SRC_NAME VARCHAR(40) NOT NULL,
            SRC_MEMO TEXT(500),
            DST_MOBILE VARCHAR(40) NOT NULL,
            DST_NAME VARCHAR(40) NOT NULL,
            DST_MEMO TEXT(500),
            MEMO VARCHAR(40), 
            LOG TEXT(200),
            BORROW_TIME TIMESTAMP,
            RETURN_TIME TIMESTAMP,
            FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE) )"""

    insert_sql = "insert into NOTE_HIS(ID, ASSETS_CODE, ASSETS_NAME, CATEGORY, MNG_USER_ID, MNG_USER_NAME, " \
                 "SRC_USER_ID, DST_USER_ID," \
                 "WITNESS_ID, SRC_MOBILE, SRC_NAME, SRC_MEMO, " \
                 "DST_MOBILE, DST_NAME, DST_MEMO, MEMO, LOG, " \
                 "BORROW_TIME, RETURN_TIME) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    query_sql = "select ID, ASSETS_CODE, ASSETS_NAME, CATEGORY, MNG_USER_ID, MNG_USER_NAME," \
                "SRC_USER_ID, DST_USER_ID, WITNESS_ID, " \
                "SRC_MOBILE, SRC_NAME, SRC_MEMO, DST_MOBILE, DST_NAME, DST_MEMO, MEMO, LOG, " \
                "BORROW_TIME, RETURN_TIME from NOTE"

    def __init__(self, _db: DB=g_db):
        self._db = _db

    def create_table(self):
        self._db.create_table(NoteHisDao.create_sql)

    def insert_note_his(self, _assets: AssetsDto, mng_user: UserDto=None,
                        src_user: UserDto=None, dst_user: UserDto=None, _note: NoteDto=None,
                        log=None, is_commit=False):
        sql = NoteHisDao.insert_sql
        para = (None, _assets.code, _assets.name, _assets.category, mng_user.id, mng_user.name,
                src_user.id, dst_user.id, _note.witness_id, src_user.mobile, src_user.name,
                src_user.memo, dst_user.mobile, dst_user.name, dst_user.memo, _note.memo, log,
                _note.borrow_time, time.time())
        self._db.execute(sql=sql, para=para, is_commit=is_commit)


g_noteHisDao = NoteHisDao()
