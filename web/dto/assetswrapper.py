#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> a
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:53 PM
@Desc   ：
=================================================='''
import time


class AssetsWrapperDto(object):
    def _init_(self,assets_code,assets_name,src_user_id, src_user_login, src_user_name,
               dst_user_id, dst_user_login, dst_user_name,
               borrow_time, reback_time, content, status):
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.src_user_login = src_user_login
        self.src_user_name = src_user_name
        self.dst_user_id = dst_user_id
        self.dst_user_login = dst_user_login
        self.dst_user_name = dst_user_name
        self.borrow_time = borrow_time
        self.reback_time = reback_time
        self.content = content
        self.status = status

    def to_dict(self):
        d = dict()
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['src_user_login'] = self.src_user_login
        d['src_user_name'] = self.src_user_name
        d['dst_user_id'] = self.dst_user_id
        d['dst_user_login'] = self.dst_user_login
        d['dst_user_name'] = self.dst_user_name
        d['content'] = self.content
        d['status'] = self.status
        if self.reback_time:
            d['reback_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.reback_time))
        else:
            d['reback_time'] = None
        if self.borrow_time:
            d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        else:
            d['borrow_time'] = None

