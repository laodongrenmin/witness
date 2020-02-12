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
import web.servlet.assets_add as servlet_assets_add
from utils import my_print
from web.test import *
from web.biz.constant import Const
import json
import time


class AssetsServletTestCase(unittest.TestCase):
    assets_code = 'A{}'.format(time.time())
    assets_code_no_attach = 'B9999'

    def setUp(self):
        self.req = get_test_request()
        self.req.parameters['code'] = AssetsServletTestCase.assets_code  # 'A8888_9'

    def test_00100_do_get_assets(self):
        """根据资产代码不能找到记录"""
        my_print('准备测试：' + self.test_00100_do_get_assets.__doc__)
        self.req.parameters["action"] = 'get_assets'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, False, '执行成功, 没有找到记录')
        self.assertEqual(Const.OpStatus.失败.value, d.get('status'), '不能找到记录')
        self.assertEqual('没有找到 code:{} 或者 login_name:login_name_0001 的记录'.format(AssetsServletTestCase.assets_code),
                         d.get('message'), '返回消息')

    def test_00200_do_post(self):
        """成功创建资产，附件方式"""
        my_print('准备测试：' + self.test_00200_do_post.__doc__)
        b_ret = servlet_assets_add.do_post(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功, 创建资产成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '创建资产成功')
        self.assertEqual('admin(login_name_0001) 添加资产 图书({})-类别一 并设置管理成功'.format(AssetsServletTestCase.assets_code),
                         d.get('message'), '返回消息')

    def test_00201_do_post(self):
        """成功创建资产，不带附件方式"""
        my_print('准备测试：' + self.test_00201_do_post.__doc__)
        self.req.parameters['image'] = None
        self.req.parameters['code'] = AssetsServletTestCase.assets_code_no_attach
        b_ret = servlet_assets_add.do_post(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功, 创建资产成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '创建资产成功')
        self.assertEqual('admin(login_name_0001) 添加资产 图书({})-类别一 并设置管理成功'.format(
            AssetsServletTestCase.assets_code_no_attach),
                         d.get('message'), '返回消息')

    def test_00300_do_get_assets(self):
        """根据资产代码能找到记录"""
        my_print('准备测试：' + self.test_00300_do_get_assets.__doc__)
        self.req.parameters["action"] = 'get_assets'
        b_ret = servlet_assets.do_get(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功，找到记录')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '能找到记录')
        self.assertEqual('找到 code:{} 或者 login_name:login_name_0001 的记录'.format(AssetsServletTestCase.assets_code),
                         d.get('message'), '消息')

    def test_00400_do_get_image(self):
        """根据资产代码能找到原始图片"""
        my_print('准备测试：' + self.test_00400_do_get_image.__doc__)
        self.req.parameters["action"] = 'get_image'
        b_ret = servlet_assets.do_get(self.req)
        self.assertEqual(b_ret, True, '执行成功，找到图片')
        self.assertEqual(self.req.res_body[:2], b'\xff\xd8')
        self.assertEqual(self.req.res_body[-2:], b'\xff\xd9')

    def test_00401_do_get_image(self):
        """根据资产代码能找到记录，但是没有图片"""
        my_print('准备测试：' + self.test_00401_do_get_image.__doc__)
        self.req.parameters["action"] = 'get_image'
        self.req.parameters['code'] = AssetsServletTestCase.assets_code_no_attach
        b_ret = servlet_assets.do_get(self.req)
        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, False, '执行成功，记录没有图片')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '不能找到图片')
        self.assertEqual('没有图像记录或者图像记录格式不对'.format(AssetsServletTestCase.assets_code),
                         d.get('message'), '消息')
#
# if __name__ == '__main__':
#     unittest.main()
