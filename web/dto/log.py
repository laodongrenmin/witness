#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> log
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:48 PM
@Desc   ：
=================================================='''
import time


class LogDto(object):
    def __init__(self, pid=None, user_id=None, op_type=None, assets_name=None, log=None, log_time=None):
        if isinstance(pid, LogDto):
            pid, user_id, op_type, assets_name, log, log_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, user_id, op_type, assets_name, log, log_time = pid
        self.id = pid
        self.user_id = user_id
        self.op_type = op_type
        self.assets_name = assets_name
        self.log = log
        self.log_time = log_time

    def get_all_property(self):
        return self.id, self.user_id, self.op_type, self.assets_name, self.log, self.log_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['user_id'] = self.user_id
        d['op_type'] = self.op_type
        d['assets_name'] = self.assets_name
        d['log'] = self.log
        d['log_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.log_time))
        return d
