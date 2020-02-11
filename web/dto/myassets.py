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
                 dst_user_name=None, dst_user_mobile=None, status=None, op_time=None, create_time=None, my_assets=None):
        if my_assets and isinstance(my_assets, MyAssetsDto):
            self.id = my_assets.id
            self.code = my_assets.code
            self.user_id = my_assets.user_id
            self.user_name = my_assets.user_name
            self.name = my_assets.name
            self.memo = my_assets.memo
            self.dst_user_name = my_assets.dst_user_name
            self.dst_user_mobile = my_assets.dst_user_mobile
            self.status = my_assets.status
            self.op_time = my_assets.op_time
            self.create_time = my_assets.create_time
        else:
            self.id = pid
            self.code = code
            self.user_id = user_id
            self.user_name = user_name
            self.name = name
            self.memo = memo
            self.dst_user_name = dst_user_name
            self.dst_user_mobile = dst_user_mobile
            self.status = status
            self.op_time = op_time
            self.create_time = create_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['memo'] = self.memo
        d['dst_user_name'] = self.dst_user_name
        d['dst_user_mobile'] = self.dst_user_mobile
        d['status'] = self.status
        d['image_url'] = '/wtn/assets?action=get_image&code=' + self.code  # 给出访问图像的地址
        d['op_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        return d

