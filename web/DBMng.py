# -*- coding: utf-8 -*-
import time
import sqlite3
import traceback
import tools
from enum import Enum

__author__ = 'zhengbangdong.wh@ccbft.com'
__version__ = '0.0.0.1'
__date__ = '2019/7/13 11:03'


class NoAssets(Exception):
    pass


class CreateAssetsException(Exception):
    pass


class BorrowAssetsException(Exception):
    pass


class NoNoteFound(Exception):
    pass


class OpType(Enum):
    系统 = 0
    新建 = 1
    借出 = 2
    归还 = 4
    生成借条 = 8


class UserDto(object):
    def __init__(self, pid=None, log_name=None, name=None, status=None, memo=None):
        if isinstance(pid, UserDto):
            pid, log_name, name, status, memo = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, log_name, name, status, memo = pid
        self.id = pid
        self.log_name = log_name
        self.name = name
        self.status = status
        self.memo = memo

    def get_all_property(self):
        return self.id, self.log_name, self.name, self.status, self.memo


class AssetsDto(object):
    def __init__(self, code=None, user_id=None, user_name=None, name=None, memo=None, image=None, create_time=None):
        if isinstance(code, AssetsDto):
            code, user_id, user_name, name, memo, image, create_time = code.get_all_property()
        elif isinstance(code, tuple):
            code, user_id, user_name, name, memo, image, create_time = code
        self.code = code
        self.user_id = user_id
        self.user_name = user_name
        self.name = name
        self.memo = memo
        self.image = image
        self.create_time = create_time

    def get_all_property(self):
        return self.code, self.user_id, self.user_name, self.name, self.memo, self.image, self.create_time

    def to_dict(self):
        d = dict()
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['memo'] = self.memo
        d['image'] = '/wtn/assets?action=get_image&code=' + self.code  # 给出访问图像的地址
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        return d


