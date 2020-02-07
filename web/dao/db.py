#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> db
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 9:06 AM
@Desc   ：
=================================================="""
import sqlite3
from web.conf import Conf
from utils import my_print


class DB(object):
    def __init__(self, para=None):
        """
        :param para:   str(filepath) or sqlite3.Connection
        """
        self.IS_PRINT_SQL = Conf.is_print_sql
        self.conn = None
        self.db_name = None
        if para is None:
            self.db_name = Conf.db_file_path_rw
            self.init_conn_by_name()
        elif isinstance(para, str):
            self.db_name = para
            self.init_conn_by_name()
        elif isinstance(para, sqlite3.Connection):
            self.conn = para

    def set_print_sql_flag(self, b_print):
        self.IS_PRINT_SQL = b_print

    def init_conn_by_name(self, _db_name: str = None):
        if self.conn:
            self.conn.close()
        if _db_name is None:
            _db_name = self.db_name
        self.conn = sqlite3.connect(database=_db_name)
        self.db_name = _db_name

    def init_conn(self, sqlite3_conn: sqlite3.Connection):
        self.db_name = None
        if self.conn:
            self.conn.close()
        self.conn = sqlite3_conn

    def reopen(self):
        if self.db_name:
            self.conn = sqlite3.connect(database=self.db_name)
        else:
            raise Exception('db_name is None, can not call reopen.')

    def close(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def get_one(self, sql, para):
        if self.IS_PRINT_SQL:
            if para:
                sz_sql = "{0} {1}".format(sql, para)
            else:
                sz_sql = sql
            my_print(sz_sql)
        cur = self.conn.cursor()
        cur.execute(sql, para)
        row = cur.fetchone()
        cur.close()
        return row

    def get_all(self, sql, para):
        if self.IS_PRINT_SQL:
            if para:
                sz_sql = "{0} {1}".format(sql, para)
            else:
                sz_sql = sql
            my_print(sz_sql)
        cur = self.conn.cursor()
        cur.execute(sql, para)
        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_one(self, sql, para, is_commit=True):
        if self.IS_PRINT_SQL:
            if para:
                sz_sql = "{0} {1}".format(sql, para)
            else:
                sz_sql = sql
            my_print(sz_sql)
        self.conn.execute(sql, para)
        if is_commit:
            self.conn.commit()

    def execute(self, sql, para=None, is_commit=True):
        if self.IS_PRINT_SQL:
            if para:
                sz_sql = "{0} {1}".format(sql, para)
            else:
                sz_sql = sql
            my_print(sz_sql)
        if para:
            self.conn.execute(sql, para)
        else:
            self.conn.execute(sql)
        if is_commit:
            self.conn.commit()

    def create_table(self, sql):
        if self.IS_PRINT_SQL:
            my_print(sql)
        try:
            self.conn.execute(sql)
            self.commit()
            # print('创建表 %s 成功' % sql)
        except sqlite3.OperationalError as e:
            print(e)
