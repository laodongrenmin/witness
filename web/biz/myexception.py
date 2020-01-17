#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> myexception
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/15/2020 9:19 AM
@Desc   ：
=================================================="""


class NoAssets(Exception):
    pass


class CreateAssetsException(Exception):
    pass


class BorrowAssetsException(Exception):
    pass


class ReturnAssetsException(Exception):
    pass


class NoNoteFound(Exception):
    pass
