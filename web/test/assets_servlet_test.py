#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets_servlet_test
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 3:35 PM
@Desc   ：
=================================================="""
import unittest
from request import HttpRequest
import web.servlet.assets as servlet_assets
import utils
from web.test import *
from web.biz.constant import Const
import json


class AssetsServletTestCase(unittest.TestCase):
    # 这里强制打印出执行的sql语句，运行时，会根据配置文件里面的是否打印sql语句参数
    from web.dao.db import g_db
    g_db.IS_PRINT_SQL = True

    def setUp(self):
        print('')
        self.req = get_test_request()

    def test_00100_do_get(self):
        print("测试 能够找到记录")
        self.req.parameters["action"] = 'get_assets'
        self.req.parameters["code"] = 'A8888'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '能找到记录')
        self.assertEqual('找到 A8888 的记录', d.get('message'), '消息')

    def test_00200_do_get(self):
        print("测试不能找到记录")
        self.req.parameters["action"] = 'get_assets'
        self.req.parameters["code"] = 'A8888_1'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, False, '执行成功, 没有找到记录')
        self.assertEqual(Const.OpStatus.失败.value, d.get('status'), '不能找到记录')
        self.assertEqual('没有找到 A8888_1 的记录', d.get('message'), '返回消息')

    def test_00300_do_post(self):
        print("测试创建资产")
        self.req.parameters['code'] = 'A9999'
        b_ret = servlet_assets.do_post(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功, 创建资产成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '创建资产成功')
        self.assertEqual('admin(login_name_0001) 添加资产 图书(A9999)-类别一 并设置管理成功', d.get('message'), '返回消息')


if __name__ == '__main__':
    unittest.main()
