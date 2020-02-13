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
from web.biz.constant import Const
from web.test import *
from utils import *
from web.conf import Conf
import web.dao as dao


def pre_db(*args, **kwargs):
    t = args[0]
    t.me._db.close()
    t.me._img_db.close()
    # 准备数据文件
    if os.path.exists(Conf.db_file_path_rw):
        os.remove(Conf.db_file_path_rw)
    if os.path.exists(Conf.db_file_path_img):
        os.remove(Conf.db_file_path_img)

    t.me._db.reopen()
    t.me._img_db.reopen()
    # create_db(db_file_path_rw)
    create_table(t.me._db, t.me._img_db)


def show_my_db(*args, **kwargs):
    show_db(Conf.db_file_path_rw)
    if Conf.db_file_path_img != Conf.db_file_path_rw:
        show_db(Conf.db_file_path_img)


class AssetsImplTestCase(unittest.TestCase):
    me = AssetsImpl()

    def setUp(self):
        self.userDto = get_test_user_dto()
        self.assetsDto = get_test_book_assets_dto()
        self.assets_reason = get_borrow_reason()
        self.return_assets_reason = get_return_reason()
        self.trace_id = get_trace_id()
        self.me.set_db(get_test_db(), get_test_img_db())

    def tearDown(self):
        self.me._db.close()

    def test_00000_pre_data(self):
        """建立数据库，以及建表，准备测试数据"""
        my_print('准备测试：'+self.test_00000_pre_data.__doc__)
        pre_db(self)

    def test_00010_create_user(self):
        """没有用户admin创建用户admin失败"""
        my_print('准备测试：' + self.test_00010_create_user.__doc__)
        self.userDto.id = 1
        _user = self.me.get_or_create_user(u=self.userDto)
        self.assertEqual(_user.login_name, self.userDto.login_name)

    def test_00011_create_user(self):
        """没有用户admin创建用户admin成功"""
        my_print('准备测试：' + self.test_00011_create_user.__doc__)
        self.userDto.id = 3
        self.userDto.login_name = 'login_name1'
        self.userDto.name = 'admin1'
        _user = self.me.get_or_create_user(u=self.userDto)

        self.assertEqual(_user.login_name, self.userDto.login_name)

    def test_00012_create_user(self):
        """没有用户 admin2 创建用户 admin2 成功"""
        my_print('准备测试：'+self.test_00012_create_user.__doc__)
        self.userDto.id = None
        self.userDto.login_name = 'login_name2'
        self.userDto.name = 'admin2'
        _user = self.me.get_or_create_user(u=self.userDto, trace_id=self.trace_id)

        self.assertEqual(_user.login_name, self.userDto.login_name)

    def test_00100_create_assets(self):
        """资产缺少名称不能成功创建"""
        my_print('准备测试：'+self.test_00100_create_assets.__doc__)
        self.assetsDto.name = None
        status, assets, op_type, message = self.me.create_assets(_user=self.userDto,
                                                                 _assets=self.assetsDto, trace_id=self.trace_id)

        self.assertEqual(status.value, Const.OpStatus.失败.value, '创建失败')
        self.assertEqual(assets, None, 'should be None')
        self.assertEqual(op_type.value, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, '添加资产,代码和名称是必须的，代码为: A8888 名称为：None', '添加资产，名称为空，不通过')

    def test_00200_create_assets(self):
        """成功创建资产A8888，随机A*****.****6个，A9999"""
        my_print('准备测试：' + self.test_00200_create_assets.__doc__)
        status, _assets, op_type, message = self.me.create_assets(_user=self.userDto,
                                                                  _assets=self.assetsDto, trace_id=self.trace_id)

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功新建资产')
        self.assertNotEqual(_assets, None, 'should be not None.')
        self.assertEqual(op_type.value, Const.OpType.新建.value, 'should be 新建')
        self.assertEqual(message, 'admin(login_name_0001) 添加资产 图书(A8888)-类别一 并设置管理成功')
        for i in range(6):
            self.assetsDto.code = 'A{0:0=8d}'.format(i)
            self.me.create_assets(_user=self.userDto,
                                  _assets=self.assetsDto, trace_id=self.trace_id)
        self.assetsDto.code = 'A9999'
        self.assetsDto.image = None
        self.me.create_assets(_user=self.userDto,
                              _assets=self.assetsDto, trace_id=self.trace_id)

    def test_00201_get_assets_by_code(self):
        """根据资产代码成功查询资产"""
        my_print('准备测试：' + self.test_00201_get_assets_by_code.__doc__)
        _assets = self.me.get_assets_by_code(code=self.assetsDto.code)
        self.assertEqual(self.assetsDto.code, _assets.code)

    def test_00202_get_assets_by_code(self):
        """根据资产代码不能成功查询"""
        my_print('准备测试：' + self.test_00202_get_assets_by_code.__doc__)
        _assets = self.me.get_assets_by_code(code='self.assetsDto.code')

        self.assertEqual(None, _assets)

    def test_00201_get_image(self):
        """根据资产代码成功查询到图像，不是缩略图"""
        my_print('test_00201_get_image 测试查询成功')
        my_print('准备测试：' + self.test_00201_get_image.__doc__)
        code, header, image = self.me.get_image(code=self.assetsDto.code)
        self.assertEqual(self.assetsDto.code, code)
        self.assertEqual('image/jpeg', header[-10:], "header 信息")
        self.assertEqual(b'\xff\xd8', image[:2])
        self.assertEqual(b'\xff\xd9', image[-2:])

    def test_00202_get_image(self):
        """根据资产代码成功查询不到图像，不是缩略图"""
        my_print('准备测试：' + self.test_00202_get_image.__doc__)
        code, header, image = self.me.get_image(code='self.assetsDto.code')
        self.assertEqual(None, image)

    def test_00203_get_assets(self):
        """通过code成功查询到资产"""
        my_print('准备测试：' + self.test_00203_get_assets.__doc__)
        lst, count = self.me.get_assets(code=self.assetsDto.code)
        self.assertEqual(self.assetsDto.code, lst[0].code)
        self.assertEqual(1, count)

    def test_00204_get_assets(self):
        """根据资产拥有者的login_name成功分页查询到资产列表，并返回总数"""
        my_print('准备测试：' + self.test_00204_get_assets.__doc__)
        lst, count = self.me.get_assets(login_name=self.userDto.login_name, limit=3, offset=0)

        self.assertEqual(3, len(lst), '应该返回3条记录')
        self.assertEqual(1, lst[0].user_id, '用户id是1')
        self.assertEqual(8, count, '总记录数是8条')

    def test_00205_get_assets(self):
        """根据资产拥有者的user_id成功分页查询到资产列表，并返回总数"""
        my_print('准备测试：' + self.test_00205_get_assets.__doc__)
        lst, count = self.me.get_assets(user_id=1, limit=2, offset=2)

        self.assertEqual(2, len(lst), '应该返回2条记录')
        self.assertEqual(1, lst[0].user_id, '用户id是1')
        self.assertEqual(8, count, '总记录数是8条')

    def test_00206_get_assets(self):
        """根据资产code以及拥有者的user_id成功分页查询到资产列表，并返回总数， 三个参数的顺序是code、user_id、login_name"""
        my_print('准备测试：' + self.test_00206_get_assets.__doc__)
        lst, count = self.me.get_assets(code=self.assetsDto.code,
                                        login_name=self.userDto.login_name, user_id=1, limit=2, offset=2)

        self.assertEqual(self.assetsDto.code, lst[0].code)
        self.assertEqual(1, count)

    def test_00300_do_biz(self):
        """资产代码code、用户login_name成功借出资产"""
        my_print('准备测试：' + self.test_00300_do_biz.__doc__)

        _user = dao.get_user_by_login_name(self.me._db, self.userDto.login_name)
        status, op_type, message = \
            self.me.do_biz(assets_code=self.assetsDto.code,
                           assets_reason=self.assets_reason,
                           _user=_user,
                           trace_id=self.trace_id)

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功借资产')
        self.assertEqual(op_type.value, Const.OpType.借出.value, 'should be 借出')
        self.assertEqual(message, 'admin(18995533533)成功借出admin的图书(A8888)')

    def test_00301_do_biz(self):
        """资产代码code、用户login_name不能成功借出不存在的资产"""
        my_print('准备测试：' + self.test_00300_do_biz.__doc__)

        _user = dao.get_user_by_login_name(self.me._db, self.userDto.login_name)
        status, op_type, message = \
            self.me.do_biz(assets_code='self.assetsDto.code',
                           assets_reason=self.assets_reason,
                           _user=_user,
                           trace_id=self.trace_id)

        self.assertEqual(status, Const.OpStatus.其他, '不能借还不存在的资产')
        self.assertEqual(op_type, Const.OpType.查询, 'should be 查询')
        self.assertEqual(message, '资产代码: self.assetsDto.code 还未入库, 不能借还。')

    def test_00400_do_biz(self):
        """资产代码code、非管理者不能成功还资产，不是管理员"""
        my_print('准备测试：' + self.test_00400_do_biz.__doc__)
        self.userDto.login_name = 'login_name2'
        _user = dao.get_user_by_login_name(self.me._db, self.userDto.login_name)
        status, op_type, message = \
            self.me.do_biz(assets_code=self.assetsDto.code,
                           assets_reason=self.return_assets_reason,
                           _user=_user,
                           trace_id=self.trace_id)

        self.assertEqual(status.value, Const.OpStatus.失败.value, '不能成功还资产')
        self.assertEqual(op_type.value, Const.OpType.归还.value, 'should be 归还')
        self.assertEqual(message, '资产: 图书(A8888) 不由你管理，不能完成归还动作')

    def test_00401_do_biz(self):
        """资产代码code、管理者用户login_name成功还资产"""
        my_print('准备测试：' + self.test_00401_do_biz.__doc__)

        _user = dao.get_user_by_login_name(self.me._db, self.userDto.login_name)
        status, op_type, message = \
            self.me.do_biz(assets_code=self.assetsDto.code,
                           assets_reason=self.return_assets_reason,
                           _user=_user,
                           trace_id=self.trace_id)

        self.assertEqual(status.value, Const.OpStatus.成功.value, '成功还资产')
        self.assertEqual(op_type.value, Const.OpType.归还.value, 'should be 归还')
        self.assertEqual(message, '管理员:admin 归还了 admin 借的 admin 的 图书')

    def test_99999_do_biz(self):
        """显示目前数据库的数据"""
        my_print('准备测试：' + self.test_99999_do_biz.__doc__)
        show_my_db(self)


#
# if __name__ == '__main__':
#     unittest.main()


