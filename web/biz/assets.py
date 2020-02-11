#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 2:58 PM
@Desc   ：
=================================================="""
import web.dao as dao
import web.dto as dto
from web.biz.constant import Const
from web.biz.log import LogImpl
from web.biz.myexception import *
import traceback


class AssetsImpl(object):
    def __init__(self, _dao=dao, _db=None, _img_db=None):
        self._dao = _dao
        self._db = _db
        if _img_db:
            self._img_db = _img_db
        else:
            self._img_db = self._db
        self.log_impl = LogImpl(self._dao, self._db)

    def set_dao(self, _dao):
        self._dao = _dao
        self.log_impl.set_dao(self._dao)

    def set_db(self, _db, _img_db=None):
        self._db = _db
        if _img_db:
            self._img_db = _img_db
        else:
            self._img_db = self._db
        self.log_impl.set_db(self._db)

    def get_image(self, code):
        return self._dao.get_assets_image_by_code(self._img_db, code=code)

    def get_or_create_user(self, u: dto.UserDto):
        """
        获取用户信息,根据u.log_name查询用户,
        如果用户存在,直接返回,不存在,根据U创建新用户并返回
        :param u:
        :return:
        """
        ret_user = self._dao.get_user_by_login_name(self._db, u.login_name)
        if not ret_user:
            try:
                self._dao.insert_user(self._db, u=u)
                ret_user = self._dao.get_user_by_login_name(self._db, login_name=u.login_name)
                self._dao.insert_log(self._db, user_id=ret_user.id, op_type=Const.OpType.系统.value, assets_code='',
                                     assets_name='', _log='新建用户: {0}[{1}({2})]'.format(u.org, u.name, u.login_name),
                                     is_commit=True)
            except Exception as e:
                self._dao.rollback(self._db)
                ret_user = None
        return ret_user

    def get_assets_by_code(self, code=None):
        return self._dao.get_assets_by_code(self._db, code=code)

    def get_assets(self, code=None, login_name=None, user_id=None, limit=10, offset=0):
        lst = list()
        count = 0
        if code:
            _assets = self._dao.get_assets_by_code(self._db, code=code)
            if _assets:
                lst.append(_assets)
                count = 1
        elif user_id:
            lst, count = self._dao.get_assets_by_user_id(self._db, user_id=user_id, limit=limit, offset=offset)
        elif login_name:
            _user = self._dao.get_user_by_login_name(self._db, login_name=login_name)
            if _user:
                lst, count = self._dao.get_assets_by_user_id(self._db, user_id=_user.id, limit=limit, offset=offset)
        return lst, count

    def create_assets(self, _user: dto.UserDto = None, _assets: dto.AssetsDto = None, trace_id=None):
        e_str = None
        ret_assets = None
        status = Const.OpStatus.失败
        try:
            if _assets and _assets.code and _assets.name:  # 传入了代码和名称，我们可以新建物品
                ret_assets = self._dao.insert_assets(self._db, self._img_db, _assets=_assets)
                message = "%s(%s) 添加资产 %s(%s)-%s 并设置管理成功" % \
                          (_user.name, _user.login_name, _assets.name, _assets.code, _assets.category)
                self._dao.insert_my_assets(self._db, assets_code=_assets.code, user_id=_user.id)
                self.log_impl.log(user_id=_user.id, user_name=_user.name, op_type=Const.OpType.新建.value,
                                  assets_code=_assets.code,
                                  assets_name=_assets.name, _log=message, is_commit=True, is_print=False)
                status = Const.OpStatus.成功
            else:
                message = "添加资产,代码和名称是必须的，代码为: %s 名称为：%s" % (_assets.code, _assets.name)
                # self.log_impl.log(user_id=_user.id, user_name=_user.name, op_type=Const.OpType.新建.value,
                #                   assets_code=_assets.code, assets_name=_assets.name, _log=message,
                #                   is_commit=True, is_print=False)
        except BaseException as b:
            tb = traceback.format_exc()
            self._dao.rollback(self._db)
            e_str = '新建资产 %s(%s)失败,跟踪号: %s' % (_assets.name, _assets.code, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise CreateAssetsException(e_str)
        return status, ret_assets, Const.OpType.新建, message

    def borrow_assets(self, _user: dto.UserDto = None, _assets: dto.AssetsDto = None, reason=None, trace_id=None):
        e_str = None
        message = '%s 的 %s 借给 %s 的 %s(%s)。' % \
                  (_assets.user_name, _assets.name, _user.memo, _user.name, _user.mobile)
        try:
            bret, message = self._dao.update_assert_status(self._db, _assets.code, _user.id, _user.name, _user.mobile,
                                                           src_status=_assets.status,
                                                           dst_status=Const.AssetsStatus.已借出.value)
            if bret:
                self._dao.insert_note(self._db, assets_code=_assets.code, assets_name=_assets.name,
                                      src_user_id=_assets.user_id,
                                      dst_user_id=_user.id, reason=reason, _log=message)
                self.log_impl.log(user_id=_user.id, user_name=_user.name, op_type=Const.OpType.借出.value,
                                  assets_code=_assets.code, assets_name=_assets.name, _log=message)
                self._dao.commit(self._db)

        except BaseException:
            tb = traceback.format_exc()
            self._dao.rollback(self._db)
            e_str = '%s 失败,跟踪号: %s' % (message, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise BorrowAssetsException(e_str)
        return Const.OpStatus.成功, message

    def return_assets(self, _user=None, _assets=None, reason=None, trace_id=None):
        e_str = None
        status = Const.OpStatus.失败
        try:
            _row = self._dao.get_my_assets(self._db, assets_code=_assets.code, user_id=_user.id)
            if not _row:
                message = "资产: {0} 不由你管理，不能完成归还动作".format(_assets.name)
            else:
                src_user = self._dao.get_user_by_id(self._db, _assets.user_id)
                dst_user = self._dao.get_user_by_id(self._db, _assets.dst_user_id)
                message = '管理员:{} 归还了 {} 借的 {} 的 {}'.format(_user.name, dst_user.name, src_user.name, _assets.name)

                self._dao.update_assert_status(self._db, _assets.code, _user.id, _user.name, _user.mobile,
                                               _assets.status, Const.AssetsStatus.已归还)

                # self._dao.insert_note_his(self._db, _assets=_assets, mng_user=_user,
                #                           src_user=src_user, dst_user=dst_user, _note=_note, _log=message)

                self.log_impl.log(user_id=_user.id, user_name=_user.name, op_type=Const.OpType.归还.value,
                                  assets_code=_assets.code, assets_name=_assets.name, _log=message,
                                  is_print=False)
                self._db.commit()
                status = Const.OpStatus.成功
        except BaseException:
            tb = traceback.format_exc()
            self._db.rollback()
            e_str = '归还资产 %s(%s) 失败,跟踪号: %s' % (_assets.name, _assets.code, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise ReturnAssetsException(e_str)
        return status, message

    def do_biz(self, assets_code=None, assets_reason=None, _user=None,  trace_id=None):
        """
        实现借还物品逻辑
        :param assets_code:
        :param assets_reason:
        :param _user:
        :param trace_id:
        :return:
        """
        if _user is None:
            raise BorrowAssetsException('user is not found.')
        _assets = self._dao.get_assets_by_code(self._db, assets_code)
        if _assets:
            if _assets.status == Const.AssetsStatus.已借出.value:  # 归还
                op_type = Const.OpType.归还
                status, message = self.return_assets(_user=_user, _assets=_assets,
                                                     reason=assets_reason, trace_id=trace_id)
            else:  # 只要不是借出，就可以借出
                op_type = Const.OpType.借出
                status, message = self.borrow_assets(_user=_user, _assets=_assets,
                                                     reason=assets_reason, trace_id=trace_id)

        # _note = self._dao.get_note_by_assets_code(self._db, assets_code)
        # if _note:
        #     op_type = Const.OpType.归还
        #     status, message = self.return_assets(_user=_user, _assets=_assets, _note=_note, trace_id=trace_id)
        # else:

        return status, op_type, message

