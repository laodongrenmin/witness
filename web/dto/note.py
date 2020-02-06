#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> note
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:50 PM
@Desc   ：
=================================================="""
import time


class NoteDto(object):
    def __init__(self, pid=None, assets_code=None, assets_name=None, src_user_id=None,
                 dst_user_id=None, witness_id=None, memo=None, log=None, borrow_time=None):
        if isinstance(pid, NoteDto):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, memo, log, borrow_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, memo, log, borrow_time = pid
        self.id = pid
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_id = witness_id
        self.memo = memo
        self.log = log
        self.borrow_time = borrow_time

    def get_all_property(self):
        return self.id, self.assets_code, self.assets_name, self.src_user_id, \
               self.dst_user_id, self.witness_id, self.memo, self.log, self.borrow_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['dst_user_id'] = self.dst_user_id
        d['witness_id'] = self.witness_id
        d['memo'] = self.memo
        d['_log'] = self.log
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        return d

