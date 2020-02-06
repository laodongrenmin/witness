#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> init_db
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/14/2020 2:47 PM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dao.log import LogDao
from web.dao.user import UserDao
from web.dao.note import NoteDao
from web.dao.assets import AssetsDao
from web.dao.my_assets import MyAssetsDao
from web.dao.notehis import NoteHisDao


def create_db(db_file_path):
    _db = DB()
    _db.init_conn_by_name(_db_name=db_file_path)
    _db.close()


def create_table(_db):
    LogDao(_db).create_table()
    NoteDao(_db).create_table()
    UserDao(_db).create_table()
    AssetsDao(_db).create_table()
    MyAssetsDao(_db).create_table()
    NoteHisDao(_db).create_table()
