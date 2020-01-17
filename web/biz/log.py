#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> log
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/13/2020 2:41 PM
@Desc   ：
=================================================="""
import logging
import web.dao as dao


def get_log(log_name):
    logging.basicConfig(
        format="%(asctime)s [%(filename)s,%(funcName)s,%(lineno)s] %(name)s %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    return logging.getLogger(log_name)


logger = get_log(__name__)


class LogImpl(object):
    def __init__(self, _dao=dao):
        self._dao = _dao

    def set_dao(self, _dao):
        self._dao = _dao

    def log(self, user_id=None, op_type=None, assets_code=None, assets_name=None, log=None,
            is_commit=False, is_print=True):
        self._dao.insert_log(user_id=user_id, op_type=op_type, assets_code=assets_code, assets_name=assets_name,
                             log=log, is_commit=is_commit)
        if is_print:
            logger.info("user: %d  type: %d assets: %s(%s) log: %s", user_id, op_type, assets_name,assets_code,log)


g_logImpl = LogImpl()

