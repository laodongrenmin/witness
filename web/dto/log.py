#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> _log
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:48 PM
@Desc   ：
=================================================="""
import time


class LogDto(object):
    def __init__(self, pid=None, user_id=None, user_name=None, op_type=None, assets_name=None,
                 message=None, log_time=None, log_dto=None):
        if log_dto and isinstance(log_dto, LogDto):
            pid, user_id, user_name, op_type, assets_name, message, log_time = log_dto.get_all_property()
        self.id = pid
        self.user_id = user_id
        self.user_name = user_name
        self.op_type = op_type
        self.assets_name = assets_name
        self.message = message
        self.log_time = log_time

    def get_all_property(self):
        return self.id, self.user_id, self.user_name, self.op_type, self.assets_name, self.message, self.log_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['op_type'] = self.op_type
        d['assets_name'] = self.assets_name
        d['message'] = self.message
        d['log_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.log_time))
        return d
