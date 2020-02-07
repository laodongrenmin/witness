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


class AssetsImplTestCase(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), r'res\d1.jpg')
        self.image_file_bytes = self.image_file_bytes = read_bytes_from_file(file_path)
        pass

    def tearDown(self):
        pass

    def test_10000_thumbnail(self):
        data = thumbnail(self.image_file_bytes)
        file_path = os.path.join(os.path.dirname(__file__), r'res\d1_thumbnail_buffer.jpg')
        write_bytes_to_file(file_path, data)
