#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> user
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/10/2020 3:15 PM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dto.user import UserDto


class UserDao(object):
    create_sql = """CREATE TABLE USER (
            ID INTEGER PRIMARY KEY,
            LOGIN_NAME VARCHAR(40) NOT NULL,
            NAME VARCHAR(40) NOT NULL,
            MOBILE VARCHAR(40),
            STATUS INT,  --0 正常 1 删除
            DEPART VARCHAR(256), -- 文字   金科/武汉事业群/架构
            ORG VARCHAR(40), -- 代号     （ 00001， 金科/武汉事业群； 00001， 金科/武汉事业群/架构； 
            MEMO TEXT(500))"""
    insert_sql = "insert into user(id,login_name,name,mobile,status,depart,org,memo) values(?,?,?,?,?,?,?,?)"
    query_sql = "select id,login_name,name,mobile,status,depart,org,memo from user"

    def __init__(self, _db: DB):
        self._db = _db

    def create_table(self):
        self._db.create_table(UserDao.create_sql)
        self._db.execute("create index USER_IND_LOGIN_NAME on USER(LOGIN_NAME)")

    def get_user_by_login_name(self, login_name: str):
        sql = UserDao.query_sql + " where LOGIN_NAME = ?"
        paras = (login_name,)
        row = self._db.get_one(sql, paras)
        if row:
            return UserDto(pid=row[0], login_name=row[1], name=row[2], mobile=row[3], status=row[4],
                           depart=row[5], org=row[6], memo=row[7])
        return None

    def get_user_by_id(self, pid):
        sql = UserDao.query_sql + " where id = ?"
        paras = (pid,)
        row = self._db.get_one(sql, paras)
        if row:
            return UserDto(pid=row[0], login_name=row[1], name=row[2], mobile=row[3], status=row[4],
                           depart=row[5], org=row[6], memo=row[7])
        return None

    def insert_user(self, login_name=None, name=None, mobile=None, depart=None, org=None, memo=None,
                    u=None, is_commit=False):
        """
        参数传入 u 或者 login_name 是tuple时候，id使用传入的数据， 按照各个变量传入， id使用None
        :param login_name:
        :param name:
        :param mobile:
        :param depart:
        :param org:
        :param memo:
        :param u:
        :param is_commit:
        :return:
        """
        sql = UserDao.insert_sql
        if u and isinstance(u, UserDto):
            para = (u.id, u.login_name, u.name, u.mobile, 0, u.depart, u.org, u.memo)
        elif isinstance(login_name, tuple):
            para = login_name
        else:
            para = (None, login_name, name, mobile, 0, depart, org, memo)
        self._db.insert_one(sql, para, is_commit)
