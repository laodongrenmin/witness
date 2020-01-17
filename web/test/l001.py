#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> l001
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/15/2020 3:07 PM
@Desc   ：
=================================================='''
from web.biz.log import g_logImpl
from web.dao.db import g_db
import web.dto as dto
import web.dao as dao

class Dao(object):
    def insert_log(self, user_id=None, op_type=None, assets_code=None, assets_name=None,
               log=None, is_commit=False):
        print('hehehe',user_id, op_type, assets_name, assets_code, log, is_commit)

if __name__ == '__main__':
    db_file_path = "test_sqlite3.db"
    g_db.init_conn_by_name(db_file_path)

    g_logImpl.log(0, 1, '111', 'name', 'test', True, True)
    my_dao = Dao()
    g_logImpl.set_dao(my_dao)
    g_logImpl.log(1, 1, '111', 'name', 'test', True, False)
    g_logImpl.set_dao(dao)
    g_logImpl.log(1, 1, '111', 'name', 'test', True, True)

    logDto = dto.LogDto(pid=0, user_id=1)
    print(logDto.user_id)

    principal = 10000
    year = 35
    month = 35 * 12
    interest = 0.0588

    index = 0
    s1 = 0
    while index < month:
        s1 = s1 + (principal + s1) * interest/12
        index = index + 1

    print('money is:', s1)
    exit(0)