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
import os
import BeautifulReport

if __name__ == "__main__1":

    # 测试用例保存的目录
    case_dirs = os.path.dirname(__file__)
    # 加载测试用例
    discover = unittest.defaultTestLoader.discover(case_dirs, "*_test.py")
    # 运行测试用例
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(discover)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    all_py = unittest.defaultTestLoader.discover(os.path.dirname(__file__), "T*_test.py")
    # # discover()方法会自动根据测试目录匹配查找测试用例文件（*.py）,并将查找到的测试用例组装到测试套件中
    [suite.addTests(py) for py in all_py]  # 列表生成式，添加文件里面的case到测试集合里面
    report_html = BeautifulReport.BeautifulReport(suite)
    report_html.report(filename='测试报告', description='测试报告')
