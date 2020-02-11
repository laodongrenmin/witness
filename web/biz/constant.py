#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> constant.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 10:13 AM
@Desc   ：
=================================================='''
from enum import Enum


class Const:
    class OpType(Enum):
        系统 = 0
        新建 = 1
        借出 = 2
        归还 = 4
        生成借条 = 8
        查询 = 16

    class AssetsStatus(Enum):
        未借出 = 0
        已借出 = 2
        已归还 = 4

    class OpStatus(Enum):
        成功 = 0
        失败 = 1
        其他 = 2



