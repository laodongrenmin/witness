#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> assets
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:45 PM
@Desc   ：
=================================================="""
import time
import base64
from web.conf import Conf


class AssetsDto(object):
    def __init__(self, code=None, user_id=None, user_name=None, name=None, category=None,
                 memo=None, image=None, create_time=None, limit_time=None, dst_user_id=None,
                 dst_user_name=None, dst_user_mobile=None, status=None, op_time=None, _assets=None):
        if isinstance(_assets, AssetsDto):
            code, user_id, user_name, name, category, memo, image, create_time, limit_time, dst_user_id, dst_user_name, dst_user_mobile, status, op_time = _assets.get_all_property()
        elif isinstance(code, tuple):
            code, user_id, user_name, name, category, memo, image, create_time, limit_time, dst_user_id, dst_user_name, dst_user_mobile, status, op_time = code

        self.code = code
        self.user_id = user_id
        self.user_name = user_name
        self.name = name
        self.category = category
        self.memo = memo
        self.image = image
        self.create_time = create_time
        self.limit_time = limit_time

        self.dst_user_id = dst_user_id
        self.dst_user_name = dst_user_name
        self.dst_user_mobile = dst_user_mobile
        self.status = status
        self.op_time = op_time

    def get_all_property(self):
        return self.code, self.user_id, self.user_name, self.name, self.category, self.memo, self.image, \
               self.create_time, self.limit_time, self.dst_user_id, self.dst_user_name, self.dst_user_mobile,\
               self.status, self.op_time

    def to_dict(self):
        d = dict()
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['category'] = self.category
        d['memo'] = self.memo
        d['image_url'] = '{0}/assets?action=get_image&code={1}'.format(Conf.root_url, self.code,)   # 给出访问图像的地址
        d['image'] = self.image
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        d['limit_time'] = self.limit_time
        d['dst_user_id'] = self.dst_user_id
        d['dst_user_name'] = self.dst_user_name
        d['dst_user_mobile'] = self.dst_user_mobile
        d['status'] = self.status
        d['op_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.op_time))
        return d

    def to_html_dict(self):
        d = self.to_dict()
        if self.image and len(self.image) > 0:
            d['image'] = 'data:image/jpeg;base64,' + base64.b64encode(self.image).decode('UTF-8')
        else:
            d['image'] = None
        return d
