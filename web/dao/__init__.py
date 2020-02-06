#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/9/2020 8:58 AM
@Desc   ：
=================================================="""
from web.dao.db import DB
from web.dao.assets import AssetsDao
from web.dao.log import LogDao
from web.dao.my_assets import MyAssetsDao
from web.dao.note import NoteDao
from web.dao.notehis import NoteHisDao
from web.dao.user import UserDao

__all__ = ['close_db', 'rollback',
           'insert_log',
           'get_assets_by_code', 'get_assets_by_user_id', 'insert_assets',
           'insert_my_assets', 'update_my_assets_status', 'get_my_assets',
           'get_user_by_login_name', 'get_user_by_id', 'get_user_by_login_name',
           'get_note_by_assets_code', 'del_note_by_id',
           'insert_note_his']


# --------------------  db     -----------------------------
def close_db(_db: DB):
    _db.close()


def rollback(_db: DB):
    _db.rollback()


# --------------------  _log     -----------------------------
def insert_log(_db: DB, user_id=None, op_type=None, assets_code=None, assets_name=None, _log=None, is_commit=False):
    log_dao = LogDao(_db)
    log_dao.insert_log(user_id=user_id, op_type=op_type, assets_code=assets_code,
                       assets_name=assets_name, _log=_log, is_commit=is_commit)


# --------------------  assets  -----------------------------
def get_assets_by_code(_db, code: str):
    assets_dao = AssetsDao(_db)
    return assets_dao.get_assets_by_code(code=code)


def get_assets_by_user_id(_db, user_id=None, limit=1000, offset=0):
    assets_dao = AssetsDao(_db)
    return assets_dao.get_assets_by_user_id(user_id=user_id, limit=limit, offset=offset)


def insert_assets(_db, code=None, user_id=None, user_name=None, assets_name=None,
                  assets_category=None, assets_memo=None, image=None, _assets=None, is_commit=False):
    assets_dao = AssetsDao(_db)
    return assets_dao.insert_assets(code=code, user_id=user_id, user_name=user_name, assets_name=assets_name,
                                    assets_category=assets_category, assets_memo=assets_memo, image=image,
                                    _assets=_assets, is_commit=is_commit)


# --------------------  my assets  -----------------------------
def insert_my_assets(_db, assets_code=None, assets_name=None, assets_memo=None,
                     user_id=None, user_name=None,
                     _user=None, _assets=None, is_commit=False):
    my_assets_dao = MyAssetsDao(_db)
    my_assets_dao.insert_my_assets(assets_code=assets_code, assets_name=assets_name, assets_memo=assets_memo,
                                   user_id=user_id, user_name=user_name,
                                   _user=_user, _assets=_assets, is_commit=is_commit)


def get_my_assets(_db, assets_code=None, user_id=None):
    my_assets_dao = MyAssetsDao(_db)
    return my_assets_dao.get_my_assets(assets_code=assets_code, user_id=user_id)


def update_my_assets_status(_db, code=None, status=None):
    my_assets_dao = MyAssetsDao(_db)
    my_assets_dao.update_my_assets_status(code=code, status=status)


# --------------------  user  -----------------------------
def get_user_by_id(_db, pid):
    user_dao = UserDao(_db)
    return user_dao.get_user_by_id(pid=pid)


def get_user_by_login_name(_db, login_name: str):
    user_dao = UserDao(_db)
    return user_dao.get_user_by_login_name(login_name=login_name)


def insert_user(_db, login_name=None, name=None, mobile=None, depart=None, org=None, memo=None,
                u=None, is_commit=False):
    user_dao = UserDao(_db)
    user_dao.insert_user(login_name=login_name, name=name, mobile=mobile, depart=depart,
                         org=org, memo=memo, u=u, is_commit=is_commit)


# --------------------  note  -----------------------------
def get_note_by_assets_code(_db, code):
    note_dao = NoteDao(_db)
    return note_dao.get_note_by_assets_code(code=code)


def insert_note(_db, assets_code=None, assets_name=None, src_user_id=None, dst_user_id=None,
                witness_id=None, reason=None, _log=None, is_commit=False):
    note_dao = NoteDao(_db)
    note_dao.insert_note(assets_code=assets_code, assets_name=assets_name, src_user_id=src_user_id,
                         dst_user_id=dst_user_id, witness_id=witness_id, reason=reason, _log=_log,
                         is_commit=is_commit)


def del_note_by_id(_db, pid, is_commit=False):
    note_dao = NoteDao(_db)
    note_dao.del_note_by_id(pid=pid, is_commit=is_commit)


# --------------------  NOTE_HIS  -----------------------------
def insert_note_his(_db, _assets=None, mng_user=None, src_user=None, dst_user=None,
                    _note=None, _log=None, is_commit=False):
    note_his_dao = NoteHisDao(_db)
    note_his_dao.insert_note_his(_assets=_assets, mng_user=mng_user, src_user=src_user,
                                 dst_user=dst_user, _note=_note, _log=_log, is_commit=is_commit)
