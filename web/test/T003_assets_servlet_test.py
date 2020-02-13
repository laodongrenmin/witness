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
from web.conf import Conf


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
            self.req.parameters['code']),
                         d.get('message'), '返回消息')

    def test_00202_do_post(self):
        """成功创建资产，不带附件方式"""
        my_print('准备测试：' + self.test_00201_do_post.__doc__)
        self.req.parameters['image'] = None
        self.req.parameters['code'] = 'servlet.assets.code'
        b_ret = servlet_assets_add.do_post(self.req)

        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '执行成功, 创建资产成功')
        self.assertEqual(Const.OpStatus.成功.value, d.get('status'), '创建资产成功')
        self.assertEqual('admin(login_name_0001) 添加资产 图书({})-类别一 并设置管理成功'.format(
            self.req.parameters['code']),
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
        self.assertEqual('资产代码:{0}, 没有图像记录或者图像记录格式不对'.format(AssetsServletTestCase.assets_code_no_attach),
                         d.get('message'), '消息')

    def test_00500_do_biz(self):
        """资产代码code、用户login_name不能成功借出不存在的资产"""
        my_print('准备测试：' + self.test_00500_do_biz.__doc__)

        self.req.parameters['code'] = 'no_assets_code'
        b_ret = servlet_assets.do_post(self.req)
        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '没有借出成功')
        self.assertEqual(d.get('status'), Const.OpStatus.其他.value, '不能借出不存在的物品')
        self.assertEqual(d.get('message'), '资产代码: no_assets_code 还未入库, 不能借还。')

    def test_00501_do_biz(self):
        """资产代码code、用户login_name成功借出资产"""
        my_print('准备测试：' + self.test_00501_do_biz.__doc__)

        b_ret = servlet_assets.do_post(self.req)
        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '借出成功')
        self.assertEqual(d.get('status'), Const.OpStatus.成功.value, '借出成功')
        self.assertEqual(d.get('message'), 'admin(18995533533)成功借出admin的图书({})'.format(self.req.parameters['code']))

    def test_00600_do_biz(self):
        """资产代码code、非管理者不能成功还资产，不是管理员"""
        my_print('准备测试：' + self.test_00600_do_biz.__doc__)

        self.req.parameters['userInfo']['login_name'] = 'is_not_mng_assets_user'
        self.req.parameters['userInfo']['id'] = None
        b_ret = servlet_assets.do_post(self.req)
        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))
        self.assertEqual(b_ret, True, '没有归还成功')
        self.assertEqual(d.get('status'), Const.OpStatus.失败.value, '不能归还不属于你管理的物品')
        self.assertEqual(d.get('message'), '资产: 图书({}) 不由你管理，不能完成归还动作'.format(self.req.parameters['code']))

    def test_00601_do_biz(self):
        """资产代码code、管理者用户login_name成功还资产"""
        my_print('准备测试：' + self.test_00601_do_biz.__doc__)

        b_ret = servlet_assets.do_post(self.req)
        d = dict()
        d.update(json.loads(self.req.res_body.decode('UTF-8')))

        self.assertEqual(b_ret, True, '归还成功')
        self.assertEqual(d.get('status'), Const.OpStatus.成功.value, '成功归还属于你管理的物品')
        self.assertEqual(d.get('message'), '管理员:admin 归还了 admin 借的 admin 的 图书')

    def test_99999_show_db(self):
        """显示目前数据库的数据"""
        my_print('准备测试：' + self.test_99999_show_db.__doc__)
        show_db(Conf.db_file_path_rw)
        if Conf.db_file_path_img != Conf.db_file_path_rw:
            show_db(Conf.db_file_path_img)
#
# if __name__ == '__main__':
#     unittest.main()
