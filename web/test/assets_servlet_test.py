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
import web.servlet.assets as servlet_assets
from utils import my_print
from web.test import *
from web.biz.constant import Const
import json


class AssetsServletTestCase(unittest.TestCase):
    # set_print_sql_flag()

    def setUp(self):
        self.req = get_test_request()
        self.req.parameters['code'] = 'A8888_9'

    def test_00100_do_get(self):
        my_print("测试不能找到记录")
        self.req.parameters["action"] = 'get_assets'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, False, '执行成功, 没有找到记录')
        self.assertEqual(Const.OpStatus.失败.value, d.get('status'), '不能找到记录')
        self.assertEqual('没有找到 A8888_9 的记录', d.get('message'), '返回消息')

    def test_00200_do_post(self):
        my_print("测试创建资产")
        b_ret = servlet_assets.do_post(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功, 创建资产成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '创建资产成功')
        self.assertEqual('admin(login_name_0001) 添加资产 图书(A8888_9)-类别一 并设置管理成功', d.get('message'), '返回消息')

    def test_00300_do_get(self):
        my_print("测试 能够找到记录")
        self.req.parameters["action"] = 'get_assets'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '能找到记录')
        self.assertEqual('找到 A8888_9 的记录', d.get('message'), '消息')




#
# if __name__ == '__main__':
#     unittest.main()
