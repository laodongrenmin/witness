#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> db
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 9:06 AM
@Desc   ：
=================================================='''
import sqlite3
from web.conf import Conf


class DB(object):
    def __init__(self, para=None):
        """
        :param para:   str(filepath) or sqlite3.Connection
        """
        self.IS_PRINT_SQL = Conf.is_print_sql
        self.conn = None
        self.db_name = None
        if isinstance(para, str):
            self.db_name = para
            self.conn = sqlite3.connect(database=self.db_name)
        elif isinstance(para, sqlite3.Connection):
            self.conn = para

    def init_conn_by_name(self, _db_name: str):
        if self.conn:
            self.conn.close()
        self.conn = sqlite3.connect(database=_db_name)
        self.db_name = _db_name

    def init_conn(self, sqlite3_conn: sqlite3.Connection):
        self.db_name = None
        if self.conn:
            self.conn.close()
        self.conn = sqlite3_conn

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def get_one(self, sql, para):
        if self.IS_PRINT_SQL:
            self.my_print(sql, para)
        cur = self.conn.cursor()
        cur.execute(sql, para)
        row = cur.fetchone()
        cur.close()
        return row

    def get_all(self, sql, para):
        if self.IS_PRINT_SQL:
            self.my_print(sql, para)
        cur = self.conn.cursor()
        cur.execute(sql, para)
        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_one(self, sql, para, is_commit=True):
        if self.IS_PRINT_SQL:
            self.my_print(sql, para)
        self.conn.execute(sql, para)
        if is_commit:
            self.conn.commit()

    def execute(self, sql, para=None, is_commit=True):
        if self.IS_PRINT_SQL:
            self.my_print(sql, para)
        if para:
            self.conn.execute(sql, para)
        else:
            self.conn.execute(sql)
        if is_commit:
            self.conn.commit()

    def create_table(self, sql):
        if self.IS_PRINT_SQL:
            self.my_print(sql)
        try:
            self.conn.execute(sql)
            self.commit()
            # print('创建表 %s 成功' % sql)
        except sqlite3.OperationalError as e:
            print(e)

    @staticmethod
    def my_print(sql, para=None):
        if para:
            print(sql, para)
        else:
            print(sql)


g_db = DB('my_sqlite3_1.db')

