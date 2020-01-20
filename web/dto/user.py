#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> userDto
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/8/2020 3:41 PM
@Desc   ：
=================================================='''


class UserDto(object):
    def __init__(self, pid=None, login_name=None, name=None, status=None, memo=None, mobile=None, _user=None):
        if _user and isinstance(_user, UserDto):
            pid, login_name, name, status, memo, mobile = _user.get_all_property()
        elif isinstance(pid, tuple):
            pid, log_name, name, status, memo, mobile = pid
        self.id = pid
        self.login_name = login_name
        self.name = name
        self.status = status
        self.memo = memo
        self.mobile = mobile

    def get_all_property(self):
        return self.id, self.login_name, self.name, self.status, self.memo, self.mobile

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['login_name'] = self.login_name
        d['name'] = self.name
        d['status'] = self.status
        d['memo'] = self.memo
        d['mobile'] = self.mobile
        return d

    def __str__(self):
        return 'id %d login_name %s name %s status %d memo %s mobile %s' % (self.get_all_property())
