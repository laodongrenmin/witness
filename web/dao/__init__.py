#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 8:58 AM
@Desc   ：
=================================================="""
from web.dao.log import g_logDao
from web.dao.user import g_userDao
from web.dao.note import g_noteDao
from web.dao.assets import g_assetsDao
from web.dao.my_assets import g_myAssetsDao
from web.dao.notehis import g_noteHisDao
from web.dao.db import g_db

__all__ = ['close_db', 'rollback',
           'insert_log',
           'get_assets_by_code', 'get_assets_by_user_id', 'insert_assets',
           'insert_my_assets', 'update_my_assets_status', 'get_my_assets',
           'get_user_by_login_name', 'get_user_by_id', 'get_user_by_login_name',
           'get_note_by_assets_code', 'del_note_by_id',
           'insert_note_his']


# --------------------  db     -----------------------------
def close_db():
    g_db.close()


def rollback():
    g_db.rollback()


# --------------------  log     -----------------------------
def insert_log(user_id=None, op_type=None, assets_code=None, assets_name=None, log=None, is_commit=False):
    g_logDao.insert_log(user_id=user_id, op_type=op_type, assets_code=assets_code,
                        assets_name=assets_name, log=log, is_commit=is_commit)


# --------------------  assets  -----------------------------
def get_assets_by_code(code: str):
    return g_assetsDao.get_assets_by_code(code=code)


def get_assets_by_user_id(user_id=None, limit=1000, offset=0):
    return g_assetsDao.get_assets_by_user_id(user_id=user_id, limit=limit, offset=offset)


def insert_assets(code=None, user_id=None, user_name=None, assets_name=None,
                  assets_category=None, assets_memo=None, image=None, _assets=None, is_commit=False):
    return g_assetsDao.insert_assets(code=code, user_id=user_id, user_name=user_name, assets_name=assets_name,
                                     assets_category=assets_category, assets_memo=assets_memo, image=image,
                                     _assets=_assets, is_commit=is_commit)


# --------------------  my assets  -----------------------------
def insert_my_assets(assets_code=None, assets_name=None, assets_memo=None,
                     user_id=None, user_name=None,
                     _user=None, _assets=None, is_commit=False):
    g_myAssetsDao.insert_my_assets(assets_code=assets_code, assets_name=assets_name, assets_memo=assets_memo,
                                   user_id=user_id, user_name=user_name,
                                   _user=_user, _assets=_assets, is_commit=is_commit)


def get_my_assets(assets_code=None, user_id=None):
    return g_myAssetsDao.get_my_assets(assets_code=assets_code, user_id=user_id)


def update_my_assets_status(code=None, status=None):
    g_myAssetsDao.update_my_assets_status(code=code, status=status)


# --------------------  user  -----------------------------
def get_user_by_id(pid):
    return g_userDao.get_user_by_id(pid=pid)


def get_user_by_login_name(login_name: str):
    return g_userDao.get_user_by_login_name(login_name=login_name)


def insert_user(login_name, user_name=None, user_memo=None, mobile=None, is_commit=False):
    return g_userDao.insert_user(login_name=login_name, user_name=user_name,
                                 user_memo=user_memo, mobile=mobile, is_commit=is_commit)


# --------------------  note  -----------------------------
def get_note_by_assets_code(code):
    return g_noteDao.get_note_by_assets_code(code=code)


def insert_note(assets_code=None, assets_name=None, src_user_id=None, dst_user_id=None,
                witness_id=None, reason=None, _log=None, is_commit=False):
    g_noteDao.insert_note(assets_code=assets_code, assets_name=assets_name, src_user_id=src_user_id,
                          dst_user_id=dst_user_id, witness_id=witness_id, reason=reason, _log=_log,
                          is_commit=is_commit)


def del_note_by_id(pid, is_commit=False):
    g_noteDao.del_note_by_id(pid=pid, is_commit=is_commit)


# --------------------  NOTE_HIS  -----------------------------
def insert_note_his(_assets=None, mng_user=None, src_user=None, dst_user=None,
                    _note=None, log=None, is_commit=False):
    g_noteHisDao.insert_note_his(_assets=_assets, mng_user=mng_user, src_user=src_user,
                                 dst_user=dst_user, _note=_note, log=log, is_commit=is_commit)
