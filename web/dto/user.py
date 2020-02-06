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
    def __init__(self, pid=None, login_name=None, name=None, mobile=None, status=None, depart=None,
                 org=None, memo=None, _user=None):
        if _user and isinstance(_user, UserDto):
            pid, login_name, name, mobile, status, depart, org, memo = _user.get_all_property()
        elif isinstance(pid, tuple):
            pid, login_name, name, mobile, status, depart, org, memo = pid
        self.id = pid
        self.login_name = login_name
        self.name = name
        self.mobile = mobile
        self.status = status
        self.depart = depart
        self.org = org
        self.memo = memo

    def get_all_property(self):
        return self.id, self.login_name, self.name, self.mobile, self.status, self.depart, self.org, self.memo

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['login_name'] = self.login_name
        d['name'] = self.name
        d['mobile'] = self.mobile
        d['status'] = self.status
        d['depart'] = self.depart
        d['org'] = self.org
        d['memo'] = self.memo

        return d

    def __str__(self):
        return 'id {0} login_name {1} name {2} mobile {3} status {4}' \
               ' depart {5} org {6} memo {7}'.format(self.get_all_property())
