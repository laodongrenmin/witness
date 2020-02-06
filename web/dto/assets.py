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
                 memo=None, image=None, create_time=None, _assets=None):
        if _assets and isinstance(_assets, AssetsDto):
            code, user_id, user_name, name, category, memo, image, create_time = _assets.get_all_property()
        elif isinstance(code, tuple):
            code, user_id, user_name, name, category, memo, image, create_time = code
        self.code = code
        self.user_id = user_id
        self.user_name = user_name
        self.name = name
        self.memo = memo
        self.category = category
        self.image = image
        self.create_time = create_time

    def get_all_property(self):
        return self.code, self.user_id, self.user_name, self.name, self.category, self.memo, self.image, self.create_time

    def to_dict(self):
        d = dict()
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['category'] = self.category
        d['memo'] = self.memo
        d['image'] = '%s/assets?action=get_image&code=%s' % (Conf.root_url, self.code)   # 给出访问图像的地址
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        return d

    def to_html_dict(self):
        d = self.to_dict()
        if self.image:
            d['image'] = base64.b64encode(self.image).decode('UTF-8')
        else:
            d['image'] = None
        return d
