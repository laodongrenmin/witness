#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> notehis
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:50 PM
@Desc   ：
=================================================='''
import time


class NoteHisDto(object):
    def __init__(self, pid, assets_code= None, assets_name=None, src_user_id= None, dst_user_id= None,
                 witness_id= None,  src_login_name= None, src_name= None, src_memo= None,
                 dst_login_name= None,dst_name= None,dst_memo= None,
                 log= None, borrow_time= None, reback_time= None, src_mobile=None, dst_mobile=None):
        if isinstance(pid, NoteHisDto):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, src_login_name, src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time, src_mobile, dst_mobile = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, assets_code, assets_name, src_user_id, dst_user_id,witness_id, src_login_name, src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time, src_mobile, dst_mobile = pid
        self.id = pid
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_id = witness_id
        self.src_login_name = src_login_name
        self.src_name = src_name
        self.src_memo = src_memo
        self.dst_login_name = dst_login_name
        self.dst_name = dst_name
        self.dst_memo = dst_memo
        self.log = log
        self.borrow_time = borrow_time
        self.reback_time = reback_time
        self.src_mobile = src_mobile
        self.dst_mobile = dst_mobile

    def get_all_property(self):
        return self.id , self.assets_code, self.assets_name, self.src_user_id ,self.dst_user_id, self.witness_id , self.src_login_name,
        self.src_name, self.src_memo, self.dst_login_name, self.dst_name, self.dst_memo, self.log = log,
        self.borrow_time, self.reback_time, self.src_mobile, self.dst_mobile

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['dst_user_id'] = self.dst_user_id
        d['witness_id'] = self.witness_id
        d['src_login_name'] = self.src_login_name
        d['src_name'] = self.src_name
        d['src_memo'] = self.src_memo
        d['dst_login_name'] = self.dst_login_name
        d['dst_name'] = self.dst_name
        d['dst_memo'] = self.dst_memo
        d['_log'] = self.log
        d['reback_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.reback_time))
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        d['src_mobile'] = self.src_mobile
        d['dst_mobile'] = self.dst_mobile
        return d
