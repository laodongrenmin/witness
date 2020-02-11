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
# vips_home = r'D:\software\vips-dev-8.7\bin'
# os.environ['PATH'] = vips_home + ';' + os.environ['PATH']
import pyvips
import time

if __name__ == '__main__1':

    print(os.environ['PATH'])
    file_path = os.path.join(os.path.dirname(__file__), r'res\d.jpg')
    thumbnail_path = os.path.join(os.path.dirname(__file__), r'res\d_thumbnail.jpg[optimize_coding,strip]')
    dst_file_path = os.path.join(os.path.dirname(__file__), r'res\d_dst.jpg[optimize_coding,strip]')
    png_path = os.path.join(os.path.dirname(__file__), r'res\d_png.png')

    t = time.time()
    out = pyvips.Image.thumbnail(file_path, 128)
    out.write_to_file(thumbnail_path, Q=75)
    t = time.time() - t
    print(t)
    t = time.time()
    img = pyvips.Image.new_from_file(file_path, shrink=1)
    img.write_to_file(dst_file_path, Q=75)
    img.write_to_file(png_path)
    t = time.time() - t
    print(t)


def get_data(*args):
    print(len(args))
    for arg in args:
        print(arg)
        for a in arg:
            print(a)


def g():
    return 'a','b'

def f():
    return 'a', 'b', 'c'

if __name__ == '__main__':
    get_data(g())
    get_data(f())

    get_data(g(), f())


    exit(0)
