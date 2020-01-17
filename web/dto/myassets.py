#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> myassets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:47 PM
@Desc   ：
=================================================='''
import time


class MyAssetsDto(object):
    def __init__(self, pid=None, code=None, user_id=None, user_name=None, name=None, memo=None,
                 status=None, create_time=None, borrow_time=None, my_assets=None):
        if my_assets and isinstance(my_assets, MyAssetsDto):
            pid, code, user_id, user_name, name, memo, status, create_time, borrow_time = my_assets.get_all_property()

        self.id = pid
        self.code = code
        self.user_id = user_id
        self.user_name = user_name
        self.name = name
        self.memo = memo
        self.status = status
        self.create_time = create_time
        self.borrow_time = borrow_time

    def get_all_property(self):
        return self.id, self.code, self.user_id, self.user_name, self.name, self.memo, self.status, self.create_time, self.borrow_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['memo'] = self.memo
        d['status'] = self.status
        d['image'] = '/wtn/assets?action=get_image&code=' + self.code  # 给出访问图像的地址
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        return d

