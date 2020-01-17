#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> note
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 5:13 PM
@Desc   ：
=================================================='''
from web.dao.db import DB, g_db
from web.dto.note import NoteDto
import time


class NoteDao(object):
    create_sql = """CREATE TABLE NOTE (
                ID INTEGER PRIMARY KEY, 
                ASSETS_CODE VARCHAR(40),
                ASSETS_NAME VARCHAR(40),
                SRC_USER_ID INT, 
                DST_USER_ID INT, 
                WITNESS_ID INT,
                MEMO VARCHAR(40),  --保存用途，比如餐卡的加班或者招待
                LOG TEXT(200),
                BORROW_TIME TIMESTAMP,
                FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE),
                FOREIGN KEY(SRC_USER_ID) REFERENCES USER(ID),
                FOREIGN KEY(DST_USER_ID) REFERENCES USER(ID) )"""

    insert_sql = "insert into NOTE(ID, ASSETS_CODE, ASSETS_NAME, SRC_USER_ID, DST_USER_ID," \
                 "WITNESS_ID, MEMO, LOG, BORROW_TIME) values(?,?,?,?,?,?,?,?,?)"
    delete_sql = "delete from NOTE"
    query_sql = "select ID, ASSETS_CODE, ASSETS_NAME,SRC_USER_ID,DST_USER_ID,WITNESS_ID,MEMO,LOG,BORROW_TIME from NOTE"

    def __init__(self, _db: DB=g_db):
        self._db = _db

    def create_table(self):
        self._db.create_table(NoteDao.create_sql)

    def get_note_by_assets_code(self, code):
        sql = NoteDao.query_sql + ' where assets_code = ?'
        paras = (code,)
        row = self._db.get_one(sql, paras)
        if row:
            return NoteDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
                           witness_id=row[5], memo=row[6], log=row[7], borrow_time=row[8])
        return None

    def insert_note(self, assets_code=None, assets_name=None, src_user_id=None, dst_user_id=None,
                    witness_id=None, reason=None, _log=None, is_commit=False):
        sql = NoteDao.insert_sql
        para = (None, assets_code, assets_name, src_user_id, dst_user_id, witness_id, reason, _log, time.time(),)
        self._db.insert_one(sql, para, is_commit)

    def del_note_by_id(self, pid, is_commit=False):
        sql = NoteDao.delete_sql + " where id=?"
        para = (pid,)
        self._db.execute(sql=sql, para=para, is_commit=is_commit)


g_noteDao = NoteDao()
