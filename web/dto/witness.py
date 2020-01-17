#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> witness
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:51 PM
@Desc   ：
=================================================='''


class WitnessDto(object):
    def __init__(self, pid=None, assets_code=None, src_user_id=None, dst_user_id=None, witness_content=None,
                 witness_image=None, witness_time=None):
        self.id = pid
        self.assets_code = assets_code
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_content = witness_content
        self.witness_image = witness_image
        self.witness_time = witness_time
