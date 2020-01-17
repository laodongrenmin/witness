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
from HttpRequest import AttachFile
from web.biz.constant import Const
from web.biz.log import g_logImpl
from web.biz.myexception import *
import traceback
import time


class AssetsImpl(object):
    def __init__(self, _dao=dao):
        self._dao = _dao
        g_logImpl.set_dao(self._dao)

    def set_dao(self, _dao):
        self._dao = _dao
        g_logImpl.set_dao(self._dao)

    def get_image(self, code):
        _assets = self._dao.get_assets_by_code(code=code)
        if _assets and _assets.image:
            head, content = _assets.image.split(b'\r\n\r\n', 2)
            attach_file = AttachFile(head.decode('utf-8'), content)
            return attach_file.content_type, attach_file.content
        return None, None

    def get_or_create_user(self, u: dto.UserDto):
        """
        获取用户信息,根据u.log_name查询用户,
        如果用户存在,直接返回,不存在,根据U创建新用户并返回
        :param u:
        :return:
        """
        ret_user = self._dao.get_user_by_login_name(u.login_name)
        if not ret_user:
            ret_user = self._dao.insert_user(login_name=u.login_name, user_name=u.name, user_memo=u.memo, mobile=u.mobile)
            dao.insert_log(user_id=0, op_type=Const.OpType.系统.value, assets_code='', assets_name='',
                           log='新建用户: %s(%s)' % (u.name, u.login_name), is_commit=True)
        return ret_user

    def create_assets(self, _user: dto.UserDto=None, _assets: dto.AssetsDto=None, trace_id=None):
        e_str = None
        ret_assets = None
        try:
            if _assets.code and _assets.name:  # 传入了代码和名称，我们可以新建物品
                ret_assets = self._dao.insert_assets(_assets=_assets)
                message = "%s(%s) 添加资产 %s(%s)-%s 并设置管理成功" % \
                          (_user.name, _user.login_name, _assets.name, _assets.code, _assets.category)
                self._dao.insert_my_assets(_user=_user, _assets=_assets)
                g_logImpl.log(user_id=_user.id, op_type=Const.OpType.新建.value, assets_code=_assets.code,
                              assets_name=_assets.name, log=message, is_commit=True, is_print=False)
            else:
                message = "添加资产,代码和名称是必须的，代码为: %s 名称为：%s" % (_assets.code, _assets.name)
                g_logImpl.log(user_id=_user.id, op_type=Const.OpType.新建.value, assets_code=_assets.code,
                              assets_name=_assets.name, log=message, is_commit=True, is_print=True)
        except BaseException as b:
            tb = traceback.format_exc()
            self._dao.rollback()
            e_str = '新建资产 %s(%s)失败,跟踪号: %s' % (_assets.name, _assets.code, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise CreateAssetsException(e_str)
        return ret_assets, message

    def borrow_assets(self, _user: dto.UserDto=None, _assets: dto.AssetsDto=None, reason=None, trace_id=None):
        e_str = None
        content = '%s 借给 %s 的 %s(%s)。' % \
                  (_assets.name, _user.memo, _user.name, _user.mobile)
        log_str = '借出资产：%s 的 %s' % (_assets.user_name, content)
        try:
            self._dao.insert_note(assets_code=_assets.code, assets_name=_assets.name, src_user_id=_assets.user_id,
                                  dst_user_id=_user.id, reason=reason, _log=content)
            self._dao.update_my_assets_status(_assets.code, 1)
            g_logImpl.log(user_id=_user.id, op_type=Const.OpType.借出.value, assets_code=_assets.code,
                          assets_name=_assets.name, log=log_str, is_commit=True, is_print=False)
        except BaseException:
            tb = traceback.format_exc()
            self._dao.rollback()
            e_str = '%s 失败,跟踪号: %s' % (log_str, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise BorrowAssetsException(e_str)
        return log_str

    def return_assets(self, _user, _assets, _note, trace_id):
        e_str = None
        try:
            _row = self._dao.get_my_assets(assets_code=_assets.code, user_id=_user.id)
            if not _row:
                e_str = "资产: %s 不由你管理，不能完成归还动作" % _assets.name
            else:
                src_user = self._dao.get_user_by_id(_note.src_user_id)
                dst_user = self._dao.get_user_by_id(_note.dst_user_id)
                content = '管理员:%s 归还了 %s 借的 %s 的 %s' % (_user.name, dst_user.name, src_user.name, _assets.name)

                self._dao.insert_note_his(_assets=_assets, mng_user=_user,
                                          src_user=src_user, dst_user=dst_user, _note=_note, log=content)
                self._dao.del_note_by_id(_note.id)
                self._dao.update_my_assets_status(_assets.code, 2)
                g_logImpl.log(user_id=_user.id, op_type=Const.OpType.归还.value, assets_code=_assets.code,
                              assets_name=_assets.name, log=content, is_commit=True, is_print=False)
        except BaseException:
            tb = traceback.format_exc()
            self._dao.rollback()
            e_str = '归还资产 %s(%s) 失败,跟踪号: %s' % (_assets.name, _assets.code, trace_id)
            print(e_str + "\r\n" + tb)
        if e_str:
            raise ReturnAssetsException(e_str)
        return content

    def do_biz(self, assets_code=None, assets_name=None, assets_category=None, assets_memo=None, assets_image=None,
               assets_reason=None, login_name=None, name=None, memo=None, mobile=None,
               trace_id=None, _assets=None, _user=None):
        """
        借还资产业务处理函数，当用户不存在时， 可以新建用户实现借动作
        :param assets_code:
        :param assets_name:
        :param assets_category:
        :param assets_memo:
        :param assets_image:
        :param assets_reason:   借阅资产的用途，分类用
        :param login_name:
        :param name:
        :param memo:
        :param mobile:
        :param trace_id:
        :param _assets:
        :param _user:
        :return: 操作的资产对象， 操作的动作
        """
        message = None
        if not _user:
            _user = dto.UserDto(None, login_name=login_name, name=name, status=0, memo=memo, mobile=mobile)
        _user = self.get_or_create_user(_user)
        if not _assets:
            _assets = dto.AssetsDto(code=assets_code, user_id=_user.id, user_name=_user.name,
                                    name=assets_name, category=assets_category, memo=assets_memo, image=assets_image)
        _assets_tmp = dao.get_assets_by_code(code=_assets.code)
        if _assets_tmp:
            _assets = _assets_tmp
            # 查找登记簿，如果有，就是还书。没有就是借书
            _note = dao.get_note_by_assets_code(_assets.code)
            if _note:
                op_type = Const.OpType.归还.value
                message = self.return_assets(_user=_user, _assets=_assets, _note=_note, trace_id=trace_id)
            else:
                op_type = Const.OpType.借出.value
                message = self.borrow_assets(_user=_user, _assets=_assets, reason=assets_reason, trace_id=trace_id)
        else:
            op_type = Const.OpType.新建.value
            _assets, message = self.create_assets(_user=_user, _assets=_assets, trace_id=trace_id)
        return _assets, op_type, message

