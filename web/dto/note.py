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
    def __init__(self, pid=None, assets_code=None, src_user_id=None, dst_user_id=None,
                 witness_id=None, borrow_reason=None, return_reason=None,
                 borrow_time=None, limit_time=None, _note=None):
        if isinstance(_note, NoteDto):
            pid, assets_code, src_user_id, dst_user_id, witness_id, borrow_reason, return_reason, limit_time, borrow_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, assets_code, src_user_id, dst_user_id, witness_id, borrow_reason, return_reason, limit_time, borrow_time = pid
        self.id = pid
        self.assets_code = assets_code
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_id = witness_id
        self.borrow_reason = borrow_reason
        self.return_reason = return_reason
        self.limit_time = limit_time
        self.borrow_time = borrow_time

    def get_all_property(self):
        return self.id, self.assets_code, self.src_user_id, self.dst_user_id, self.witness_id, \
               self.borrow_reason, self.return_reason, self.limit_time, self.borrow_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['assets_code'] = self.assets_code
        d['src_user_id'] = self.src_user_id
        d['dst_user_id'] = self.dst_user_id
        d['witness_id'] = self.witness_id
        d['borrow_reason'] = self.borrow_reason
        d['return_reason'] = self.return_reason
        d['limit_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.limit_time))
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        return d

