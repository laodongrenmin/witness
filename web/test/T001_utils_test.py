#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> T001_utils_test
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：2/7/2020 10:40 PM
@Desc   ：
=================================================="""
import unittest
from utils import *
import os
# import BeautifulReport


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), r'res\d.jpg')
        self.image_file_bytes = read_bytes_from_file(file_path)
        pass

    def tearDown(self):
        pass

    # 没有图片显示到报告中，因为程序代码里面是写死的png，而且目录是 img下
    # @BeautifulReport.BeautifulReport.add_test_img(r'res\d_thumbnail_file.jpg')
    def test_10000_thumbnail(self):
        """测试缩略图生成，生成256大小的缩略图"""
        my_print("准备测试："+self.test_10000_thumbnail.__doc__)
        data = thumbnail(self.image_file_bytes, 256)
        file_path = os.path.join(os.path.dirname(__file__), r'res\d_thumbnail_file.jpg')
        write_bytes_to_file(file_path, data)
        tmp = read_bytes_from_file(file_path)

        self.assertEqual(tmp[:2], b'\xff\xd8')
        self.assertEqual(tmp[-2:], b'\xff\xd9')
