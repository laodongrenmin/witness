#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> user
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/10/2020 3:15 PM
@Desc   ：
=================================================="""
from web.dao.db import DB, g_db
from web.dto.user import UserDto


class UserDao(object):
    create_sql = """CREATE TABLE USER (
            ID INTEGER PRIMARY KEY,
            LOGIN_NAME VARCHAR(40) NOT NULL,
            NAME VARCHAR(40) NOT NULL,
            MOBILE VARCHAR(40),
            STATUS INT,  --0 正常 1 删除
            MEMO TEXT(500))"""
    insert_sql = "insert into user(id,login_name,name,status,memo,mobile) values(?,?,?,?,?,?)"
    query_sql = "select id,login_name,name,status,memo,mobile from user"

    def __init__(self, _db: DB=g_db):
        self._db = _db

    def create_table(self):
        self._db.create_table(UserDao.create_sql)

    def get_user_by_login_name(self, login_name: str):
        sql = UserDao.query_sql + " where LOGIN_NAME = ?"
        paras = (login_name,)
        row = self._db.get_one(sql, paras)
        if row:
            return UserDto(pid=row[0], login_name=row[1], name=row[2], status=row[3], memo=row[4], mobile=row[5])
        return None

    def get_user_by_id(self, pid):
        sql = UserDao.query_sql + " where id = ?"
        paras = (pid,)
        row = self._db.get_one(sql, paras)
        if row:
            return UserDto(pid=row[0], login_name=row[1], name=row[2], status=row[3], memo=row[4], mobile=row[5])
        return None

    def insert_user(self, login_name, user_name=None, user_memo=None, mobile=None,
                    u=None, is_commit=False):
        sql = UserDao.insert_sql
        if u and isinstance(u, UserDto):  # 当第一个参数是DTO时候
            para = (None, u.login_name, u.name, 0, u.memo, u.mobile, )
        else:
            para = (None, login_name, user_name, 0, user_memo, mobile,)
        self._db.insert_one(sql, para, is_commit)
        return self.get_user_by_login_name(login_name)


g_userDao = UserDao()

