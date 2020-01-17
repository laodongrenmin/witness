#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/14/2020 2:22 PM
@Desc   ：
=================================================='''


def get_log(log_name):
    logging.basicConfig(
        format="%(asctime)s [%(filename)s,%(funcName)s,%(lineno)s] %(name)s %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    return logging.getLogger(log_name)


logger = get_log(__name__)

if __name__ == '__main__':
    logger.info('000')
    exit(0)