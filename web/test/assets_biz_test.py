#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets_biz_test
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/14/2020 2:22 PM
@Desc   ：
=================================================="""
import unittest
import os
import sqlite3
from web.dao.init_db import create_db, create_table
from web.biz.assets import AssetsImpl
import utils
from web.biz.constant import Const
from web.test import *
from utils import my_print


def pre_db(*args, **kwargs):
    t = args[0]
    t.me._db.close()
    # 准备数据文件
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
    t.me._db.reopen()
    # create_db(db_file_path)
    create_table(t.me._db)


def show_db(*args, **kwargs):
    with sqlite3.connect(database=db_file_path) as conn:
        query_table_sql = "select name from sqlite_master where type='table'"
        t_cur = conn.cursor()
        t_cur.execute(query_table_sql)
        t_rows = t_cur.fetchone()
        while t_rows:
            table_name = t_rows[0]
            my_print('-' * 15 + table_name + '-' * 15)
            cur = conn.cursor()
            cur.execute("select * from %s" % table_name)
            rows = cur.fetchone()
            while rows:
                # for row in rows:
                #     if type(row) == bytes:
                #         print(row.decode('UTF-8'))
                my_print(rows)
                rows = cur.fetchone()
            t_rows = t_cur.fetchone()


class AssetsImplTestCase(unittest.TestCase):
    me = AssetsImpl()

    # set_print_sql_flag()

    def setUp(self):
        self.userDto = get_test_user_dto()
        self.assetsDto = get_test_book_assets_dto()
        self.assets_reason = get_borrow_reason()
        self.me.set_db(get_test_db())

    def tearDown(self):
        self.me._db.close()

    def test_00000_pre_data(self):
        my_print('test_00000_pre_data')
        pre_db(self)

    def test_00100_do_biz(self):
        # 1. 创建用户 以及 新建 不成功的资产 admin
        my_print('test_00100_do_biz 测试：' + '创建用户 以及 新建 不成功的资产')
        self.assetsDto.name = None
        status, assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.失败.value, '创建失败')
        self.assertEqual(assets, None, 'should be None')
        self.assertEqual(op_type.value, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, '添加资产,代码和名称是必须的，代码为: A8888 名称为：None', '添加资产，名称为空，不通过')

    def test_00110_do_biz(self):
        # 1. 创建用户 以及 新建 不成功的资产 admin
        my_print('test_00100_do_biz 测试：' + '创建用户 以及 新建 不成功的资产')
        self.assetsDto.name = None
        self.userDto.login_name = 'login_name2'
        self.userDto.name = 'admin2'
        status, assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.失败.value, '创建失败')
        self.assertEqual(assets, None, 'should be None')
        self.assertEqual(op_type.value, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, '添加资产,代码和名称是必须的，代码为: A8888 名称为：None', '添加资产，名称为空，不通过')

    def test_00200_do_biz(self):
        # 1. 新建资产成功
        my_print('test_00200_do_biz 测试：' + '成功新建资产')

        status, _assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功新建资产')
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type.value, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, 'admin(login_name_0001) 添加资产 图书(A8888)-类别一 并设置管理成功')

    def test_00300_do_biz(self):
        # 1. 借资产成功
        my_print('test_00300_do_biz 测试：' + '成功借资产')

        status, _assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功借资产')
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type.value, Const.OpType.借出.value, 'should be 借出')
        self.assertEqual(message, 'admin 的 图书 借给 ccb_ft 的 admin(18999999999)。')

    def test_00400_do_biz(self):
        # 1. 还资产成功
        my_print('test_00400_do_biz 测试：' + '成功还资产')

        status, _assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功还资产')
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type.value, Const.OpType.归还.value, 'should be 归还')
        self.assertEqual(message, '管理员:admin 归还了 admin 借的 admin 的 图书')

    def test_00411_do_biz(self):
        # 1. 不能还资产成功
        my_print('test_00400_do_biz 测试：' + '不能成功还资产')
        self.userDto.login_name = 'login_name2'
        self.do_biz()
        status, _assets, op_type, message = self.do_biz()

        self.assertEqual(status.value, Const.OpStatus.失败.value, '不能成功还资产')
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type.value, Const.OpType.归还.value, 'should be 归还')
        self.assertEqual(message, '资产: 图书 不由你管理，不能完成归还动作')

    def test_99999_do_biz(self):
        show_db(self)

    def do_biz(self):
        trace_id = utils.generate_trace_id()
        return self.me.do_biz(assets_code=self.assetsDto.code, assets_name=self.assetsDto.name,
                              assets_category=self.assetsDto.category,
                              assets_memo=self.assetsDto.memo,
                              assets_image=self.assetsDto.image, assets_reason=self.assets_reason,
                              login_name=self.userDto.login_name,
                              name=self.userDto.name, memo=self.userDto.memo, mobile=self.userDto.mobile,
                              trace_id=trace_id)

#
# if __name__ == '__main__':
#     unittest.main()


