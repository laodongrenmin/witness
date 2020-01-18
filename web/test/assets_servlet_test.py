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


class AssetsImplTestCase(unittest.TestCase):

    def test_00100_do_get(self):
        req = HttpRequest()
        req.parameters["action"] = 'get_assets'
        req.parameters["code"] = 'A8888'
        b_ret = servlet_assets.do_get(req)
        print(req.res_body)
        self.assertEqual(True, b_ret, '能找到记录')

    def test_00200_do_get(self):
        req = HttpRequest()
        req.parameters["action"] = 'get_assets'
        req.parameters["code"] = 'A8888_1'
        b_ret = servlet_assets.do_get(req)
        print(req.res_body)
        self.assertEqual(False, b_ret, '不能找到记录')

    def test_00300_do_post(self):
        req = HttpRequest()

        self.assertEqual(False, b_ret, '不能找到记录')

if __name__ == '__main__':
    unittest.main()
