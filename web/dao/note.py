#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> note
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 5:13 PM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dto.note import NoteDto


class NoteDao(object):
    create_sql = """CREATE TABLE NOTE (
                ID INTEGER PRIMARY KEY, 
                ASSETS_CODE VARCHAR(40),
                SRC_USER_ID INT, 
                DST_USER_ID INT, 
                WITNESS_ID INT,
                BORROW_REASON VARCHAR(256),  --保存用途，比如餐卡的加班或者招待
                RETURN_REASON VARCHAR(256),  --保存归还原因，比如超期，催还, 一般用于借出未规划时候
                BORROW_TIME TIMESTAMP,
                LIMIT_TIME TIMESTAMP,   -- 保存操作时间，比如中间有催还，记录催还时间, 预计归还时间，提醒时间
                FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE),
                FOREIGN KEY(SRC_USER_ID) REFERENCES USER(ID),
                FOREIGN KEY(DST_USER_ID) REFERENCES USER(ID) )"""

    insert_sql = "insert into NOTE(ID, ASSETS_CODE, SRC_USER_ID, DST_USER_ID," \
                 "WITNESS_ID, BORROW_REASON, RETURN_REASON, BORROW_TIME, LIMIT_TIME) values(?,?,?,?,?,?,?,?,?)"
    delete_sql = "delete from NOTE"
    query_sql = "select ID, ASSETS_CODE, SRC_USER_ID, DST_USER_ID, WITNESS_ID, " \
                "BORROW_REASON, RETURN_REASON, BORROW_TIME, LIMIT_TIME from NOTE"

    def __init__(self, _db: DB):
        self._db = _db

    def create_table(self):
        self._db.create_table(NoteDao.create_sql)
        self._db.execute("create index MY_ASSETS_INDEX_CODE on NOTE(ASSETS_CODE)")

    def get_note_by_assets_code(self, code):
        sql = NoteDao.query_sql + ' where ASSETS_CODE = ?'
        paras = (code,)
        row = self._db.get_one(sql, paras)
        if row:
            return NoteDto(pid=row[0], assets_code=row[1], src_user_id=row[2], dst_user_id=row[3],
                           witness_id=row[4], borrow_reason=row[5], return_reason=row[6],
                           borrow_time=row[7], limit_time=row[8])
        return None

    def insert_note(self, _note: NoteDto, is_commit=False):
        sql = NoteDao.insert_sql
        para = (_note.id, _note.assets_code, _note.src_user_id, _note.dst_user_id,
                _note.witness_id, _note.borrow_reason, _note.return_reason, _note.borrow_time,
                _note.limit_time)
        self._db.insert_one(sql, para, is_commit)

    def del_note_by_id(self, pid, is_commit=False):
        sql = NoteDao.delete_sql + " where id=?"
        para = (pid,)
        self._db.execute(sql=sql, para=para, is_commit=is_commit)