class MyAssetsDto(object):
    def __init__(self,pid=None,code=None,user_id=None,user_name=None,name=None,memo=None,status=None,create_time=None):
        id = pid
        if isinstance(pid, MyAssetsDto):
            id, code, user_id, user_name, name, memo, status, create_time = pid.get_all_property()
        elif isinstance(pid , tuple):
            id, code, user_id, user_name, name, memo, status, create_time = pid
        self.id = id
        self.code = code
        self.user_id = user_id
        self.user_name = user_name
        self.name = name
        self.memo = memo
        self.status = status
        self.create_time = create_time

    def get_all_property(self):
        return self.id, self.code, self.user_id, self.user_name, self.name, self.memo, self.status, self.create_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['code'] = self.code
        d['user_id'] = self.user_id
        d['user_name'] = self.user_name
        d['name'] = self.name
        d['memo'] = self.memo
        d['status'] = self.status
        d['image'] = '/wtn/assets?action=get_image&code=' + self.code  # 给出访问图像的地址
        d['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
        return d


class LogDto(object):
    def __init__(self, pid=None, user_id=None, op_type=None, assets_name=None, log=None, log_time=None):
        if isinstance(pid, LogDto):
            pid, user_id, op_type, assets_name, log, log_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, user_id, op_type, assets_name, log, log_time = pid
        self.id = pid
        self.user_id = user_id
        self.op_type = op_type
        self.assets_name = assets_name
        self.log = log
        self.log_time = log_time

    def get_all_property(self):
        return self.id, self.user_id, self.op_type, self.assets_name, self.log, self.log_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['user_id'] = self.user_id
        d['op_type'] = self.op_type
        d['assets_name'] = self.assets_name
        d['log'] = self.log
        d['log_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.log_time))
        return d


class NoteDto(object):
    def __init__(self, pid=None, assets_code=None, assets_name=None, src_user_id=None,
                 dst_user_id=None, witness_id=None, log=None, borrow_time=None):
        if isinstance(pid, NoteDto):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, log, borrow_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, log, borrow_time = pid
        self.id = pid
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_id = witness_id
        self.log = log
        self.borrow_time = borrow_time

    def get_all_property(self):
        return self.id, self.assets_code, self.assets_name, self.src_user_id, self.dst_user_id, self.witness_id, self.log, self.borrow_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['dst_user_id'] = self.dst_user_id
        d['witness_id'] = self.witness_id
        d['log'] = self.log
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        return d


class NoteHisDto(object):
    def __init__(self, pid, assets_code= None, assets_name=None, src_user_id= None, dst_user_id= None,
                 witness_id= None,  src_login_name= None, src_name= None, src_memo= None,
                 dst_login_name= None,dst_name= None,dst_memo= None,
                 log= None,borrow_time= None, reback_time= None):
        if isinstance(pid, NoteHisDto):
            pid, assets_code, assets_name, src_user_id, dst_user_id, witness_id, src_login_name, src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time = pid.get_all_property()
        elif isinstance(pid, tuple):
            pid, assets_code, assets_name, src_user_id, dst_user_id,witness_id, src_login_name, src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time = pid
        self.id = pid
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_id = witness_id
        self.src_login_name = src_login_name
        self.src_name = src_name
        self.src_memo = src_memo
        self.dst_login_name = dst_login_name
        self.dst_name = dst_name
        self.dst_memo = dst_memo
        self.log = log
        self.borrow_time = borrow_time
        self.reback_time = reback_time

    def get_all_property(self):
        return self.id , self.assets_code, self.assets_name, self.src_user_id ,self.dst_user_id, self.witness_id , self.src_login_name,
        self.src_name, self.src_memo, self.dst_login_name, self.dst_name, self.dst_memo, self.log = log,
        self.borrow_time, self.reback_time

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['dst_user_id'] = self.dst_user_id
        d['witness_id'] = self.witness_id
        d['src_login_name'] = self.src_login_name
        d['src_name'] = self.src_name
        d['src_memo'] = self.src_memo
        d['dst_login_name'] = self.dst_login_name
        d['dst_name'] = self.dst_name
        d['dst_memo'] = self.dst_memo
        d['log'] = self.log
        d['reback_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.reback_time))
        d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        return d


class WitnessDto(object):
    def __init__(self, pid=None, assets_code=None, src_user_id=None, dst_user_id=None, witness_content=None,
                 witness_image=None, witness_time=None):
        self.id = pid
        self.assets_code = assets_code
        self.src_user_id = src_user_id
        self.dst_user_id = dst_user_id
        self.witness_content = witness_content
        self.witness_image = witness_image
        self.witness_time = witness_time

class AssetsWrapperDto(object):
    def _init_(self,assets_code,assets_name,src_user_id, src_user_login, src_user_name,
               dst_user_id, dst_user_login, dst_user_name,
               borrow_time, reback_time, content, status):
        self.assets_code = assets_code
        self.assets_name = assets_name
        self.src_user_id = src_user_id
        self.src_user_login = src_user_login
        self.src_user_name = src_user_name
        self.dst_user_id = dst_user_id
        self.dst_user_login = dst_user_login
        self.dst_user_name = dst_user_name
        self.borrow_time = borrow_time
        self.reback_time = reback_time
        self.content = content
        self.status = status

    def to_dict(self):
        d = dict()
        d['assets_code'] = self.assets_code
        d['assets_name'] = self.assets_name
        d['src_user_id'] = self.src_user_id
        d['src_user_login'] = self.src_user_login
        d['src_user_name'] = self.src_user_name
        d['dst_user_id'] = self.dst_user_id
        d['dst_user_login'] = self.dst_user_login
        d['dst_user_name'] = self.dst_user_name
        d['content'] = self.content
        d['status'] = self.status
        if self.reback_time:
            d['reback_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.reback_time))
        else:
            d['reback_time'] = None
        if self.borrow_time:
            d['borrow_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.borrow_time))
        else:
            d['borrow_time'] = None


class DBMng(object):
    def __init__(self, para):
        self.conn = None
        self.db_name = None
        if isinstance(para, str):
            self.db_name = para
            self.conn = sqlite3.connect(database=self.db_name)
        elif isinstance(para, sqlite3.Connection):
            self.conn = para

    def init_conn_byname(self, _db_name: str):
        self.conn = sqlite3.connect(database=_db_name)

    def init_conn(self, sqlite3_conn:sqlite3.Connection):
        self.conn = sqlite3_conn

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def get_one(self, sql, para):
        cur = self.conn.cursor()
        cur.execute(sql, para)
        row = cur.fetchone()
        cur.close()
        return row

    def get_all(self, sql, para):
        cur = self.conn.cursor()
        cur.execute(sql, para)
        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_one(self, sql, para, is_commit=True):
        self.conn.execute(sql, para)
        if is_commit:
            self.conn.commit()

    def log(self, user_id, op_type, assets_name, log, is_commit=False):
        para = (None, user_id, op_type, assets_name, log, time.time(),)
        self.insert_one('insert into log values(?,?,?,?,?,?)',
                        para, is_commit)
        return para

    def get_log_by_login_name(self, user_login_name, limit=1000, offset=0):
        _user = self.get_user_by_logname(user_login_name)
        if _user:
            return self.get_log(_user.id, limit, offset)
        else:
            return list()

    def get_my_borrow(self, user_login_name, limit=1000, offset=0):
        return self.get_note_by_login_name(user_login_name, limit, offset)

    def get_borrow_by_code(self, code=None):
        noteDto = self.get_note_by_assets_code(code)
        his = list()
        if noteDto:
            _src_user = self.get_user_by_id(noteDto.src_user_id)
            _dst_user = self.get_user_by_id(noteDto.dst_user_id)
            if _src_user and _dst_user:
                his.append(NoteHisDto(pid=None, assets_code=noteDto.assets_code, assets_name=noteDto.assets_name,
                                      src_user_id=noteDto.src_user_id, dst_user_id=noteDto.dst_user_id,
                                      witness_id=None, src_login_name=_src_user.log_name, src_name=_src_user.name,
                                      src_memo=_src_user.memo, dst_login_name=_dst_user.log_name, dst_name=_dst_user.name,
                                      dst_memo=_dst_user.memo, log=noteDto.log, borrow_time=noteDto.borrow_time, reback_time=None).to_dict())
        return his

    def get_my_reback(self, user_login_name, limit=1000, offset=0):
        return self.get_note_his_by_login_name(user_login_name, limit, offset)

    def get_reback_by_code(self, assets_code, limit=1000, offset=0):
        return self.get_note_his_by_assets_code(assets_code, limit, offset)

    def get_my_log(self, user_login_name, limit=1000, offset=0, op_type=None):
        logs = list()
        _user = self.get_user_by_logname(user_login_name)
        op_type_sql = ''
        if op_type:
            op_type_sql = ' and op_type=' + op_type
        if _user:
            sql = "select id, user_id, op_type, assets_name, log, log_time from log where user_id=? " + op_type_sql + " order by id desc limit ? offset ?"
            paras = (_user.id, limit, offset,)
            rows = self.get_all(sql, paras)
            for row in rows:
                logs.append(LogDto(pid=row[0], user_id=row[1], op_type=row[2], assets_name=row[3], log=row[4],
                                   log_time=row[5]).to_dict())

        return logs

    def get_log(self, user_id=None, limit=1000, offset=0):
        '''
        获取记录的日志
        :param user_id:
        :param limit:
        :param offset:
        :return:  日志记录
        '''
        if user_id:
            sql = "select id, user_id, op_type, assets_name, log, log_time from log where user_id=? order by id desc limit ? offset ?"
            paras = (user_id, limit, offset,)
        else:
            sql = "select id, user_id, op_type, assets_name, log, log_time from log order by id desc limit ? offset ?"
            paras = (limit, offset,)
        rows = self.get_all(sql, paras)
        logs = list()
        for row in rows:
            logs.append(LogDto(pid=row[0], user_id=row[1], op_type=row[2], assets_name=row[3], log=row[4], log_time=row[5]).to_dict())
        return logs

    def get_or_create_user(self, u):
        ''' 获取用户信息,根据u.log_name查询用户,
        如果用户存在,直接返回,不存在,根据U创建新用户并返回 '''
        ret_user = dbMng.get_user_by_logname(u.log_name)
        if not ret_user:
            # 1
            self.insert_user(u.log_name, u.name, u.memo)
            self.log(0, OpType.系统.value, '', '新建用户: %s(%s)' % (u.name, u.log_name), True)
            ret_user = self.get_user_by_logname(u.log_name)
        return ret_user

    def insert_user(self, login_name, user_name=None, user_memo=None, is_commit=False):
        if isinstance(login_name, UserDto):  # 当第一个参数是DTO时候
            u = login_name
            para = (None, u.login_name, u.name, 0, u.memo,)
        else:
            para = (None, login_name, user_name, 0, user_memo,)
        self.insert_one("insert into user values(?,?,?,?,?)",para , is_commit)
        return UserDto(para)

    def get_myassets_by_user_id(self, user_id=None, limit=1000, offset=0):
        '''
        获取某个用户管理的的资产，用于还资产
        :param user_id:
        :param limit:
        :param offset:
        :return:  资产，但是不包含图片字段
        '''
        paras = (user_id, limit, offset,)
        rows = self.get_all("select id, code, user_id, user_name, name, memo, status, create_time from my_assets where user_id = ? order by create_time desc limit ? offset ?", paras)
        assets = list()
        for row in rows:
            assets.append(MyAssetsDto(pid=row[0], code=row[1], user_id=row[2], user_name=row[3], name=row[4],
                                    memo=row[5], status=row[6], create_time=row[7]).to_dict())
        return assets

    def insert_myassets(self, _user, _assets):
        para = (None,_assets.code, _user.id, _user.name , _assets.name, _assets.memo, 0, time.time())
        self.insert_one("insert into my_assets values(?,?,?,?,?,?,?,?)", para, False)
        self.log(_user.id,OpType.系统.value,_assets.name,'添加'+_assets.user_name+'的物品code:' + _assets.code + " 名称:"+_assets.name + ' ' + _user.name +' 来管理', True)
        return MyAssetsDto(para).to_dict()

    def insert_assets(self, code, user_id=None, user_name=None, assets_name=None, assets_memo=None, image=None, is_commit=False):
        if isinstance(code, AssetsDto):
            a = code
            para = (a.code, a.user_id, a.user_name, a.name, a.memo, a.image, time.time())
        else:
            para = (code, user_id, user_name, assets_name, assets_memo, image, time.time())
        self.insert_one("insert into assets values(?,?,?,?,?,?,?)", para, is_commit)
        return AssetsDto(para)

    def get_assets_by_user_id(self, user_id=None, limit=1000, offset=0):
        '''
        获取某个用户下的资产
        :param user_id:
        :param limit:
        :param offset:
        :return:  资产，但是不包含图片字段
        '''
        paras = (user_id, limit, offset,)
        rows = self.get_all("select code, user_id, user_name, name, memo, create_time from assets where user_id = ? order by create_time desc limit ? offset ?", paras)
        assets = list()
        for row in rows:
            assets.append(AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                                    memo=row[4], create_time=row[5]).to_dict())
        return assets

    def get_assets_bycode(self, code:str):
        row = self.get_one("select code, user_id, user_name,name,memo,image,create_time from assets where code = ?", (code,))
        if row:
            return AssetsDto(code=row[0], user_id=row[1], user_name=row[2], name=row[3],
                             memo=row[4], image=row[5], create_time=row[6])
        return None

    def get_user_by_id(self, pid):
        row = self.get_one("select id, login_name, name, status, memo from user where id = ?", (pid,))
        if row:
            return UserDto(pid=row[0], log_name=row[1], name=row[2], status=row[3], memo=row[4])
        return None

    def get_user_by_logname(self, logname:str):
        row = self.get_one("select id,login_name,name,status,memo from user where LOGIN_NAME = ?", (logname,))
        if row:
            return UserDto(pid=row[0], log_name=row[1], name=row[2], status=row[3], memo=row[4])
        return None

    def get_note_by_id(self, pid):
        row = self.get_one('''select id, assets_code, assets_name, src_user_id, dst_user_id, witness_id,
                            log, borrow_time from note where id = ?''', (pid,))
        if row:
            return NoteDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
                           witness_id=row[5], log=row[6], borrow_time=row[7])

    def get_note_by_login_name(self, login_name, limit=20, offset=0):
        notes = list()

        _user = self.get_user_by_logname(login_name)
        if _user:
            paras = (_user.id, limit, offset,)
            rows = self.get_all(
                "select id, assets_code, assets_name, src_user_id, dst_user_id, witness_id, log, borrow_time from note where dst_user_id = ? order by id desc limit ? offset ?",
                paras)
            for row in rows:
                notes.append(NoteDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
                           witness_id=row[5], log=row[6], borrow_time=row[7]).to_dict())
        return notes

    def get_note_by_assets_code(self, code):
        row = self.get_one('''select id, assets_code, assets_name, src_user_id, dst_user_id, witness_id,
                            log, borrow_time from note where assets_code = ?''', (code,))
        if row:
            return NoteDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
                           witness_id=row[5], log=row[6], borrow_time=row[7])
        return None

    def get_note_his_by_login_name(self, login_name, limit=20, offset=0):
        his = list()
        _user = self.get_user_by_logname(login_name)
        if _user:
            paras = (_user.id, limit, offset,)
            rows = self.get_all(
                "select id, assets_code, assets_name, src_user_id, dst_user_id, witness_id, src_login_name, "
                "src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time "
                "from note_his where dst_user_id = ? order by id desc limit ? offset ?",
                paras)
            for row in rows:
                his.append(NoteHisDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
                 witness_id=row[5], src_login_name=row[6], src_name=row[7], src_memo=row[8],
                 dst_login_name=row[9], dst_name=row[10], dst_memo=row[11],
                 log=row[12], borrow_time=row[13], reback_time=row[14]).to_dict())
        return his

    def get_note_his_by_assets_code(self, code, limit=20, offset=0):
        his = list()
        paras = (code, limit, offset,)
        rows = self.get_all(
            "select id, assets_code, assets_name, src_user_id, dst_user_id, witness_id, src_login_name, "
            "src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time "
            "from note_his where assets_code = ? order by id desc limit ? offset ?",
            paras)
        for row in rows:
            his.append(NoteHisDto(pid=row[0], assets_code=row[1], assets_name=row[2], src_user_id=row[3], dst_user_id=row[4],
             witness_id=row[5], src_login_name=row[6], src_name=row[7], src_memo=row[8],
             dst_login_name=row[9], dst_name=row[10], dst_memo=row[11],
             log=row[12], borrow_time=row[13], reback_time=row[14]).to_dict())
        return his

    def get_witness_by_id(self, witnesss_id):
        row = self.get_one('''select id, assets_code, src_user_id, dst_user_id ,
            witness_content, witness_image, witness_time from witness where id = ?''', (witnesss_id,))
        if row:
            return WitnessDto(pid=row[0], assets_code=row[1], src_user_id=row[2], dst_user_id=row[3],
                              witness_content=row[4], witness_image=row[5], witness_time=row[6])

    def insert_witness(self, assets_code, src_user_id, dst_user_id, witness_content, witness_image, is_commit=False):
        if isinstance(assets_code, WitnessDto):
            a = assets_code
            para = (None, a.assets_code, a.src_user_id, a.dst_user_id, a.witness_content, a.witness_image, time.time())
        else:
            para = (None, assets_code, src_user_id, dst_user_id, witness_content, witness_image, time.time())
        self.insert_one("insert into witness values(?,?,?,?,?,?,?)", para, is_commit)
        return WitnessDto(para)

    def create_witness(self, op_log_name, note_id=None, note_his_id=None):
        if note_id:
            _note = self.get_note_by_id(note_id)
        elif note_his_id:
            _note_his = self.get_note_his_by_id(note_id)
        _note = _note if _note else _note_his
        if not _note:
            raise NoNoteFound('没有登记簿，不能生成见证书')
        _assets = self.get_assets_bycode(_note.assets_code)
        _dst_user = self.get_user_by_id(_note.dst_user_id)
        _src_user = self.get_user_by_id(_note.src_user_id)
        # 如果不是资产拥有着或者借出者，就不能生成witness
        if op_log_name in (_src_user.log_name, _dst_user.log_name):
            date_format = "%Y-%m-%d %H:%M:%S"
            str_date = time.strftime(date_format, time.localtime(_note.borrow_time))
            # content = '某年某月某日,某部门的某人（手机号）借的某件物品属实'  # 见证书的文本内容
            content = '我见证了 %s %s 部门的%s(%s) 借 %s(%s)的 %s。' % (str_date, _dst_user.memo,_dst_user.name,
                                                            _dst_user.log_name, _src_user.name,_src_user.log_name,
                                                            _assets.name)
            image = b''   # 见证书的图片信息

            ret_witness = self.insert_witness(_assets.code, _note.src_user_id, _note.dst_user_id, content, image)
            self.log(_src_user.id if op_log_name == _src_user.log_name else _dst_user.log_name,
                     OpType.生成借条.value, _assets.name, content)
            return ret_witness
        else:
            raise Exception('此用户无权生成此见证书')

    def del_note_by_id(self, pid, is_commit=False):
        self.conn.execute("delete from note where id = ?", (pid,))
        if is_commit:
            self.commit()

    def insert_note(self, assets_code, assets_name, src_user_id, dst_user_id,
                    witness_id, log, borrow_time, is_commit=False):
        para = (None, assets_code, assets_name, src_user_id, dst_user_id, witness_id, log, borrow_time,)
        self.insert_one("insert into note values(?,?,?,?,?,?,?,?)",
                        para, is_commit)
        return NoteDto(para)

    def insert_note_his(self, assets_code, assets_name, src_user_id, dst_user_id,  witness_id,  src_login_name, src_name,
                        src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time, reback_time, is_commit=False):
        para = (None, assets_code, assets_name, src_user_id, dst_user_id,  witness_id,  src_login_name,
                         src_name, src_memo, dst_login_name, dst_name, dst_memo, log, borrow_time,
                         reback_time,)
        self.insert_one("insert into note_his values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        para, is_commit)
        return NoteHisDto(para)

    def create_assets(self, user, assets):
        # 2.1
        if not assets.name:  # 新建资产,肯定是有名称的,没有名称,就是希望扫码借或者还
            raise NoAssets('没有编号为:%s 的相关资产在库' % assets.code)
        e_str = None
        try:
            _assets = AssetsDto(assets)
            _assets.user_id = user.id
            _assets.user_name = user.name
            self.insert_assets(_assets)
            self.log(user.id, OpType.新建.value, _assets.name, '新建资产：%s(%s) 资产 %s' % (user.name, user.log_name, _assets.name))
            self.commit()

        except BaseException:
            trace_id = tools.Utils.generate_id()
            e_str = '新建资产失败,跟踪号: %s' % trace_id
            print(e_str + "\r\n" + traceback.format_exc())
        if e_str:
            raise CreateAssetsException(e_str)

    def update_my_assets_status(self, code=None, status=None):
        self.conn.execute("update my_assets set status = ? where code = ?", (status, code))

    def borrow_assets(self, user, assets):
        e_str = None
        content = '%s 借给 %s 的 %s(%s)。' % \
                  (assets.name, user.memo, user.name, user.log_name)
        log_str = '借出资产：%s 的 %s' % (assets.user_name, content)
        try:
            self.insert_note(assets.code, assets.name, assets.user_id, user.id, None, content, time.time())
            self.update_my_assets_status(assets.code, 1)
            self.log(user.id, OpType.借出.value, assets.name, log_str)
            self.commit()
        except BaseException:
            self.rollback()
            trace_id = tools.Utils.generate_id()
            e_str = '%s 失败,跟踪号: %s' % (log_str, trace_id)
            print(e_str + "\r\n" + traceback.format_exc())
        if e_str:
            self.log(user.id, OpType.借出.value, assets.name, "程序运行失败："+ e_str, True)
            raise BorrowAssetsException(e_str)

    def reback_assets(self, user, assets, note):
        e_str = None

        try:
            _row = self.get_one("select id from my_assets where  code = ? and user_id = ? ", (assets.code, user.id,))
            if not _row:
                e_str = assets.name + ' 不由你管理，不能完成归还动作'
            else:
                src_user = self.get_user_by_id(note.src_user_id)
                dst_user = self.get_user_by_id(note.dst_user_id)
                content = '%s 归还了 %s 借的 %s 的 %s' % (user.name, dst_user.name, src_user.name, assets.name)
                log_str = '归还资产：%s 的 %s' % (assets.user_name, assets.name)

                self.insert_note_his(note.assets_code, note.assets_name, src_user.id, dst_user.id, note.witness_id, src_user.log_name,
                                     src_user.name, src_user.memo, dst_user.log_name, dst_user.name,
                                     dst_user.memo, note.log, note.borrow_time, time.time())
                self.del_note_by_id(note.id)
                self.update_my_assets_status(assets.code, 2)
                self.log(user.id, OpType.归还.value, assets.name, content)
                self.commit()
        except BaseException:
            self.rollback()
            trace_id = tools.Utils.generate_id()
            e_str = '归还资产失败,跟踪号: %s' % trace_id
            print(e_str + "\r\n" + traceback.format_exc())
        if e_str:
            self.log(user.id, OpType.借出.value, assets.name, "程序运行失败：" + e_str, True)
            raise BorrowAssetsException(e_str)

    def do_biz(self, user, assets):
        '''
        :param user:  如果用户已经存在,就关心 log_name, 否则就要全部字段上送,用于插入新的用户
        :param assets: 如果资产已经存在,就关心 code,否则就要全部字段上送,用于新建
        :return:
        '''
        _user = self.get_or_create_user(user)
        _assets = self.get_assets_bycode(assets.code)
        op_type = OpType.借出
        if not _assets:
            self.create_assets(_user, assets)
            op_type = OpType.新建
        else:
            # 3
            note = self.get_note_by_assets_code(_assets.code)
            if note:
                # 3.2 还, 把登记簿的记录移到历史中,删除登记簿中的记录,记录日志
                # 暂时都弄的单表查询,不用表关联查询,以后可以无限制的拆分数据库
                self.reback_assets(_user, _assets, note)
                op_type = OpType.归还
            else:
                # 3.1 借
                self.borrow_assets(_user, _assets)
                op_type = OpType.借出
        return op_type

def create_table(conn, table_name, create_sql):
    Table_Name = table_name
    # 连接数据库,如果不存在则会在当前目录创建
    # conn = sqlite3.connect(database=db_name)
    try:
        # 创建游标
        cursor = conn.cursor()
        # 创建STUDENT表的SQL语句,默认编码为UTF-8
        SQL = create_sql
        # 创建数据库表
        cursor.execute(SQL)

        # 提交到数据库
        conn.commit()
        print('创建数据库表 %s 成功' % (Table_Name))
    except Exception as e:
        # 回滚
        conn.rollback()
        import traceback
        print(traceback.format_exc())
        if (str(e).find('already exists') != -1):
            print('存在数据库表 %s' % Table_Name)
        else:
            print('创建数据库表 %s 失败' % Table_Name)
    finally:
        # 关闭数据库
        # conn.close()
        pass



# INTEGER 能够自增长,INT不能够
# USER 用户信息表
# ASSETS 资产信息表
# LOG 操作日志表
# NOTE 登记簿,只保存当前借出
# NOTE_HIS 历史登记簿,保存所有的借出、归还数据
# WITNESS 见证信息表,保存某一资产的见证信息
tables = {
    #
    "USER": ['''CREATE TABLE USER (
            ID INTEGER PRIMARY KEY,
            LOGIN_NAME VARCHAR(40) NOT NULL,
            NAME VARCHAR(40) NOT NULL,
            STATUS INT,  --0 正常 1 删除
            MEMO TEXT(500))''',
             "insert into user values(?,?,?,?,?)",
             [(None, '00000000000', '系统用户', 0, '记录系统日志的用户'),
              (None, '13517227956', '小李子', 0, '建设银行/金融科技/武汉事业群/技术服务/前端开发'),
              (None, '18995533521', '小东子', 0, '建设银行/金融科技/武汉事业群/技术服务/后端开发'),]],

    "ASSETS":['''CREATE TABLE ASSETS (
                CODE VARCHAR(40),
                USER_ID INT,
                USER_NAME VARCHAR(40), 
                NAME VARCHAR(40) NOT NULL,
                MEMO TEXT(500),
                IMAGE BLOB, 
                CREATE_TIME TIMESTAMP,
                PRIMARY KEY(CODE),
                FOREIGN KEY(USER_ID) REFERENCES USER(ID))''',
                "insert into ASSETS values(?,?,?,?,?,?,?)",
              [('A0001', 2, '小李子', '饭卡1', '加班用', bytearray(b'image of A0001'),time.time()),
               ('A0002', 3, '小东子', '饭卡2', '加班用', bytearray(b'image of A0002'),time.time()),
               ('A0003', 3, '小东子', '饭卡3', '招待用', bytearray(b'image of A0002'), time.time()),]],

    "MY_ASSETS":['''CREATE TABLE MY_ASSETS (
                ID INTEGER PRIMARY KEY, 
                CODE VARCHAR(40),
                USER_ID INT,
                USER_NAME VARCHAR(40), 
                NAME VARCHAR(40) NOT NULL,
                MEMO TEXT(500),
                STATUS INT,  --enum,  0 此物品未借出 1 此物品已借出 2 此物品已归还
                CREATE_TIME TIMESTAMP,
                FOREIGN KEY(USER_ID) REFERENCES USER(ID))''',
                "insert into MY_ASSETS values(?,?,?,?,?,?,?,?)",
              [(None,'A0001', 2, '小李子', '饭卡1', '加班用', 0, time.time()),
               (None,'A0002', 3, '小东子', '饭卡2', '加班用', 1, time.time()),
               (None,'A0003', 3, '小东子', '饭卡3', '招待用', 2, time.time()),]],

    "LOG":['''CREATE TABLE LOG (
                ID INTEGER PRIMARY KEY, 
                USER_ID INT, 
                OP_TYPE INT,  --enum 见 OpType 
                ASSETS_NAME VARCHAR(40),
                LOG TEXT(200),
                LOG_TIME TIMESTAMP)''',
                "insert into LOG values(?,?,?,?,?,?)",
                [(None, 3, OpType.借出.value, '餐卡','小李子借给小东子餐卡', time.time()),
                 (None, 2, OpType.借出.value, '餐卡','小东子借给小李子餐卡', time.time()),]],

    "NOTE":['''
        CREATE TABLE NOTE (
            ID INTEGER PRIMARY KEY, 
            ASSETS_CODE VARCHAR(40),
            ASSETS_NAME VARCHAR(40),
            SRC_USER_ID INT, 
            DST_USER_ID INT, 
            WITNESS_ID INT,
            LOG TEXT(200),
            BORROW_TIME TIMESTAMP,
            FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE),
            FOREIGN KEY(SRC_USER_ID) REFERENCES USER(ID),
            FOREIGN KEY(DST_USER_ID) REFERENCES USER(ID) )''',
            "insert into note values(?,?,?,?,?,?,?,?)",
            [(None, 'A0001','饭卡1',1,2, None, '1 to 2',time.time()),
             (None, 'A0002','饭卡2',2,1, None, '2 to 1',time.time()),]
        ],
    "NOTE_HIS": ['''CREATE TABLE NOTE_HIS (
            ID INTEGER PRIMARY KEY,
            ASSETS_CODE VARCHAR(40),
            ASSETS_NAME VARCHAR(40),
            SRC_USER_ID INT,
            DST_USER_ID INT,
            WITNESS_ID INT,
            SRC_LOGIN_NAME VARCHAR(40) NOT NULL,
            SRC_NAME VARCHAR(40) NOT NULL,
            SRC_MEMO TEXT(500),
            DST_LOGIN_NAME VARCHAR(40) NOT NULL,
            DST_NAME VARCHAR(40) NOT NULL,
            DST_MEMO TEXT(500),
            LOG TEXT(200),
            BORROW_TIME TIMESTAMP,
            REBACK_TIME TIMESTAMP,
            FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE) )
        ''',
            "insert into note_his values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [(None, 'A0001','饭卡1',1, 2, None, '13517227956', '小李子','建设银行/金融科技/武汉事业群/技术服务/前端开发'
                ,'18995533521','小东子','建设银行/金融科技/武汉事业群/技术服务/后端开发','记录其他一些个信息',time.time() - 24*60*60 ,time.time()),]
        ],

    "WITNESS": ['''
        CREATE TABLE WITNESS (
            ID INTEGER PRIMARY KEY, 
            ASSETS_CODE VARCHAR(40),
            SRC_USER_ID INT, 
            DST_USER_ID INT, 
            WITNESS_CONTENT TEXT(200),
            WITNESS_IMAGE BLOB,
            WITNESS_TIME TIMESTAMP,
            FOREIGN KEY(ASSETS_CODE) REFERENCES ASSETS(CODE),
            FOREIGN KEY(SRC_USER_ID) REFERENCES USER(ID),
            FOREIGN KEY(DST_USER_ID) REFERENCES USER(ID) )''',
            "insert into WITNESS values(?,?,?,?,?,?,?)",
            [(None, 'A0001',1,2,'某年某月某日,某部门的某人（手机号）借的某件物品属实', u'存放图片字节流信息'.encode('UTF-8'),time.time()),
            ]
        ]

    }
