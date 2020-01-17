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
import logging
import os
import sqlite3
from web.dao.init_db import create_db, create_table
from web.biz.assets import AssetsImpl
import web.dto as dto
import web.dao as dao
import web.util as util
from web.biz.constant import Const


def get_log(log_name):
    logging.basicConfig(
        format="%(asctime)s [%(filename)s,%(funcName)s,%(lineno)s] %(name)s %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    return logging.getLogger(log_name)


logger = get_log(__name__)


db_file_path = "test_sqlite3.db"


def pre_db():
    # 准备数据文件
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
    create_db(db_file_path)
    create_table()


def show_db():
    with sqlite3.connect(database=db_file_path) as conn:
        query_table_sql = "select name from sqlite_master where type='table'"
        t_cur = conn.cursor()
        t_cur.execute(query_table_sql)
        t_rows = t_cur.fetchone()
        while t_rows:
            table_name = t_rows[0]
            print(t_rows[0])
            cur = conn.cursor()
            cur.execute("select * from %s" % table_name)
            print('-' * 15, table_name, '-' * 15)
            rows = cur.fetchone()
            while rows:
                # for row in rows:
                #     if type(row) == bytes:
                #         print(row.decode('UTF-8'))
                print(rows)
                rows = cur.fetchone()
            t_rows = t_cur.fetchone()


class AssetsImplTestCase(unittest.TestCase):
    userDto = dto.UserDto(pid=0, login_name='login_name_0001', name='admin', status='0',
                          memo='ccb_ft', mobile='18999999999')
    assetsDto = dto.AssetsDto(code='A8888', user_id=0, user_name='admin',
                              name='图书', category='类别一', memo='很牛的书', image=b'jpeg\r\n\r\njpeg_content')
    assets_reason = 'overtime'

    me = AssetsImpl()

    def test_do_biz00100(self):
        # 1. 创建用户 以及 新建 不成功的资产
        print('test_do_biz00100 测试：' + '创建用户 以及 新建 不成功的资产')
        name = self.assetsDto.name
        self.assetsDto.name = None
        assets, op_type, message = self.do_biz()

        self.assertEqual(assets, None, 'should be None')
        self.assertEqual(op_type, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, '添加资产,代码和名称是必须的，代码为: A8888 名称为：None', '添加资产，名称为空，不通过')
        self.assetsDto.name = name

    def test_do_biz00200(self):
        # 1. 新建资产成功
        print('test_do_biz00200 测试：' + '成功新建资产')

        _assets, op_type, message = self.do_biz()
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, 'admin(login_name_0001) 添加资产 图书(A8888)-类别一 并设置管理成功')

    def test_do_biz00300(self):
        # 1. 借资产成功
        print('test_do_biz00300 测试：' + '成功借资产')

        _assets, op_type, message = self.do_biz()
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type, Const.OpType.借出.value, 'should be 借出')
        self.assertEqual(message, '借出资产：admin 的 图书 借给 ccb_ft 的 admin(18999999999)。')

    def test_do_biz00400(self):
        # 1. 还资产成功
        print('test_do_biz00300 测试：' + '成功还资产')

        _assets, op_type, message = self.do_biz()
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type, Const.OpType.归还.value, 'should be 归还')
        self.assertEqual(message, '管理员:admin 归还了 admin 借的 admin 的 图书')

    def test_multiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)

    def test_do_biz9999999(self):
        dao.close_db()
        show_db()
        os.remove(db_file_path)
        self.assertEqual(1, 1)

    def do_biz(self):
        trace_id = util.generate_trace_id()
        return self.me.do_biz(assets_code=self.assetsDto.code, assets_name=self.assetsDto.name,
                              assets_category=self.assetsDto.category,
                              assets_memo=self.assetsDto.memo,
                              assets_image=self.assetsDto.image, assets_reason=self.assets_reason,
                              login_name=self.userDto.login_name,
                              name=self.userDto.name, memo=self.userDto.memo, mobile=self.userDto.mobile,
                              trace_id=trace_id)


if __name__ == '__main__':

    pre_db()

    unittest.main()


