#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> l001
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/15/2020 3:07 PM
@Desc   ：
=================================================='''
import os
vips_home = r'D:\software\vips-dev-8.7\bin'
os.environ['PATH'] = vips_home + ';' + os.environ['PATH']
import pyvips
import time

if __name__ == '__main__':

    print(os.environ['PATH'])
    file_path = os.path.join(os.path.dirname(__file__), 'd.jpg')
    dst_file_path = os.path.join(os.path.dirname(__file__), 'test_thumbnail.jpg')
    image = pyvips.Image.new_from_file(file_path)
    t = time.time()
    out = pyvips.Image.thumbnail(file_path, 56)
    out.write_to_file(dst_file_path, Q=95)
    t = time.time() - t
    print(t)
    exit(0)