import os
db_name = 'my_sqlite3.db'
db_filepath = os.path.realpath(db_name)
print(db_filepath)

def pre_db():
    import os
    import shutil
    import decimal
    if os.path.isfile(db_filepath):
        # 先备份,再删除
        shutil.copyfile(db_filepath, db_filepath+str(decimal.Decimal(time.time()*10000000))+'.bak')
        os.remove(db_name)
        pass
    with sqlite3.connect(database=db_filepath) as conn:
        for table_name in tables:
            try:
                create_table(conn, table_name, tables[table_name][0])
                cur = conn.cursor()
                print(tables[table_name][1])
                print(tables[table_name][2])
                cur.executemany(tables[table_name][1], tables[table_name][2])
                cur.close()
                conn.commit()
            except Exception:
                conn.rollback()
                print(table_name, traceback.format_exc())


def show_db():
    with sqlite3.connect(database=db_name) as conn:
        for table_name in tables:
            cur = conn.cursor()
            cur.execute("select * from %s" % table_name)
            print('-' * 15, table_name, '-' * 15)
            rows = cur.fetchone()
            while rows:
                # for row in rows:
                #     if type(row) == bytes:
                #         print(row.decode('UTF-8'))
                print(rows)
                rows = cur.fetchone()

# show_db()

