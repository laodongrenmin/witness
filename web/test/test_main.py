#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> test_main
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/19/2020 11:18 AM
@Desc   ：
=================================================='''
import unittest
from web.test import *

project_path = r"C:\Users\zbd\PycharmProjects\witness"

if __name__ == "__main__":

    set_print_sql_flag(False)
    # 测试用例保存的目录
    case_dirs = project_path + r"\web\test"
    # 加载测试用例
    discover = unittest.defaultTestLoader.discover(case_dirs, "*_test.py")
    # 运行测试用例
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(discover)
