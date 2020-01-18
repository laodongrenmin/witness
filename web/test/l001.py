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
import time

class Dao(object):
    def insert_log(self, user_id=None, op_type=None, assets_code=None, assets_name=None,
               log=None, is_commit=False):
        print('hehehe',user_id, op_type, assets_name, assets_code, log, is_commit)

if __name__ == '__main__':

    a = dto.AssetsDto('code',1,'admin','book','type1','ccbft',None,time.time())

    b = a.to_html_dict()

    print(b)

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