def test_db():
    with sqlite3.connect(database=db_name) as conn:
        cur = conn.cursor()
        id = '1 or 1 = 1'
        type = 0
        args = (id, type)
        cur.execute("select * from USER where id = ? and status = ?", args)
        print('-' * 15, 'USER', '-' * 15)
        rows = cur.fetchone()
        while rows:
            # for row in rows:
            #     if type(row) == bytes:
            #         print(row.decode('UTF-8'))
            print(rows)
            rows = cur.fetchone()

# test_db()


if __name__ == '__main__':
    pre_db()
    # show_db()
    dbMng = DBMng(db_name)
    dbMng = DBMng(dbMng.conn)

    # 1. 第一步,从用户表里面查询用户,如果不存在,就直接插入用户 1.1
    #    1.1 插入用户,写日志
    # 2. 第二步,从资产表里面查询资产,如果不存在,就是新建 2.1, 如果存在就第三步
    #    2.1 新建资产,写日志后返回
    # 3. 第三步,从note表中查询,如果不存在,就用户借出逻辑 3.1,如果存在,就用户归还 3.2
    #    3.1 借出逻辑,写日志后返回,借出是把资产表、用户表的信息填入
    #    3.2 归还逻辑,写日志返回
    #
    system_user_id = 0  # 需要去数据库查询
    req_user = UserDto(None, '18995533528', '西施', 0, 'ccb/bianwai')
    req_assets = AssetsDto('A0004',None, None, 'Python程序员之美','一本介绍美女程序员的书',
                           b'pic stream of book', time.time())
    try:
        # 验证1.1 用户不存在
        req_user.log_name = 'test_user_no_exit'
        dbMng.do_biz(req_user, req_assets)

        # 验证2.1 资产不存在,建资产
        req_user.log_name = 'test_user_no_exit'
        req_assets.code = 'A9999'
        # req_assets.name = None
        dbMng.do_biz(req_user, req_assets)

        # 验证3.1 借出资产
        dbMng.do_biz(req_user, req_assets)

        # 生成见证书
        note = dbMng.get_note_by_assets_code(req_assets.code)
        dbMng.create_witness(req_user.log_name, note.id)

        # 验证3.2 归还资产
        dbMng.do_biz(req_user, req_assets)

        # 查询见证书
        dbMng.get_witness_by_id(req_assets.code)

    except Exception:
        dbMng.rollback()
        print(traceback.format_exc())

    show_db()


dbMng = DBMng(db_filepath)
