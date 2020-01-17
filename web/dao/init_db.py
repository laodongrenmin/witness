#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> init_db
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/14/2020 2:47 PM
@Desc   ：
=================================================="""
from web.dao.db import g_db
from web.dao.log import g_logDao
from web.dao.user import g_userDao
from web.dao.note import g_noteDao
from web.dao.assets import g_assetsDao
from web.dao.my_assets import g_myAssetsDao
from web.dao.notehis import g_noteHisDao


def create_db(db_file_path):
    g_db.init_conn_by_name(_db_name=db_file_path)


def create_table():
    g_logDao.create_table()
    g_noteDao.create_table()
    g_userDao.create_table()
    g_assetsDao.create_table()
    g_myAssetsDao.create_table()
    g_noteHisDao.create_table()
